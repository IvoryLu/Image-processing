# -*- coding: utf-8 -*-
"""
Created on Mon May 27 11:48:52 2019

@author: Ivory.Lu
"""
#import exifread
#import pandas as pd 
#data = pd.read_csv('C:/Users/ivory.lu/animalornot/summary/sequence_mornington.csv')
#
#sequence = []
#i = 0
#for ele in data.filepath:
#    print(ele)
#    f = open(ele,'rb')
#
#    tags = exifread.process_file(f)
##    break
#    i = i + 1
#    
#    for tag in tags.keys():
#        #if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
#        print ("Key: %s, value %s" % (tag, tags[tag]))
#    
##    print(tags['EXIF MakerNote'])
#
#    note = []
#    
#    #Sequence 14 
#    #Temperature 40 
#    #Moonphase 36
#    #Saturation 78
#    #Contrast 72
#    #Sharpness 
#
#    for item in tags['EXIF MakerNote'].values:
#        note.append(item)
#    
#    sequence.append(note[76])
#            
#    if i == 1:
#        break

import exifread
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from struct import *

#image = Image.open("C:/Ivory backup/animalornot/test/sub_3/IMG_9989.JPG")


#%%
def get_name(info):

    note = []
#    temp = []
    for tag, value in info.items():    
        key = TAGS.get(tag, tag) 
        print(key + " " + str(value))
        if key == 'MakerNote':
            name = []
            for i, ele in enumerate(value):
                note.append(str(ele))
    #            print(i)
    #           Convert to byte 
                x = ele.to_bytes(1,byteorder='big')
    #            print(x.decode("latin-1"))
    #           Decode it "latin-1"
                if i >= 86 and i <= 100 and x != b'\x00':
                    name.append(x.decode("latin-1"))
                    print(x.decode("latin-1"))
            name = ''.join(name)
            print(name)

#        temp = value.decode('latin-1')
#%%
def get_geotagging(info):
    geotagging = {}
    for (idx, tag) in TAGS.items():
        if tag == 'GPSInfo':
            if idx not in info:
                raise ValueError("No EXIF geotagging found")
            for (key, val) in GPSTAGS.items():
                if key in info[idx]:
                    geotagging[val] = info[idx][key]
                
    return geotagging
#%%
file = r"C:\TEMP-UPLOADS\Ecohealth - Exclosure wide cameras\2017-2018\Middle third of exclosure\EW0 p+p\11\2018 01 01\IMG_0001.JPG"
image = Image.open(file)
info = image._getexif()
for key in sorted(info):
    print(str(key) + ": " + str(info[key]))
    
for tag, value in info.items():    
    key = TAGS.get(tag, tag) 
    print(key + " " + str(value))
geotags = get_geotagging(info)
print(geotags)

#i = 0            
#for ele in note:
#    print(ele.encode("latin-1","strict"))
#    i = i + 1 
#    if i == 50: 
#        break
#    
    
#        temp = value.decode("ISO-8859-1")

#for ele in temp:
#    print(ele)

#f = open('C:/Ivory backup/animalornot/test/sub_3/IMG_9989.JPG','rb')
#
#tags =  exifread.process_file(f)
#
#for tag in tags.keys():
##        #if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
#    print ("Key: %s, value %s" % (tag, tags[tag]))
#    note = []
#
#    for item in tags['EXIF MakerNote'].values:
#        note.append(item)
#print(note[78])
#print(tags['EXIF ExposureTime'])
