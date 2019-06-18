# -*- coding: utf-8 -*-
"""
Created on Mon May 27 11:48:52 2019

@author: Ivory.Lu
"""
import exifread
import pandas as pd 
data = pd.read_csv('C:/Users/ivory.lu/animalornot/summary/sequence_mornington.csv')

sequence = []
i = 0
for ele in data.filepath:
    print(ele)
    f = open(ele,'rb')

    tags = exifread.process_file(f)
#    break
    i = i + 1
    
    for tag in tags.keys():
        #if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
        print ("Key: %s, value %s" % (tag, tags[tag]))
    
#    print(tags['EXIF MakerNote'])

    note = []
    
    #Sequence 14 
    #Temperature 40 
    #Moonphase 36
    #Saturation 78
    #Contrast 72
    #Sharpness 64

    for item in tags['EXIF MakerNote'].values:
        note.append(item)
    
    sequence.append(note[76])
            
    if i == 1:
        break