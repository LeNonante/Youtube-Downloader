from pytube import YouTube
from tkinter import *
import customtkinter
from PIL import Image



def TelechargerUneVideo(Lien, Output, format="mp4"):
    try:
        yt = YouTube(Lien)

        if format == "MP4":
            # Télécharger la vidéo avec la plus haute résolution
            yd = yt.streams.get_highest_resolution()
        elif format == "MP3":
            # Télécharger uniquement l'audio
            yd = yt.streams.filter(only_audio=True).first()

        # Télécharger le fichier dans le dossier spécifié
        downloaded_file = yd.download(output_path=Output)

        # Si c'est un format audio (mp3), renommer le fichier en .mp3
        if format == "MP3":
            base, ext = os.path.splitext(downloaded_file)
            new_file = base + '.mp3'
            os.rename(downloaded_file, new_file)
            print("Téléchargement terminé en format MP3.")
        else:
            print("Téléchargement terminé en format MP4.")
    except Exception as e:
        print("Une erreur s'est produite:", str(e))

def RecupTitreVideo(Lien):
    try:
        yt = YouTube(Lien)
        titre = yt.title
        return titre
    except Exception as e:
        return "Erreur de lien"


class Window(Tk):
    def __init__(self):
        super().__init__()
        self.title=("YouDown")
        self.geometry("740x580")
        self.configure(background="#F3F3F3")


        #Frame des entrées---------------
        self.Logo = customtkinter.CTkImage(light_image=Image.open("assets/LogoYouDownLight.png"),
                                  dark_image=Image.open("assets/LogoYouDownDark.png"),size=(100, 69))

        self.FrameEntrees=customtkinter.CTkFrame(self, width=235, height=580, fg_color=("#F3F3F3","#494949"))

        self.LabelLogo=customtkinter.CTkLabel(self.FrameEntrees, image=self.Logo, text="")
        self.LabelLogo.place(x=67,y=15)

        customtkinter.CTkLabel(self.FrameEntrees, text="Lien de la vidéo : ", fg_color="transparent").place(x=0, y=110)
        self.EntryLien=customtkinter.CTkEntry(self.FrameEntrees, placeholder_text="https://www.youtube.com/...", corner_radius=15, width=235, height=38, fg_color=("#D9D9D9","#252525"))
        self.EntryLien.bind("<FocusIn>", self.ResetNomVideo)
        self.EntryLien.place(x=0, y=135)

        self.BoutonvaliderLien=customtkinter.CTkButton(self.FrameEntrees, text='Ok', corner_radius=15, width=45, height=30, fg_color=("#D9D9D9","#252525"), hover_color=("red","#A50000"), command=self.AfficherNomVideo)
        self.BoutonvaliderLien.place(x=0, y=533)

        customtkinter.CTkLabel(self.FrameEntrees, text="Titre de la vidéo : ", fg_color="transparent").place(x=0, y=180)

        self.BoutonDossier=customtkinter.CTkButton(self.FrameEntrees, text="Choix du dossier de sortie", corner_radius=15, width=235, height=38, fg_color=("#D9D9D9","#252525"), hover_color=("red","#A50000"))
        self.BoutonDossier.place(x=0, y=250)
        customtkinter.CTkLabel(self.FrameEntrees, text="Dossier de sortie séléctionné : ", fg_color="transparent").place(x=0, y=290)

        customtkinter.CTkLabel(self.FrameEntrees, text="Format de sortie : ", fg_color="transparent").place(x=0, y=360)

        self.radio_var = IntVar(value=1)
        self.radiobutton_mp4 = customtkinter.CTkRadioButton(self.FrameEntrees, text="MP4",
                                             variable= self.radio_var, value=1)
        self.radiobutton_mp3 = customtkinter.CTkRadioButton(self.FrameEntrees, text="MP3",
                                             variable= self.radio_var, value=2)

        self.radiobutton_mp4.place(x=50,y=390)
        self.radiobutton_mp3.place(x=130,y=390)

        self.BoutonConvert=customtkinter.CTkButton(self.FrameEntrees, text="Telecharger / Ajouter à la liste", corner_radius=15, width=235, height=38, fg_color=("red","#DF0000"), hover_color=("#DF0000","red"))
        self.BoutonConvert.place(x=0, y=450)

        self.FrameEntrees.place(x=430,y=0)




        self.ModeBouton= StringVar(value="Light")
        self.BoutonMode=customtkinter.CTkButton(self, textvariable=self.ModeBouton, corner_radius=15, width=45, height=30, fg_color=("#D9D9D9","#252525"), hover_color=("red","#A50000"), command=self.SwitchTheme)
        self.BoutonMode.place(x=665, y=533)

    def ResetNomVideo(self, event=0):
        customtkinter.CTkLabel(self.FrameEntrees, bg_color=("#F3F3F3","#494949"), width=235, height=49, text="").place(x=0,y=200)
    def AfficherNomVideo(self):
        self.ResetNomVideo()
        lien=self.EntryLien.get()
        if lien!="" :
            titre=RecupTitreVideo(lien)
            customtkinter.CTkLabel(self.FrameEntrees, text=titre, bg_color=("#F3F3F3","#494949"), width=235).place(x=0,y=210)


    def SwitchTheme(self):
        if self.ModeBouton.get()=="Light":
            self.SetLightTheme()
        else :
            self.SetDarkTheme()

    def SetDarkTheme(self):
        customtkinter.set_appearance_mode("Dark")
        self.ModeBouton.set("Light")
        self.configure(background="#494949")

    def SetLightTheme(self):
        customtkinter.set_appearance_mode("Light")
        self.ModeBouton.set("Dark")
        self.configure(background="#F3F3F3")

    def Afficher(self):
        self.SetDarkTheme()
        self.mainloop()


Fenetre=Window()
Fenetre.Afficher()

#Verif si deja dans la liste avant de DL
#Compter le nombre de DL a faire








