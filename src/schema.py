from enum import Enum


class Model_List(str, Enum):
    Linear_reg = "Linear Regression Model"
    K_nn = "k-Nearest Neighbor Model"
    Lstm = "LSTM Model"