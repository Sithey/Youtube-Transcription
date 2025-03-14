import os
import yt_dlp
import whisper
import re
import webbrowser
from tqdm import tqdm
from pytube import YouTube
import shutil
import sys

# Import youtube_dl comme méthode alternative
import youtube_dl

def get_video_id(youtube_url):
    """Extracts the video ID from the YouTube URL"""
    video_id = re.search(r"(?<=v=)[\w-]+", youtube_url)
    if not video_id:
        video_id = re.search(r"(?<=be/)[\w-]+", youtube_url)
    return video_id.group() if video_id else None

def download_with_yt_dlp(youtube_url, output_path):
    """Downloads the audio track of a YouTube video using the latest yt-dlp"""
    try:
        print("Tentative de téléchargement avec yt-dlp 2025.2.19...")
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': output_path + '.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'quiet': False,
            'noprogress': False,
            # Options pour contourner les restrictions
            'nocheckcertificate': True,
            'ignoreerrors': True,
            'no_warnings': False,
            'sleep_interval': 1,
            'max_sleep_interval': 5,
            'geo_bypass': True,
            'geo_bypass_country': 'US',
            'extractor_args': {
                'youtube': {
                    'player_client': ['android', 'web'],
                    'player_skip': ['js', 'configs']
                }
            }
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=False)
            print(f"Vidéo trouvée: {info.get('title', 'Titre inconnu')}")
            ydl.download([youtube_url])
        
        return output_path + '.mp3'
    except Exception as e:
        print(f"Erreur avec yt-dlp: {str(e)}")
        return None

def download_with_youtube_dl(youtube_url, output_path):
    """Télécharge l'audio avec youtube_dl comme méthode alternative"""
    try:
        print("Tentative de téléchargement avec youtube_dl...")
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': output_path + '.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'quiet': False,
            'no_warnings': False,
            'ignoreerrors': False
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])
        
        return output_path + '.mp3'
    except Exception as e:
        print(f"Erreur avec youtube_dl: {str(e)}")
        return None

def download_youtube_with_pytube(youtube_url, output_path):
    """Downloads YouTube audio using pytube library"""
    try:
        print("Téléchargement avec pytube...")
        # Create YouTube object with bypass
        yt = YouTube(youtube_url, use_oauth=False, allow_oauth_cache=False)
        
        try:
            # Try to get title (might fail)
            title = yt.title
            print(f"Titre de la vidéo: {title}")
        except Exception:
            print("Impossible d'accéder au titre de la vidéo, mais tentative de téléchargement quand même...")
        
        # Get the best audio stream
        audio_stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
        
        if not audio_stream:
            print("Aucun flux audio trouvé.")
            return None
        
        # Download the file
        try:
            print(f"Téléchargement du flux audio...")
            output_dir = os.path.dirname(output_path)
            download_path = audio_stream.download(output_path=output_dir)
            
            # Rename to mp3
            base, ext = os.path.splitext(download_path)
            output_file = f"{base}.mp3"
            
            # Rename the file to mp3
            try:
                os.rename(download_path, output_file)
                print(f"Fichier renommé en: {output_file}")
            except Exception as e:
                print(f"Erreur lors du renommage: {e}")
                # If rename fails due to file already existing, create a copy
                shutil.copy(download_path, output_file)
                os.remove(download_path)
                print(f"Fichier copié vers: {output_file}")
                
            return output_file
        except Exception as e:
            print(f"Erreur lors du téléchargement: {e}")
            return None
            
    except Exception as e:
        print(f"Erreur avec pytube: {str(e)}")
        # Print more details for debugging
        print(f"Type d'erreur: {type(e).__name__}")
        print(f"Détails de l'erreur: {str(e)}")
        return None

def try_external_downloader(youtube_url, output_path, video_id):
    """Try to download using external methods"""
    print("\nTentative d'utilisation d'une méthode manuelle de téléchargement...")
    
    # Ask user if they want to try downloading manually
    manual_choice = input("Voulez-vous ouvrir un site web pour télécharger l'audio manuellement? (o/n): ")
    if manual_choice.lower() == 'o':
        # Open a popular YouTube to MP3 converter in the browser
        converter_url = f"https://www.y2mate.com/youtube/{video_id}"
        print(f"Ouverture de {converter_url} dans votre navigateur...")
        webbrowser.open(converter_url)
        
        print("\nInstructions:")
        print("1. Utilisez le site web pour télécharger le fichier MP3")
        print("2. Sauvegardez le fichier MP3 à un emplacement que vous pouvez trouver")
        print("3. Revenez à ce programme une fois terminé")
        
        wait_for_download = input("\nAppuyez sur Entrée lorsque vous avez terminé le téléchargement du fichier MP3...")
        
        # Ask for the file path
        mp3_path = input("Entrez le chemin vers le fichier MP3 téléchargé: ")
        if os.path.exists(mp3_path):
            # Move the file to our expected location
            try:
                output_file = output_path + '.mp3'
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                
                # Copy the file instead of moving it
                with open(mp3_path, 'rb') as src_file:
                    with open(output_file, 'wb') as dst_file:
                        dst_file.write(src_file.read())
                
                print(f"Fichier copié vers: {output_file}")
                return output_file
            except Exception as e:
                print(f"Erreur lors de la copie du fichier: {str(e)}")
                # If copy fails, just use the original path
                return mp3_path
        else:
            print(f"Erreur: Le fichier {mp3_path} n'existe pas.")
            return None
    
    return None

def process_local_mp3(mp3_path):
    """Processes a local MP3 file and returns the file path and a directory name for output"""
    if not os.path.exists(mp3_path):
        print(f"Erreur: Le fichier {mp3_path} n'existe pas.")
        return None, None
    
    # Create a directory based on the file name without extension
    file_name = os.path.basename(mp3_path)
    name_without_ext = os.path.splitext(file_name)[0]
    directory = os.path.join(os.getcwd(), f"local_{name_without_ext}")
    os.makedirs(directory, exist_ok=True)
    
    return mp3_path, directory

def transcribe_audio_with_progress(audio_path):
    """Transcribes an audio file with progress tracking"""
    model = whisper.load_model("medium")
    
    result = model.transcribe(audio_path, verbose=True)
    
    transcription = result['text']
    
    print("Transcription en cours...")
    for _ in tqdm(range(100), desc="Progression de la transcription"):
        pass 
    return transcription

def format_transcription(transcription):
    """Adds a newline after each sentence"""
    formatted_transcription = transcription.replace('. ', '.\n')
    formatted_transcription = formatted_transcription.replace('? ', '?\n')
    formatted_transcription = formatted_transcription.replace('! ', '!\n')
    return formatted_transcription

def display_youtube_download_alternatives(video_id):
    """Displays alternative options when YouTube download fails"""
    print("\n==== SOLUTIONS ALTERNATIVES ====")
    print("Option 1: Télécharger l'audio manuellement en utilisant des extensions de navigateur ou des services en ligne")
    print(f"       Vous pouvez essayer des sites comme y2mate.com, savefrom.net, ou ytmp3.cc")
    print(f"       ID de vidéo: {video_id}")
    print(f"       URL complète: https://www.youtube.com/watch?v={video_id}")
    print("Option 2: Connectez-vous à votre compte Google dans votre navigateur et réessayez")
    print("Option 3: Utilisez un VPN pour changer votre adresse IP et réessayez")
    print("===========================")

def main():
    print("Bienvenue dans l'outil de transcription YouTube/MP3")
    print("1. Rechercher et transcrire une vidéo YouTube")
    print("2. Transcrire un fichier MP3 local")
    
    choice = input("Entrez votre choix (1 ou 2): ")
    
    audio_file = None
    directory = None
    
    if choice == "1":
        youtube_url = input("Entrez l'URL de la vidéo YouTube: ")
        
        # Extracting the video ID
        video_id = get_video_id(youtube_url)
        if not video_id:
            print("Impossible d'extraire l'ID de la vidéo.")
            return
        
        # Create a directory based on the video ID
        directory = os.path.join(os.getcwd(), video_id)
        os.makedirs(directory, exist_ok=True)
        
        audio_path = os.path.join(directory, 'audio')
        
        # Méthode 1: Téléchargement via yt-dlp 2025.2.19
        print("Téléchargement de l'audio...")
        audio_file = download_with_yt_dlp(youtube_url, audio_path)
        
        # Méthode 2: Si yt-dlp échoue, essayer youtube_dl
        if not audio_file or not os.path.exists(audio_file):
            print("Échec avec yt-dlp, essai avec youtube_dl...")
            audio_file = download_with_youtube_dl(youtube_url, audio_path)
        
        # Méthode 3: Si youtube_dl échoue, essayer pytube
        if not audio_file or not os.path.exists(audio_file):
            print("Échec avec youtube_dl, essai avec pytube...")
            audio_file = download_youtube_with_pytube(youtube_url, audio_path)
        
        # Si toutes les méthodes automatiques échouent, proposer solutions alternatives
        if not audio_file or not os.path.exists(audio_file):
            print("Échec du téléchargement automatique de l'audio.")
            # Show alternatives when YouTube download fails
            display_youtube_download_alternatives(video_id)
            
            # Try external downloader
            audio_file = try_external_downloader(youtube_url, audio_path, video_id)
            
            if not audio_file:
                # Ask if user wants to try with a local file instead
                retry_choice = input("\nVoulez-vous essayer avec un fichier MP3 local à la place? (o/n): ")
                if retry_choice.lower() == 'o':
                    mp3_path = input("Entrez le chemin vers votre fichier MP3: ")
                    audio_file, directory = process_local_mp3(mp3_path)
                    if not audio_file:
                        return
                else:
                    return
        else:
            print(f"Audio téléchargé: {audio_file}")
    
    elif choice == "2":
        mp3_path = input("Entrez le chemin vers votre fichier MP3: ")
        audio_file, directory = process_local_mp3(mp3_path)
        if not audio_file:
            return
    
    else:
        print("Choix invalide. Veuillez exécuter le programme à nouveau et sélectionner 1 ou 2.")
        return
    
    # Transcribe the audio file
    transcription = transcribe_audio_with_progress(audio_file)
    
    formatted_transcription = format_transcription(transcription)

    transcription_file = os.path.join(directory, "transcription.txt")
    with open(transcription_file, "w", encoding='utf-8') as f:
        f.write(formatted_transcription)
    
    print(f"Transcription terminée ! Le texte a été enregistré dans '{transcription_file}'.")

if __name__ == "__main__":
    main()
