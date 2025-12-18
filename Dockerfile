# Dockerfile para el Scanner de Vulnerabilidades con ML
# Imagen optimizada para ejecución en CI/CD

FROM node:20-slim

# Metadatos
LABEL maintainer="Security Team"
LABEL description="ML-based Vulnerability Scanner for Python and JavaScript"
LABEL version="1.0.0"




# Directorio de trabajo
WORKDIR /app





# Copiar código fuente


# Copiar archivos de Node.js
COPY package.json .
COPY package-lock.json .
COPY app.js .

# Instalar dependencias de Node.js
RUN npm install --omit=dev


# Exponer el puerto de la app Node.js
EXPOSE 3000

# Comando por defecto
CMD ["npm", "start"]
