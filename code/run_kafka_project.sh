#!/bin/bash

# Función para verificar si un comando se ejecutó correctamente
check_command() {
  if [ $? -ne 0 ]; then
    echo "Error: $1 no se ejecutó correctamente."
    exit 1
  fi
}

# Instalar dependencias
echo "Instalando dependencias..."
pip install -r requirements.txt
check_command "pip install -r requirements.txt"

# Levantar los servicios con Docker Compose
echo "Iniciar servicios con Docker Compose..."
docker compose up -d
check_command "docker compose up -d"

# Esperar unos segundos para asegurar que todos los servicios estén levantados
echo "Esperando 20 segundos para estabilizar servicios..."
for i in {1..20}; do
    echo -n "$i."
    sleep 1
done
#sleep 20  # Ajusta según sea necesario

# Verificar el estado de KSQLDB
echo "Verificando estado de KSQLDB server..."
python verificar_estado_ksqldb_server.py
check_command "verificar_estado_ksqldb_server.py"

sleep 2
# Ejecutar los pasos operativos en paralelo

## Paso 1: Leer CSV y pasar a un topic 1
echo "Ejecutando ingesta de datos..."
nohup python step1.py > step1.log 2>&1 &
check_command "step1.py"

## Paso 2: Consumir datos de topic 1, realizar análisis de sentimiento y pasar a topic 2
echo "Ejecutando Análisis de sentimiento..."
nohup python step2.py > step2.log 2>&1 &
check_command "step2.py"

## Paso 3: Consumir datos de topic 2 y escribir en MongoDB
echo "Guardando datos de análsis de sentimiento en mongodb..."
nohup python step3_db_writer.py > step3_db_writer.log 2>&1 &
check_command "step3_db_writer.py"

# Esperar 5 segundos antes de ejecutar los siguientes pasos
echo "Esperando 5 segundos... por procesos iniciales para agregacion"
sleep 5

## Paso 4: Crear tablas de agregación con ksqldb a partir de topic 2 y crear topic 3
echo "Ejecutando agregación con ksqldb..."
nohup python step3_ksqldb.py > step3_ksqldb.log 2>&1 &
check_command "step3_ksqldb.py"

## Paso 5: Consumir topic 3 y guardar en MongoDB
echo "Guardando datos agregados en mongodb..."
nohup python step4_save_mongodb.py > step4_save_mongodb.log 2>&1 &
check_command "step4_save_mongodb.py"

echo "Todos los pasos se ejecutaron correctamente."

# Configurar la aplicación Flask
export FLASK_APP=app.py

# Iniciar la aplicación Flask
echo "Iniciando la aplicación Flask..."
nohup flask run --host=0.0.0.0 --port=5000 > flask.log 2>&1 &
check_command "flask run"

sleep 3
echo "Aplicación Flask iniciada correctamente."

    xdg-open http://localhost:5000/


echo "Si web app no se abre en browser automaticamente, ir a http://localhost:5000/"

