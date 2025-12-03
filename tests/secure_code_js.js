// Código JavaScript seguro - Buenas prácticas

// 1. Validación de entrada sin eval()
function processUserInput(userInput) {
    // Validar y sanitizar entrada
    const sanitized = String(userInput).replace(/[^a-zA-Z0-9]/g, '');
    return sanitized.toLowerCase();
}

// 2. Consultas preparadas (Prepared Statements)
function getUserData(username) {
    // Usar parametrización
    const query = "SELECT * FROM users WHERE username = ?";
    return db.execute(query, [username]);
}

// 3. Escape de salida para prevenir XSS
function displayMessage(message) {
    const safe = document.createTextNode(message);
    document.getElementById('output').textContent = message;
}

// 4. Variables de entorno para credenciales
const API_KEY = process.env.API_KEY;
const DB_PASSWORD = process.env.DB_PASSWORD;

// 5. Validación de comandos
const { execFile } = require('child_process');
function runCommand(cmd) {
    // Usar lista blanca de comandos
    const allowedCommands = ['list', 'status', 'info'];
    if (allowedCommands.includes(cmd)) {
        execFile('ls', ['-l'], (error, stdout) => {
            console.log(stdout);
        });
    }
}

// 6. Generador criptográfico seguro
const crypto = require('crypto');
function generateToken() {
    return crypto.randomBytes(32).toString('hex');
}

// 7. Validación de path
const path = require('path');
const fs = require('fs');
function readFile(filename) {
    const safePath = path.join('/data', path.basename(filename));
    return fs.readFileSync(safePath, 'utf8');
}

// 8. Prevención de Prototype Pollution
function merge(target, source) {
    for (let key in source) {
        if (Object.prototype.hasOwnProperty.call(source, key) && key !== '__proto__') {
            target[key] = source[key];
        }
    }
    return target;
}

// 9. Validación de JSON
function deserialize(data) {
    try {
        const parsed = JSON.parse(data);
        // Validar estructura esperada
        if (typeof parsed === 'object' && parsed !== null) {
            return parsed;
        }
    } catch (e) {
        return null;
    }
}

// 10. Sanitización de consultas NoSQL
function findUser(username) {
    // Validar tipo y contenido
    if (typeof username !== 'string') return null;
    const sanitized = username.replace(/[^\w\s]/gi, '');
    return db.collection('users').findOne({ username: sanitized });
}
