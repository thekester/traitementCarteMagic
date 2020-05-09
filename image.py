#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Programme d'affichage d'une image par la librairie PIL
# Dominique Lefebvre pour TangenteX.com
# 5 janvier 2016
#



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
import urllib.parse as urlParse

""" https://stackoverflow.com/questions/31147660/importerror-no-module-named-selenium """
from selenium import webdriver

"""https://stackoverflow.com/questions/11783875/importerror-no-module-named-bs4-beautifulsoup"""
from bs4 import BeautifulSoup

webpage = r"https://www.magic-ville.com/fr/" # edit me
searchterm = "Cavalière meurtrière" # edit me

driver = webdriver.Firefox()
driver.get(webpage)

sbox = driver.find_element_by_class_name("search_input")
sbox.send_keys(searchterm)

#submit = driver.find_element_by_tag_name(input)
#submit = driver.find_element_by_link_text('https://www.magic-ville.com/fr/graph/head/go.png')
submit = driver.find_element_by_xpath("//input[@type='image']")
submit.click()

"""

requete = requests.get("https://www.magic-ville.com/fr/")
page = requete.content
soup = BeautifulSoup(page, 'html.parser')
print(soup.prettify())

input = soup.find("input", {"class": "search_input"} , {"name": "recherche_titre" } )
print(input.string)
#n = BeautifulSoup('Cavalière meurtrière' % input.string)

n = BeautifulSoup('Cavalière meurtrière')
input.replace_with(n.body.contents[0])
#input.string.replace_with("Cavalière meurtrière")

submit = driver.find_element_by_class_name("sbtSearch")
submit.click()

"""


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


#https://stackoverflow.com/questions/20894969/python-reading-and-writing-to-tty
"""
tty = io.TextIOWrapper(
        io.FileIO(
            os.open(
                "image.py",
                os.O_NOCTTY | os.O_RDWR),
            "r+"))

for line in iter(tty.readline, None):
    print(line.strip())
"""


"""
root = Tk()
root.geometry("550x300+300+150")
root.resizable(width=True, height=True)

def openfn():
    filename = filedialog.askopenfilename(title='open')
    return filename
def open_img():
    x = openfn()
    img = Image.open(x)
    img = img.resize((250, 250),Image.ANTIALIAS)
    img = Image.PhotoImage(img)
    panel = Label(root, image=img)
    panel.image = img
    panel.pack()

btn = Button(root, text='open image', command=open_img).pack()

root.mainloop()
"""


#size = 1482 , 2062

"""

size = 741, 1031 #Les cartes font 741*1031 pixels

for infile in glob.glob("images/*.jpg"):
    file, ext = os.path.splitext(infile)
    im = Image.open(infile)
    im.thumbnail(size)
    im.save(file + ".thumbnail", "JPEG")
    im.save(file + ".thumbnail", "png")
    im.show()
    
    """

"""folder_path = "/images"

for path, dirs, files in os.walk(folder_path):
    for filename in files:
        print(filename)"""
"""
# ouverture du fichier image
ImageFile = 'images/cava.jpg'
Image.open(ImageFile)
try:
   img = Image.open(ImageFile)
   img = img.thumbmail(741,1031)
   img.save('images/test.png')
except:
    print ('Erreur sur ouverture du fichier ' + ImageFile)
    sys.exit(1)

# affichage des caractéristiques de l'image
print (img.format,img.size, img.mode)



# affichage de l'image
img.show()
# fermeture du fichier image
img.close()
"""
