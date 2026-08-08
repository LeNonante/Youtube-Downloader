import os
import yt_dlp
from pathlib import Path

def get_downloads_folder():
    # Détecte automatiquement le dossier Téléchargements de l'utilisateur
    if os.name == 'nt':
        return os.path.join(os.environ['USERPROFILE'], 'Downloads')
    return os.path.join(os.path.expanduser('~'), 'Downloads')

def main():
    print("=== Téléchargeur YouTube CLI ===")
    url = input("Entrez le lien (vidéo ou playlist) : ").strip()
    choix = input("Format ? (1 = Audio MP3, 2 = Vidéo MP4) : ").strip()

    downloads_path = get_downloads_folder()
    
    # Options de base de yt-dlp
    ydl_opts = {
        'outtmpl': os.path.join(downloads_path, '%(title)s.%(ext)s'),
        'ignoreerrors': True, # Continue si une vidéo de la playlist est bloquée
        'quiet': False,
        'no_warnings': True
    }

    if choix == '1':
        print("\n[~] Préparation du téléchargement Audio (MP3)...")
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        })
    else:
        print("\n[~] Préparation du téléchargement Vidéo (MP4)...")
        ydl_opts.update({
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'merge_output_format': 'mp4',
        })

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print(f"\n[✔] Terminé ! Fichiers sauvegardés dans : {downloads_path}")
    except Exception as e:
        print(f"\n[X] Erreur : {e}")
    
    input("\nAppuyez sur Entrée pour quitter...")

if __name__ == "__main__":
    main()