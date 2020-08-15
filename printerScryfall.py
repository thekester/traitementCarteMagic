#!/usr/bin/env python3
# -*- coding: utf-8 -*-.

import os
import time
import scrython
import sys
import tkinter as tk
import urllib.request
from tkinter import Tk
from tkinter import ttk
from tkinter import Entry
from tkinter import Button
from tkinter import Label
from tkinter import Toplevel

from tkinter.filedialog import askopenfilename
from tkinter.messagebox import askyesno


"""
rep=tk.messagebox.askyesno(title="Proxy", message="Avez vous un proxy?")

if (rep==1):
    fen2 = Tk()
    fen2.title("Proxy")
    entree2 = Entry(fen2)#demande la valeur
    ok = Button(fen2, text = "ok", command = fen2.destroy)
    ok.pack()
    entree2.pack() # integration du widget a la fenetre principale
    label=Label(fen2,text="Ex:http://192.168.0.3:3128")
    label.pack()
    fen2.mainloop()
    #create the object, assign it to a variable
    chaineProxy = entree2.get()
    #proxy = urllib.request.ProxyHandler({'http': '192.168.0.3:3128'})
    proxy = urllib.request.ProxyHandler({chaineProxy})
    # construct a new opener using your proxy settings
    opener = urllib.request.build_opener(proxy)
    # install the openen on the module-level
    urllib.request.install_opener(opener)
"""

#Le code d'avant doit s'éxécuter sans proxy
#Le code d 'après s'éxécute avec un proxy si vous en avez un et normalement sinon


# make a request

#print(os.listdir())
os.chdir("traitementCarteMagic/images")


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
        imageSouhait=GetMagicCardImage(searchterm)
        listeCarteAvecNbExemplaires.append(listeCombo.get())
        listeCarteAvecNbExemplaires.append(imageSouhait)
    return imageSouhait #recupére la valeur saisie

def faireApparaitreProxy():
    top=Toplevel(fen1)
    label=Label(top,text="Ex:192.168.0.3:3128")
    label.pack()
    entree2 = Entry(top)#demande la valeur
    entree2.pack() # integration du widget a la fenetre principale
    ok = Button(top, text = "ok", command = top.destroy)
    ok.pack()
    #create the object, assign it to a variable
    chaineProxy = entree2.get()
    #proxy = urllib.request.ProxyHandler({'http': '192.168.0.3:3128'})
    proxy = urllib.request.ProxyHandler({'http': chaineProxy})
    # construct a new opener using your proxy settings
    opener = urllib.request.build_opener(proxy)
    # install the openen on the module-level
    urllib.request.install_opener(opener)


fen1 = Tk()
fen1.title("Magic pour les non programmeurs")
fen1.geometry("500x250")
listeCarteAvecNbExemplaires=[]
labelCarte = tk.Label(fen1, text = "Tapez le nom de la carte en dessous")
labelCarte.pack()
entree = Entry(fen1)#demande la valeur
entree.pack() # integration du widget a la fenetre principale
labelChoixFormatImage=tk.Label(fen1, text = "Choix du format de l'image")
labelChoixFormatImage.pack()
listeFormats=["art_crop","border_crop","large","normal","png","small"]
listeComboFormat = ttk.Combobox(fen1, values=listeFormats)
listeComboFormat.pack()
listeComboFormat.bind("<<ComboboxSelected>>", getFormat)


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

proxy=Button(fen1, text="proxy", command=faireApparaitreProxy)
proxy.pack()

print (saisie)
fen1.mainloop()