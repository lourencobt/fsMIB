import numpy as np
import cv2

def adjust_contrast(src_paths, dst_paths):
    imgs = []
    for i in src_paths:
        imgs.append(cv2.imread(i))

    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    clahe2 = cv2.createCLAHE(clipLimit=1.5, tileGridSize=(4,4))
    cl = []
    for i in imgs:
        i = cv2.cvtColor(i, cv2.COLOR_BGR2GRAY)
        if np.asarray(i).mean() > 127.5:
            i = cv2.bitwise_not(i)
        
        i = clahe.apply(i)
        i = clahe2.apply(i)
        cl.append(i)

    for i, img in zip(dst_paths, cl):
        cv2.imwrite(i, img)
