import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

def drawMatches (img1, kp1, img2, kp2, matches):
    colors = ['r', 'g', 'b', 'c', 'm', 'y']

    rows1 = img1.shape[0]
    cols1 = img1.shape[1]
    rows2 = img2.shape[0]
    cols2 = img2.shape[1]

    out = np.zeros((max([rows1, rows2]), cols1 + cols2), dtype='uint8')
    out[:rows1, :cols1] = img1
    out[:rows2, cols1:cols1 + cols2] = img2
    plt.imshow(out, cmap=cm.gray)
    plt.xlim(0, out.shape[1])
    plt.ylim(out.shape[0], 0)

    color = 0
    for mat in matches:
        img1_idx = mat.queryIdx
        img2_idx = mat.trainIdx

        (x1,y1) = kp1[img1_idx].pt
        (x2,y2) = kp2[img2_idx].pt
        
        plt.plot([x1, x2+cols1], [y1, y2], colors[color], linewidth=2)
        color = (color + 1) % len(colors)
        
    
