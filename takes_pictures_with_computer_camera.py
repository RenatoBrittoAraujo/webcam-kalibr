import cv2
import os

cap = cv2.VideoCapture(0)
num = 0
pwd = os.getcwd()

while cap.isOpened():
    succes, img = cap.read()

    k = cv2.waitKey(5)

    if k == 27:  # 'esc' to exit
        break
    elif k == ord("s"):  # 's' to save
        path = f"{pwd}/data_inside_container/images"
        file = f"{path}/img{str(num)}.png"
        cv2.imwrite(file, img)
        print(
            "image saved! to ",
            file,
        )
        num += 1

    cv2.imshow("Img", img)

cap.release()
cv2.destroyAllWindows()
