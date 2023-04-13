from ExtractValues import *
from formant_analysis import *
from MovingAverages import *
from FormantCleaning import *
from Assignment_2 import *

def test():
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
    print("time differences b/w sequences")

    for k in range(len(intensity_ts) - 1):
       print("int/form: " + str(round(intensity_ts[k] - formants_ts[k], 4)) +
       "\tint/pitch: " + str(round(intensity_ts[k] - pitch_ts[k], 4)) +
       "\tForm/pitch: " + str(round(formants_ts[k] - pitch_ts[k], 4)))


def main():
    snd = pm.Sound("Thats One Small.wav")

    intensity = snd.to_intensity(time_step=0, minimum_pitch=75)
    # intensity = intensity.extract(from_time=0.001, to_time=numPitchFrames*pitchFrameLength)
    numIntFrames = intensity.get_number_of_frames()
    # timeStep

    pitch = snd.to_pitch_spinet(time_step=0.001, window_length=0.005)
    numPitchFrames = pitch.get_number_of_frames()
    pitchFrameLength = pitch.get_time_from_frame_number(1)
    pitch_ts = pitch.ts()
    # print(pitch.time_step)

    formants = snd.to_formant_burg(time_step=0.001, window_length=pitchFrameLength)
    numFormantFrames = formants.get_number_of_frames()

    pitch_vals = []
    formant_vals = []
    intensity_vals = []
    intensityFromPitch = []
    intensityFromTime = []

    pitch_frame_one = pitch.get_frame(1)
    print(pitch_frame_one)

    for i in range(1, numPitchFrames+1):
        intensityFromPitch.append(pitch.get_frame(i).intensity)
        intensityFromTime.append(intensity.get_value(pitch.get_time_from_frame_number(i)))
        pitch_vals.append(pitch.get_value_in_frame(i))

        # print(f"Time = {pitch_ts[i-1]}\tIntensity From Pitch: {intensityFromPitch[i-1]}\tIntensity from Time: {intensityFromTime[i-1]}")
        # print(f"Time = {pitch_ts[i-1]}\t intensity ratio [time/pitch] = {intensityFromTime[i-1] / intensityFromPitch[i-1]}")



    print("Number of Intensity vals From Time: ")
    print(len(intensityFromTime))
    print("Number of Intensity vals From Pitch: ")
    print(len(intensityFromPitch))
    print("Number of Pitch Frames: ")
    print(numPitchFrames)
    print("Number of Formant Frames: ")
    print(numFormantFrames)
    print("Number of Intensity Frames")
    print(numIntFrames)

    # for i in range(numPitchFrames):
    #     print(f"Time: {pitch_ts[i]}\tPitch: {pitch_vals[i]}")

    return True


if __name__ == "__main__":
    main()