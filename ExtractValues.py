
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
        fig.savefig(outFile + "_formants.png")
        return fig
    else:
        return False

def getVals(inFile: str):
    #check if valid wave file
    if path.isfile(inFile) and inFile.endswith(".wav"):
        #import sound object
        snd = pm.Sound(inFile)

        #extract data objects
        pitch = snd.to_pitch(time_step=0.001)
        formants = snd.to_formant_burg(time_step=0.001)
        intensity = snd.to_intensity(time_step=0.001)

        #get time sequences and make times superlist
        pitch_ts = pitch.ts()
        formants_ts = formants.ts()
        intensity_ts = intensity.ts()
        times = [pitch_ts, formants_ts, intensity_ts]

        #get raw pitch and formant data
        f0 = []
        f1 = []
        f2 = []
        f3 = []
        f4 = []
        int = []
        vals = [f0, f1, f2, f3, f4, int]
        for i in times[0]:
            temp = pitch.get_value_at_time(i)
            if (math.isnan(temp) == True):
                vals[0].append(0)
            else:
                vals[0].append(temp)
        for i in range(1, 5):
            for j in times[1]:
                temp = formants.get_value_at_time(i, j)
                if (math.isnan(temp) == True):
                    vals[i].append(0)
                else:
                    vals[i].append(temp)
        for i in times[2]:
            temp = intensity.get_value(i)
            if (math.isnan(temp) == True):
                vals[5].append(0)
            else:
                vals[5].append(temp)

        #calculate differences
        f0_diffs = [0]
        f1_diffs = [0]
        f2_diffs = [0]
        f3_diffs = [0]
        f4_diffs = [0]
        int_diffs = [0]
        diffs = [f0_diffs, f1_diffs, f2_diffs, f3_diffs, f4_diffs, int_diffs]
        for i in range(len(vals[0])-1):
            temp = vals[0][i] - vals[0][i + 1]
            if (math.isnan(temp) == True):
                diffs[0].append(0)
            else:
                diffs[0].append(temp)
        for i in range(1, 5):
            for j in range(len(vals[i])-1):
                temp = vals[i][j] - vals[i][j + 1]
                if (math.isnan(temp) == True):
                    diffs[i].append(0)
                else:
                    diffs[i].append(temp)
        for i in range(len(vals[5])-1):
            temp = vals[5][i] - vals[5][i+1]
            if (math.isnan(temp) == True):
                diffs[5].append(0)
            else:
                diffs[5].append(temp)

        # 3-D array of format values[time_sequence[pitch=0/formants=1[index]]][raw data[data 0-5[index]]][differences[data  0-5[index]]]
        values = [times, vals, diffs]
        return values


def main():
    inFile = "Thats One Small.wav"
    outFile = inFile.replace(".wav", "")

    values = getVals(inFile)

    plt.figure(figsize=(12.8, 7.2))
    plt.subplot(1, 2, 1)
    plt.plot(values[0][0], values[1][0], label="Pitch")
    for i in range(1, 4):
        plt.plot(values[0][1], values[1][i], label=f"formant {i}")
    plt.xlabel("Time [s]")
    plt.ylabel("Frequency [Hz]")
    plt.twinx()
    plt.ylabel("Amplitude [dB]")
    plt.plot(values[0][2], values[1][5], label="intensity")
    plt.title("Raw Data")

    plt.subplot(1, 2, 2)
    plt.plot(values[0][0], values[2][0], label="pitch")
    for i in range(1, 4):
        plt.plot(values[0][1], values[2][i], label=f"formant {i}")
    plt.xlabel("Time [s]")
    plt.ylabel("Difference [Hz]")
    plt.twinx()
    plt.ylabel("Amplitude Difference [dB]")
    plt.plot(values[0][2], values[2][5], label="intensity")

    plt.show()

if __name__ == '__main__':
    main()

