// Código JavaScript con múltiples vulnerabilidades

// 1. Uso de eval() - Code Injection
function processUserInput(userInput) {
    return eval(userInput);
}

// 2. SQL Injection
function getUserData(username) {
    const query = "SELECT * FROM users WHERE username = '" + username + "'";
    return db.execute(query);
}

// 3. XSS - Cross-Site Scripting
function displayMessage(message) {
    document.getElementById('output').innerHTML = message;
}

// 4. Hardcoded credentials
const API_KEY = "sk-1234567890abcdef";
const DB_PASSWORD = "admin123";

// 5. Command Injection
const { exec } = require('child_process');
function runCommand(cmd) {
    exec('ls ' + cmd, (error, stdout) => {
        console.log(stdout);
    });
}

// 6. Insecure Random
function generateToken() {
    return Math.random().toString(36).substring(7);
}

// 7. Path Traversal
const fs = require('fs');
function readFile(filename) {
    return fs.readFileSync('/data/' + filename, 'utf8');
}

// 8. Prototype Pollution
function merge(target, source) {
    for (let key in source) {
        target[key] = source[key];
    }
    return target;
}

// 9. Insecure Deserialization
function deserialize(data) {
    return JSON.parse(data);
}

// 10. NoSQL Injection
function findUser(username) {
    return db.collection('users').find({ username: username });
}
