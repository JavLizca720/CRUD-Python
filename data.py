#Importaciones
from flask import Flask
from flask import render_template,request,redirect,url_for,flash
#Nombre de la foto
from datetime import datetime
#Elimina la foto
import os

#MOSTRAR FOTO
from flask import send_from_directory

#Conexion
from flaskext.mysql import MySQL


#Creo la app
app= Flask(__name__)

app.secret_key="Caos720"

#Base de datos
mysql = MySQL()
app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']='12345'
app.config['MYSQL_DATABASE_DB']='phytoncrud'
mysql.init_app(app)

FOLDER = os.path.join('uploads')
app.config['FOLDER']=FOLDER

#MOSTRAR FOTO
@app.route('/uploads/<namePhoto>')
def uploads(namePhoto):
    return send_from_directory(app.config['FOLDER'],namePhoto)

#Solicitudes en el host
@app.route('/')
def index():

    #Intrucciones SQL
    sql="SELECT * FROM `phytoncrud`.`usuarios`"
    conn = mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql)

    #CONSULTA
    users=cursor.fetchall();
    print(users)

    conn.commit()

    return render_template('users/index.html', users=users)


    #ELIMINAR
@app.route('/destroy/<int:id>')
def destroy(id):
        conn = mysql.connect()
        cursor=conn.cursor()

        #REMOVER FOTO
        cursor.execute("SELECT aparicion FROM usuarios WHERE id=%s", id)
        row=cursor.fetchall()

        os.remove(os.path.join(app.config['FOLDER'],row[0][0]))

        cursor.execute("DELETE FROM usuarios WHERE id=%s",(id))
        conn.commit()
        return redirect('/')

    #EDITAR
@app.route('/edit/<int:id>')
def edit(id):
    conn = mysql.connect()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE id=%s", (id))

    #CONSULTA
    users=cursor.fetchall();
    conn.commit()
    print(users)

    return render_template('users/edit.html',users=users)


    #EDITAR FUNCION
@app.route('/update', methods=['POST'])
def update():
        _name=request.form['txtName']
        _front=request.files['txtFront']
        id=request.form['txtID']
        sql="UPDATE `phytoncrud`.`usuarios` SET `nombre` = %s WHERE id=%s;"
#set nombre se iguala al name de abajo
        datos=(_name,id)


        conn = mysql.connect()
        cursor=conn.cursor()

        now= datetime.now()
        time=now.strftime("%Y%H%M%S")

        if _front.filename!='':

            newName=time+_front.filename
            _front.save("uploads/"+newName)

            cursor.execute("SELECT aparicion FROM usuarios WHERE id=%s", id)
            row=cursor.fetchall()

            os.remove(os.path.join(app.config['FOLDER'],row[0][0]))
            cursor.execute("UPDATE usuarios SET aparicion=%s WHERE id=%s", (newName,id))
            conn.commit()

        cursor.execute(sql, datos)
        conn.commit()
        return redirect('/')
            


    #VISTA CREATE
@app.route('/create')
def create():
        return render_template('users/create.html')


    #STORAGE
@app.route('/store', methods=['POST'])
def storage():



        _name=request.form['txtName']
        _front=request.files['txtFront']



        ####ESTA ES PA QUE NO SE REPITAN
        sql="SELECT * FROM usuarios WHERE nombre = %s"
        data=(_name,)
        conn = mysql.connect()
        cursor=conn.cursor()
        cursor.execute(sql, data)
        conn.commit()
        conn.close()
        row = cursor.fetchone()
           
        if row != None:
            user = [row [0], row [1], row[2]]
            flash('El nombre ya existe')
            return redirect(url_for('create'))

        else:

            if _name=='' or _front=='':
                flash('Debes llenar los campos')
                return redirect(url_for('create'))

            now= datetime.now()
            time=now.strftime("%Y%H%M%S")

            if _front.filename!='':
                newName=time+_front.filename
                _front.save("uploads/"+newName)

            sql="INSERT INTO `phytoncrud`.`usuarios` ( `id`, `nombre`, `aparicion`) VALUES ( NULL, %s, %s);"

            datos=(_name,newName)


            conn = mysql.connect()
            cursor=conn.cursor()
            cursor.execute(sql, datos)
            conn.commit()

            return redirect('/')

if __name__=='__main__':
        app.run(debug=True)
