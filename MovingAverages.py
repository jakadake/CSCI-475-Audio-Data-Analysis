##      MovingAverages.py
##
##      Description: a program to take in .wav files and produce a waveform
##          and spectrogram plot as output images
##
##      Author: Jacob Haapoja
##
##      ©2023
##

import numpy as np
import math

##  plotValues
##  pre:
##          inFile is a valid .wav file
##          outFile is the name of the file to save to
##  Post:
##          an image of the formants plot is saved to "[outFile]_formants.png"
##          returns - a spectrogram plot figure
##
def trailingAvg(movingList, frameSize = 3):
    avgList = []
    for k in range(len(movingList)):
        averageSum = 0
        divisor = 0
        for n in range(frameSize):
            if k-n >= 0:
                divisor += 1
                averageSum += movingList[k-n]
        avgList.append(averageSum/divisor)
        #print(avgList)

    return avgList

##  middleAvg
##  pre:
##
##
##  Post:
##          an image of the formants plot is saved to "[outFile]_formants.png"
##          returns - a spectrogram plot figure
##
def middleAvg(movingList, frameSize = 3):
    if (frameSize % 2 == 0):
        frameSize += 1

    #for k in range(floor(frameSize/2)):
    #    avgList.append(movingList[k])
    avgList = []
    for k in range(len(movingList)):
        averageSum = 0
        divisor = 0
        for n in range(-math.floor(frameSize/2), math.floor(frameSize/2)):
            if k - n >= 0 and k-n<= len(movingList) -1:
                divisor += 1
                averageSum += movingList[k - n]
        avgList.append(averageSum / divisor)
        # print(avgList)
    return avgList


def main():
    movingList = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    frameSize = 3
    newAverage = middleAvg(movingList, frameSize)
    print(newAverage)


if __name__ == "__main__":
    main()