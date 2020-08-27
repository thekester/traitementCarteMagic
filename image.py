#!/usr/bin/env python3
# -*- coding: utf-8 -*-.

import PIL
import os

from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
""" https://www.blitzresults.com/fr/pixels/ """

police = ImageFont.truetype("font/TimesNewRoman.ttf", 50)
policeProxy = ImageFont.truetype("font/TimesNewRoman.ttf", 25)
os.chdir("images")

img1 = Image.open('Anax, Hardened in the Forge.png')
img2 = Image.open('Crash Through.png')
img3 = Image.open('Fervent Champion.png')
img4 = Image.open('Fiery Emancipation.png')
img5 = Image.open('Heartfire.png')
img6 = Image.open('Light Up the Stage.png')
img7 = Image.open('Runaway Steam-Kin .png')
img8 = Image.open('Scorch Spitte.png')
img9 = Image.open('Torch Courier.png')

#feuille de 2235*3120 si carte toute collé
#Il faut rajouter des marges de 128 px
#Ce qui donne une feuille de 2619*3504

#Écrire à imprimer en cm (l*3+marge*3mm )
#Donc à imprimer en 20.064cm * 27.264 cm


def creerImagePage(listImage):
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
    page.save("page.png")
    
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
    
listeImage=[img1,img2,img3,img4,img5,img6,img7,img8,img9]
creerImagePage(listeImage)