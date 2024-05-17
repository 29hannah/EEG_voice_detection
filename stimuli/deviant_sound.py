"""Generate deviant sound based on the 1.0 morph
-Focus on the vocal aspect of the sound """
from pydub import AudioSegment

filename = "/Users/hannahsmacbook/PycharmProjects/EEG_voice_detection/stimuli/sound_files/env_morphs/r_e_s_d_c_morph-1.0.wav"
sound = AudioSegment.from_file(filename, format=filename[-3:])
octaves = 0.5
new_sample_rate = int(sound.frame_rate * (2.0 ** octaves))
hipitch_sound = sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})
hipitch_sound = hipitch_sound.set_frame_rate(48828)#export / save pitch changed sound
hipitch_sound.export(f"octave_{octaves}.wav", format="wav")
