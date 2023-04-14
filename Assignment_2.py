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
    """
        Extracts the values pitch from the pitch object. Optionally filters out formant that occur when
        intensity is below a certain value.
        :param pitch: a parselmouth.Pitch object
        :param intensity: a parselmouth.Intensity object
        :param intensity_filter: sets the value at or below which pitch will be filtered out. Does nothing if set to zero
        :param nan_as_zero: converts nan values to 0.0 if True, leaves them if False
        :return: a tuple containing the list of time steps and the list of pitch values
        """
    values = []
    for t in pitch.ts():
        if intensity_filter == 0 or intensity.get_value(time=t) >= intensity_filter:
            val = pitch.get_value_at_time(t)
            if np.isnan(val) and nan_as_zero:
                values.append(0.0)
            else:
                values.append(val)
        else:
            values.append(0.0)
    return pitch.ts(), values


def get_formant_values(formant_number: int, formants: pm.Formant, intensity: pm.Intensity,
                       intensity_filter: float = 0, nan_as_zero=True) -> tuple[list[float, ...], list[float, ...]]:
    """
    Extracts the formant values for a particular formant from the formants object. Optionally filters out formants
    that occur when intensity is below a certain value.
    :param formant_number: The formant to extract
    :param formants: a parselmouth.Formants object
    :param intensity: a parselmouth.Intensity object
    :param intensity_filter: sets the value at or below which formants will be filtered out. Does nothing if set to zero
    :param nan_as_zero: converts nan values to 0.0 if True, leaves them if False
    :return: a tuple containing the list of time steps and the list of formant values
    """
    values = []
    for t in formants.ts():
        if intensity_filter == 0 or intensity.get_value(time=t) >= intensity_filter:
            val = formants.get_value_at_time(formant_number, t)
            if np.isnan(val) and nan_as_zero:
                values.append(0.0)
            else:
                values.append(val)
        else:
            values.append(0.0)
    return formants.ts(), values


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
    :param nan_as_zero: converts nan values to 0.0 if True, leaves them if False
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


def get_formant_differences(formants: list[tuple[list[float, ...], list[float, ...]]]) -> list[
    tuple[list[float, ...], list[float, ...]]]:
    """
    :param formants: 2-d list in the form returned by get_formants
    :return: 2-d list in the form returned by get_formants containing the differences
            note: differences list will have one fewer element than the original list,
                  if list has values at indices i=0..len-1, then return list will contain elements L[i+1] - L[i]
    """
    diffs = []
    for f_list in formants:
        f_times = []
        f_diffs = []
        assert (len(f_list[0]) == len(f_list[1]))  # if assert fails, there is an issue with the way the lists are built
        for k in range(1, len(f_list[0])):
            f_times.append((f_list[0][k - 1] + f_list[0][k]) / 2)
            if f_list[1][k - 1] == 0 or f_list[1][k] == 0:
                f_diffs.append(0)
            else:
                f_diffs.append(f_list[1][k] - f_list[1][k - 1])
        diffs.append((f_times, f_diffs))
    return diffs


def plot_diffs_color(formant_data: tuple[list[float, ...], list[float, ...]],
                     diff_data: tuple[list[float, ...], list[float, ...]], y_min: float = None,
                     y_max: float = None):
    """
    Colors the background of the plot based off of the differences from formant value to formant value
    using a diverging color gradient with 0 at the center
    :param formant_data: formant data for a particular formant
    :param diff_data: differences obtained from get_formant_differences
    :param y_min: lowest value to color
    :param y_max: highest value to color
    :return: nothing
    """
    formant_times, formant_values = formant_data
    diff_times, diffs = diff_data
    color_matrix = np.array(diffs).reshape(1, len(diffs))
    plt.imshow(
        color_matrix,
        cmap='seismic',
        aspect='auto',
        alpha=0.4,
        norm=TwoSlopeNorm(0),  # https://stackoverflow.com/a/20146989
        extent=(
            formant_times[0],
            formant_times[-1],
            y_min or np.nanmin(formant_values),
            y_max or np.nanmax(formant_values)
        ),
        interpolation='none'
    )
    plt.colorbar()


def first_part(filename: str):
    snd = pm.Sound(filename)
    pitch = snd.to_pitch_ac(pitch_ceiling=300)
    formants = snd.to_formant_burg()
    intensity = snd.to_intensity()

    values = get_formants(pitch, formants, intensity, nan_as_zero=True)
    diffs = get_formant_differences(values)

    plt.figure(figsize=(32, 18))

    for f_n, (fList, diffList) in enumerate(zip(values, diffs)):
        f_times, f_vals = fList
        plt.subplot(2, 3, f_n + 1)
        plt.ylim((0, np.nanmax(f_vals) * 1.20))  # set y lims to 20% higher than max data value to give space at top
        plt.title(f'F{f_n}')
        plt.xlabel('Time (s)')
        plt.ylabel('Frequency (Hz)')
        plt.plot(f_times, f_vals)
        plot_diffs_color(
            fList,
            diffList,
            -1,  # set y_min to -1 because zero doesn't work for some reason I guess
            np.nanmax(f_vals) * 1.20  # set y_max to 20% higher for same reason as above
        )
    plt.tight_layout()
    plt.show()


def first_part_separate(filename: str):
    snd = pm.Sound(filename)
    pitch = snd.to_pitch_ac(time_step=.01, pitch_ceiling=300)
    formants = snd.to_formant_burg(time_step=.01)
    intensity = snd.to_intensity(time_step=.01)

    values = get_formants(pitch, formants, intensity, nan_as_zero=True)
    diffs = get_formant_differences(values)

    for f_n, (fList, diffList) in enumerate(zip(values, diffs)):
        plt.figure(figsize=(11, 9))
        f_times, f_vals = fList
        plt.ylim((0, np.nanmax(f_vals) * 1.20))  # set y lims to 20% higher than max data value to give space at top
        plt.title(f'F{f_n}')
        plt.xlabel('Time (s)')
        plt.ylabel('Frequency (Hz)')
        plt.plot(f_times, f_vals)
        plot_diffs_color(
            fList,
            diffList,
            y_min=-1,  # set y_min to -1 because zero doesn't work for some reason I guess
            y_max=np.nanmax(f_vals) * 1.20  # set y_max to 20% higher for same reason as above
        )
        plt.savefig(f'formant_{f_n}_plot.png')


def second_part(filename: str, from_time: float, to_time: float):
    # set just noticeable difference thresholds
    JNDs = [5, 60, 200, 400, 650]
    # import sound and extract IPA sound part
    snd = pm.Sound(filename)
    ipaSnd = snd.extract_part(from_time=from_time, to_time=to_time)

    # extract relevant values from the sound part
    ipaPitch = ipaSnd.to_pitch_ac(time_step=.001, pitch_ceiling=300)
    ipaFormants = ipaSnd.to_formant_burg(time_step=.001)
    ipaIntensity = ipaSnd.to_intensity(time_step=.001)

    # format values for easy processing
    ipaValues = get_formants(ipaPitch, ipaFormants, ipaIntensity)

    # initialize output string
    out = "Formant averages and trajectories:\n\n"
    out += f"On Interval:\n \tFrom: {from_time} s \n\tTo: {to_time} s:\n\n"
    # step through pitch & formants, calculate average and net change
    # all values are truncated to
    # prepare analysis output
    for i, (f_times, f_vals) in enumerate(ipaValues):
        out += f"Formant {i}:\n"

        out += f"\tAverage: {np.trunc(np.nanmean(f_vals))} Hz\n"
        netChange = f_vals[-1] - f_vals[0]
        # treat netChange greater or less than Just Noticeable Difference as rising or falling, resp.
        # if within JND, consider it flat
        if netChange > JNDs[i]:
            out += f"\tRising\n\tΔ = {np.trunc(netChange)} Hz\n\n"
        elif netChange < -JNDs[i]:
            out += f"\tFalling\n\tΔ = {np.trunc(netChange)} Hz\n\n"
        else:
            out += f"\tFlat\n\tΔ = {np.trunc(netChange)} Hz\n\n"

    with open('ipa sound report.txt', 'w', encoding='utf8') as f:
        f.write(out)
    # report success
    label = tk.Label(None, text=out, font=('Times', '18'), fg='blue', justify='left')
    label.pack()
    label.mainloop()
    return True


def main():
    inFile = "One Small Step.wav"
    # inFile = "D:\\My Drive\\2023\\Computational Linguistics\\moonspeech2 Henry Marty.wav"
    # inFile = "Thats.wav"
    startTime = 3.711298
    # startTime = 3.7
    endTime = 3.844613
    first_part_separate(inFile)
    second_part(inFile, startTime, endTime)
    exit()


if __name__ == '__main__':
    main()
