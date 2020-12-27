# -*- coding: utf-8 -*-.
import os
import time
import os.path
import scrython
import sys
import tkinter as tk
import urllib.request
import PIL
import re
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
from tkinter import Tk
from tkinter import ttk
from tkinter import Entry
from tkinter import Button
from tkinter import Label
from tkinter import Toplevel
from tkinter import Scrollbar
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import askyesno
import io
from io import BytesIO
from unicodedata import name
import pickle


class Magic(Tk):
    def __init__(self):
        super(Magic, self).__init__()
        self.nom="Magic"
        self.police = ImageFont.truetype("font/TimesNewRoman.ttf", 50)
        self.police_proxy = ImageFont.truetype("font/TimesNewRoman.ttf", 25)
        self.liste_nb_cartes_dans_decklist=[]
        self.liste_nom_cartes_dans_decklist=[]
        self.liste_position_extension_dans_decklist=[]
        self.liste_extension_dans_decklist=[]
        self.liste_nom_a_coller=[]
        self.liste_avec_tous_les_noms_encore=[]
        os.chdir("images")
        try:
            self.spam = self.clipboard_get()
        except tk.TclError:
            self.spam = "None"
        self.title("Magic pour les non programmeurs")
        self.geometry("500x300")
        self.liste_carte_avec_nb_exemplaires=[]
        self.label_vide = tk.Label(self, text = "                                ")
        self.label_vide.grid(row=0,column=0)
        self.label_carte = tk.Label(self, text = "Tapez le nom de la carte en dessous")
        self.label_carte.grid(row=0,column=1)
        self.entree = Entry(self)#demande la valeur
        self.entree.grid(row=1,column=1) # integration du widget a la fenetre principale
        self.label_choix_format_image=tk.Label(self, text = "Choix du format de l'image")
        self.label_choix_format_image.grid(row=2,column=1)
        self.liste_formats=["art_crop","border_crop","large","normal","png","small"]
        self.liste_combo_format = ttk.Combobox(self, values=self.liste_formats)
        self.liste_combo_format.grid(row=3,column=1)
        self.liste_combo_format.bind("<<ComboboxSelected>>", self.get_format)
        self.label_choix_nb_exemplaire = tk.Label(self, text = "Nb Exemplaires")
        self.label_choix_nb_exemplaire.grid(row=4,column=1)
        self.liste_nb_exemplaire=("1", "2","3","4","5","6","7") #On va jusqu'à sept à cause des sept nains mais avec les pétitionnaires tenaces faut voir 
        self.liste_combo = ttk.Combobox(self, values=self.liste_nb_exemplaire)
        self.liste_combo.current(0)
        self.liste_combo.grid(row=5,column=1)
        self.liste_combo.bind("<<ComboboxSelected>>", self.get_nb_exemplaires)
        self.valider = Button(self, text = 'valider', command = self.saisie)
        self.valider.grid(row=6,column=1)
        self.button_import = Button(self, text = 'Import', command = self.func_import)
        self.button_import.grid(row=7,column=1)
        self.deck_list = tk.StringVar()
        self.deck_list.set(self.spam)
        self.box = Entry(self, textvariable = self.deck_list)
        self.box.grid(row=8, column=1 ,   sticky='ew')
        self.scroll_y = tk.Scrollbar(self.box, orient="vertical")
        self.scroll_y.pack(side="right", expand=True, fill="y")
        self.quitter = Button(self, text = "quitter", command = self.destroy)
        self.quitter.grid(row=10,column=1)
        self.proxy=Button(self, text="proxy", command=self.faire_apparaitre_proxy)
        self.proxy.grid(row=11,column=1)
            #self.fen1.mainloop()

    def purge(self,dir, pattern):
        for f in os.listdir(dir):
            if re.search(pattern, f):
                os.remove(os.path.join(dir, f))

    def somme(self):
        liste=self.liste_nb_cartes_dans_decklist
        _somme = 0
        for i in liste:
            _somme = _somme + int(i)
        return _somme
        
    def creer_image_page2(self,list_image,nom_page):
        x=0
        y=0
        longueur=745
        hauteur=1040
        marge= int(longueur /  10)
        boxl=longueur+marge
        boxh=hauteur+marge
        size=((boxl*3)-marge,boxh*3-marge)
        page = Image.new("RGB",size,(255,255,255))
        chaine_proxy="Proxy not for Sale"
        for y in range(3):
            for x in range(3):
                #Faudrait essayer d'assombrir les images , elles sont trop claires par rapport aux vraies cartes
                try:
                    print("Je commence par prendre",list_image[3*y+x])
                    image_to_draw=Image.open(list_image[3*y+x])
                    each_image_draw = ImageDraw.Draw(image_to_draw)
                    print("Image prise",list_image[3*y+x])
                    print("Test Collage",each_image_draw)
                    print(type(each_image_draw))
                    each_image_draw.text((marge+200, hauteur-marge+40),chaine_proxy,(255,255,255),font=self.police_proxy)
                    page.paste(image_to_draw,(boxl*x,boxh*y))
                except ValueError:
                    print("Erreur",list_image[3*y+x])
                    image_to_draw=Image.open(list_image[3*y+x])
                    each_image_draw=image_to_draw
                    each_image_draw.text((marge+200, hauteur-marge+40),chaine_proxy,(255,255,255),font=self.police_proxy)
                    page.paste(image_to_draw,(boxl*x,boxh*y))
        draw = ImageDraw.Draw(page)
        marge_reelle=6.27/4
        chaine="À imprimer en %d cm * %d cm"  % (int(6.27*3+marge_reelle),int(8.67*3+marge_reelle))
        draw.text((boxl+marge, hauteur),chaine,(0,0,0),font=self.police)
        page.save(nom_page)

    def creer_doc(self):
        print("Hello")

    def get_magic_card_image(self,searchterm):
        #ne pas oublier les time.sleep afin de ne pas surcharger scryfall
        try:
            time.sleep(1)
            card = scrython.cards.Named(fuzzy=searchterm)
            time.sleep(1)
            print(card.image_uris())
            format_var = self.liste_combo_format.get()
            print("Format choisi"+format_var)
            card2 = card.image_uris(0,format_var) #index ?
            time.sleep(1)
            if(format_var=="png"):
                urllib.request.urlretrieve(card2,searchterm+".png")
                time.sleep(1)
            else:
                urllib.request.urlretrieve(card2,searchterm+".jpg")
                time.sleep(1)
        except Exception:
            print('not found')
            searchterm=""
            #continue if file not found
        print("T'as fini youpi")
        return searchterm

    def get_format(self,event):
        format_var = self.liste_combo_format.get()
        return format_var

    def get_nb_exemplaires(self,event):
        select = self.liste_combo.get()
        print("Vous avez sélectionné : '", select,"'")

    def saisie(self):
        searchterm = self.entree.get() #On lit la carte
        if(searchterm == ""):
            sys.exit("La carte qui a aucun nom n'existe pas") #Il faudra voir pour afficher un message d'erruer en rouge
        else:
            #GetMagicCardImage(searchterm).show()
            image_souhait=self.get_magic_card_image(searchterm)
            self.liste_carte_avec_nb_exemplaires.append(self.liste_combo.get())
            self.liste_carte_avec_nb_exemplaires.append(image_souhait)
        return image_souhait #recupére la valeur saisie
    
    def ecriture_carte_double(self,carte_double,regex_carte_face_double,name32,nbcards,extension,position):
        carte_double_face_tab=[]
        carte_double_face=""
        nom_carte_face_double=""
        left=""
        right=""
        str_carte_double=""
        carte_double_face_tab= carte_double.card_faces()
        if len(carte_double_face_tab) >1:
            carte_double_face = str(carte_double_face_tab[1])
            nom_carte_face_double = re.search(regex_carte_face_double,carte_double_face)
            nom_carte_face_double=str(nom_carte_face_double)
            left=name32
            right="\'\">"
            nom_carte_face_double=nom_carte_face_double[nom_carte_face_double.index(left)+len(left):nom_carte_face_double.index(right)]
            str_carte_double="{0} {1} {2} {3}".format(nbcards,nom_carte_face_double,extension,position)
            deck_txt="deck_txt"
            deck= open(deck_txt, "a")
            deck.write("\n")
            deck.close()
            deck= open(deck_txt, "a")
            deck.write(str_carte_double)
            deck.close()
        else:
            print("")
        
    
    def ecriture1(self,nom_carte,regex_carte_face_double,nbcards,extension,position,name32):
        carte_double=""
        info_carte_modale=""
        carte_modale=""
        if nom_carte:
            try:
                carte_double = scrython.cards.Named(fuzzy=nom_carte)
                if carte_double.card_faces():
                    print('')
                else:
                    info_carte_modale=carte_double.card_faces()
                    carte_modale=str(info_carte_modale[1])
                    if "\'colors\': []" in carte_modale:
                        self.ecriture_carte_double(carte_double,regex_carte_face_double,name32,nbcards,extension,position)
                    else:
                        print("")
            except:
                i=0
                if(i==1):
                    sys.exit()
                else:
                    print("")
        return nom_carte
    
    def func_nom_carte(self,nom_carte,instant_adventure,nbcards,extension,position,regex_carte_face_double,name):
        nom_carte=nom_carte.group(1)
        print(nom_carte)
        print("Je décide de planter")
        self.liste_nom_cartes_dans_decklist.append(nom_carte)
        self.liste_avec_tous_les_noms_encore.append(nom_carte)
        print("J'ai planté")
        try:
            carte_double = scrython.cards.Named(fuzzy=nom_carte)
            carte_double_face_tab= carte_double.card_faces()
            carte_double_face = str(carte_double_face_tab[0])
            if instant_adventure or "Sorcery — Adventure" in carte_double_face: #Attention les cartes avec aventure = cartes doubles et ont 'type_line':
                print("Bonjour carte aventure")
            else:
                carte_double_face_tab= carte_double.card_faces()
                if len(carte_double_face_tab) >1:
                    carte_double_face = str(carte_double_face_tab[0])
                    self.liste_nb_cartes_dans_decklist.append(nbcards)
                    self.liste_extension_dans_decklist.append(extension)
                    self.liste_position_extension_dans_decklist.append(position)
                    nom_carte_face_double = re.search(regex_carte_face_double,carte_double_face)
                    nom_carte_face_double=str(nom_carte_face_double)
                    left="name': '"
                    right="\'\">"
                    nom_carte_face_double=nom_carte_face_double[nom_carte_face_double.index(left)+len(left):nom_carte_face_double.index(right)]
                    self.liste_nom_cartes_dans_decklist.append(nom_carte_face_double)
                    self.liste_avec_tous_les_noms_encore.append(nom_carte_face_double)
                    print("La carte double a comme nom",nom_carte_face_double)
        except:
            i=0
            if(i==1):
                sys.exit()
            else:
                print("")

    def ecriture2(self,instant_adventure,regex_carte_face_double):
        deck = open("deck.txt", "r") #On lit deck.txt
        lines = deck.readlines() #On définit les lignes
        deck.close()
        print("lines:",lines)
        for line in lines: #On boucle pour chaque ligne
            if not line.isspace(): #Pour ne pas metre de lignes vides
                intermediaire=line.split(" ")
                nbcards=intermediaire[0]
                self.liste_nb_cartes_dans_decklist.append(nbcards)
                print("Il faut ",nbcards)
                extension=intermediaire[-2]
                print("La carte est dans l'extension",extension)
                self.liste_extension_dans_decklist.append(extension)
                position=intermediaire[-1]
                print("La position est",position)
                self.liste_position_extension_dans_decklist.append(position)
                nom_carte=re.search(r"^\d+ ([,\-\'\w\s]*) ",line)
                if nom_carte:
                    self.func_nom_carte(nom_carte,instant_adventure,nbcards,extension,position,regex_carte_face_double,name)
                else:
                    sys.exit("Erreur Carte existe pas")
            else:
                sys.exit()
            print("La carte a pour nom",nom_carte)

    def parcour1(self,nom_carte,nbcards,extension,position,regex_carte_face_double,name32):
        time.sleep(1)
        card = scrython.cards.Named(fuzzy=nom_carte)
        print(card)
        time.sleep(1)
        try:
            carte_double = scrython.cards.Named(fuzzy=nom_carte)
            if carte_double.card_faces():
                    print('')
            else:
                carte_double_face_tab= carte_double.card_faces()
                if len(carte_double_face_tab) >1:
                    chaine2=str(carte_double_face_tab[0])
                    print("Info sur la carte",chaine2)
                    lien_carte_face_double2 = re.search(r"'normal': '[\W\S\s\w./-cards/]* 'large'",chaine2).group() #Il faut faire des groupes car il y a des limites
                    print(lien_carte_face_double2)
                    nom_carte_face_double2=str(lien_carte_face_double2)
                    print(nom_carte_face_double2)
                    left2="normal': '"
                    right2="', 'large"
                    lien_carte_face_double2=lien_carte_face_double2[lien_carte_face_double2.index(left2)+len(left2):lien_carte_face_double2.index(right2)]
                    print(lien_carte_face_double2)
                    time.sleep(1)
                    try:
                        urllib.request.urlretrieve(lien_carte_face_double2,nom_carte+".png")
                        Image.open(nom_carte+".png")
                    except ValueError:
                        urllib.request.urlretrieve(lien_carte_face_double2,nom_carte+".jpg")
                        img2=Image.open(nom_carte+".jpg")
                        img2.save(nom_carte+".png")
                    carte_double_face = str(carte_double_face_tab[1])
                    self.liste_nb_cartes_dans_decklist.append(nbcards)
                    self.liste_extension_dans_decklist.append(extension)
                    self.liste_position_extension_dans_decklist.append(position)
                    nom_carte_face_double = re.search(regex_carte_face_double,carte_double_face)
                    nom_carte_face_double=str(nom_carte_face_double)
                    left=name32
                    right="\'\">"
                    nom_carte_face_double=nom_carte_face_double[nom_carte_face_double.index(left)+len(left):nom_carte_face_double.index(right)]
                    print("La carte double a comme nom",nom_carte_face_double)
                    chaine3=str(carte_double_face_tab[1])
                    print(chaine3)
                    lien_carte_face_double3 = re.search(r"'normal': '[\W\S\s\w./-cards/]* 'large'",chaine3).group() #Il faut faire des groupes car il y a des limites
                    print(lien_carte_face_double3)
                    nom_carte_face_double3=str(lien_carte_face_double3)
                    print(nom_carte_face_double3)
                    left3="normal': '"
                    right3="', 'large"
                    lien_carte_face_double3=lien_carte_face_double3[lien_carte_face_double3.index(left3)+len(left3):lien_carte_face_double3.index(right3)]
                    print(lien_carte_face_double3)
                    time.sleep(1)
                    try:
                        urllib.request.urlretrieve(lien_carte_face_double3,nom_carte_face_double+".png")
                        Image.open(nom_carte+".png")
                        #Il faut faire un try et essayer de l'ouvrir sinon l'enregistrer en jpg puis la transformer en png
                    except ValueError:
                        urllib.request.urlretrieve(lien_carte_face_double3,nom_carte+".jpg")
                        img3=Image.open(nom_carte+".jpg")
                        img3.save(nom_carte+".png")
        except:
            i=0
            if(i==1):
                sys.exit()
            else:
                print(card.image_uris())
                card2 = card.image_uris(0,"png") #index ?
                time.sleep(1)
                urllib.request.urlretrieve(card2,nom_carte+".png")

    def position_collage(self,image_pas_encore_coller):
        x2=0
        y2=0
        if image_pas_encore_coller == 1:
            x2=1
            y2=0
        if image_pas_encore_coller == 2:
            x2=2
            y2=0
        if image_pas_encore_coller == 3:
            x2=0
            y2=1
        if image_pas_encore_coller == 4:
            x2=1
            y2=1
        if image_pas_encore_coller == 5:
            x2=2
            y2=1
        if image_pas_encore_coller == 6:
            x2=0
            y2=2
        if image_pas_encore_coller == 7:
            x2=1
            y2=2
        if image_pas_encore_coller == 8:
            x2=2
            y2=2
        return x2,y2
    
    def collage(self,nbcards,extension,position,regex_carte_face_double,name32,total_cartes):
        nb_avant9=0
        nombre_page=0
        nb_carte_mise=0
        nom_carte=self.liste_nom_cartes_dans_decklist.pop(0)
        print("Je prends la carte",nom_carte)
        try:
            self.parcour1(nom_carte,nbcards,extension,position,regex_carte_face_double,name32)
        except Exception:
            print('not found')
            print("Je n'ai pas trouvé la carte",nom_carte)
            #si je comprends bien les cartes doubles non pas de image_uris mais que card_faces
            #continue if file not found
        print("T'as fini youpi")
        nb_carte_a_coller=int(self.liste_nb_cartes_dans_decklist.pop(0))
        card3=Image.open(nom_carte+".png")
        buffer = io.BytesIO()
        card3.save(buffer, format='PNG')
        card3.save(nom_carte+".png")
        if(".png" in nom_carte)==0:
            nom_carte=nom_carte.replace(".jpg",".png")
            card3=nom_carte+".png"
        # You probably want
        for nb in range(nb_carte_a_coller):
            self.liste_nom_a_coller.append(card3)
            nb_avant9=nb_avant9+1
            nb_carte_mise=nb_carte_mise+1
            print("Jai déjà coller",nb)
            print("Il faut coller",nb_carte_a_coller)
            print("La carte à coller s'appelle",card3)
            if(total_cartes==nb_carte_mise and nb_carte_mise%9==0):
                self.liste_nom_a_coller.append("../images/imageVide.png")
                nb_avant9=nb_avant9+1
                print("Il reste avant la fin pour image vide",nb_avant9)
                nb_carte_mise=nb_carte_mise+1
        #C'est là qu'il faut faire des trucs spéciaux pour la dernière page qui n'apparait pas
        if nb_avant9==9: #On ne peut coller que jusqu'à neuf cartes sur une feuille
            nom_page="page %d .png" % nombre_page
            print("Le nom de la page est",nom_page)
            self.creer_image_page2(self.liste_nom_a_coller,nom_page)
            nombre_page=nombre_page+1
            nb_avant9=0
            del self.liste_nom_a_coller[:] #On réinitialise la liste
        #Il ne faut pas oublier de coller ce qui reste car les decks ne sont pas modulo 9
        #On n'arrive pas à entrer dans le if suivant
        print("Nombre carteMise",nb_carte_mise)
        #nbCarteMise = 64
        #Faudra faire un sum() de ce tableau
        print(total_cartes)
        if nb_carte_mise==total_cartes:#La condition
            taille_restante_a_parcourir=len(self.liste_nom_a_coller)
            nom_page="page %d .png" % nombre_page
            image_pas_encore_coller=0
            x2=0
            y2=0
            longueur2=745
            hauteur2=1040
            marge2= int(longueur2 /  10)
            boxl2=longueur2+marge2
            boxh2=hauteur2+marge2
            size2=((boxl2*3)-marge2,boxh2*3-marge2)
            page2 = Image.new("RGB",size2,(255,255,255))
            chaine_proxy2="Proxy not for Sale"
            for reste_a_parcourir in range (taille_restante_a_parcourir):
                print(reste_a_parcourir)
                print("Taille restante à parcourir",taille_restante_a_parcourir)
                image_spec=self.liste_nom_a_coller.pop(0)
                print("Image prise dans la liste",image_spec)
                image_spec=Image.open(image_spec)
                print("Image réelle prise",image_spec)
                each_image_draw2 = ImageDraw.Draw(image_spec)
                each_image_draw2.text((marge2+200, hauteur2-marge2+40),chaine_proxy2,(255,255,255),font=self.police_proxy)
                page2.paste(image_spec,(boxl2*x2,boxh2*y2))
                image_pas_encore_coller=image_pas_encore_coller+1
                x2,y2=self.position_collage(image_pas_encore_coller)
            draw2 = ImageDraw.Draw(page2)
            marge_reelle=6.27/4
            chaine="À imprimer en %d cm * %d cm"  % (int(6.27*3+marge_reelle),int(8.67*3+marge_reelle))
            draw2.text((boxl2+marge2, hauteur2),chaine,(0,0,0),font=self.police)
            page2.save(nom_page)

    def func_import(self):
        name32="name': '"
        instant_adventure="Instant — Adventure"
        deck_txt='deck.txt'
        regex_carte_face_double=r"'name': '[\w\s]*'"
        print(os.listdir()) #On est dans image
        os.chdir("../deck/") #On va dans deck
        import_deck_list=""
        import_deck_list = self.box.get() #On prend ce qu'on a mis dans le champ textuel
        os.sync()
        if not os.path.isfile(deck_txt):
            f = open(deck_txt,'w')
            f.write(str(import_deck_list))
            f.close()
        else:
            os.remove(deck_txt)
            f = open(deck_txt,'w')
            f.write(str(import_deck_list))
            f.close()
        os.sync()
        deck2 = open(deck_txt, "r+") #On lit deck.txt
        lines = deck2.readlines() #On définit les lignes
        deck2.close()
        print("Voici le résultat",lines)
        intermediaire=""
        nbcards=""
        extension=""
        position=""
        nom_carte=""
        line=""
        for line in lines:
            if not line.isspace(): #Pour ne pas metre de lignes vides
                intermediaire=line.split(" ")
                nbcards=intermediaire[0]
                print("Il faut",nbcards)
                extension=intermediaire[-2]
                print("La carte est dans l'extension",extension)
                position=intermediaire[-1]
                print("La position est",position)
                nom_carte=re.search(r"^\d+ ([,\-\'\w\s]*) ",line)
                nom_carte=nom_carte.group(1) #On a bien les noms de cartes
                nom_carte=self.ecriture1(nom_carte,regex_carte_face_double,nbcards,extension,position,name32) #Pour réduire la complexité
                #On intègre nos changements
        deck2.close() #On ferme le deck
        deck = open(deck_txt, "r") #On lit deck.txt
        lines = deck.readlines() #On définit les lignes
        deck.close()
        print("J'ai lu les lignes du fichier",lines)
        self.ecriture2(instant_adventure,regex_carte_face_double)
        parcour=len(self.liste_nom_cartes_dans_decklist)
        print(self.liste_nom_cartes_dans_decklist)
        print(self.liste_nb_cartes_dans_decklist)
        total_cartes=self.somme()
        print("IL y a %d de cartes dans la liste",total_cartes)
        for _ in range(parcour):
            self.collage(nbcards,extension,position,regex_carte_face_double,name32,total_cartes)
        deck.close()
        print("On a tous le deck maintenant")
        #https://stackoverflow.com/questions/1548704/delete-multiple-files-matching-a-pattern


    def faire_apparaitre_proxy(self):
        top=Toplevel(self)
        label=Label(top,text="Ex:192.168.0.13:3128")
        label.pack()
        entree2 = Entry(top)#demande la valeur
        entree2.pack() # integration du widget a la fenetre principale
        ok = Button(top, text = "ok", command = top.destroy)
        ok.pack()
        #create the object, assign it to a variable
        chaine_proxy = entree2.get()
        proxy = urllib.request.ProxyHandler({'http': chaine_proxy})
        # construct a new opener using your proxy settings
        opener = urllib.request.build_opener(proxy)
        # install the openen on the module-level
        urllib.request.install_opener(opener)


app = Magic()
app.mainloop()
