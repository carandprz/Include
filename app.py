from flask import Flask, render_template, request, redirect, url_for,flash
from flask_mysqldb import MySQL
import voz 
import database as db

#modelos para login 
from models.ModelUser import ModelUser
from models.entities.User import User

app = Flask(__name__)

#app.config['MYSQL_HOST'] = 'localhost'
#app.config['MYSQL_USER'] = 'root'
#app.config['MYSQL_PASSWORD'] = ''
#app.config['MYSQL_DB'] = 'BD'
mysql = MySQL(app)

# settings
app.secret_key = 'mysecretkey'

# Rutas ---------------------------------------------------------------------
@app.route('/')
def index():
    return render_template('home.html')

# Indice 

@app.route('/servicios')
def pag_servicio():
    return render_template('servicios.html')

@app.route('/audiolibros')
def pag_audiolibros():
    return render_template('audiolibros.html')

@app.route('/podcast')
def pag_podcast():
    return render_template('podcast.html')

@app.route('/cursos')
def pag_cursos():
    return render_template('cursos.html')

#Usuario
@app.route('/registro')
def pag_registrar():
    return render_template('auth/registro_usuarios.html')

@app.route('/login')
def pag_login():
    return render_template('auth/login.html')

@app.route('/ingreso_user')
def pag_ingreso():
    return render_template('ingreso.html')

#rutas pie de paginas
@app.route('/normas')
def pag_normas():
    return render_template('normas.html')

@app.route('/contacto')
def pag_contacto():
    return render_template('contacto.html')

@app.route('/sobre-include')
def pag_nosotros():
    return render_template('sobre-include.html')

#administrador
@app.route('/admin-home')
def pag_admin_home():
    return render_template('admin-home.html')

@app.route('/admin-login')
def pag_admin_login():
    return render_template('auth/admin-login.html')


#funciones 
#guardar datos de registro
@app.route('/agregar_usuario', methods=['POST'])
def agregar_usuario():
    if request.method == 'POST':
        id_usuario = request.form['username']
        nombre = request.form['name']
        apellido = request.form['lastname']
        correo_electronico = request.form['email']
        contras1 = request.form['password']
        contrasena = request.form['confirm_password']
        fecha_nacimiento = request.form['birth_date']
        telefono = request.form['phone']
        pais = request.form['country']
        
        if contras1 != contrasena:
            flash('Las contraseñas no coinciden')
            return redirect(url_for('pag_registrar'))
        
        try:
            # conexion con mysql
            cursor = db.database.cursor()
            sql ="INSERT INTO usuarios (id_usuario, nombre, apellido, correo_electronico, contrasena, fecha_nacimiento, telefono, pais) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            data = (id_usuario, nombre, apellido, correo_electronico, contrasena, fecha_nacimiento, telefono, pais)
            cursor.execute(sql, data )
            db.database.commit()
            #flash('Usuario agregado exitosamente')
        except MySQLdb.Error as e:
            flash(f'Error al agregar el usuario: {e}')
            return redirect(url_for('pag_registrar'))
        
        return redirect(url_for('pag_registrar'))

#para login 
@app.route('/ingresar_usuario', methods=['GET','POST'])
def ingresar_usuario():
    if request.method == 'POST':
        user = User(request.form['username'],request.form['password'])
        logger_user = ModelUser.login(db,user)
        # Verifca usuario y contraseña 
        if logger_user is not None :
            if logger_user.password == user.password:
                return redirect(url_for('pag_ingreso'))
            else:
                flash("Usuario/ contraseña incorrecto")
                return render_template('auth/login.html')
        else: #no existe usuario
            flash("Usuario/ contraseña incorrecto..")
            return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')
    
@app.route('/escuhar_mp3')
def podcast():
    with connection.cursor() as cursor:
        # Consulta para obtener las rutas de los audios
        sql = "SELECT nombre, ruta FROM archivos"
        cursor.execute(sql)
        audios = cursor.fetchall()
    return render_template('podcast.html', audios=audios)

if __name__ == "__main__":
    app.run(port=5000, debug=True)