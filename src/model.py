__author__ = "Jeremy Nelson"

"""Complies and loads Tensorflow models"""

import pathlib
import tensorflow as tf  # type: ignore
from typing import Tuple

class Model(object):

    def __init__(self, config: dict, loss: str) -> None:
         self.config = config
         self.loss = loss
         self.model = None

    def load(self, checkpoint_path: pathlib.Path) -> None:
        if self.model is None:
            raise NameError("Cannot load, missing model")
        self.model.load_weights(checkpoint_path)
        

    def save(self, checkpoint_path: pathlib.Path) -> None:
        if self.model is None:
            raise NameError("Cannot save, missing model")
        self.model.save_weight(checkpoint_path)

  
    def build_model(self):
        raise NotImplementedError


class SimpleMnistModel(Model):

    def __init__(self, 
                 config: dict,
                 input_shape: Tuple,
                 loss: str='sparse_categorical_crossentropy') -> None:
        super(SimpleMnistModel, self).__init__(config, loss)
        self.input_shape = input_shape
        self.build_model()

    def build_model(self) -> None:
        self.model = tf.keras.models.Sequential()
        self.model.add(tf.keras.layers.Dense(32, 
            activation='relu', 
            input_shape=self.input_shape))
        self.model.add(tf.keras.layers.Dense(15, activation='relu'))
        self.model.add(tf.keras.layers.Dense(10, activation='softmax'))
        self.model.compile(
            loss=self.loss,
            optimizer='admin',
            metrics=['acc'])

                               

           

        

def compile_feedforward(number_classes):
    model = tf.keras.Sequential(
        [
            tf.keras.layers.Dense(64, activation="relu"),
            tf.keras.layers.Dense(64, activation="relu"),
            tf.keras.layers.Dense(number_classes, activation="softmax"),
        ]
    )
    model.compile(
        optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"]
    )
    return model
