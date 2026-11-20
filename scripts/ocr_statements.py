import cv2, sys, glob, subprocess, os
import numpy as np
for pdf in sorted(glob.glob('/mnt/user-data/uploads/*-20[12][0-9].pdf')):
    y=os.path.basename(pdf).split('-')[-1][:4]
    subprocess.run(['pdftoppm','-r','300','-png',pdf,f'c{y}'],check=True)
for p in sorted(glob.glob('c20*.png')):
    im=cv2.imread(p,0)
    bw=cv2.threshold(im,200,255,cv2.THRESH_BINARY_INV)[1]
    h=cv2.morphologyEx(bw,cv2.MORPH_OPEN,cv2.getStructuringElement(cv2.MORPH_RECT,(80,1)))
    v=cv2.morphologyEx(bw,cv2.MORPH_OPEN,cv2.getStructuringElement(cv2.MORPH_RECT,(1,40)))
    lines=cv2.dilate(cv2.bitwise_or(h,v),np.ones((3,3),np.uint8))
    clean=cv2.bitwise_not(cv2.bitwise_and(bw,cv2.bitwise_not(lines)))
    cv2.imwrite('x'+p,clean)
    subprocess.run(['tesseract','x'+p,'x'+p[:-4],'--psm','6','-c','preserve_interword_spaces=1'],capture_output=True)
