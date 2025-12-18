// app.js
// Aplicación Node.js segura y simple para despliegue en Railway

const express = require('express');
const helmet = require('helmet');
const app = express();
const PORT = process.env.PORT || 3000;

// Seguridad básica
app.use(helmet());

// Ruta principal
app.get('/', (req, res) => {
  res.send('¡App segura desplegada en Railway!');
});

app.listen(PORT, () => {
  console.log(`Servidor escuchando en puerto ${PORT}`);
});
