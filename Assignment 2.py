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

def main():
    snd = pm.Sound("Thats One Small.wav")

    print("_________________________________________________")
    intensity = snd.to_intensity(time_step=0.001)
    #print(intensity)
    intensity_ts = intensity.ts()
    intensity_vals = []
    for k in intensity_ts:
        intensity_vals.append(intensity.get_value(k))

    print(f"Intensity Time Sequence: {list(k for k in intensity_ts)}")
    print(f"Intensity Values: {list(k for k in intensity_vals)}")
    print(f"intensity TS entries: {len(intensity_ts)}\t")
    print("_________________________________________________")
    formants = snd.to_formant_burg(time_step=0.001, window_length=0.032169)
    # print(formants)
    formants_ts = formants.ts()
    formant1_vals = []
    for k in formants_ts:
        formant1_vals.append(formants.get_value_at_time(1, k))
    print(f"Formant Time Sequence: {list(k for k in formants_ts)}")
    print(f"Formant 1: {list(k for k in formant1_vals)}")
    print("_________________________________________________")
    pitch = snd.to_pitch(time_step=0.001)
    # print(pitch)
    pitch_ts = pitch.ts()
    pitch_vals = []
    for k in pitch_ts:
        pitch_vals.append(pitch.get_value_at_time(k))

    print(f"Pitch Time Sequence: {list(k for k in pitch_ts)}")
    print(f"Pitch Values: {list( k for k in pitch_vals)}")
    print("_________________________________________________")
    # print("time differences b/w sequences")

    #for k in range(len(intensity_ts) - 1):
    #    print("int/form: " + str(round(intensity_ts[k] - formants_ts[k], 4)) +
    #    "\tint/pitch: " + str(round(intensity_ts[k] - pitch_ts[k], 4)) +
    #    "\tForm/pitch: " + str(round(formants_ts[k] - pitch_ts[k], 4)))


if __name__ == '__main__':
    main()
