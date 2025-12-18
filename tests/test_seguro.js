// test_seguro.js
// Versión segura del test: sin vulnerabilidades

function ejecutarCodigoSeguro(codigo) {
    // No usar eval, solo operaciones seguras
    try {
        // Solo permitimos operaciones matemáticas simples
        let resultado = Number(codigo) + 2;
        return resultado;
    } catch (e) {
        return null;
    }
}

function consultaSQLSeguro(userInput) {
    // Usar parámetros en la consulta (simulado)
    let query = "SELECT * FROM users WHERE name = ?";
    // En una app real, pasar userInput como parámetro
    return query;
}

function xssSeguro(userInput) {
    // No usar innerHTML, usar textContent para evitar XSS
    document.getElementById('output').textContent = userInput;
}

// Pruebas de ejemplo
console.log(ejecutarCodigoSeguro('2'));
console.log(consultaSQLSeguro("admin' OR '1'='1"));
xssSeguro('<img src=x onerror=alert(1)>');
