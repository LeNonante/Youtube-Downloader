from pytube import YouTube
from tkinter import *
from tkinter import filedialog, ttk
import customtkinter
from PIL import Image
import time

import ffmpeg
import yt_dlp

##def TelechargerUneVideo(Lien, Output, Format="MP4"):
##    try:
##        yt = YouTube(Lien)
##
##        if Format == "MP4":
##            # Télécharger la vidéo avec la plus haute résolution
##            yd = yt.streams.get_highest_resolution()
##        elif Format == "MP3":
##            # Télécharger uniquement l'audio
##            yd = yt.streams.filter(only_audio=True).first()
##
##        # Télécharger le fichier dans le dossier spécifié
##        downloaded_file = yd.download(output_path=Output)
##
##        # Si c'est un format audio (mp3), renommer le fichier en .mp3
##        if Format == "MP3":
##            base, ext = os.path.splitext(downloaded_file)
##            new_file = base + '.mp3'
##            os.rename(downloaded_file, new_file)
##            print("Téléchargement terminé en format MP3.")
##        else:
##            print("Téléchargement terminé en format MP4.")
##    except Exception as e:
##        print("Une erreur s'est produite:", str(e))

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
        self.resizable(False,False)
        self.CheminDossier=""


        self.listeURL=[] #Contiendra la liste des liens de de la forme [lien,Format,Dossier, Bool, titre] avec Bool sur False tant que le lien n'a pas été converti
        self.TelechargementLance=False
        self.NombreTelecharges=0#Compte le nombre de videos telechargees
        #Frame des entrées---------------
        self.Logo = customtkinter.CTkImage(light_image=Image.open("assets/LogoYouDownLight.png"),
                                  dark_image=Image.open("assets/LogoYouDownDark.png"),size=(100, 69))

        self.FrameEntrees=customtkinter.CTkFrame(self, width=235, height=580, fg_color=("#F3F3F3","#494949"))

        self.LabelLogo=customtkinter.CTkLabel(self.FrameEntrees, image=self.Logo, text="")
        self.LabelLogo.place(x=67,y=15)

        customtkinter.CTkLabel(self.FrameEntrees, text="Lien de la vidéo : ", fg_color="transparent").place(x=0, y=110)
        self.EntryLien=customtkinter.CTkEntry(self.FrameEntrees, placeholder_text="https://www.youtube.com/...", corner_radius=15, width=235, height=38, fg_color=("#D9D9D9","#252525"))
        self.EntryLien.place(x=0, y=135)


        self.BoutonDossier=customtkinter.CTkButton(self.FrameEntrees, text="Choix du dossier de sortie",text_color=("black","#dce4ee") ,corner_radius=15, width=235, height=38, fg_color=("#D9D9D9","#252525"), hover_color=("red","#A50000"), command=self.ChoisirDossier)
        self.BoutonDossier.place(x=0, y=190)
        customtkinter.CTkLabel(self.FrameEntrees, text="Dossier de sortie séléctionné : ", fg_color="transparent").place(x=0, y=230)

        self.TextDossierChoisi=StringVar(value="")
        self.LabelnomDossier=customtkinter.CTkLabel(self.FrameEntrees,width=235, textvariable=self.TextDossierChoisi)
        self.LabelnomDossier.place(x=0,y=250)


        customtkinter.CTkLabel(self.FrameEntrees, text="Format de sortie : ", fg_color="transparent").place(x=0, y=300)

        self.radio_var = IntVar(value=1)
        self.radiobutton_mp4 = customtkinter.CTkRadioButton(self.FrameEntrees, text="MP4",
                                             variable= self.radio_var, value=1,fg_color=("red","#DF0000"), hover_color=("#d9d9d9","#252525"))
        self.radiobutton_mp3 = customtkinter.CTkRadioButton(self.FrameEntrees, text="MP3",
                                             variable= self.radio_var, value=2, fg_color=("red","#DF0000"), hover_color=("#d9d9d9","#252525"))

        self.radiobutton_mp4.place(x=50,y=330)
        self.radiobutton_mp3.place(x=130,y=330)

        self.BoutonAddToList=customtkinter.CTkButton(self.FrameEntrees, text="Ajouter à la liste", corner_radius=15, width=235, height=38, fg_color=("red","#DF0000"), hover_color=("#DF0000","red"), command=self.AppuiBoutonAddToList)
        self.BoutonAddToList.place(x=0, y=390)

        self.TextConfirmationGauche=StringVar(value="")
        self.LabelConfirmationGauche=customtkinter.CTkLabel(self.FrameEntrees, textvariable=self.TextConfirmationGauche,width=235, height=100)
        self.LabelConfirmationGauche.place(x=0,y=430)



        self.MasquePartieEntrees=customtkinter.CTkLabel(self.FrameEntrees, text="Veuillez attendre la fin\ndes telechargements pour ajouter\nde nouvelles vidéos",width=235, height=430, fg_color=("#F3F3F3","#494949"))
        self.FrameEntrees.place(x=75,y=0)



        #Séparateur ---------------------------------------------------
        self.Separateur=customtkinter.CTkFrame(self, width=4, height=412, fg_color=("red","#DF0000"))
        self.Separateur.place(x=380,y=84)

        self.ModeBouton= StringVar(value="Light")
        self.BoutonMode=customtkinter.CTkButton(self, textvariable=self.ModeBouton,text_color=("black","#dce4ee"), corner_radius=15, width=45, height=30, fg_color=("#D9D9D9","#252525"), hover_color=("red","#A50000"), command=self.SwitchTheme)
        self.BoutonMode.place(x=427, y=30)


        self.BoutonDoc=customtkinter.CTkButton(self, text="Aide",text_color=("black","#dce4ee"), corner_radius=15, width=45, height=30, fg_color=("#D9D9D9","#252525"), hover_color=("red","#A50000"))
        self.BoutonDoc.place(x=497, y=30)


        #PARTIE Droites-------------------------------------------------
        # Création du Treeview
        self.tree = ttk.Treeview(self, columns=("col1", "col2", "col3", "col4", "col5"), show="headings")

        # Définir les colonnes
        self.tree.heading("col1", text="Titre")
        self.tree.heading("col2", text="Format")
        self.tree.heading("col3", text="Etat")
        self.tree.heading("col4", text="lien")
        self.tree.heading("col5", text="Output")

        self.tree.column("col1", width=132, anchor="center")
        self.tree.column("col2", width=60, anchor="center")
        self.tree.column("col3", width=75, anchor="center")
        self.tree.column("col3", width=75, anchor="center")
        self.tree.column('col4', width=0, stretch=NO)
        self.tree.column('col5', width=0, stretch=NO)

        self.tree.place(x=427,y=84, height=286)


        self.BoutonConvert=customtkinter.CTkButton(self, text="Telecharger", corner_radius=15, width=235, height=38, fg_color=("red","#DF0000"), hover_color=("#DF0000","red"), command=self.AppuiBoutonConvert)
        self.BoutonConvert.place(x=443, y=390)

        self.TextConfirmationDroite=StringVar(value="")
        self.LabelConfirmationDroite=customtkinter.CTkLabel(self, textvariable=self.TextConfirmationDroite,width=235, height=100, bg_color="red")
        self.LabelConfirmationDroite.place(x=443,y=440)

        self.ProgressValue=0
        self.ProgressBar=customtkinter.CTkProgressBar(self, width=235,mode="determinate", progress_color=("red","#DF0000"),corner_radius=15, fg_color=("#D9D9D9","#252525"))
        self.ProgressBar.set(0)
        self.ProgressBar.place(x=1000, y=1000)

    def AppuiBoutonAddToList(self):
        lien=self.EntryLien.get()
        if lien=="" :
            self.TextConfirmationGauche.set("Veuillez renseigner une vidéo")
            self.LabelConfirmationGauche.configure(text_color=("red","#DF0000"))

        else :
            titre=RecupTitreVideo(self.EntryLien.get())
            if titre=="Erreur de lien":
                self.TextConfirmationGauche.set("Il semble y avoir\nune erreur de lien")
                self.LabelConfirmationGauche.configure(text_color=("red","#DF0000"))

            else:
                if self.CheminDossier=="":
                    self.TextConfirmationGauche.set("Veuillez sélectionner un dossier de sortie")
                    self.LabelConfirmationGauche.configure(text_color=("red","#DF0000"))
                else :
                        if any(lien in elements for elements in self.listeURL): #On verifie si le lien est déja dans la liste
                            self.TextConfirmationGauche.set("Cette vidéo est déja dans la liste")
                            self.LabelConfirmationGauche.configure(text_color=("red","#DF0000"))
                        else :
                            Format=['MP4','MP3'][self.radio_var.get()-1]
                            Etat="Attente"
                            Dossier=self.CheminDossier
                            self.listeURL.append([lien,Format,Dossier,False,titre])
                            self.tree.insert("", "end", values=(titre, Format, Etat, lien, Dossier))
                            if len(titre)>25:
                                self.TextConfirmationGauche.set(titre[:22]+ "...\n a été ajouté à la liste")
                                self.LabelConfirmationGauche.configure(text_color=("black","#dce4ee"))
                            else :
                                self.TextConfirmationGauche.set(titre+ "\n a été ajouté à la liste")
                                self.LabelConfirmationGauche.configure(text_color=("black","#dce4ee"))

    def AppuiBoutonConvert(self):
        self.MasquePartieEntrees.place(x=0,y=100)
        liste_video=[]
        for Id_video in self.tree.get_children() :
            liste_video.append([Id_video,self.tree.item(Id_video)['values']]) #On otbient une liste de la forme [Id_video,[Infos Vide], ...]
        for video in liste_video:
            Id= video[0]
            titre= video[1][0]
            Format= video[1][1]
            Etat= video[1][2]
            Lien= video[1][3]
            output= video[1][4]

        #Mettre fpocus sur celui qui se fait DL
            self.ProgressBar.place(x=443, y=450)
            if len(titre)>25:
                self.TextConfirmationDroite.set(str(self.ProgressValue)+"%\n"+titre[:22]+ "...\n en cours de télechargement")
            else :
                self.TextConfirmationDroite.set(titre+ "\n en cours de télechargement")
            self.download_une_video(Lien, output, Format)

        self.ProgressBar.place(x=1000, y=1000)
        self.MasquePartieEntrees.place(x=1000,y=1000)

    def ChoisirDossier(self):
        """Cette fonction ouvre l'explorateur de fichier et permet d'ouvrir un dossier en renvoyant son chemin"""
        self.CheminDossier = filedialog.askdirectory(title="Dossier de sortie")
        Nom=self.CheminDossier.split("/")[-1]
        self.TextDossierChoisi.set(Nom)

    def SwitchTheme(self):

        if self.ModeBouton.get()=="Light":
            self.SetLightTheme()
        else :
            self.SetDarkTheme()

    def SetDarkTheme(self):
        customtkinter.set_appearance_mode("Dark")
        self.ModeBouton.set("Light")
        self.configure(background="#494949")

        self.treestyle = ttk.Style()
        self.treestyle.theme_use('default')
        self.treestyle.configure("Treeview", background="#252525", foreground="#dce4ee", fieldbackground="#252525", borderwidth=0)
        self.treestyle.map('Treeview', background=[('selected', "#252525")], foreground=[('selected', "red")])


    def SetLightTheme(self):
        customtkinter.set_appearance_mode("Light")
        self.ModeBouton.set("Dark")
        self.configure(background="#F3F3F3")

        self.treestyle = ttk.Style()
        self.treestyle.theme_use('default')
        self.treestyle.configure("Treeview", background="#D9D9D9", foreground="black", fieldbackground="#D9D9D9", borderwidth=0)
        self.treestyle.map('Treeview', background=[('selected', "#D9D9D9")], foreground=[('selected', "red")])


    def progress_hook(self,d):
        if d['status'] == 'downloading':
            if 'progress' in d:
                self.ProgressValue = d['progress'] * 100
        elif d['status'] == 'finished':
            self.ProgressValue


    def download_une_video(self, Lien, Output, Format="MP4"):
        # Configure l'option de téléchargement en fonction du format choisi
        if Format == 'MP4':
            ydl_opts = {
                'format': 'mp4',
                'outtmpl': '%(title)s.%(ext)s',
                'progress_hooks': [self.progress_hook],
            }
        elif Format == 'MP3':
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'outtmpl': '%(title)s.%(ext)s',
                'progress_hooks': [self.progress_hook],
            }
        else:
            raise ValueError("Format choisi non supporté. Utilisez 'mp4' ou 'mp3'.")

        # Création d'une instance yt_dlp.YoutubeDL avec les options configurées
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(Lien, download=True, )


            # Boucle pour mettre à jour la variable d'avancement toutes les secondes
            while self.ProgressValue < 100:
                self.ProgressBar.set(self.ProgressValue/100)
            print("Téléchargement terminé.")






    def Afficher(self):
        self.SetDarkTheme()
        self.mainloop()







Fenetre=Window()
Fenetre.Afficher()

#Compter le nombre de DL a faire








