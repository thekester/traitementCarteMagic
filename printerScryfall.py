#!/usr/bin/env python3
# -*- coding: utf-8 -*-.
import copy
import os
import time
import tkinter
import scrython
import sys
import tkinter as tk
import urllib.request
import PIL
import json
import tempfile
from tkinter import Tk
from tkinter import ttk
from tkinter import Entry
from tkinter import Button
from tkinter import Label
from tkinter import Toplevel
from tkinter import Scrollbar
from PIL import Image

from tkinter.filedialog import askopenfilename
from tkinter.messagebox import askyesno

#https://forums.commentcamarche.net/forum/affich-3053256-python-limiter-un-entry

""" https://vonkrafft.fr/console/redimensionner-images-python/"""

#Le code d'avant doit s'éxécuter sans proxy
#Le code d 'après s'éxécute avec un proxy si vous en avez un et normalement sinon

#pip install cmake

#pip3 install opencv-python


# make a request

tableauAvecToutesLesLignes=[]
listeNbCartesDansDecklist=[]
listePositionExtensionDansDecklist=[]


#print(os.listdir())
os.chdir("images")


new_size = (226,315)

img = Image.open('Anax, Hardened in the Forge.png')
img = img.resize(new_size, PIL.Image.ANTIALIAS)

img.save('test1.png', optimize=True, quality=100 , dpi=(300,300))

def creer_doc():
    print("Hello")

def get_magic_card_image(searchterm):
    #ne pas oublier les time.sleep afin de ne pas surcharger scryfall
    try:
        time.sleep(1)
        card = scrython.cards.Named(fuzzy=searchterm)
        time.sleep(1)
        print(card.image_uris())
        format_var = liste_combo_format.get()
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

def get_format(event):
    format_var = liste_combo_format.get()
    return format_var

def get_nb_exemplaires(event):
	# Obtenir l'élément sélectionné
    select = liste_combo.get()
    print("Vous avez sélectionné : '", select,"'")

def saisie():
    searchterm = entree.get() #On lit la carte
    if(searchterm == ""):
        sys.exit("La carte qui a aucun nom n'existe pas") #Il faudra voir pour afficher un message d'erruer en rouge
    else:
        #GetMagicCardImage(searchterm).show()
        image_souhait=get_magic_card_image(searchterm)
        liste_carte_avec_nb_exemplaires.append(liste_combo.get())
        liste_carte_avec_nb_exemplaires.append(image_souhait)
    return image_souhait #recupére la valeur saisie


def funcImport():
    print(os.listdir()) #On est dans image
    os.chdir("../deck/")
    print(os.listdir()) #On est dans deck
    importDeckList = box.get()
    with open("deck.txt", "w") as deck:
	    deck.write(importDeckList) #On met la decklist au format mtga dans le deck.txt
    deck = open("deck.txt", "r")
    lines = deck.readlines()
    
    for line in lines:
        if not line.isspace(): #Pour ne pas metre de lignes vides
            tableauAvecToutesLesLignes.append(line.split(" "))
    deck.close() #On ferme le fichier
    #Maintenant on a tout ce qu'il nous faut
    print(tableauAvecToutesLesLignes)
    """
  [['4', 'Fabled', 'Passage', '(M21)', '246\n'], ['4', 'Island', '(M21)', '265\n'], ['4', 'Zagoth', 'Triome', '(IKO)', '259\n'], ['4', 'Overgrown', 'Tomb', '(GRN)', '253\n'], ['4', 'Breeding', 'Pool', '(RNA)', '246\n'], ['4', 'Watery', 'Grave', '(GRN)', '259\n'], ['2', 'Forest', '(M21)', '274\n'], ['1', 'Castle', 'Vantress', '(ELD)', '242\n'], ['1', 'Castle', 'Locthwain', '(ELD)', '241\n'], ['1', 'Swamp', '(M21)', '268\n'], ['4', 'Narset,', 'Parter', 'of', 'Veils', '(WAR)', '61\n'], ['2', 'Nissa,', 'Who', 'Shakes', 'the', 'World', '(WAR)', '169\n'], ['4', 'Shark', 'Typhoon', '(IKO)', '67\n'], ['4', 'Agonizing', 'Remorse', '(THB)', '83\n'], ['1', 'Cultivate', '(M21)', '177\n'], ['1', 'Casualties', 'of', 'War', '(WAR)', '187\n'], ['3', 'Aether', 'Gust', '(M20)', '42\n'], ['2', 'Eliminate', '(M21)', '97\n'], ['2', 'Mystical', 'Dispute', '(ELD)', '58\n'], ['1', 'Negate', '(RIX)', '44\n'], ['4', 'Uro,', 'Titan', 'of', "Nature's", 'Wrath', '(THB)', '229\n'], ['2', 'Hydroid', 'Krasis', '(RNA)', '183\n'], ['1', 'Brazen', 'Borrower', '(ELD)', '39\n'], ['3', 'Heartless', 'Act', '(IKO)', '91\n'], ['3', 'Extinction', 'Event', '(IKO)', '88\n'], ['2', 'Cry', 'of', 'the', 'Carnarium', '(RNA)', '70\n'], ['2', 'Elder', 'Gargaroth', '(M21)', '179\n'], ['1', 'Lochmere', 'Serpent', '(ELD)', '195\n'], ['2', 'Eliminate', '(M21)', '97\n'], ['2', 'Negate', '(RIX)', '44']]
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
        tableauAvecToutesLesLignes.pop([0][0])
        #listePositionExtensionDansDecklist.append(tableauAvecToutesLesLignes[i][-1])
        indiceASupprimer=len(tableauAvecToutesLesLignes[0])
        print("La taille de la ligne est",len(tableauAvecToutesLesLignes[0]))
        #tableauAvecToutesLesLignes.pop([i][1])
    print(tableauAvecToutesLesLignes)
    

    
    
    
    
    
    
    
    
    

    """
    with open('deck.txt') as file, open('deck.json', 'w') as deck_file:
        items = []
        for line in file:
            if not line.strip():
                continue
            d = {}
            data = line.split('|')
            for val in data:
                key, sep, value = val.partition(':')
             d[key.strip()] = value.strip()
            items.append(d)
        json.dump(items, deck_file)
    print("")
    """
    
def faire_apparaitre_proxy():
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
liste_carte_avec_nb_exemplaires=[]
labelVide = tk.Label(fen1, text = "                                ")
labelVide.grid(row=0,column=0)
label_carte = tk.Label(fen1, text = "Tapez le nom de la carte en dessous")
label_carte.grid(row=0,column=1)
entree = Entry(fen1)#demande la valeur
entree.grid(row=1,column=1) # integration du widget a la fenetre principale
label_choix_format_image=tk.Label(fen1, text = "Choix du format de l'image")
label_choix_format_image.grid(row=2,column=1)
liste_formats=["art_crop","border_crop","large","normal","png","small"]
liste_combo_format = ttk.Combobox(fen1, values=liste_formats)
liste_combo_format.grid(row=3,column=1)
liste_combo_format.bind("<<ComboboxSelected>>", get_format)


label_choix_nb_exemplaire = tk.Label(fen1, text = "Nb Exemplaires")
label_choix_nb_exemplaire.grid(row=4,column=1)



liste_nb_exemplaire=("1", "2","3","4","5","6","7") #On va jusqu'à sept à cause des sept nains mais avec les pétitionnaires tenaces faut voir 
liste_combo = ttk.Combobox(fen1, values=liste_nb_exemplaire)
liste_combo.current(0)
liste_combo.grid(row=5,column=1)

liste_combo.bind("<<ComboboxSelected>>", get_nb_exemplaires)
 
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

scroll_y = tk.Scrollbar(box, orient="vertical")
scroll_y.pack(side="right", expand=True, fill="y")


quitter = Button(fen1, text = "quitter", command = fen1.destroy)
quitter.grid(row=10,column=1)

proxy=Button(fen1, text="proxy", command=faire_apparaitre_proxy)
proxy.grid(row=11,column=1)

print (saisie)
fen1.mainloop()
