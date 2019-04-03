from tensorflow import keras
from tensorflow.keras.utils import plot_model

# First install graphviz and pydot through pip3
# Then install graphviz as application: https://www.graphviz.org/

MODEL_PATH = '../models/trained_with_random'
MODEL_NUMBER = "500000_moves"

print("Start loading model")
model = keras.models.load_model(f"{MODEL_PATH}/model_jort_{MODEL_NUMBER}.h5")
print("Finished loading model")

plot_model(model, show_shapes=True, show_layer_names=False, to_file="../models/trained_with_random/model_jort_500000_moves.pdf")