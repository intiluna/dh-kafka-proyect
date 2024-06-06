#!/bin/bash

# Función para matar un proceso por su nombre
kill_process() {
  process_name=$1
  pids=$(ps aux | grep $process_name | grep -v grep | awk '{print $2}')
  
  if [ -z "$pids" ]; then
    echo "No se encontraron procesos para $process_name"
  else
    echo "Eliminando procesos para $process_name"
    for pid in $pids; do
      kill $pid
      echo "Proceso $pid eliminado"
    done
  fi
}

# Procesos a matar
processes=("step1_ingest_producer.py" "step2_cp_sa.py" "step3_consumer_db_writer.py" "step3_ksql_agg.py" "step4_datos_agregados_save_mongodb.py", "flask")

# Matar todos los procesos
for process in "${processes[@]}"; do
  kill_process $process
done

echo "Todos los procesos han sido eliminados."

