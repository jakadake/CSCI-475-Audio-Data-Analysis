import parselmouth as pm
import numpy as np


def get_pitch_values(pitch: pm.Pitch, intensity: pm.Intensity, intensity_filter: float = 0):
    if intensity_filter == 0:
        return [pitch.get_value_at_time(t) for t in pitch.ts()]
    values = []
    for t in pitch.ts():
        if intensity.get_value(time=t) > intensity_filter:
            values.append(pitch.get_value_at_time(t))
        else:
            values.append(0.0)
    return values


def get_formant_values(formant_number: int, formants: pm.Formant, intensity: pm.Intensity, intensity_filter: float = 0):
    if intensity_filter == 0:
        return [formants.get_value_at_time(formant_number, t) for t in formants.ts()]
    values = []
    for t in formants.ts():
        if intensity.get_value(time=t) > intensity_filter:
            values.append(formants.get_value_at_time(formant_number, t))
        else:
            values.append(0.0)
    return values


def get_formants(pitch: pm.Pitch, formants: pm.Formant, intensity: pm.Intensity,
                 which_formants: tuple[int, ...] = (0, 1, 2, 3, 4), intensity_filter: float = 0) -> list[list[float]]:
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


def get_formant_differences(formants: list[list[float, ...]]):
    """
    :param formants: 2-d list in the form returned by get_formants
    :return: 2-d list in the form returned by get_formants containing the differences
            note: differences list will have one fewer element than the original list,
                  if list has values at indices i=0..len-1, then return list will contain elements L[i] - L[i+1]
    """
    return [np.diff(f_list) for f_list in formants]


def main():
    import matplotlib.pyplot as plt
    sound: pm.Sound = pm.Sound('from jake/test_speech.wav')
    pitch = sound.to_pitch()
    formant = sound.to_formant_burg()
    intensity = sound.to_intensity()
    diffs = get_formant_differences(get_formants(pitch, formant, intensity, intensity_filter=50))
    for x in diffs:
        print(np.nansum(x))

    plt.figure()
    for x in diffs:
        plt.plot(x)
    plt.show()


if __name__ == '__main__':
    main()
    exit()
