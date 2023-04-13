import parselmouth as pm
import os.path as path
import numpy as np
from FormantCleaning import draw_spectrogram
from ExtractValues import *
from matplotlib.colors import TwoSlopeNorm

def plot_differences(times, differences, maxF, minF):
    # differences = np.diff(data)
    max_abs_diff = np.max(np.abs(differences))
    normalized_diff = differences / max_abs_diff

    num_vertical_repeats = 100
    color_matrix = np.tile(normalized_diff, (num_vertical_repeats, 1))

    # plt.figure(figsize=(len(data), 5))
    plt.imshow(color_matrix, cmap='coolwarm', aspect='auto', extent=(np.min(times), np.max(times), minF, maxF))
    plt.colorbar(label='Difference Magnitude')

    # Add the amplitude time series line plot on top of the color gradient
    # plt.plot(times, , color='black', linewidth=2, marker='o', markersize=6)

    # Adjust the x-axis labels
    plt.xticks(times)

    plt.xlabel('Interval Index')
    plt.ylabel('Amplitude')
    plt.title('Color Gradient Representation of Differences with Amplitude Time Series')
    # plt.show()

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
    # assert pitch.ts() == formants.ts()

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


def main():
    import matplotlib.pyplot as plt

    # getVals("Thats One Small.wav")

    sound: pm.Sound = pm.Sound('Thats one small.wav')
    pitch = sound.to_pitch()
    formant = sound.to_formant_burg(time_step=.05)
    intensity = sound.to_intensity()
    # spectrogram = sound.to_spectrogram()
    formants_list = get_formants(pitch, formant, intensity, intensity_filter=50)
    diffs = get_formant_differences(formants_list)
    #
    plt.figure(figsize=(12.8, 7.2))
    # print(len(diffs[0]))
    # for x in formants_list:
    # from test2 import plot_diffs_color
    plt.scatter(*formants_list[2], s=1)
    plot_diffs_color(formants_list[2], diffs[2])
    # plt.scatter(*diffs[2])
    plt.xlim([0, np.max(formants_list[2][0])])
    # plt.scatter([0], [0])
    # print((formants_list[2][0][0], formants_list[2][0][1]))
    plt.show()


if __name__ == '__main__':
    main()
    exit()
