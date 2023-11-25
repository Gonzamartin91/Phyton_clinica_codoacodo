//Declaracion de constantes

const LONG_MIN_NOMBRE = 3;
const LONG_MIN_APELLIDO = 1;
const LONG_MIN_CONSULTA = 3;
const REGEX_CORREO = /^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/;


const FONDO_ERROR = 'rgba(255, 0, 0, 0.1)';
const FONDO_OK = '#ffffff';


// Funciones de validación


// Si el campo nombre tiene menos de <LONG_MIN_NOMBRE> caracteres, el fondo cambia a <FONDO_ERROR>
function validarNombre() {
    let valido = false;
    const nombre = document.getElementById('nombre');

    if (nombre.value.length < LONG_MIN_NOMBRE) {
        nombre.style.backgroundColor = FONDO_ERROR;
    } else {
        nombre.style.backgroundColor = FONDO_OK;
        valido = true;
    }

    return valido;
}

/*
// Si el campo apellido tiene menos de <LONG_MIN_APELLIDO> caracteres, el fondo cambia a <FONDO_ERROR>
function validarApellido() {
    let valido = false;
    const apellido = document.getElementById('apellido');

    if (apellido.value.length < LONG_MIN_APELLIDO) {
        apellido.style.backgroundColor = FONDO_ERROR;
    } else {
        apellido.style.backgroundColor = FONDO_OK;
        valido = true;
    }

    return valido;
}

*/

// Si el campo email no matchea con la <REGEX_CORREO>, el fondo cambia a <FONDO_ERROR>
function validarEmail() {
    let valido = false;
    const email = document.getElementById('email');

    if (!REGEX_CORREO.test(email.value)) {
        email.style.backgroundColor = FONDO_ERROR;
    } else {
        email.style.backgroundColor = FONDO_OK;
        valido = true;
    }

    return valido;
}

// Si el campo consulta tiene menos de <LONG_MIN_CONSULTA> caracteres, el fondo cambia a <FONDO_ERROR>
function validarConsulta() {
    let valido = false;
    const consulta = document.getElementById('');

    if (consulta.value.length < LONG_MIN_CONSULTA) {
        consulta.style.backgroundColor = FONDO_ERROR;
    } else {
        consulta.style.backgroundColor = FONDO_OK;
        valido = true;
    }
    return valido;
}

// Si alguno de los campos no es válido no envía la consulta y cambia a <FONDO_ERROR>
function validar() {
    let valido = validarNombre();
    valido = validarApellido() && valido;
    valido = validarEmail() && valido;
    valido = validarConsulta() && valido;
    return valido;
}


