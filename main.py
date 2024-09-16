import os
import yt_dlp
import whisper
import re
from tqdm import tqdm  

def get_video_id(youtube_url):
    """Extracts the video ID from the YouTube URL"""
    video_id = re.search(r"(?<=v=)[\w-]+", youtube_url)
    if not video_id:
        video_id = re.search(r"(?<=be/)[\w-]+", youtube_url)
    return video_id.group() if video_id else None

def download_youtube_video(youtube_url, output_path):
    """Downloads the audio track of a YouTube video and returns the path of the downloaded file"""
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_path + '.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': False, 
        'noprogress': False 
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])

    return output_path + '.mp3'

def transcribe_audio_with_progress(audio_path):
    """Transcribes an audio file with progress tracking"""
    model = whisper.load_model("medium")
    
    result = model.transcribe(audio_path, verbose=True)
    
    transcription = result['text']
    
    print("Transcription in progress...")
    for _ in tqdm(range(100), desc="Transcription progress"):
        pass 
    return transcription

def format_transcription(transcription):
    """Adds a newline after each sentence"""
    formatted_transcription = transcription.replace('. ', '.\n')
    formatted_transcription = formatted_transcription.replace('? ', '?\n')
    formatted_transcription = formatted_transcription.replace('! ', '!\n')
    return formatted_transcription

def main():
    youtube_url = input("Enter the YouTube video URL: ")
    
    # Extracting the video ID
    video_id = get_video_id(youtube_url)
    if not video_id:
        print("Unable to extract the video ID.")
        return
    
    # Create a directory based on the video ID
    directory = os.path.join(os.getcwd(), video_id)
    os.makedirs(directory, exist_ok=True)
    
    audio_path = os.path.join(directory, 'audio')
    
    # Download the YouTube video (audio only)
    print("Downloading the audio...")
    audio_file = download_youtube_video(youtube_url, audio_path)
    
    if os.path.exists(audio_file):
        print(f"Audio downloaded: {audio_file}")
        
        transcription = transcribe_audio_with_progress(audio_file)
        
        formatted_transcription = format_transcription(transcription)

        transcription_file = os.path.join(directory, "transcription.txt")
        with open(transcription_file, "w", encoding='utf-8') as f:
            f.write(formatted_transcription)
        
        print(f"Transcription complete! The text has been saved to '{transcription_file}'.")
    else:
        print("Failed to download the audio or the audio file was not found.")

if __name__ == "__main__":
    main()
