from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as colors
from scipy.signal import convolve2d
from scipy.ndimage.filters import gaussian_filter
from scipy.ndimage import measurements
from sklearn.linear_model.logistic import LogisticRegression
import os

def discreteImage(matrix):
    max = np.max(matrix)
    min = np.min(matrix)
    cmap = plt.get_cmap("jet", max - min + 1)
    plt.matshow(matrix, cmap=cmap, vmin = min - 0.5, vmax = max + 0.5)
    plt.colorbar(ticks=np.arange(min, max + 1))

def getInputFromPic(pic, filename):
    pixels = np.array(pic)
    digits = getFourDigits(pixels, filename)
    inputArray = []
    for d in digits:
        values = calculatePopulation(d)
        inputArray.append(values)
    return inputArray

def getFourDigits(pixels, filename):
    boundary = 170
    fourSlicesFound = False;
    while(not(fourSlicesFound) and boundary > 100):
        pixels2 = (pixels <= boundary) * 1
        labeled = measurements.label(pixels2, np.ones((3, 3)))[0]
        
        slices = measurements.find_objects(labeled)
        if (len(slices) == 4):
            fourSlicesFound = True
            slices = sortSlices(slices)
            digits = [
                normalizeDigitSize(pixels2[slices[0]]),
                normalizeDigitSize(pixels2[slices[1]]),
                normalizeDigitSize(pixels2[slices[2]]),
                normalizeDigitSize(pixels2[slices[3]])
            ]              
            return digits
        else:
            boundary = boundary-5
    print("could not process " + str(filename) + ", not 4 slices found")
    
def sortSlices(array):
    slices = list(array)
    for i in range(0,4):
        for j in range(i+1, 4):
            if(slices[i][1].start > slices[j][1].start):
                slices[j], slices[i] = slices[i], slices[j]
    return slices
            
def normalizeDigitSize(digit):
    h = len(digit)
    w = len(digit[0])
    if (h % 2 == 1):
        digit = np.append(np.zeros((1,w)), digit, axis=0)
        h = len(digit)
    rest = h-w
    if(rest<0):
        rest = w-h
    if (rest % 2 == 1):
        digit = np.append(np.zeros((h,1)), digit, axis=1)
    halfRest = int(rest / 2)
    prepend = np.zeros((h,halfRest))
    digit = np.append(prepend, digit, axis=1)
    digit = np.append(digit, prepend, axis=1)
    return digit

def calculatePopulation(digit):
    quarter = int(len(digit)/2)
    end = len(digit)
    population = []
    pop0 = 0
    pop1 = 0
    pop2 = 0
    pop3 = 0
    for x in range(0, quarter):
        for y in range(0,quarter):
            pop0 += digit[y,x]
            
    for x in range(0,quarter):
        for y in range(quarter, end):
            pop1 += digit[y,x]
            
    for x in range(quarter, end):
        for y in range(0,quarter):
            pop2 += digit[y,x]
            
    for x in range(quarter, end):
        for y in range(quarter, end):
            pop3 += digit[y,x]
    population.append(pop0/quarter)
    population.append(pop1/quarter)
    population.append(pop2/quarter)
    population.append(pop3/quarter)
    return population

def getOutputFromFileName(file):
    output = [
        int(file[0:1]),
        int(file[1:2]),
        int(file[2:3]),
        int(file[3:4])
    ]
    return output

def prepare(imageFolder):
    print("preparing images...")
    inputData = []
    outputData = []
    for file in os.listdir(imageFolder):
        if (len(file) == 8):
            inputData += getInputFromPic(Image.open(imageFolder + file).convert("L"), file)
            outputData += getOutputFromFileName(file)
    print("training model...")
    model = LogisticRegression()
    model.fit(inputData, outputData) 
    return model

def crack(model, path):
    pic = Image.open(path).convert("L")   
    digits = getInputFromPic(pic, "")
    outputString = ""
    for d in digits:
        outputString = outputString + str(model.predict([d])[0])   
    return outputString

def crackAll(model, folderPath):
    print("try to crack images...")
    filesTried = 0
    filesCracked = 0
    for file in os.listdir(folderPath):
        if (len(file) == 8):
            crackedValue = crack(model, folderPath + file)
            actualValue = file[:4]
            filesTried = filesTried + 1
            if (crackedValue == actualValue):
                filesCracked = filesCracked + 1
            for i in range(4):
                success = crackedValue[i]==actualValue[i]
                updateSuccessMatrix(int(actualValue[i]), success)
                
    globalSuccessRate = (filesCracked/filesTried)*100
    print(str(filesCracked) + " from " + str(filesTried) + " files cracked => " + "{0:.1f}".format(globalSuccessRate) + "% global succes rate");

successMatrix = [
    [0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]
]
    
def updateSuccessMatrix(digit, success):
    successMatrix[digit][success] = successMatrix[digit][success]+1

def analyzeSuccessMatrix():
    for i in range(10):
        tries = successMatrix[i][0] + successMatrix[i][1]
        if (tries > 0):
            successRate = (successMatrix[i][1] / tries) * 100
            print(str(i) + " => " + "{0:.1f}".format(successRate) + "% success rate")
        
            
        
model = prepare("c:/Users/Matze/projects/JupyterNotebooks/captchas/")

crackAll(model, "c:/Users/Matze/projects/JupyterNotebooks/captchas/")

analyzeSuccessMatrix()

#print(crack(model, "c:/Users/Matze/projects/JupyterNotebooks/captchas/5689.png"))

 
    