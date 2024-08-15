// Configuración del reconocimiento de voz inicial para elegir entre registro o menú
function speak(text) {
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = 'es-ES';
    window.speechSynthesis.speak(utterance);
}

const initialRecognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
initialRecognition.lang = 'es-ES';

initialRecognition.onstart = function() {
    speak('Se encuentra en la pagina de registar usuario.Si desea registarse , diga registrar. En cambio, si desea ver los demas servicios diga menu');
};

initialRecognition.onresult = function(event) {
    const speechResult = event.results[0][0].transcript.toLowerCase();

    if (speechResult.includes('menu')) {
        speak('Las siguientes opciones son: Para ingresar, diga ingresar. Si quiere saber más sobre Include, diga sobre include. Si quiere ver servicios, diga servicios. Puede saber sobre cada uno: audiolibros, cursos, y podcast. Si quiere contactar, diga contacto.');
        initialRecognition.stop(); // Detenemos el primer reconocimiento
        menuRecognition.start(); // Iniciamos el reconocimiento para el menú
        console.log("voz del menu.");

    } else if (speechResult.includes('registrar')) {
        initialRecognition.stop(); 
        speak('Por favor, indique su nombre.');// Detenemos el primer reconocimiento
        registrationRecognition.start(); // Iniciamos el reconocimiento para el registro
    } else {
        speak('Lo siento, no entendí eso.');
    }
};

// configuro menu de reconocimiento
const menuRecognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
menuRecognition.lang = 'es-ES';

menuRecognition.onresult = function(event) {
    const speechMenu = event.results[0][0].transcript.toLowerCase();
    if (speechMenu.includes('ingresar')) {
        menuRecognition.stop();
        window.location.href = '/login';
    } else if (speechMenu.includes('contacto')) {
        menuRecognition.stop();
        window.location.href = '/contacto';
    } else if (speechMenu.includes('servicios')) {
        menuRecognition.stop();
        window.location.href = '/servicios';
    } else if (speechMenu.includes('cursos')) {
        menuRecognition.stop();
        window.location.href = '/cursos';
    } else if (speechMenu.includes('podcast')) {
        menuRecognition.stop();
        window.location.href = '/podcast';
    } else if (speechMenu.includes('audiolibros')) {
        menuRecognition.stop();
        window.location.href = '/audiolibros';
    } else if (speechMenu.includes('sobre include')) {
        menuRecognition.stop();
        window.location.href = '/sobre-include';    
    }else if (speechMenu.includes('normas')) {
        menuRecognition.stop();
        window.location.href = '/normas';        
    } else {
        speak('Lo siento, no entendí eso.');
    }
};


// Configuración del reconocimiento de voz para el registro
const registrationRecognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
registrationRecognition.lang = 'es-ES';

registrationRecognition.onresult = function(event) {
    const transcript = event.results[0][0].transcript.toLowerCase();

    const nameU_Field = document.getElementById('username');
    const nameField = document.getElementById('name');
    const lastnameField=document.getElementById('lastname')
    const emailField = document.getElementById('email');
    const passwordField = document.getElementById('password');
    const conf_passwordField = document.getElementById('confirm_password');
    const birthField = document.getElementById('birth_date');
    const phoneField = document.getElementById('phone');
    const countryField = document.getElementById('country');

    if (!nameU_Field.value) {
        nameU_Field.value = transcript;
        speak('Nombre de usuario registrado. Ahora, indique su nombre.');
    }else if(!nameField.value){
        nameField.value = transcript;
        speak('Nombre registrado. Ahora, indique su correo apellido.');
    }else if(!lastnameField.value){
        lastnameField.value = transcript;
        speak('Apellido registrado. Ahora, indique su correo.');
    }else if (!emailField.value) {
        emailField.value = transcript.replace(/\s+/g, '') + '@ejemplo.com';
        speak('Correo electrónico registrado. Ahora, indique su contraseña.');
    }else if(!passwordField.value){
        passwordFieldd.value = transcript;
        speak('contraseña registrado. Vuelva a repetir la contraseña.');
    }else if(!conf_passwordField.value){
        conf_passwordFieldd.value = transcript;
        speak('Contraseña registrada. Ahora, indique su fecha de nacimiento.');
    }else if (!birthField.value) {
        birthField.value = transcript.replace(/\s+/g, '') + '@ejemplo.com';
        speak('Fecha de nacimiento registrada. Ahora, indique su telefono.');
    }else if (!phoneField.value) {
        phoneField.value = transcript.replace(/\s+/g, '') + '@ejemplo.com';
        speak('Telefono registrado. Ahora, indique su pais.'); 
    }else if (!countryField.value) {
        countryField.value = transcript.split(' ').join('');
        speak('Pais registrad. Proceso de registro completado.Diga enviar para finalizar');
        console.log("Detección de voz para el formulario terminada.")
        registrationRecognition.stop(); // Detenemos el reconocimiento una vez que el registro esté completo
        enviarRecognition.star()
    } else {
        speak('Lo siento, no entendí eso.');
    }
};

// Configuración del reconocimiento de voz para "enviar"
const enviarRecognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
enviarRecognition.lang = 'es-ES';

enviarRecognition.onresult = function(event) {
    const speechenviar = event.results[0][0].transcript.toLowerCase();
    if (speechenviar.includes('enviar')) {
        speak('Formulario enviado.');
        document.getElementById('registration-form').submit(); // Enviamos el formulario
        enviarRecognition.stop(); // Detenemos el reconocimiento de voz
    } else {
        speak('Lo siento, no entendí eso. Por favor, diga "enviar" para enviar el formulario.');
    }
};

// Iniciar el reconocimiento de voz inicial automáticamente
window.onload = function() {
    initialRecognition.start();
};