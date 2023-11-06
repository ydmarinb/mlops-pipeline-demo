import os
import subprocess
import glob
from google.cloud import storage
from google.cloud import pubsub

# Configura las credenciales de autenticación de Google Cloud
# 
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials.json"

# Configura el cliente de almacenamiento de Google Cloud
client = storage.Client()


project_id = 'ydmarinb'

topic_name = "new-model"

# Ruta al directorio base que contiene las carpetas de modelos
base_dir = "C:/Users/ydmarinb/Desktop/demo/models-demo-mlops/"

# Nombre del bucket de almacenamiento de Google Cloud
bucket_name = "registry-models"


def run_tests_and_upload_model(model_dir_path):

    model_name = model_dir + '.pkl'
    hiper_name = 'hiperparametros_' + model_dir + '.txt'

    if model_name:

        tests_dir = model_dir_path + '/tests/'
        os.chdir(tests_dir)

        # Ejecuta los tests unitarios en el directorio del modelo
        result = subprocess.run(["pytest"], capture_output=True)

        # Retornar al directorio del modelo
        os.chdir('../')

        if result.returncode == 0:

            

            # Los tests pasaron, verifica y guarda el modelo si es necesario
            model_path = model_dir_path + f'/{model_name}'
            hiper_path = model_dir_path + f'/{hiper_name}'
            
            if not is_model_uploaded(model_name):
                # Guarda el modelo en el bucket de almacenamiento
                upload_file(model_path)

                # Guarda hiperparametros
                upload_file(hiper_path)

                # Retornar al directorio raiz
                os.chdir('../')
                print("Nuevo modelo registrado: ", model_name)
                publish_message("Nuevo modelo")
            else:
                print("Modelo ya registrado:", model_name)

        else:
            # Los tests fallaron
            print("Los tests no pasaron para el modelo:", os.path.basename(model_dir))

    else:
        print('Modelo sin finalizar: ', model_dir_path)

    
def is_model_uploaded(model_name):
    # Verifica si el modelo ya está guardado en el bucket de almacenamiento
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(model_name)
    return blob.exists()

def upload_file(model_path):
    # Guarda el modelo en el bucket de almacenamiento
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(os.path.basename(model_path))
    blob.upload_from_filename(model_path)




def publish_message(message):
    # Crea el cliente de Pub/Sub
    publisher = pubsub.PublisherClient()

    # Crea el nombre completo del tema
    topic_path = publisher.topic_path(project_id, topic_name)

    # Convierte el mensaje a bytes
    message_bytes = message.encode("utf-8")

    # Publica el mensaje en el tema
    future = publisher.publish(topic_path, data=message_bytes)
    message_id = future.result()

    print("Mensaje publicado en Pub/Sub. ID del mensaje:", message_id)

if __name__ == "__main__":
    # Obtén las carpetas que comienzan con "model" en el directorio base
    model_dirs = [folder for folder in os.listdir(base_dir) if folder.startswith("model")]

    for model_dir in model_dirs:
        model_dir_path = os.path.join(base_dir, model_dir)
        run_tests_and_upload_model(model_dir_path)


####