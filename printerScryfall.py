#!/usr/bin/env python3
# -*- coding: utf-8 -*-.


import scrython
import time
import urllib.request
import os
import sys
import tkinter as tk
from tkinter import Tk
from tkinter import Entry
from tkinter import Button
#from tkinter import *    ## notice lowercase 't' in tkinter here
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror
from tkinter import ttk




#Le code d'avant doit s'éxécuter sans proxy
#Le code d 'après s'éxécute avec un proxy si vous en avez un et normalement sinon

#create the object, assign it to a variable
proxy = urllib.request.ProxyHandler({'http': '192.168.0.3:3128'})
# construct a new opener using your proxy settings
opener = urllib.request.build_opener(proxy)
# install the openen on the module-level
urllib.request.install_opener(opener)
# make a request

print(os.listdir())
os.chdir("traitementCarteMagic")


def creerDoc():
    print("Hello")

def GetMagicCardImage(searchterm):
    #ne pas oublier les time.sleep afin de ne pas surcharger scryfall
    #print("Hello")
    #print(os.path)
    try:
        time.sleep(1)
        card = scrython.cards.Named(fuzzy=searchterm)
        time.sleep(1)
        card2 = card.image_uris(0,"png") #index ?
        time.sleep(1)
        urllib.request.urlretrieve(card2,searchterm+".png")
        time.sleep(1)
    except Exception:
        print('not found')
        searchterm=""
        #continue if file not found
    print("T'as fini youpi")
    return searchterm



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
        imageSouhait=GetMagicCardImage(searchterm)
        listeCarteAvecNbExemplaires.append(listeCombo.get())
        listeCarteAvecNbExemplaires.append(imageSouhait)
    return imageSouhait #recupére la valeur saisie

fen1 = Tk()
fen1.title("Magic pour les non programmeurs")
fen1.geometry("500x250")
listeCarteAvecNbExemplaires=[]
entree = Entry(fen1)#demande la valeur
entree.pack() # integration du widget a la fenetre principale
labelChoixNbExemplaire = tk.Label(fen1, text = "Nb Exemplaires")
labelChoixNbExemplaire.pack()

listeNbExemplaire=[1, 2,3,4,5,6,7] #On va jusqu'à sept à cause des sept nains mais avec les pétitionnaires tenaces faut voir 

listeCombo = ttk.Combobox(fen1, values=listeNbExemplaire)
listeCombo.current(0)
listeCombo.pack()

listeCombo.bind("<<ComboboxSelected>>", getNbExemplaires)
 
valider = Button(fen1, text = 'valider', command = saisie)
valider.pack()

#creerDoc = Button(fen1, text = 'Créer le document', command = creerDoc)
#creerDoc.pack()

quitter = Button(fen1, text = "quitter", command = fen1.destroy)
quitter.pack()

print (saisie)
fen1.mainloop()