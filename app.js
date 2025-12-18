// app.js
// Aplicación Node.js segura y simple para despliegue en Railway

const express = require('express');
const helmet = require('helmet');
const app = express();
const PORT = process.env.PORT || 3000;

// Seguridad básica
app.use(helmet());
app.use(express.json());

// Ruta principal
app.get('/', (req, res) => {
  res.send('¡Despliegue actualizado en Railway! 🚀 Cambios reflejados en producción.');
});

// Ruta de prueba segura
app.post('/echo', (req, res) => {
  // Sanitizar entrada (solo texto alfanumérico)
  const input = req.body.input;
  if (typeof input !== 'string' || !/^[\w\s]+$/.test(input)) {
    return res.status(400).json({ error: 'Entrada inválida' });
  }
  res.json({ echo: input });
});

app.listen(PORT, () => {
  console.log(`Servidor escuchando en puerto ${PORT}`);
});
