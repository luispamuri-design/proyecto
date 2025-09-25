# Imagen base con Python 3.12 slim
FROM python:3.12-slim

# Evitar generación de archivos pyc y buffer
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Instalar dependencias del sistema necesarias para Django, Pillow y PostgreSQL
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    libfreetype6-dev \
    liblcms2-dev \
    libopenjp2-7-dev \
    libtiff5-dev \
    libwebp-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copiar archivo de dependencias
COPY requirements.txt .

# Instalar pip y dependencias de Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copiar todo el proyecto al contenedor
COPY . .

# Crear carpeta para archivos estáticos
RUN mkdir -p /app/staticfiles

# Exponer puerto 8000
EXPOSE 8000

# Comando para correr Django con Gunicorn
CMD ["gunicorn", "veterinaria.wsgi:application", "--bind", "0.0.0.0:8000"]
