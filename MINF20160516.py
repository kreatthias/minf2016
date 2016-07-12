
# coding: utf-8

# In[1]:

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from PIL import Image
import cv2


# In[2]:

y, x = np.ogrid[-5:5:100j, -5:5:100j]
plt.imshow(x * x + (y - y), cmap=cm.gray, vmin=-.5, vmax=2)


# In[3]:

plt.imshow(x * y, cmap=cm.gray, vmin=-1, vmax=1)


# In[4]:

finkenau = np.array(Image.open("finkenau.jpg").convert("L"))
fig = plt.figure()
fig.set_size_inches((13, 13))
plt.imshow(finkenau, cmap=cm.gray)


# In[5]:

from skimage.feature import corner_harris, corner_peaks


# In[6]:

fig = plt.figure()
fig.set_size_inches((13, 13))
plt.imshow(corner_harris(finkenau), cmap=cm.gray)


# In[7]:

fig = plt.figure()
fig.set_size_inches((13, 13))
plt.imshow(corner_harris(finkenau), cmap=cm.gray_r, vmin=-1, vmax=1)


# In[8]:

corners = corner_peaks(corner_harris(finkenau))
corners[:5]


# In[9]:

yCorners, xCorners = list(zip(*corners))

fig = plt.figure()
fig.set_size_inches((13, 13))
plt.imshow(finkenau, cmap=cm.gray)
plt.scatter(xCorners, yCorners, c='r', s=30)


# In[10]:

chess = np.array(Image.open("chess.png").convert("L"))
fig = plt.figure()
fig.set_size_inches((9, 9))
plt.imshow(chess, cmap=cm.gray)


# In[12]:

fig = plt.figure()
fig.set_size_inches((9, 9))
plt.imshow(chess, cmap=cm.gray)
yCorners, xCorners = list(zip(*corner_peaks(corner_harris(chess))))
plt.scatter(xCorners, yCorners, c='r', s=100)


# In[13]:

sift = cv2.xfeatures2d.SIFT_create()


# In[14]:

kp = sift.detect(finkenau, None)


# In[15]:

kp[:5]


# In[16]:

kp0 = kp[0]


# In[17]:

kp0.pt


# In[18]:

kp0.octave


# In[19]:

kp0.size


# In[20]:

kp0.angle


# In[21]:

fig = plt.figure()
fig.set_size_inches((13, 13))
plt.imshow(cv2.drawKeypoints(finkenau, kp, None))


# In[22]:

kp, descr = sift.compute(finkenau, kp)


# In[23]:

descr[0]


# In[24]:

descr[0].shape


# In[25]:

detail = np.array(Image.open("detail.jpg"))

fig = plt.figure()
fig.set_size_inches((12, 12))
plt.imshow(detail)


# In[26]:

kp1, descr1 = sift.detectAndCompute(detail, None)


# In[27]:

all = np.array(Image.open("all.jpg"))

fig = plt.figure()
fig.set_size_inches((12, 12))
plt.imshow(all)


# In[28]:

kp2, descr2 = sift.detectAndCompute(all, None)


# In[29]:

bf = cv2.BFMatcher()


# In[30]:

matches = bf.match(descr1, descr2)


# In[31]:

matches[:3]


# In[32]:

matches[0].distance


# In[33]:

matches = sorted(matches, key = lambda m: m.distance)


# In[34]:

len(matches)


# In[35]:

get_ipython().magic('run drawMatches.py')


# In[36]:

detailBW = np.array(Image.open("detail.jpg").convert("L"))
allBW = np.array(Image.open("all.jpg").convert("L"))
fig = plt.figure()
fig.set_size_inches((17, 17))
drawMatches(detailBW, kp1, allBW, kp2, matches[:10])


# In[ ]:



