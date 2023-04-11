###################################################################
##
##    Assignment 2.py
##
##    Desc:
##
##    Author: Jacob Haapoja
##
##    ©2023
##
###################################################################

import parselmouth as pm
import numpy as np
import scipy.io as scipy
from FormantCleaning import *
from MovingAverages import *
from ExtractValues import *
from formant_analysis import *

def main():
    inFile = "One Small Step.wav"
    snd = pm.Sound(inFile)

    startTime = 3.711298
    endTime

    sndPart = snd.extract_part(from_time=3.711298, to_time=3.844613)
    pitch = snd.to_pitch_spinet(time_step=0.005, window_length=0.01)
    formants = snd.to_formant_burg(time_step=0.001, window_length=pitch.get_time_from_frame_number(1))
    intensity = snd.to_intensity(time_step=0.000951)

    vals = getVals(inFile)
    values = get_formants(pitch, formants, intensity)

    diffs = get_formant_differences(values)

    plt.figure(figsize=(12.8, 7.2))

    JNDs = [5, 60, 200, 400, 650]
    colors = ['r', '#FFA500', 'y', 'g', 'b']

    for i, fList in reversed(list(enumerate(diffs))):
        plt.subplot(2,3, i+1)
        for fTime, fDiff in fList:
            if abs(fDiff) > JNDs[i]:
                plt.scatter(fTime, fDiff, color=colors[i])
    plt.grid(visible=True)
    # plt.show()

    # plt.scatter(vals[0][0], vals[2][0], label='Pitch', color='r', linewidths=1)
    # # F1 plotted in orange
    # plt.scatter(vals[0][1], vals[2][1], label='F1', color='#FFA500', linewidths=1)
    # # F2 plotted in yellow
    # plt.scatter(vals[0][1], vals[2][2], label='F2', color='y', linewidths=1)
    # # F3 plotted in green
    # plt.scatter(vals[0][1], vals[2][3], label='F3', color='g', linewidths=1)
    # # F4 plotted in blue
    # plt.scatter(vals[0][1], vals[2][4], label='F4', color='b', linewidths=1)

    plt.show()
    # plt.figure(figsize=(12.8, 7.2))







    # snd = pm.Sound("Thats One Small.wav")
    #
    # print("_________________________________________________")
    # intensity = snd.to_intensity(time_step=0.001)
    # #print(intensity)
    # intensity_ts = intensity.ts()
    # intensity_vals = []
    # for k in intensity_ts:
    #     intensity_vals.append(intensity.get_value(k))
    #
    # print(f"Intensity Time Sequence: {list(k for k in intensity_ts)}")
    # print(f"Intensity Values: {list(k for k in intensity_vals)}")
    # print(f"intensity TS entries: {len(intensity_ts)}\t")
    # print("_________________________________________________")
    # formants = snd.to_formant_burg(time_step=0.001, window_length=0.032169)
    # # print(formants)
    # formants_ts = formants.ts()
    # formant1_vals = []
    # for k in formants_ts:
    #     formant1_vals.append(formants.get_value_at_time(1, k))
    # print(f"Formant Time Sequence: {list(k for k in formants_ts)}")
    # print(f"Formant 1: {list(k for k in formant1_vals)}")
    # print("_________________________________________________")
    # pitch = snd.to_pitch(time_step=0.001)
    # # print(pitch)
    # pitch_ts = pitch.ts()
    # pitch_vals = []
    # for k in pitch_ts:
    #     pitch_vals.append(pitch.get_value_at_time(k))
    #
    # print(f"Pitch Time Sequence: {list(k for k in pitch_ts)}")
    # print(f"Pitch Values: {list( k for k in pitch_vals)}")
    # print("_________________________________________________")
    # # print("time differences b/w sequences")
    #
    # #for k in range(len(intensity_ts) - 1):
    # #    print("int/form: " + str(round(intensity_ts[k] - formants_ts[k], 4)) +
    # #    "\tint/pitch: " + str(round(intensity_ts[k] - pitch_ts[k], 4)) +
    # #    "\tForm/pitch: " + str(round(formants_ts[k] - pitch_ts[k], 4)))


if __name__ == '__main__':
    main()
