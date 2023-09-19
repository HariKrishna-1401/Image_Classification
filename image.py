import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras import datasets,layers,models

(training_images,training_labels),(testing_images,testing_labels)= datasets.cifar10.load_data()

training_images,testing_images = training_images/255,testing_images/255

class_names = ['plane','car','bird','cat','deer','dog','frog','horse','ship','truck']

for i in range(16):
    plt.subplot(4,4,i+1)
    plt.xticks([])
    plt.yticks([])
    plt.imshow(training_images[i],cmap=plt.cm.binary)
    plt.xlabel(class_names[training_labels[i][0]])
plt.show()

training_images = training_images[:20000]
training_labels = training_labels[:20000]
testing_images = testing_images[:4000]
testing_labels = testing_labels[:4000]

#model = models.Sequential()
##convolution layer filters features in a image
##32,32,3  resolution and colors ie 3
#model.add(layers.Conv2D(32,(3,3), activation='relu',input_shape=(32,32,3)))
##maxpooling layer simplfies and reduces to essential information
#model.add(layers.MaxPooling2D((2,2)))
#model.add(layers.Conv2D(64,(3,3),activation='relu'))
#model.add(layers.MaxPooling2D((2,2)))
#model.add(layers.Conv2D(64,(3,3),activation='relu'))
#model.add(layers.Flatten())
#model.add(layers.Dense(64,activation='relu'))
#model.add(layers.Dense(10,activation='softmax'))
##softmax - scales to addup to 1

#model.compile(optimizer = 'adam',loss='sparse_categorical_crossentropy',metrics=['accuracy'])
#model.fit(training_images,training_labels,epochs=10,validation_data=(testing_images,testing_labels))

#model.save('image_classifer.model')
model = models.load_model('image_classifer.model')


img = cv.imread('deer.jpg')
img = cv.cvtColor(img,cv.COLOR_BGR2RGB)

plt.imshow(img,cmap=plt.cm.binary)

prediction = model.predict(np.array([img])/255)
index = np.argmax(prediction)

print(f'class name={class_names[index]}')
plt.show()

