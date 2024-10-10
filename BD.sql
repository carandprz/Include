create database bd;
#drop database bd;
-- Tabla para almacenar información de los usuarios
CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario varchar(10) PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    correo_electronico VARCHAR(100) NOT NULL,
    contrasena VARCHAR(255) NOT NULL, -- Se recomienda usar un hash en lugar de almacenar la contraseña directamente
    fecha_nacimiento DATE NOT NULL,
    telefono VARCHAR(20),
    pais VARCHAR(50),
    fecharegistro TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
);

#-------------------- Tabla para almacenar información del contenido -------------------------------------
CREATE TABLE IF NOT EXISTS biblioteca (
    id_biblioteca INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    titulo VARCHAR(100) NOT NULL,
    descripcion TEXT,
    fecha_publicacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_canciones int not null , 
    id_autor int not null
);

drop table canciones;
create table autor (
id_autor int ,
nombre varchar (50) not null,
apellido varchar (50) not null
);

---para el usuario crear listas
CREATE TABLE IF NOT EXISTS listas_reproduccion (
#permite a los usuarios crear listas personalizadas de canciones. Cada lista tiene un nombre y está asociada a un usuario a través de su ID.
    id_lista INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    usuario_id varchar(10) NOT NULL
);

CREATE TABLE IF NOT EXISTS canciones (
    id_canciones INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(100) NOT NULL,
    id_autor int NOT NULL,
    album VARCHAR(100),
    duracion INT , -- Duración en segundos
    ruta_mp3 VARCHAR(255) NOT NULL, -- Ruta al archivo de la canción en el sistema de archivos o URL
    imagen_album VARCHAR(255), -- Ruta a la imagen del álbum en el sistema de archivos o URL
    genero VARCHAR(50)
    ---contiene informacion sobre las canciones 
);
create table autor(
id_autor varchar(10) primary key not null,
nombre varchar (50) not null , 
apellido varchar (50) not null, 
genero varchar(10) not null 
);

CREATE TABLE IF NOT EXISTS lista_canciones (
    lista_id INT NOT NULL,
    cancion_id INT NOT NULL,
    FOREIGN KEY (lista_id) REFERENCES listas_reproduccion(id_lista),
    FOREIGN KEY (cancion_id) REFERENCES canciones(id_canciones)
    #relacion entre canciones y lista de usuarios
);

#-------------------------------- ADMINISTRADORES ------------------------------------
-- Tabla para almacenar información de los administradores
CREATE TABLE IF NOT EXISTS administradores (
    usuario varchar(10) primary key,
    nombre_completo VARCHAR(50) NOT NULL,
    correo_electronico VARCHAR(100) NOT NULL,
    contrasena VARCHAR(255) NOT NULL, -- Se recomienda usar un hash en lugar de almacenar la contraseña directamente
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


#tabla que habla sobre el archivo 
CREATE TABLE audios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    file_name VARCHAR(255) NOT NULL,
    file_path VARCHAR(255) NOT NULL
);

-- Tabla para almacenar el contenido subido por los administradores
CREATE TABLE IF NOT EXISTS contenido_administrador (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(100) NOT NULL,
    descripcion TEXT,
    contenido TEXT NOT NULL,
    fecha_publicacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    administrador_id INT NOT NULL,
    FOREIGN KEY (administrador_id) REFERENCES administradores(id_admi)
);

-- Tabla de registro de acciones de administrador
CREATE TABLE IF NOT EXISTS registro_actividades_administrador (
    id_act INT AUTO_INCREMENT PRIMARY KEY,
    fecha_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    administrador_id INT NOT NULL,
    accion VARCHAR(100) NOT NULL,
    detalle TEXT,
    FOREIGN KEY (administrador_id) REFERENCES administradores(id_admi)
);
#---------------------------- PERMISOS DE ADMINISTRADORES ---------------------------------------
CREATE TABLE IF NOT EXISTS permisos (
    id_permiso INT AUTO_INCREMENT PRIMARY KEY,
    nombre_permiso VARCHAR(100) NOT NULL,
    descripcion TEXT
);
CREATE TABLE IF NOT EXISTS asignacion_permisos (
    id_admi INT NOT NULL,
    id_permiso INT NOT NULL,
    PRIMARY KEY (id_admi, id_permiso),
    FOREIGN KEY (id_admi) REFERENCES administradores(id_admi),
    FOREIGN KEY (id_permiso) REFERENCES permisos(id_permiso)
);


#-------------------- RELACIONES ---------------------
ALTER TABLE listas_reproduccion ADD CONSTRAINT fk_usuario_id
FOREIGN KEY (usuario_id) REFERENCES usuarios(id_usuario);

Alter table autor add primary key (id_autor);

ALTER TABLE canciones ADD CONSTRAINT fk_autor
FOREIGN KEY (id_autor) REFERENCES autor(id_autor);

ALTER TABLE biblioteca ADD CONSTRAINT fk_id_autor
FOREIGN KEY (id_autor) REFERENCES autor(id_autor);
