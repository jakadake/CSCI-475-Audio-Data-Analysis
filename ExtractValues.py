
import parselmouth as pm
import matplotlib.pyplot as plt
import numpy as np
import os.path as path
from FormantCleaning import *
from MovingAverages import *

##  plotWaveform
##  pre:
##          inFile is a valid .wav file
##          outFile is the name of the file to save to
##  Post:
##          an image of the waveform plot is saved to [outFile].png
##          returns - a waveform plot figure
##
def plotWaveform(inFile, outFile="default"):
    if path.isfile(inFile) and inFile.endswith(".wav"):
        wf = plt.figure(figsize=(12.8, 7.2))
        snd = pm.Sound(inFile)
        plt.plot()
        plt.plot(snd.xs(), snd.values.T)
        plt.xlim([snd.xmin, snd.xmax])
        plt.xlabel("time [s]")
        plt.ylabel("amplitude")
        plt.savefig(outFile + "waveform.png")
        return wf

##  plotSpectrogram
##  pre:
##          inFile is a valid .wav file
##          outFile is the name of the file to save to
##  Post:
##          an image of the spectrogram plot is saved to [outFile].png
##          returns - a spectrogram plot figure
##
def plotSpectrogram(inFile, outFile="default", dynamic_range = 70):
    if path.isfile(inFile) and inFile.endswith(".wav"):
        fig = plt.figure(figsize=(12.8, 7.2))  # set figure to 1280x720
        snd = pm.Sound(inFile)
        sg = snd.to_spectrogram(window_length=0.032169, time_step=0.001)
        X, Y = sg.x_grid(), sg.y_grid()
        sg_db = 10 * np.log10(sg.values)
        plt.pcolormesh(X, Y, sg_db, vmin=sg_db.max() - dynamic_range, cmap='binary')
        plt.ylim([sg.ymin, sg.ymax])
        plt.xlabel("time [s]")
        plt.ylabel("frequency [Hz]")
        plt.savefig(outFile + "spectrogram.png")
        return fig

##  plotValues
##  pre:
##          inFile is a valid .wav file
##          outFile is the name of the file to save to
##  Post:
##          an image of the formants plot is saved to "[outFile]_formants.png"
##          returns - a spectrogram plot figure
##
def plotValues(inFile, outFile):
    if path.isfile(inFile) and inFile.endswith(".wav"):
        fig = plt.figure(figsize=(12.8, 7.2))  # set figure to 1280x720
        # Load the sound file
        snd = pm.Sound(inFile)
        # get spectrogram
        spec = snd.to_spectrogram(window_length=0.032169, time_step=0.001)
        # get intensity
        intensity = snd.to_intensity(time_step=0.001)
        # Get the formants
        formants = snd.to_formant_burg(time_step=0.001, window_length=0.032169)
        # Get the pitch
        pitch = snd.to_pitch(time_step=0.001019)
        # Extract the formant/pitch/intensity values and times
        values = clean_formants(pitch, formants, intensity)
        # draw values
        fig = draw_values(values, spec)
        fig.savefig(outFile + "formants.png")
        return fig
    else:
        return False


