from ExtractValues import *
from formant_analysis import *
from MovingAverages import *
from FormantCleaning import *
from Assignment_2 import *


def main():
    snd = pm.Sound("Thats One Small.wav")

    pitch = snd.to_pitch_spinet(time_step=0.001, window_length=0.005)
    numPitchFrames = pitch.get_number_of_frames()
    pitchFrameLength = pitch.get_time_from_frame_number(1)
    pitch_ts = pitch.ts()
    #print(pitch.time_step)

    intensity = snd.to_intensity(time_step=0.001)
    numIntFrames = intensity.get_number_of_frames()

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


        # print(f"Time = {pitch_ts[i-1]}\t intensity ratio [time/pitch] = {intensityFromTime[i-1] / intensityFromPitch[i-1]}")



    # print("Number of Intensity vals From Time: ")
    # print(len(intensityFromTime))
    # print("Number of Intensity vals From Pitch: ")
    # print(len(intensityFromPitch))
    # print("Number of Pitch Frames: ")
    # print(numPitchFrames)
    # print("Number of Formant Frames: ")
    # print(numFormantFrames)
    # print("Number of Intensity Frames")
    # print(numIntFrames)

    # for i in range(numPitchFrames):
    #     print(f"Time: {pitch_ts[i]}\tPitch: {formants}")

    return True


if __name__ == "__main__":
    main()