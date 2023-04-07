import parselmouth as pm
import os.path as path
import numpy as np
from FormantCleaning import draw_spectrogram


def get_pitch_values(pitch: pm.Pitch, intensity: pm.Intensity,
                     intensity_filter: float = 0) -> list[tuple[float, float]]:
    if intensity_filter == 0:
        return [(t, pitch.get_value_at_time(t)) for t in pitch.ts()]
    values = []
    for t in pitch.ts():
        if intensity.get_value(time=t) > intensity_filter:
            values.append((t, pitch.get_value_at_time(t)))
        else:
            values.append((t, 0.0))
    return values


def get_formant_values(formant_number: int, formants: pm.Formant, intensity: pm.Intensity,
                       intensity_filter: float = 0) -> list[tuple[float, float]]:
    if intensity_filter == 0:
        return [(t, formants.get_value_at_time(formant_number, t)) for t in formants.ts()]
    values = []
    for t in formants.ts():
        if intensity.get_value(time=t) > intensity_filter:
            values.append((t, formants.get_value_at_time(formant_number, t)))
        else:
            values.append((t, 0.0))
    return values

def get_formants(pitch: pm.Pitch, formants: pm.Formant, intensity: pm.Intensity,
                 which_formants: tuple[int, ...] = (0, 1, 2, 3, 4), intensity_filter: float = 0) -> list[
    list[tuple[float, float]]]:
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
            formant_values.append(get_pitch_values(pitch, intensity, intensity_filter))
        else:
            formant_values.append(get_formant_values(f, formants, intensity, intensity_filter))

    return formant_values


def get_formant_differences(formants: list[list[tuple[float, float], ...]]) -> list[list[tuple[float, float]]]:
    """
    :param formants: 2-d list in the form returned by get_formants
    :return: 2-d list in the form returned by get_formants containing the differences
            note: differences list will have one fewer element than the original list,
                  if list has values at indices i=0..len-1, then return list will contain elements L[i] - L[i+1]
    """
    # formant value is second in the two-tuple
    diffs = []
    for f_list in formants:
        f_list_diff = []
        for k in range(1, len(f_list)):
            f_list_diff.append(
                (f_list[k - 1][0] + f_list[k][0] / 2,  # average of time of formant values
                 f_list[k - 1][1] - f_list[k][1])  # difference between two formant values
            )

            # return [np.diff(f_list[0]) for f_list in formants]
        diffs.append(f_list_diff)
    return diffs


def main():
    import matplotlib.pyplot as plt

    getVals("Thats One Small.wav")

    # sound: pm.Sound = pm.Sound('Thats One Small.wav')
    # pitch = sound.to_pitch()
    # formant = sound.to_formant_burg()
    # intensity = sound.to_intensity()
    # spectrogram = sound.to_spectrogram()
    # formants_list = get_formants(pitch, formant, intensity, intensity_filter=50)
    # diffs = get_formant_differences(formants_list)
    #
    # # for x in diffs:
    # #     print(np.nansum(x))
    # #
    # # draw_spectrogram(spectrogram)
    #
    # plt.figure(figsize=(12.8, 7.2))
    # print(len(diffs[0]))
    # for x in diffs:
    #     plt.plot(*zip(*x))
    # plt.show()


if __name__ == '__main__':
    main()
    exit()
