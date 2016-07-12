from PIL import Image
import numpy as np

def isShadeOfGrey(value):
    return (value[0] == value[1] == value[2])

adjacentPixels = [
        [-1,-1],
        [-1, 0],
        [-1, 1],
        [ 0,-1],
        [ 0, 1],
        [ 1,-1],
        [ 1, 0],
        [ 1, 1]
    ]

def cleanPixelFromAdjacent(pixels, x, y, w, h): 
    if (isShadeOfGrey(pixels[y,x])):
        return
    
    adjacentGreyColorValues = []
    for xDiff, yDiff in adjacentPixels:
        adjacentX = x+xDiff
        adjacentY = y+yDiff    
        if (adjacentPixelIsInBounds(adjacentX, adjacentY, w, h)):
            adjacentValue = pixels[adjacentY][adjacentX]
            if (isShadeOfGrey(adjacentValue)):
                adjacentGreyColorValues.append(adjacentValue)
    
    if (len(adjacentGreyColorValues) == 0):
        return
    
    newPixelValue = 0
    for c in adjacentGreyColorValues:
        newPixelValue += c[0]
    newPixelValue = newPixelValue / len(adjacentGreyColorValues)
    
    pixelColor = pixels[y,x]
    pixelColor[0] = newPixelValue
    pixelColor[1] = newPixelValue
    pixelColor[2] = newPixelValue
    
def adjacentPixelIsInBounds(x,y,w,h):
    return (x >= 0 and x < w) and (y >= 0 and y < h)

def clean(pathFrom, pathTo):
    pic = Image.open(pathFrom)
    w, h = pic.size
    pixels = np.array(pic)
    for x in range(w):
        for y in range(h):
            cleanPixelFromAdjacent(pixels, x, y, w, h)
    picClean = Image.fromarray(pixels)
    picClean.save(pathTo)
    
clean('c:/Users/Matze/projects/JupyterNotebooks/dirty/horse_dirty.png', "c:/Users/Matze/projects/JupyterNotebooks/dirty/horse_clean.png")