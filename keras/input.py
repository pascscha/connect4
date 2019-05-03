import numpy as np

big_array = np.zeros((1642, 6, 7, 2))
target_array = np.zeros(1642)
counter = 0


def unison_shuffled_copies(a, b):
    assert len(a) == len(b)
    p = np.random.permutation(len(a))
    return a[p], b[p]


def get_new_array(array, target):
    global counter
    for j in range(21):

        if array[j][0][0] != 4:
            new = np.zeros((6, 7, 2))
            ref = np.zeros((6, 7, 2))
            for k in range(6):
                for q in range(7):
                    if array[j][k][q] == 0:
                        new[k][q][0] = 1
                        ref[k][6 - q][0] = 1
                    elif array[j][k][q] == 1:
                        new[k][q][1] = 1
                        ref[k][6 - q][1] = 1

            big_array[counter] = new.copy()
            big_array[counter + 1] = ref.copy()
            target_array[counter] = target[j][0]
            target_array[counter + 1] = target[j][0]

            counter += 2


for i in range(1, 33):
    array = np.load('../games/1x{}.npy'.format(i))
    target = np.load('../games/1y{}.npy'.format(i))
    get_new_array(array, target)

for i in range(2, 33):
    array = np.load('../games/{}x1.npy'.format(i))
    target = np.load('../games/{}y1.npy'.format(i))
    get_new_array(array, target)

data_x, data_y = unison_shuffled_copies(big_array, target_array)

len = int(len(data_x) * 0.8)


train_x = data_x[:len]  #.reshape(1313, 6, 7, 2, 1)
train_y = data_y[:len]
test_x = data_x[len:]  # .reshape(329, 6, 7, 2, 1)
test_y = data_y[len:]

print(train_x.shape)

from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, Conv3D

model = Sequential()
model.add(Conv2D(16, kernel_size=(4, 4), activation='relu', input_shape=(6, 7, 2)))
model.add(Dropout(0.2))
model.add(Conv2D(16, (3, 3), activation='relu'))
model.add(Flatten())
model.add(Dropout(0.4))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(1, activation='linear'))

model.compile(loss='mse', optimizer='adam')

model.fit(train_x, train_y,
          batch_size=64,
          epochs=2048,
          verbose=2,
          validation_split=0.2)
score = model.evaluate(test_x, test_y, verbose=0)

model.save("AnkerAI")

print('Test loss:', score)
