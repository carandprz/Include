from flask import Flask, render_template, request, redirect, url_for,flash
from flask_mysqldb import MySQL
import database as db

from flask_login import LoginManager, login_user,logout_user,login_required
#from flask_wtf.csrf import CSRFProtect
#modelos para login 
from models.ModelUser import ModelUser
from models.entities.User import User
from models.ModelAdmi import ModelAdmi
from models.entities.Admi import Admi

app = Flask(__name__)

mysql = MySQL(app)

login_manager_app= LoginManager(app) 

#---------- LOGEAR NOMBRE EN BIENVENIDOS 

@login_manager_app.user_loader
def load_user(user_id):
    # Intenta cargar como usuario regular
    user = ModelUser.get_by_id(db, user_id)
    if user is not None:
        return user
    
    # Si no existe como usuario regular, intenta cargar como administrador
    admin = ModelAdmi.get_by_id(db, user_id)
    if admin is not None:
        return admin
    
    return None  # Si no se encontró ningún usuario

# settings
app.secret_key = 'mysecretkey'

# Rutas ---------------------------------------------------------------------
@app.route('/')
def index():
    return render_template('home.html')

# Indice 

@app.route('/servicios') # esto va para el htlm
def pag_servicio():
    return render_template('servicios.html') # ruta del archivo para q lo distinga python 

@app.route('/lector')
def pag_lector():
    return render_template('servicios/lector.html')

@app.route('/audioLibro')
def pag_audiolibros():
    return render_template('servicios/audioLibro.html')

@app.route('/podcast')
def pag_podcast():
    return render_template('servicios/podcast.html')

@app.route('/cursos')
def pag_cursos():
    return render_template('servicios/cursos.html')

#REGISTRO Y LOGIN -------------------------
@app.route('/registro')
def pag_registrar():
    return render_template('auth/registro_usuarios.html')

@app.route('/login')
def pag_login():
    return render_template('auth/login.html')

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
@app.route('/admi')
def pag_admin():
    return render_template('admi.html')

@app.route('/admin-home')
def pag_admin_home():
    return render_template('admin-home.html')

@app.route('/admin-login')
def pag_admin_login():
    return render_template('auth/admin-login.html')

#pagina de registro exitoso y usuario logeado
@app.route('/ingreso')
def pag_bienvenido():
    return render_template('auth/ingreso.html')

@app.route('/reg_exitoso')
def pag_reg_exitoso():
    return render_template('aut/reg_exitoso.html')


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
            flash('Usuario agregado exitosamente')
            return render_template('auth/reg_exitoso.html') # Redirige a página de éxito
        except MySQLdb.Error as e:
            flash(f'Error al agregar el usuario: {e}')
            return redirect(url_for('pag_registrar'))
        
    return redirect(url_for('pag_registrar'))

#para login 
@app.route('/ingresar_usuario', methods=['GET','POST'])
def ingresar_usuario():
    if request.method == 'POST':
        # Capturar los datos del formulario
        username = request.form['username']
        password = request.form['password']

        # Crear un objeto Usuario
        user = User(username, password)

        # Intentar hacer login
        try:
            logger_user = ModelUser.login(db, user)
            # Verifica si el usuario existe
            if logger_user is not None:
                # Comparar las contraseñas (texto plano)
                if logger_user.password == user.password:
                    return render_template('auth/ingreso.html')  # Redirige al éxito
                else:
                    flash("Usuario o contraseña incorrectos")
                    return render_template('auth/login.html')
            else:
                flash("Usuario o contraseña incorrectos")
                return render_template('auth/login.html')

        except Exception as e:
            flash(f'Error durante el inicio de sesión: {str(e)}')  # Captura el error
            return render_template('auth/login.html')

    # Si es un método GET, simplemente renderiza la página de login
    return render_template('auth/login.html')

# INGRESAR ADMINISTRADOR 
@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login(): 
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        admi = Admi(username, password)
        try:
            logged_admi = ModelAdmi.login(db.database, admi)
            if logged_admi is not None:
                if logged_admi.password == admi.password:
                    login_user(logged_admi)
                    # Pasar nombre y apellido al template
                    try:
                        return render_template('auth/pag_admi/ingreso_admi.html', nombre=logged_admi.name)
                    except Exception as e:
                        flash(f'Error al renderizar la plantilla: {str(e)}')
                        return redirect(url_for('admin_login'))  # O cualquier otra ruta que quieras
                    #return render_template('auth/pag_admi/ingreso_admi.html', nombre=logged_admi.name)
                else:
                    flash("contraseña incorrectos")
            else:
                flash("Usuario incorrectos")
        except Exception as e:
            flash(f'Error durante el inicio de sesión: {str(e)}')
    return render_template('auth/login_admi.html')
#@app.route('/escuhar_mp3')
#def podcast():
#    with connection.cursor() as cursor:
#        # Consulta para obtener las rutas de los audios
#        sql = "SELECT nombre, ruta FROM archivos"
#        cursor.execute(sql)
#        audios = cursor.fetchall()
#    return render_template('podcast.html', audios=audios)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
