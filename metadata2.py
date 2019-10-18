# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 16:25:18 2019

@author: Ivory.Lu
"""

#import json
import os
import csv
import exifread

images = []

curr_dir = os.getcwd()

#curr_dir = "C:/Ivory backup/animalornot/test/sub_3"

for root, dirs, files in os.walk(curr_dir):
    for file in files:
        if file.endswith(".JPG"):
            images.append(os.path.join(root,file))
                            
#with open('C:/Ivory backup/Documents/Bullo River.json','w') as outfile:              
#    json.dump(filepath,outfile,indent=4)
    
curr_dir = os.getcwd()

outputfile = curr_dir + "/"+ "image_metadata.csv"

with open(outputfile,'w') as writeFile:
    fieldnames = ['ID','Image','Sequence','Temperature','Time','Make',
                  'Moonphase','ExposureTime','ISOSpeedRatings','SceneCaptureType',
                  'WhiteBalance','ExposureMode','ImageLength','ImageWidth',
                  'ColorSpace','FlashPixVersion','XResolution','YResolution',
                  'ResolutionUnit','YCbCrPositioning','ExifOffset','ComponentsConfiguration',
                  'Flash','Saturation','Contrast','Sharpness',
                  'Detection','Score']
    writer = csv.DictWriter(writeFile, fieldnames=fieldnames, lineterminator='\n')
    writer.writeheader()
writeFile.close()

for index in range (0,len(images)):
        
    f = open(images[index],'rb')
     
    tags = exifread.process_file(f)
     
    note = []
    
    for item in tags['EXIF MakerNote'].values:
            note.append(item)
    
#        print(images[index])
    sequence = note[14]
    temperature = note[40]
    image_date = 'Image DateTime'
    if image_date in tags.keys():
        date_time = tags['Image DateTime']
    else:
        date_time = None
        
    image_make = 'Image Make'
    if image_make in tags.keys():
        Make = tags['Image Make']
    else:
        Make = None

    capture = 'EXIF SceneCaptureType'
    if capture in tags.keys():
        SceneCaptureType = tags['EXIF SceneCaptureType']
    else:
        SceneCaptureType = None
        
    whitebalance = 'EXIF WhiteBalance'
    if whitebalance in tags.keys():
        WhiteBalance = tags['EXIF WhiteBalance']
    else:
        WhiteBalance = None
        
    exposure = 'EXIF ExposureMode'
    if exposure in tags.keys():
        ExposureMode = tags['EXIF ExposureMode']
    else:
        ExposureMode = None
        
    flash = 'EXIF Flash'
    if flash in tags.keys():
        Flash = tags['EXIF ExposureMode']
    else:
        Flash = None
    
    Saturation = note[78]
    Contrast = note[176]
    Sharpness = note[172]
        
    moonphase = ['New', 'New Crescent', 'First Quater', 'Waxing Gibbous',
                 'Full', 'Waning Gibbous', 'Last Quater', 'Old Crescent']
            
    with open(outputfile,'a') as writeFile:
        fieldnames = ['id','image','sequence','temperature','time','make','Moonphase',
                      'ExposureTime','ISOSpeedRatings','SceneCaptureType','WhiteBalance',
                      'ExposureMode','ImageWidth','ImageLength','ColorSpace','FlashPixVersion',
                      'XResolution','YResolution','Image ResolutionUnit','YCbCrPositioning',
                      'ExifOffset','ComponentsConfiguration','Flash',
                      'Saturation','Contrast','Sharpness']
        
        writer = csv.DictWriter(writeFile, fieldnames=fieldnames, lineterminator='\n')
        writer.writerow({'id': index + 1,'image':images[index],'sequence':sequence,
                         'temperature':temperature,'time':date_time, 'make':Make,
                         'Moonphase':moonphase[note[36]],
                         'ExposureTime':tags['EXIF ExposureTime'],
                         'ISOSpeedRatings':tags['EXIF ISOSpeedRatings'], 'SceneCaptureType':SceneCaptureType,
                         'WhiteBalance':WhiteBalance, 'ExposureMode':ExposureMode,
                         'ImageLength':tags['EXIF ExifImageWidth'],'ImageWidth':tags['EXIF ExifImageWidth'],
                         'ColorSpace':tags['EXIF ColorSpace'],
                         'FlashPixVersion':tags['EXIF FlashPixVersion'],'XResolution':tags['Image XResolution'],
                         'YResolution':tags['Image YResolution'],'Image ResolutionUnit':tags['Image ResolutionUnit'],
                         'YCbCrPositioning':tags['Image YCbCrPositioning'],'ExifOffset':tags['Image ExifOffset'],
                         'ComponentsConfiguration':tags['EXIF ComponentsConfiguration'],'Flash':Flash,
                         'Saturation':Saturation,'Contrast':Contrast,'Sharpness':Sharpness
                         })
    writeFile.close()
