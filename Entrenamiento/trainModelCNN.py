import tensorflow as tf
from tensorflow.keras import layers, models
import cv2, os, numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

# Función para cargar imágenes
def load_images(path, label, size=(64,64)):
    X, y = [], []
    for file in os.listdir(path):
        img = cv2.imread(os.path.join(path, file), cv2.IMREAD_GRAYSCALE)
        if img is None:
            continue
        img = cv2.resize(img, size)
        X.append(img/255.0)  # normalizar
        y.append(label)
    return X, y

# Cargar dataset
X_good, y_good = load_images(r"Entrenamiento\Zeta_augmented\Zetas_Buenas_aug", 0)
X_bad, y_bad = load_images(r"Entrenamiento\Zeta_augmented\Zetas_Malas_aug", 1)

X = np.array(X_good + X_bad).reshape(-1,64,64,1)
y = np.array(y_good + y_bad)

# Split train/test
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2,stratify=y)

# Modelo CNN
model = models.Sequential([
    layers.Conv2D(32,(3,3),activation="relu",input_shape=(64,64,1)),
    layers.MaxPooling2D((2,2)),
    layers.Conv2D(64,(3,3),activation="relu"),
    layers.MaxPooling2D((2,2)),
    layers.Flatten(),
    layers.Dense(64,activation="relu"),
    layers.Dense(1,activation="sigmoid")  # salida binaria
])

model.compile(optimizer="adam",loss="binary_crossentropy",metrics=["accuracy"])

# Entrenamiento
history = model.fit(X_train,y_train,epochs=20,validation_data=(X_test,y_test))

# Guardar modelo en el mismo lugar donde corres el script
model.save("clasificador_zetas_cnn_V4.h5")

# Evaluación
y_pred = (model.predict(X_test) > 0.5).astype("int32")

print("📊 Reporte de clasificación:")
print(classification_report(y_test, y_pred, target_names=["Buena","Mala"]))

# Matriz de confusión
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=["Buena","Mala"], yticklabels=["Buena","Mala"])
plt.xlabel("Predicción")
plt.ylabel("Real")
plt.title("Matriz de Confusión")
plt.show()

