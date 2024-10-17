import os
from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory
from flask_mysqldb import MySQL
import database as db
import MySQLdb.cursors
from werkzeug.utils import secure_filename
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

#onfiguración para la subida de archivos
UPLOAD_FOLDER = 'audios/'  # Carpeta donde se guardarán los archivos
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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

#rutas pie de paginas --------------------------------------------
@app.route('/normas')
def pag_normas():
    return render_template('normas.html')

@app.route('/contacto')
def pag_contacto():
    return render_template('contacto.html')

@app.route('/sobre-include')
def pag_nosotros():
    return render_template('sobre-include.html')

#---------------------------- administrador ------------------------------------------
@app.route('/registroProducto')
@login_required
def pag_registroProd():
    if session.get('is_admin'):
        if 'logged_in' in session and session['logged_in']:
            nombre_completo = session.get('nombre_completo', 'Usuario')
            #nombre_completo = session.get('nombre', 'Usuario') + " " + session.get('apellido', '')
            return render_template('auth/pag_admi/registro_producto.html', nombre_completo=nombre_completo)
        else:
            flash("Por favor, inicia sesión para acceder a esta página.")
            return redirect(url_for('pag_admin_login'))
        #return render_template('auth/admin_home.html')
    else:
        flash("Acceso denegado. Esta página es solo para administradores.")
        return redirect(url_for('pag_admin_login'))

@app.route('/admin-home')
@login_required
def pag_admin_home():
    if 'logged_in' in session and session['logged_in']:
        nombre_completo = session.get('nombre_completo', 'Usuario')
        #nombre_completo = session.get('nombre', 'Usuario') + " " + session.get('apellido', '')
        return render_template('auth/admin_home.html', nombre_completo=nombre_completo)
    else:
        flash("Por favor, inicia sesión para acceder a esta página.")
        return redirect(url_for('pag_admin_login'))
    #return render_template('auth/admin_home.ht11ml')

@app.route('/admin-login')
def pag_admin_login():
    return render_template('auth/admin-login.html')

#------------------------ pagina de registro exitoso ------------------
@app.route('/reg_exitoso')
def pag_reg_exitoso():
    return render_template('auth/reg_exitoso.html')


#------------------------ pagina usuario logeado ------------------
@app.route('/ingreso')
def pag_bienvenido():
    return render_template('auth/ingresoUsuario.html')


# --------------------------------- SALIR ------------------
#log out usuario
@app.route('/logout')
@login_required # protege paginas solo usuarios logeados pueden entrar
def logout():
    session.clear() #limpiar todas las paginas variables
    #sesion.pop('usuario',None)
    logout_user()
    print('has cerrado exitosamente la pagina')
    return redirect(url_for('index'))


#funciones 
# --------------------------------- REGISTRO DE USUARIOS ---------------------------------
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
        
        flash('Usuario ya existe')
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

#--------------------------- loggear USUARIO --------------------------------------
@app.route('/ingresar_usuario', methods=['GET', 'POST'])
def ingresar_usuario():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User(username, password)  # No es necesario pasar nombre y apellido aquí aún

        try:
            logged_user = ModelUser.login(db.database, user)

            if logged_user is not None:
                if logged_user.password == user.password:
                    login_user(logged_user)
                    # Almacenar datos en la sesión
                    session['logged_in'] = True
                    session['username'] = logged_user.username
                    session['nombre'] = logged_user.name
                    session['apellido'] = logged_user.lastname
                    session['is_admin'] = False  # Usuario regular
                    # Pasar nombre y apellido al template
                    return render_template('auth/ingresoUsuario.html', nombre=logged_user.name, apellido=logged_user.lastname)
                else:
                    flash("Usuario o contraseña incorrectos")
            else:
                flash("Usuario o contraseña incorrectos")

        except Exception as e:
            flash(f'Error durante el inicio de sesión: {str(e)}')

    return render_template('auth/login.html')



# --------------------------- PARA INGRESAR ADMINISTRADOR ----------------------------
@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login(): 
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        admi = Admi(username, password)
        try:
            logged_admi = ModelAdmi.login(db.database, admi)
            if logged_admi is not None:
                #session['usuario'] = logged_in_user.username
                if logged_admi.password == admi.password:
                    login_user(logged_admi)
                    # Almacenar datos en la sesión
                    session['logged_in'] = True
                    session['username'] = logged_admi.username
                    session['nombre'] = logged_admi.name
                    session['is_admin'] = True  # Usuario administrador
                    # Pasar nombre y apellido al template
                    try:
                        return render_template('auth/admin_home.html', nombre=logged_admi.name)
                    except Exception as e:
                        flash(f'Error al renderizar la plantilla: {str(e)}')
                        return redirect(url_for('admin-login'))  # O cualquier otra ruta que quieras
                    #return render_template('auth/pag_admi/ingreso_admi.html', nombre=logged_admi.name)
                else:
                    flash("contraseña incorrectos")
            else:
                flash("Usuario incorrectos")
        except Exception as e:
            flash(f'Error durante el inicio de sesión: {str(e)}')
    return render_template('auth/admin-login.html')


# -------------------------- FUNCION PARA LOS AUDIOS -----------------------
# Extensiones permitidas
ALLOWED_EXTENSIONS = {'mp3', 'wav', 'm4a'}

# Función para verificar si el archivo tiene una extensión permitida
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Ruta para servir los archivos subidos
@app.route('/audios/<filename>')
def audios(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/upload', methods=['POST'])
def upload_file():
    if session.get('is_admin'):
    # Recibir los datos del formulario
        titulo = request.form['titulo']
        descripcion = request.form['descripcion']
        tipo = request.form['tipo']
        autor = request.form['autor']

    # Verificar si se ha subido un archivo
        if 'archivo' not in request.files:
            flash('No se seleccionó ningún archivo')
            return redirect(url_for('pag_registroProd'))

        archivo = request.files['archivo']

    # Verificar si el archivo es válido
        if archivo.filename == '':
            flash('El nombre del archivo está vacío. Por favor selecciona un archivo.')
            return redirect(url_for('pag_registroProd'))
            #return 'No se seleccionó ningún archivo', 400

        if archivo and allowed_file(archivo.filename):
            # Guardar el archivo en el servidor
            filename = secure_filename(archivo.filename)
            archivo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # Guardar la información en la base de datos
            try:
                cursor = db.database.cursor()
                sql = """
                INSERT INTO audiolibros_podcasts (titulo, autor, descripcion, tipo, archivo)
                VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (titulo, autor, descripcion, tipo, filename))
                db.database.commit()
                cursor.close()
                db.database.close()
                flash('Archivo subido exitosamente')
                return redirect(url_for('pag_registroProd'))
            except Exception as e:
                flash(f'Error al subir el archivo: {str(e)}')
                return redirect(url_for('pag_registroProd'))
                #return f'Error al subir el archivo a la base de datos: {str(e)}', 500
        else:
            flash('Tipo de archivo no permitido. Solo se permiten archivos mp3, wav y m4a.')
            return redirect(url_for('pag_registroProd'))
            #return 'Tipo de archivo no permitido', 400

#---------------------- MOSTRAR BILIOTECA DE ADMINISTRADOR ---------------------------
@app.route('/library')
@login_required
def library():
    if session.get('is_admin'):
        try:
            cursor = db.database.cursor()
            sql = "SELECT titulo, descripcion, tipo, archivo, fecha_subida FROM audiolibros_podcasts"
            cursor.execute(sql)
            archivos = cursor.fetchall()
            cursor.close()
            db.database.close()
            return render_template('auth/pag_admi/biblioteca.html', archivos=archivos)
        
        except Exception as e:
            flash(f'Error al obtener los archivos: {str(e)}')
            return redirect(url_for('pag_admin_home'))
    else:
        flash("Acceso denegado. Esta página es solo para administradores.")
        return redirect(url_for('pag_admin_home'))


if __name__ == "__main__":
    # Crear la carpeta de uploads si no existe
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    
    app.run(port=5000, debug=True)
