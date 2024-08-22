import ffmpeg

import yt_dlp
import time

# Variable globale pour suivre l'avancement du téléchargement
download_progress = 0

def download_video(url, format_choice):
    # Configure l'option de téléchargement en fonction du format choisi
    if format_choice == 'mp4':
        ydl_opts = {
            'format': 'mp4',
            'outtmpl': '%(title)s.%(ext)s',
            'progress_hooks': [progress_hook],
        }
    elif format_choice == 'mp3':
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': '%(title)s.%(ext)s',
            'progress_hooks': [progress_hook],
        }
    else:
        raise ValueError("Format choisi non supporté. Utilisez 'mp4' ou 'mp3'.")

    # Création d'une instance yt_dlp.YoutubeDL avec les options configurées
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        video_title = info_dict.get('title', 'video')

        # Affichage du nom de la vidéo
        print(f"Téléchargement de : {video_title}")

        # Boucle pour mettre à jour la variable d'avancement toutes les secondes
        while download_progress < 100:
            print(f"Avancement du téléchargement : {download_progress}%")
            time.sleep(1)
        print("Téléchargement terminé.")

def progress_hook(d):
    global download_progress

    if d['status'] == 'downloading':
        if 'progress' in d:
            download_progress = d['progress'] * 100
    elif d['status'] == 'finished':
        download_progress = 100

