# pip install google-cloud-aiplatform -> instalar el cdk de vertex ai para python

import pickle
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import  manejador_datos


manejador_datos.copiar_ultimo_archivo_en_carpeta_actual()
model = 'model_v1'

# load data
df = pd.read_csv(manejador_datos.obtener_nombre_csv_unico('./'))
X = df.drop(columns=['id_usuario', 'direccion', 'producto'])
y = df['producto']


 
# split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

# train ml model
rf = RandomForestClassifier(n_estimators=50, random_state=42, max_features="log2")
rf.fit(X_train, y_train)

# Abre un archivo de texto en modo escritura
with open(f"hiperparametros_{model}.txt", "w", encoding="utf-8") as file:
    # Escribe los hiperparámetros en el archivo
    file.write(f"Tipo de modelo:{type(rf)}\n")
    for k,v in rf.get_params().items():
        file.write(f"{k}: {v}\n")


# Save the model to a file
with open(f"{model}.pkl", "wb") as f:
    pickle.dump(rf, f)








