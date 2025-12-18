// vulnerable_code_js.js
// Ejemplo de código vulnerable para pruebas ML

function ejecutarCodigo(codigo) {
    // Vulnerabilidad: uso de eval
    return eval(codigo);
}

function consultaSQL(userInput) {
    // Vulnerabilidad: concatenación directa en consulta SQL
    let query = "SELECT * FROM users WHERE name = '" + userInput + "'";
    return query;
}

function xssVulnerable(userInput) {
    // Vulnerabilidad: asignación directa a innerHTML
    document.getElementById('output').innerHTML = userInput;
}

// Pruebas de ejemplo
console.log(ejecutarCodigo('2+2'));
console.log(consultaSQL("admin' OR '1'='1"));
xssVulnerable('<img src=x onerror=alert(1)>');
