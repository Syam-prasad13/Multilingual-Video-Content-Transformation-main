
import os 
import sys
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips
import speech_recognition as sr 
from googletrans import Translator
from gtts import gTTS

def convert_video_to_audio(video_file):
    try:
        audio_file = os.path.splitext(video_file)[0]+".wav"
        clip=VideoFileClip(video_file)
        clip.audio.write_audiofile(audio_file)
        print("Audio Extracted successfully!")
        return audio_file
    except Exception as e:
        print(f"Error extracting audio from video: {e}")
        return None

def transcribe_audio(audio_file):
    try: 
        r=sr.Recognizer()
        with sr.AudioFile(audio_file) as source:
            audio_text=r.listen(source)
            try:
                rec_text=r.recognize_google(audio_text)
                print("Converting audio to text...")
            except:
                print("run again...")
            print("Transcribing Done Successfully!")
        return rec_text
    except Exception as e:
        print(f"Error transcabing audio: {e}")
        return None
        
def translate_text(rec_text,language_to_dub):
    try: 
        translator = Translator()
        translated_text = translator.translate(rec_text,dest=language_to_dub).text
        print("Translation Done Successfully!")
        return translated_text
    except Exception as e:
        print(f"Error translating text: {e}")
        return None

def text_to_audio(translated_text,language_to_dub,audio_file):
    try: 
        translated_audio= gTTS(translated_text,lang=language_to_dub)
        output_audio_file=r"D:\Practice Aishwarya Raut\Video_dubbing\translated_audio_file.wav"
        translated_audio.save(output_audio_file)
        print("Created translated audio successfully!")
        return output_audio_file
    except Exception as e:
        print(f"Error creating audio from text: {e}")
        return None

def merge_audio_to_video(video_file_path,output_audio_file):
    try: 
        video_clip=VideoFileClip(video_file_path)
        audio_clip = AudioFileClip(output_audio_file)
        final_clip= video_clip.set_audio(audio_clip)
        final_clip.write_videofile("Dubbed video"+".mp4")
        print("Dubbed Video saved !")
    except Exception as e:
        print(f"Error saving audio to video: {e}")
        return None
    

def video_dubbing(video_file_path, language_to_dub):
    # Convert video to audio
        audio_file=convert_video_to_audio(video_file_path)
        if audio_file is None:
                return 
    
    # Transcribe audio to text
        rec_text = transcribe_audio(audio_file)
        if rec_text is None:
                return
    
    # Translate text to another language
        translated_text = translate_text(rec_text, language_to_dub)
        if translated_text is None:
                return
    
    # Convert text to audio
        output_audio_file = text_to_audio(translated_text, language_to_dub, audio_file)
        if output_audio_file is None:
                return
    # Merge audio to video
        merge_audio_to_video(video_file_path, output_audio_file)
        
    # Return the dubbed video file name
        return "Dubbed video"+".mp4"


video_dubbing(r"D:\Practice Aishwarya Raut\Video_dubbing\How Civil Servants Built Modern India _ Flashback with Palki Sharma.mp4","te")