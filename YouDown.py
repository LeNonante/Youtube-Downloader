from pytube import YouTube
from tkinter import *
from tkinter import filedialog, ttk
import customtkinter
from PIL import Image

import time #??
import asyncio

def TelechargerUneVideo(Lien, Output, Format="MP4"):
    try:
        yt = YouTube(Lien)

        if Format == "MP4":
            # Télécharger la vidéo avec la plus haute résolution
            yd = yt.streams.get_highest_resolution()
        elif Format == "MP3":
            # Télécharger uniquement l'audio
            yd = yt.streams.filter(only_audio=True).first()

        # Télécharger le fichier dans le dossier spécifié
        downloaded_file = yd.download(output_path=Output)

        # Si c'est un format audio (mp3), renommer le fichier en .mp3
        if Format == "MP3":
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

        self.CheminDossier=""


        self.listeURL=[] #Contiendra la liste des liens de de la forme [lien,Format,Dossier, Bool] avec Bool sur False tant que le lien n'a pas été converti
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

        self.BoutonConvert=customtkinter.CTkButton(self.FrameEntrees, text="Telecharger / Ajouter à la liste", corner_radius=15, width=235, height=38, fg_color=("red","#DF0000"), hover_color=("#DF0000","red"), command=self.AppuiBoutonConvert)
        self.BoutonConvert.place(x=0, y=390)

        self.TextConfirmation=StringVar(value="")
        self.LabelConfirmation=customtkinter.CTkLabel(self.FrameEntrees, textvariable=self.TextConfirmation,width=235, height=100)
        self.LabelConfirmation.place(x=0,y=430)




        self.FrameEntrees.place(x=430,y=0)



        #Séparateur ---------------------------------------------------
        self.Separateur=customtkinter.CTkFrame(self, width=4, height=412, fg_color=("red","#DF0000"))
        self.Separateur.place(x=351,y=84)

        self.ModeBouton= StringVar(value="Light")
        self.BoutonMode=customtkinter.CTkButton(self, textvariable=self.ModeBouton,text_color=("black","#dce4ee"), corner_radius=15, width=45, height=30, fg_color=("#D9D9D9","#252525"), hover_color=("red","#A50000"), command=self.SwitchTheme)
        self.BoutonMode.place(x=42, y=30)


        self.BoutonDoc=customtkinter.CTkButton(self, text="Aide",text_color=("black","#dce4ee"), corner_radius=15, width=45, height=30, fg_color=("#D9D9D9","#252525"), hover_color=("red","#A50000"))
        self.BoutonDoc.place(x=112, y=30)


        #PARTIE GAUCHE-------------------------------------------------
        # Création du Treeview
        self.tree = ttk.Treeview(self, columns=("col1", "col2", "col3"), show="headings")

        # Définir les colonnes
        self.tree.heading("col1", text="Titre")
        self.tree.heading("col2", text="Format")
        self.tree.heading("col3", text="Etat")
        self.tree.column("col1", width=132, anchor="center")
        self.tree.column("col2", width=60, anchor="center")
        self.tree.column("col3", width=75, anchor="center")


        self.tree.place(x=42,y=84, height=412)


    def AppuiBoutonConvert(self):
        lien=self.EntryLien.get()
        if lien=="" :
            self.TextConfirmation.set("Veuillez renseigner une vidéo")
            self.LabelConfirmation.configure(text_color=("red","#DF0000"))

        else :
            titre=RecupTitreVideo(self.EntryLien.get())
            if titre=="Erreur de lien":
                self.TextConfirmation.set("Il semble y avoir\nune erreur de lien")
                self.LabelConfirmation.configure(text_color=("red","#DF0000"))

            else:
                if self.CheminDossier=="":
                    self.TextConfirmation.set("Veuillez sélectionner un dossier de sortie")
                    self.LabelConfirmation.configure(text_color=("red","#DF0000"))
                else :
                        if ((lien, False) in self.listeURL) or ((lien, True) in self.listeURL):
                            self.TextConfirmation.set("Cette vidéo est déja dans la liste")
                            self.LabelConfirmation.configure(text_color=("red","#DF0000"))
                        else :
                            Format=['MP4','MP3'][self.radio_var.get()-1]
                            Etat="Attente"
                            Dossier=self.CheminDossier
                            self.listeURL.append([lien,Format,Dossier,False])
                            self.tree.insert("", "end", values=(titre, Format, Etat))
                            if len(titre)>25:
                                self.TextConfirmation.set(titre[:22]+ "...\n a été ajouté à la liste")
                                self.LabelConfirmation.configure(text_color=("black","#dce4ee"))
                            else :
                                self.TextConfirmation.set(titre+ "\n a été ajouté à la liste")
                                self.LabelConfirmation.configure(text_color=("black","#dce4ee"))

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
    def Afficher(self):
        self.SetDarkTheme()
        self.mainloop()

    def telechargerListe(self):
        print('qdqsdqsd') #??
        if self.TelechargementLance==False : #Si aucun telechargment n'est en cours
            self.TelechargementLance=True#On enregoistre l'etat des telechargement sur True
            while self.NombreTelecharges!= len(self.listeURL) : #Tant qu'on a pas tout telechargé
                for i in range(len(self.listeURL)): #On parcourt la liste jusqu'a trouvé le premier non telechargé
                    if self.listeURL[i][3]==False :
                        lien=self.listeURL[i][0]
                        Format=self.listeURL[i][1]
                        Dossier=self.listeURL[i][2]
                        #TelechargerUneVideo(lien, Dossier, Format)
                        print(lien,Format,Dossier)#??
                        time.sleep(5)#??
                        self.listeURL[i][3]=True
                        self.NombreTelecharges+=1
                        break



Fenetre=Window()
Fenetre.Afficher()

#Compter le nombre de DL a faire








