#!/usr/bin/env python3
# -*- coding: utf-8 -*-.


import scrython
import time
import urllib.request
card = scrython.cards.Named(fuzzy="Black Lotus")

print(card.id())
card2 = card.image_uris(0,"png") #index ?
print(card.image_uris(0,"art_crop"))


#Le code d'avant doit s'éxécuter sans proxy
#Le code d 'après s'éxécute avec un proxy si vous en avez un et normalement sinon

#create the object, assign it to a variable
proxy = urllib.request.ProxyHandler({'http': '192.168.0.3:3128'})
# construct a new opener using your proxy settings
opener = urllib.request.build_opener(proxy)
# install the openen on the module-level
urllib.request.install_opener(opener)
# make a request
urllib.request.urlretrieve(card2,"Image4.png")

#ssl:default [Name or service not known]


"""
proxies = {'http': 'http:/192.168.0.13:3128'}
print("Using HTTP proxy %s" % proxies['http'])
urllib.request.urlopen(card2, "Image.png" , proxies=proxies)

urllib.request.urlretrieve(card2, "Image.png")
print(card2) #On obtient un lien qui nous donne une image png
"""
