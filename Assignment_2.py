##################################################################
#
#    Assignment 2.py
#
#    Desc: a program to accept a wave file, calculate pitch
#           & formants, graph significant changes based on the
#           just noticeable difference for each formant, then
#           takes a single IPA sound and calculates the average
#           pitch and formants over that interval, and checks
#           if they're rising or falling
#
#    Author: Hannah Loukusa, Henry Marty, Jacob Haapoja
#
#    ©2023
#
##################################################################

import parselmouth as pm
import numpy as np
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm


def get_pitch_values(pitch: pm.Pitch, intensity: pm.Intensity,
                     intensity_filter: float = 0, nan_as_zero=True) -> tuple[list[float, ...], list[float, ...]]:
    values = [0.0 for _ in range(len(pitch.ts()))]
    for i, t in enumerate(pitch.ts()):
        if intensity.get_value(time=t) > intensity_filter:
            val = pitch.get_value_at_time(t)
            if np.isnan(val) and nan_as_zero:
                values[i] = 0.0
            else:
                values[i] = val
    return pitch.ts(), values

def get_formants(pitch: pm.Pitch, formants: pm.Formant, intensity: pm.Intensity,
                 which_formants: tuple[int, ...] = (0, 1, 2, 3, 4), intensity_filter: float = 0, nan_as_zero=True) -> \
        list[
            tuple[list[float, ...], list[float, ...]]]:
    """
    :param pitch: parselmouth Pitch
    :param formants: parselmouth Formants
    :param intensity: parselmouth Intensity
    :param which_formants: tuple that contains the formants to get
    :param intensity_filter: float that when 0 does nothing and when > 0 sets returned formant values to 0 if the
                                intensity at that time is not above the filter value
    :return: a list that contains lists of the formant values. The order of the formant lists matches the
                                order of the which_formants tuple
    """

    formant_values = []
    for f in which_formants:
        if f == 0:
            formant_values.append(get_pitch_values(pitch, intensity, intensity_filter, nan_as_zero=nan_as_zero))
        else:
            formant_values.append(get_formant_values(f, formants, intensity, intensity_filter, nan_as_zero=nan_as_zero))

    return formant_values

def get_formant_values(formant_number: int, formants: pm.Formant, intensity: pm.Intensity,
                       intensity_filter: float = 0, nan_as_zero=True) -> tuple[list[float, ...], list[float, ...]]:
    values = [0.0 for _ in range(len(formants.ts()))]
    for i, t in enumerate(formants.ts()):
        if intensity.get_value(time=t) > intensity_filter:
            val = formants.get_value_at_time(formant_number, t)
            if np.isnan(val) and nan_as_zero:
                values[i] = 0.0
            else:
                values[i] = val
    return formants.ts(), values

def get_formant_differences(formants: list[tuple[list[float, ...], list[float, ...]]]) -> list[
    tuple[list[float, ...], list[float, ...]]]:
    """
    :param formants: 2-d list in the form returned by get_formants
    :return: 2-d list in the form returned by get_formants containing the differences
            note: differences list will have one fewer element than the original list,
                  if list has values at indices i=0..len-1, then return list will contain elements L[i] - L[i+1]
    """
    diffs = []
    for f_list in formants:
        f_times = []
        f_diffs = []
        assert (len(f_list[0]) == len(f_list[1]))  # if assert fails, there is an issue with the way the lists are built
        for k in range(1, len(f_list[0])):
            f_times.append((f_list[0][k - 1] + f_list[0][k]) / 2)
            f_diffs.append(f_list[1][k] - f_list[1][k - 1])
        diffs.append((f_times, f_diffs))
    return diffs

def plot_diffs_color(formant_data: tuple[list[float, ...], list[float, ...]], diff_data, y_min=None, y_max=None):
    formant_times, formant_values = formant_data
    diff_times, diffs = diff_data
    color_matrix = np.array(diffs).reshape(1, len(diffs))
    plt.imshow(
        color_matrix,
        cmap='seismic',
        aspect='auto',
        alpha=0.3,
        norm=TwoSlopeNorm(0),  # sets center of gradient to zero (I think) https://stackoverflow.com/a/20146989
        extent=(formant_times[0],
                formant_times[-1],
                y_min or np.min(formant_values),
                y_max or np.max(formant_values)),
        interpolation='none'
    )
    # plt.colorbar(label='Difference Magnitude')
    plt.colorbar()

def first_part(filename: str):
    snd = pm.Sound(filename)
    pitch = snd.to_pitch_spinet(time_step=0.01, window_length=0.05)
    formants = snd.to_formant_burg(time_step=0.01, window_length=pitch.get_time_from_frame_number(1))
    intensity = snd.to_intensity(time_step=0.000951)

    values = get_formants(pitch, formants, intensity)
    diffs = get_formant_differences(values)

    fig = plt.figure(figsize=(20, 15))
    # outer_grid = fig.add_gridspec(2, 1)

    JNDs = [5, 60, 200, 400, 650]
    colors = ['r', '#FFA500', 'y', 'g', 'b']

    for f_n, (fList, diffList) in enumerate(zip(values, diffs)):
        f_times, f_vals = fList
        d_times, d_vals = diffList
        plt.subplot(2, 3, f_n + 1)
        plt.ylim((0, max(f_vals) * 1.25))
        plt.title(f'F{f_n}')
        plt.plot(f_times, f_vals) #, s=7, marker='o')
        plot_diffs_color(fList, diffList, 0, max(f_vals) * 1.25)
    plt.tight_layout()
    plt.show()

def second_part(filename: str, sTime: float, eTime: float):
    # set just noticeable difference thresholds
    JNDs = [5, 60, 200, 400, 650]
    # import sound and extract IPA sound part
    snd = pm.Sound(filename)
    sndPart = snd.extract_part(from_time=sTime, to_time=eTime)
    # extract relevant values from the sound part
    pitchPart = sndPart.to_pitch()
    formantsPart = sndPart.to_formant_burg()
    intensityPart = sndPart.to_intensity()
    # format values for easy processing
    valuesPart = get_formants(pitchPart, formantsPart, intensityPart)
    # initialize output string
    out = "Formant averages and trajectories:\n"
    # step through pitch & formants, calculate average and net change
    # prepare analysis output
    for i, fList in enumerate(valuesPart):
        out += f"Formant {i}: {np.nanmean([v[1] for v in fList])}\n"
        netChange = fList[-1][1] - fList[0][1]
        if netChange > JNDs[i]:
            out += f"Rising: {netChange}\n"
        elif netChange < -JNDs[i]:
            out += f"Falling: {netChange}\n"
        else:
            out += f"Flat: {netChange}\n"

    label = tk.Label(None, text=out, font=('Times', '18'), fg='blue')
    label.pack()
    label.mainloop()
    # report success
    return True

def main():
    inFile = "One Small Step.wav"
    # first_part(inFile)
    second_part(inFile, 3.711298, 3.844613)
    exit(0)

if __name__ == '__main__':
    main()
