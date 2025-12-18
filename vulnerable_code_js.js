function ejecutarOperacion(operacion, a, b) {
    const operacionesPermitidas = {
        suma: (x, y) => x + y,
        resta: (x, y) => x - y,
        multiplicacion: (x, y) => x * y,
        division: (x, y) => y !== 0 ? x / y : null
    };

    if (!operacionesPermitidas[operacion]) {
        throw new Error("Operación no permitida");
    }

    return operacionesPermitidas[operacion](a, b);
}