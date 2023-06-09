import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import cv2
import matplotlib.pyplot as plt
import seaborn as sns
import keyboard
from PIL import Image
import PIL.ImageOps

X = np.load("image.npz")["arr_0"]
Y = pd.read_csv("labels.csv")["labels"]
classes = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
number_of_classes = len(classes)

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, random_state = 0, train_size = 2500, test_size = 7500)

X_train_scaled = X_train/255.0
X_test_scaled = X_test/255.0

classifier = LogisticRegression(solver = "saga", multi_class = "multinomial")
classifier.fit(X_train_scaled, Y_train)

Y_pred = classifier.predict(X_test_scaled)
accuracy = accuracy_score(Y_test, Y_pred)
print("Accuracy: ", (accuracy * 100))

capture = cv2.VideoCapture(0)
while(True):
    # try:
        ret, frame = capture.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        height, width = gray.shape
        upper_left = (int(width/2 - 56), int(height/2 - 56))
        bottom_right = (int(width/2 + 56), int(height/2 + 56))
        cv2.rectangle(gray, upper_left, bottom_right, (255, 0, 0), 2)
            
        roi = gray[upper_left[1]:bottom_right[1], upper_left[0]:bottom_right[0]]
        im_pil = Image.fromarray(roi)

        image_bw = im_pil.convert("L")
        image_bw_resized = image_bw.resize((28, 28), Image.LANCZOS)

        image_bw_resized_inverted = PIL.ImageOps.invert(image_bw_resized)
        pixel_filter = 20

        min_pixel = np.percentile(image_bw_resized_inverted, pixel_filter)
        image_bw_resized_inverted_scaled = np.clip(image_bw_resized_inverted-min_pixel, 0, 255)
        max_pixel = np.max(image_bw_resized_inverted)

        image_bw_resized_inverted_scaled = np.asarray(image_bw_resized_inverted_scaled)/max_pixel

        test_sample = np.array(image_bw_resized_inverted_scaled).reshape(1, 784)
        test_pred = classifier.predict(test_sample)
        print("Predicted class is :", test_pred)

        cv2.imshow("Alphabet Recognition", gray)
        if cv2.waitKey(1) & keyboard.is_pressed("q") | keyboard.is_pressed("esc"):
            break
    # except Exception as e:
        # pass

capture.release()
cv2.destroyAllWindows()