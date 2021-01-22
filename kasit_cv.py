import os
import cv2

txt_path = "./V005"
rgb_path = "./visible"
lwir_path = "./lwir"

txts = os.listdir(txt_path)
for txt in txts:
    f = open(txt_path+'/'+txt,'r')
    lines = f.readlines()[1:]
    if len(lines) == 0:
        continue
    img = cv2.imread(rgb_path + '/' + txt.replace('txt', 'jpg'))
    timg = cv2.imread(lwir_path + '/' + txt.replace('txt', 'jpg'))
    for line in lines:
        line = line.strip().split(' ')
        names, x, y, w, h = line[0], int(line[1]), int(line[2]), int(line[3]), int(line[4])
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 1)
        cv2.putText(img, names, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0, 0), 1)
        cv2.rectangle(timg, (x, y), (x + w, y + h), (255, 0, 0), 1)
        cv2.putText(timg, names, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 1)
    cv2.imshow('img', img)
    cv2.imshow('timg',timg)
    k = cv2.waitKey(0)
    if k == ord('n'):  
        continue
cv2.destroyAllWindows()



