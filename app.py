from flask import Flask, render_template, redirect, url_for, flash, request, session, jsonify
import mysql.connector, joblib



app = Flask(__name__)
app.secret_key = 'video' 

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    port="3306",
    database='video'
)

mycursor = mydb.cursor()

def executionquery(query,values):
    mycursor.execute(query,values)
    mydb.commit()
    return

def retrivequery1(query,values):
    mycursor.execute(query,values)
    data = mycursor.fetchall()
    return data

def retrivequery2(query):
    mycursor.execute(query)
    data = mycursor.fetchall()
    return data



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        c_password = request.form['c_password']

        if password == c_password:
            query = "SELECT email FROM users"
            email_data = retrivequery2(query)
            email_data_list = []
            for i in email_data:
                email_data_list.append(i[0])

            if email not in email_data_list:
                query = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
                values = (name, email, password)
                executionquery(query, values)

                return render_template('login.html', message="Successfully Registered!")
            return render_template('register.html', message="This email ID is already exists!")
        return render_template('register.html', message="Conform password is not match!")
    return render_template('register.html')


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        query = "SELECT email FROM users"
        email_data = retrivequery2(query)
        email_data_list = []
        for i in email_data:
            email_data_list.append(i[0])

        if email in email_data_list:
            query = "SELECT * FROM users WHERE email = %s"
            values = (email,)
            password__data = retrivequery1(query, values)
            if password == password__data[0][3]:
                session["user_email"] = email
                session["user_id"] = password__data[0][0]
                session["user_name"] = password__data[0][1]

                return redirect("/home")
            return render_template('login.html', message= "Invalid Password!!")
        return render_template('login.html', message= "This email ID does not exist!")
    return render_template('login.html')



@app.route('/home')
def home():
    return render_template('home.html')


########################################################################################################################
############################################## TRANSLATION SECTION #####################################################
########################################################################################################################

import os
from moviepy.editor import VideoFileClip, AudioFileClip
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import yt_dlp as youtube_dl

def extract_audio(video_path):
    try:
        print(12340, os.path.splitext(video_path)[0])
        audio_path = os.path.splitext(video_path)[0] + ".wav"
        print(56789, audio_path)
        clip = VideoFileClip(video_path)
        print("*************")
        clip.audio.write_audiofile(audio_path)
        print("=====================")
        return audio_path
    except Exception as e:
        print(f"Error extracting audio from video: {e}")
        return None
    
def transcribe_audio(audio_file):
    try:
        r = sr.Recognizer()
        with sr.AudioFile(audio_file) as source:
            audio_text = r.listen(source)
            try:
                rec_text = r.recognize_google(audio_text)
                print("Converting audio to text...")
            except:
                print("Run again...")
            print("Transcribing Done Successfully!")
        return rec_text
    except Exception as e:
        print(f"Error transcribing audio: {e}")
        return None
    
def translate_text(rec_text, language_to_dub):
    try:
        translator = Translator()
        translated_text = translator.translate(rec_text, dest=language_to_dub).text
        print("Translation Done Successfully!")
        return translated_text
    except Exception as e:
        print(f"Error translating text: {e}")
        return None
    
def text_to_audio(translated_text, output_audio_file, language_to_dub):
    try:
        translated_audio = gTTS(translated_text, lang=language_to_dub)
        translated_audio.save(output_audio_file)
        print("Created translated audio successfully!")
        return output_audio_file
    except Exception as e:
        print(f"Error creating audio from text: {e}")
        return None
    
def merge_audio_to_video(video_file_path, output_audio_file):
    try:
        video_clip = VideoFileClip(video_file_path)
        audio_clip = AudioFileClip(output_audio_file)
        final_clip = video_clip.set_audio(audio_clip)
        dubbed_video_path = "static/saved_video/Dubbed_video.mp4"
        final_clip.write_videofile(dubbed_video_path)
        print("Dubbed Video saved!")
        return dubbed_video_path
    except Exception as e:
        print(f"Error saving audio to video: {e}")
        return None
    
def download_youtube_video(url):
    try:
        ydl_opts = {
            # 'outtmpl': 'static/saved_video/%(title)s.%(ext)s',  # Set output path
            'outtmpl': 'static/saved_video/downloaded_video.%(ext)s',  # Set output path
            'format': 'bestvideo+bestaudio/best',  # Download best quality video and audio
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',  # Convert to mp4 format
            }],
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            },
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            # video_title = info_dict.get('title', None)
            video_title = "downloaded_video"
            video_path = f"static/saved_video/{video_title}.mp4"
            return video_path
    except Exception as e:
        print(f"Error downloading YouTube video: {e}")
        return None

    

@app.route('/translation', methods=["GET", "POST"])
def translation():
    if request.method == "POST":
        language_to_dub = request.form["language"]
        url = request.form.get("url", None)
        video = request.files.get("video", None)
        output_audio_file = "static/saved_video/translated_audio_file.wav"

        if video:
            fn = video.filename
            video_path = os.path.join('static/saved_video/', fn)
            video.save(video_path)
        else:
            video_path = download_youtube_video(url)
            print(111111111111, video_path)

        audio_path = extract_audio(video_path)
        print(2222222222222, audio_path)

        if audio_path:
            rec_text = transcribe_audio(audio_path)

            if rec_text:
                translated_text = translate_text(rec_text, language_to_dub)

                if translated_text:
                    text_to_audio(translated_text, output_audio_file, language_to_dub)

                    dubbed_video_path = merge_audio_to_video(video_path, output_audio_file)

                    if dubbed_video_path:
                        return render_template('translation.html', path = dubbed_video_path)
                    else:
                        return render_template('translation.html', message = "Error creating dubbed video. Please try again.")
                else:
                    return render_template('translation.html', message = "Error translating text. Please try again.")
            else:
                return render_template('translation.html', message = "Error transcribing audio. Please try again.")
        else:
            return render_template('translation.html', message = "Error extracting audio. Please try again.")
            
    return render_template('translation.html')




if __name__ == '__main__':
    app.run(debug = True)