import pickle

def load_model():
    with open("model.pkl", "rb") as f:
        model = pickle.load(f)
    return model

# Cargar el modelo una sola vez al importar el módulo
ml_model = load_model()