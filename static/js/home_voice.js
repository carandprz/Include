// Función para convertir texto a voz
function speak(text) {
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = 'es-ES';
    window.speechSynthesis.speak(utterance);
}

// Configuración del reconocimiento de voz
const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
recognition.lang = 'es-ES';

recognition.onstart = function() {
    speak('Bienvenido a include .¿En qué puedo ayudarte?.Si desea registrarse, diga registrar. Para ingresar, diga ingresar.Si quiere saber más sobre include, diga sobre include.Si quiere ver servicios, diga servicios.Puede saber sobre cada uno: audiolibros, cursos, y podcast. Si quiere contactar, diga contacto.');
};

recognition.onresult = function(event) {
    const speechResult = event.results[0][0].transcript.toLowerCase();
    if (speechResult.includes('registrar')) {
        recognition.stop(); // detiene reconocimiento de voz
        window.location.href = '/registro';
        console.log('Redireccionando a la página "registrar"');
    } else if (speechResult.includes('ingresar')) {
        recognition.stop();
        window.location.href = '/login';
    } else if (speechResult.includes('contacto')) {
        recognition.stop();
        window.location.href = '/contacto';
    } else if (speechResult.includes('servicios')) {
        recognition.stop();
        window.location.href = 'servicios';
    } else if(speechResult.includes('cursos')) {
        recognition.stop();
        window.location.href = '/cursos';
    } else if(speechResult.includes('podcast')) {
        recognition.stop();
        window.location.href = '/podcast';
    } else if(speechResult.includes('audiolibros')) {
        recognition.stop();
        window.location.href = '/audiolibros';
    } else if (speechResult.includes('sobre include')) {
        recognition.stop();
        window.location.href = '/nosotros';    
    } else {
        speak('Lo siento, no entendí eso.');
    }
};

document.getElementById('start-listening').addEventListener('click', function() {
    recognition.start();
});

// Leer el contenido del atributo title al pasar el puntero del mouse sobre la frase
const welcomeMessage = document.getElementById('welcome-message');
welcomeMessage.addEventListener('mouseover', function() {
    const titleText = welcomeMessage.getAttribute('title');
    speak(titleText);
});

//FUNCIONA 