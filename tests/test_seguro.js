// test_seguro.js
// Versión segura del test: sin vulnerabilidades

function ejecutarCodigoSeguro(codigo) {
    // Solo operaciones matemáticas simples
    let resultado = Number(codigo) + 2;
    return resultado;
}

function consultaSQLSeguro(userInput) {
    // Simulación de consulta segura (sin SQL real)
    let query = "Consulta segura ejecutada";
    return query;
}

function xssSeguro(userInput) {
    // No usar innerHTML, usar textContent para evitar XSS
    document.getElementById('output').textContent = userInput;
}

// Pruebas de ejemplo
console.log(ejecutarCodigoSeguro('2'));
console.log(consultaSQLSeguro("admin"));
xssSeguro('prueba');
