#!/usr/bin/env python3
# -*- coding: utf-8 -*-.
import os
import time
import tkinter
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

#print (re.search(r"^\d+ ([\w\s]*) ","4 Fabled Passage (M21) 246").group(1)+"fin")
#Fabled Passagefin

#https://www.magic-ville.com/fr/decks/showdeck?ref=412707&mt8=1

#https://forums.commentcamarche.net/forum/affich-3053256-python-limiter-un-entry

# https://vonkrafft.fr/console/redimensionner-images-python/ 

#Le code d'avant doit s'éxécuter sans proxy
#Le code d 'après s'éxécute avec un proxy si vous en avez un et normalement sinon

# make a request

police = ImageFont.truetype("font/TimesNewRoman.ttf", 50)
policeProxy = ImageFont.truetype("font/TimesNewRoman.ttf", 25)

listeNbCartesDansDecklist=[]
listeNomCartesDansDecklist=[]
listePositionExtensionDansDecklist=[]
listeExtensionDansDecklist=[]
listeNomAColler=[]

#print(os.listdir())
os.chdir("images")


new_size = (226,315)

img = Image.open('Anax, Hardened in the Forge.png')
img = img.resize(new_size, PIL.Image.ANTIALIAS)

img.save('test1.png', optimize=True, quality=100 , dpi=(300,300))

def creerImagePage2(listImage,nomPage):
    x=0
    y=0
    longueur=745
    hauteur=1040
    marge= int(longueur /  10)
    boxl=longueur+marge
    boxh=hauteur+marge
    size=((boxl*3)-marge,boxh*3-marge)
    page = Image.new("RGB",size,(255,255,255))
    for y in range(3):
        for x in range(3):
            eachImageDraw = ImageDraw.Draw(listImage[3*y+x])
            chaineProxy="Proxy not for Sale"
            eachImageDraw.text((marge+200, hauteur-marge+40),chaineProxy,(255,255,255),font=policeProxy)
            page.paste(listImage[3*y+x],(boxl*x,boxh*y))
    draw = ImageDraw.Draw(page)
    margeReelle=6.27/4
    chaine="À imprimer en %d cm * %d cm"  % (int(6.27*3+margeReelle),int(8.67*3+margeReelle))
    draw.text((boxl+marge, hauteur),chaine,(0,0,0),font=police)
    page.save(nomPage)

def creerDoc():
    print("Hello")

def getMagicCardImage(searchterm):
    #ne pas oublier les time.sleep afin de ne pas surcharger scryfall
    try:
        time.sleep(1)
        card = scrython.cards.Named(fuzzy=searchterm)
        time.sleep(1)
        print(card.image_uris())
        formatVar = listeComboFormat.get()
        print("Format choisi"+formatVar)
        card2 = card.image_uris(0,formatVar) #index ?
        time.sleep(1)
        if(formatVar=="png"):
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

def getFormat(event):
    formatVar = listeComboFormat.get()
    return formatVar

def getNbExemplaires(event):
	# Obtenir l'élément sélectionné
    select = listeCombo.get()
    print("Vous avez sélectionné : '", select,"'")

def saisie():
    searchterm = entree.get() #On lit la carte
    if(searchterm == ""):
        sys.exit("La carte qui a aucun nom n'existe pas") #Il faudra voir pour afficher un message d'erruer en rouge
    else:
        #GetMagicCardImage(searchterm).show()
        imageSouhait=getMagicCardImage(searchterm)
        listeCarteAvecNbExemplaires.append(listeCombo.get())
        listeCarteAvecNbExemplaires.append(imageSouhait)
    return imageSouhait #recupére la valeur saisie


def funcImport():
    print(os.listdir()) #On est dans image
    os.chdir("../deck/")
    print(os.listdir()) #On est dans deck
    importDeckList = box.get()
    with open("deck.txt", "w") as deck:
	    deck.write(importDeckList) #On met la decklist au format mtga dans le deck.txt
    deck = open("deck.txt", "r")
    lines = deck.readlines()
    intermediaire=""
    nbcards=""
    extension=""
    position=""
    nomCarte=""
    for line in lines:
        if not line.isspace(): #Pour ne pas metre de lignes vides
            intermediaire=line.split(" ")
            nbcards=intermediaire[0]
            listeNbCartesDansDecklist.append(nbcards)
            print("Il faut",nbcards)
            extension=intermediaire[-2]
            print("La carte est dans l'extension",extension)
            listeExtensionDansDecklist.append(extension)
            position=intermediaire[-1]
            print("La position est",position)
            listePositionExtensionDansDecklist.append(position)
            nomCarte=re.search(r"^\d+ ([,\w\s]*) ",line)
            #nomCarte=re.match(r"[0-9]+ (.*)\(",line)
            #nomCarte=re.match(r"\d+ (\b*)\(",line)
            if nomCarte:
                nomCarte=nomCarte.group(1)
                listeNomCartesDansDecklist.append(nomCarte)
            else:
                sys.exit("Erreur Carte existe pas")
        else:
            print("")
        print("La carte a pour nom",nomCarte)
        #tableauAvecToutesLesLignes.append(line.split(" "))
    deck.close() #On ferme le fichier
    parcour=len(listeNomCartesDansDecklist)
    nbAvant9=0
    nombrePage=0
    for k in range(parcour):
        nomCarte=listeNomCartesDansDecklist.pop(0)
        try:
            time.sleep(1)
            card = scrython.cards.Named(fuzzy=nomCarte)
            time.sleep(1)
            print(card.image_uris())
            card2 = card.image_uris(0,"png") #index ?
            time.sleep(1)
            urllib.request.urlretrieve(card2,nomCarte+".png")
        except Exception:
            print('not found')
            searchterm=""
            #continue if file not found
        print("T'as fini youpi")
        nbCarteAColler=int(listeNbCartesDansDecklist.pop(0))
        card3=Image.open(nomCarte+".png")
        for nb in range(nbCarteAColler):
            listeNomAColler.append(card3)
            nbAvant9=nbAvant9+1
            if nbAvant9==9: #On ne peut coller que jusqu'à neuf cartes surune feuille
                nomPage="page %d .png" % nombrePage
                print("Le nom de la page est",nomPage)
                creerImagePage2(listeNomAColler,nomPage)
                nombrePage=nombrePage+1
                nbAvant9=0
                del listeNomAColler[:] #On réinitialise la liste

    #getMagicCardImage(searchterm)
    #Maintenant on a tout ce qu'il nous faut
    #print(tableauAvecToutesLesLignes)

    """
[['4', 'Fabled', 'Passage', '(M21)', '246\n'], ['4', 'Island', '(M21)', '265\n'], ['4', 'Zagoth', 'Triome', '(IKO)', '259\n'], ['4', 'Overgrown', 'Tomb', '(GRN)', '253\n'], ['4', 'Breeding', 'Pool', '(RNA)', '246\n'], ['4', 'Watery', 'Grave', '(GRN)', '259\n'], ['2', 'Forest', '(M21)', '274\n'], ['1', 'Castle', 'Vantress', '(ELD)', '242\n'], ['1', 'Castle', 'Locthwain', '(ELD)', '241\n'], ['1', 'Swamp', '(M21)', '268\n'], ['4', 'Narset,', 'Parter', 'of', 'Veils', '(WAR)', '61\n'], ['2', 'Nissa,', 'Who', 'Shakes', 'the', 'World', '(WAR)', '169\n'], ['4', 'Shark', 'Typhoon', '(IKO)', '67\n'], ['4', 'Agonizing', 'Remorse', '(THB)', '83\n'], ['1', 'Cultivate', '(M21)', '177\n'], ['1', 'Casualties', 'of', 'War', '(WAR)', '187\n'], ['3', 'Aether', 'Gust', '(M20)', '42\n'], ['2', 'Eliminate', '(M21)', '97\n'], ['2', 'Mystical', 'Dispute', '(ELD)', '58\n'], ['1', 'Negate', '(RIX)', '44\n'], ['4', 'Uro,', 'Titan', 'of', "Nature's", 'Wrath', '(THB)', '229\n'], ['2', 'Hydroid', 'Krasis', '(RNA)', '183\n'], ['1', 'Brazen', 'Borrower', '(ELD)', '39\n'], ['3', 'Heartless', 'Act', '(IKO)', '91\n'], ['3', 'Extinction', 'Event', '(IKO)', '88\n'], ['2', 'Cry', 'of', 'the', 'Carnarium', '(RNA)', '70\n'], ['2', 'Elder', 'Gargaroth', '(M21)', '179\n'], ['1', 'Lochmere', 'Serpent', '(ELD)', '195\n'], ['2', 'Eliminate', '(M21)', '97\n'], ['2', 'Negate', '(RIX)', '44']]
"""
"""
    print(tableauAvecToutesLesLignes[1]) #['4', 'Island', '(M21)', '265\n']
    print(tableauAvecToutesLesLignes[1][1]) #Island
    print(len(tableauAvecToutesLesLignes)) #30
    tableauAvecToutesLesLignes.append("")
    tailleTableau=len(tableauAvecToutesLesLignes)
    print(tableauAvecToutesLesLignes[0][0])
    for i in range(tailleTableau-1):
        print("On est à la ligne",i)
        print(tableauAvecToutesLesLignes[0])
        print("Dernier élément",tableauAvecToutesLesLignes[0][-1])
        listePositionExtensionDansDecklist.append(tableauAvecToutesLesLignes[0][-1])
        tableauAvecToutesLesLignes2.append(tableauAvecToutesLesLignes[0])
        tableauAvecToutesLesLignes.pop([0][-1])
        #listePositionExtensionDansDecklist.append(tableauAvecToutesLesLignes[i][-1])
        indiceASupprimer=len(tableauAvecToutesLesLignes[0])
        print("La taille de la ligne est",len(tableauAvecToutesLesLignes[0]))
        #tableauAvecToutesLesLignes.pop([i][1])
    print(tableauAvecToutesLesLignes) #ON obtient un tableau vide
    print(listePositionExtensionDansDecklist)
    print(tableauAvecToutesLesLignes2)

"""

def faireApparaitreProxy():
    top=Toplevel(fen1)
    label=Label(top,text="Ex:192.168.0.3:3128")
    label.pack()
    entree2 = Entry(top)#demande la valeur
    entree2.pack() # integration du widget a la fenetre principale
    ok = Button(top, text = "ok", command = top.destroy)
    ok.pack()
    #create the object, assign it to a variable
    chaine_proxy = entree2.get()
    #proxy = urllib.request.ProxyHandler({'http': '192.168.0.3:3128'})
    proxy = urllib.request.ProxyHandler({'http': chaine_proxy})
    # construct a new opener using your proxy settings
    opener = urllib.request.build_opener(proxy)
    # install the openen on the module-level
    urllib.request.install_opener(opener)

"""
class MyClass:
    def method(self, arg):
        print(arg)

my_object = MyClass()
my_other_object.method("foo")  
"""
"""
class MyClass:
    def defilGest(L):
        
        op, deCombien = L[0], L[1]
        if op == 'scroll':
            units = L[2]
            box.xview_scroll(deCombien, units)
        elif op == 'moveto':
            box.xview_moveto(deCombien)

"""









fen1 = Tk()
spam = fen1.clipboard_get()
fen1.title("Magic pour les non programmeurs")
fen1.geometry("500x300")
listeCarteAvecNbExemplaires=[]
labelVide = tk.Label(fen1, text = "                                ")
labelVide.grid(row=0,column=0)
labelCarte = tk.Label(fen1, text = "Tapez le nom de la carte en dessous")
labelCarte.grid(row=0,column=1)
entree = Entry(fen1)#demande la valeur
entree.grid(row=1,column=1) # integration du widget a la fenetre principale
labelChoixFormatImage=tk.Label(fen1, text = "Choix du format de l'image")
labelChoixFormatImage.grid(row=2,column=1)
listeFormats=["art_crop","border_crop","large","normal","png","small"]
listeComboFormat = ttk.Combobox(fen1, values=listeFormats)
listeComboFormat.grid(row=3,column=1)
listeComboFormat.bind("<<ComboboxSelected>>", getFormat)


labelChoixNbExemplaire = tk.Label(fen1, text = "Nb Exemplaires")
labelChoixNbExemplaire.grid(row=4,column=1)



listeNbExemplaire=("1", "2","3","4","5","6","7") #On va jusqu'à sept à cause des sept nains mais avec les pétitionnaires tenaces faut voir 
listeCombo = ttk.Combobox(fen1, values=listeNbExemplaire)
listeCombo.current(0)
listeCombo.grid(row=5,column=1)

listeCombo.bind("<<ComboboxSelected>>", getNbExemplaires)
 
valider = Button(fen1, text = 'valider', command = saisie)
valider.grid(row=6,column=1)

#creerDoc = Button(fen1, text = 'Créer le document', command = creerDoc)
#creerDoc.pack()

buttonImport = Button(fen1, text = 'Import', command = funcImport)
buttonImport.grid(row=7,column=1)


deckList = tk.StringVar()
deckList.set(spam)

box = Entry(fen1, textvariable = deckList)
box.grid(row=8, column=1 ,   sticky='ew')

scrollY = tk.Scrollbar(box, orient="vertical")
scrollY.pack(side="right", expand=True, fill="y")


quitter = Button(fen1, text = "quitter", command = fen1.destroy)
quitter.grid(row=10,column=1)

proxy=Button(fen1, text="proxy", command=faireApparaitreProxy)
proxy.grid(row=11,column=1)

print (saisie)
fen1.mainloop()
