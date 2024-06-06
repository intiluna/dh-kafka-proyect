import requests
import time

def check_ksqldb_status(url, retries=5, delay=10):
    for i in range(retries):
        try:
            response = requests.get(url)
            response.raise_for_status()
            if '"serverStatus":"RUNNING"' in response.text:
                print("KSQLDB está corriendo.")
                return True
        except requests.RequestException as e:
            print(f"Intento {i+1}/{retries}: Error al verificar el estado de KSQLDB: {e}")
        print(f"Esperando {delay} segundos antes de reintentar...")
        time.sleep(delay)
    return False

def main():
    ksqldb_url = "http://localhost:8088/info"
    while not check_ksqldb_status(ksqldb_url):
        print("KSQLDB no está en estado RUNNING. Reintentando...")
        time.sleep(5)
    print("KSQLDB está en estado RUNNING. Procediendo con el resto de los scripts.")

if __name__ == "__main__":
    main()

