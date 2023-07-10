import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Reshape, SimpleRNN, Dense, LSTM, Dropout
from utils import get_data_set_full, eval_result, eval_descansos, graficar, graficar_matrices
from excel import np_to_excel
rows = 15
cols = 32
depth = 3

model = Sequential()
model.add(Reshape((rows, cols*depth), input_shape=(rows, cols, depth)))
model.add(SimpleRNN(units=32, activation='relu', return_sequences=True))
model.add(LSTM(units=64, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(units=128, activation='relu'))
model.add(Dense(units=rows*cols*depth, activation='linear'))

model.compile(loss='mean_squared_error', optimizer='adam')

x, y = get_data_set_full()

X_train = np.array(x)
Y_train = np.array(y)

print(X_train.shape)
print(Y_train.shape)

y_train = Y_train.reshape((Y_train.shape[0], rows*cols*depth))

num_epochs = 15
model.fit(X_train, y_train, epochs=num_epochs, batch_size=32, verbose=1)


X_test = np.array([X_train[0]])
Y_test = np.array([Y_train[0]])
y_pred = model.predict(X_test)

y_pred = y_pred.reshape((y_pred.shape[0], rows, cols, depth))

np_to_excel('output',y_pred[0])


def round_to_closest(number):
    return number > 0.35

vectorized_round = np.vectorize(round_to_closest)

rounded_arr = vectorized_round(y_pred[0])

rounded_arr = np.rint(rounded_arr).astype(int)


np_to_excel('output_round',rounded_arr)

acc = eval_result(rounded_arr)
descansos = eval_descansos(rounded_arr)

graficar([Y_test[0],rounded_arr,y_pred[0]],['Propuesta Real','Propuesta del modelo ajustada','Propuesta del modelo'])
print('acc',acc)
print('desc',descansos)