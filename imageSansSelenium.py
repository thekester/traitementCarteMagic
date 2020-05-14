#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Programme d'affichage d'une image par la librairie PIL
# Dominique Lefebvre pour TangenteX.com
# 5 janvier 2016
#

#https://gatherer.wizards.com/Pages/Search/Default.aspx?name=+[Cavali%c3%a8re]+[meurtri%c3%a8re]

""" https://github.com/mozilla/geckodriver/releases """
""" https://pypi.org/project/selenium/ """

# importation des librairies
import io,sys

if sys.version_info[0] == 3:
    # for Python3
    from tkinter import *   ## notice lowercase 't' in tkinter here
    from tkinter.filedialog import askopenfilename
    from tkinter.messagebox import showerror
else:
    # for Python2
    from Tkinter import *   ## notice capitalized T in Tkinterfrom PIL import ImageTk, Image
#from tkinter import filedialog
import glob, os
from fileinput import filename
from PIL import Image
import csv
import requests
#https://urllib3.readthedocs.io/en/latest/advanced-usage.html#ssl-warnings
from io import BytesIO 
#import urllib.parse as urlParse
#import urllib.request
#import image
"""https://stackoverflow.com/questions/11914472/stringio-in-python3"""
from io import StringIO ## for Python 3

"""https://stackoverflow.com/questions/11783875/importerror-no-module-named-bs4-beautifulsoup"""
from bs4 import BeautifulSoup

from io import BytesIO
from PIL import Image, ImageFile
#import numpy
#from rawkit import raw

def GetMagicCardImage(searchterm):


    #https://gatherer.wizards.com/Pages/Search/Default.aspx?name=+[Cavali%c3%a8re]+[meurtri%c3%a8re]
    parseWords=searchterm.split(' ')
    stringATransforme = "["
    for i in range(len(parseWords)):
        #stringATransforme += requests.utils.quote(parseWords[i]) 
        stringATransforme += parseWords[i] 
        if (i < len(parseWords)-1):
            stringATransforme += ']+['
        else:
            stringATransforme += ']'
    #stringATransforme = searchterm
    #stringATransforme = stringATransforme.replace(' ',']+[')
    #stringATransforme="["+stringATransforme+"]"
    #link = "https://gatherer.wizards.com/Pages/Search/Default.aspx?name=+" + requests.utils.quote(stringATransforme)
    link = "https://gatherer.wizards.com/Pages/Search/Default.aspx?name=+" + stringATransforme
    print("Le lien est :",link)
    
    #requete = requests.get(link)
    #https://www.developpez.net/forums/d1926656/autres-langages/python/reseau-web/erreur-requete-site-https-certificat/
    requete = requests.get(link,verify=True , params=link, auth=('user', 'pass'))
    #https://urllib3.readthedocs.io/en/latest/advanced-usage.html#ssl-warnings
    
    #https://stackoverflow.com/questions/27981545/suppress-insecurerequestwarning-unverified-https-request-is-being-made-in-pytho
    
    """
    Piste : Changer le user agent
    
    """
    
    page = requete.content
    soup = BeautifulSoup(page, 'html.parser')
    linkImageSrc = None
    for tag in soup.find_all("img"):
        print(tag['src'])
        if("Handlers/Image.ashx?multiverseid=" in tag['src'] ):
            linkImageSrc = tag['src']
            break
    if (linkImageSrc == None):
        print ("Image source correspondante à la recherche non trouvée")
        sys.exit (-2)
        
    linkImage = "https://gatherer.wizards.com/"+ linkImageSrc
    linkImage = linkImage.replace('../../', '')
    #print("Le lien de l'image est :",linkImage)

    imageResponse=requests.get(linkImage, stream=True)
    if imageResponse.status_code == 200:
        image=Image.open(io.BytesIO(imageResponse.content))
        
    else:
        print ("Erreur réseau pendant la récupération de l'image")

    return image

GetMagicCardImage("Cavalière meurtrière").show()
imageLegendaire = GetMagicCardImage("Cavalière meurtrière")
"""Il ne reste plus qu'à prendre l'image et la mettre dans le dossier images"""

imageLegendaire = imageLegendaire.save("images/resultatFonction.png") 




""" Le code qui transforme les images une fois mis dans le dossier images pour les mettre dans images.png """


#http://code.activestate.com/recipes/412982-use-pil-to-make-a-contact-sheet-montage-of-images/

def make_contact_sheet(fnames,v1,v2,v3,padding):
    
    (ncols,nrows)=v1
    (photow,photoh)=v2
    (marl,mart,marr,marb)=v3
    
    """\
    Make a contact sheet from a group of filenames:

    fnames       A list of names of the image files
    
    ncols        Number of columns in the contact sheet
    nrows        Number of rows in the contact sheet
    photow       The width of the photo thumbs in pixels
    photoh       The height of the photo thumbs in pixels

    marl         The left margin in pixels
    mart         The top margin in pixels
    marr         The right margin in pixels
    marl         The left margin in pixels

    padding      The padding between images in pixels

    returns a PIL image object.
    """

    # Read in all images and resize appropriately
    imgs = [Image.open(fn).resize(v2) for fn in fnames]

    #imgs = [Image.open(fn).resize((photow,photoh)) for fn in fnames]

    # Calculate the size of the output image, based on the
    #  photo thumb sizes, margins, and padding
    marw = marl+marr
    marh = mart+ marb

    padw = (ncols-1)*padding
    padh = (nrows-1)*padding
    isize = (ncols*photow+marw+padw,nrows*photoh+marh+padh)

    # Create the new image. The background doesn't have to be white
    white = (255,255,255)
    inew = Image.new('RGB',isize,white)

    # Insert each thumb:
    for irow in range(nrows):
        for icol in range(ncols):
            left = marl + icol*(photow+padding)
            right = left + photow
            upper = mart + irow*(photoh+padding)
            lower = upper + photoh
            bbox = (left,upper,right,lower)
            try:
                img = imgs.pop(0)
            except:
                break
            inew.paste(img,bbox)
    return inew

files = glob.glob("images/*.jpg")

ncols,nrows = 3,3

# Don't bother reading in files we aren't going to use
if len(files) > ncols*nrows: files = files[:ncols*nrows]

# These are all in terms of pixels:
photow,photoh = 741,1031 #Les cartes font 741*1031 pixels

photo = (photow,photoh)

margins = [15,15,15,15]

padding = 1

inew = make_contact_sheet(files,(ncols,nrows),photo,margins,padding)
inew.save('images.png')
os.system('display images.png')
os.system('open images.png')
