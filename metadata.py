# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 16:25:18 2019

@author: Ivory.Lu
"""
#import json
import os
import csv
import exifread
import pandas as pd
import numpy as np
from sys import stdout
from time import sleep
#%%
def metadata(curr_dir, filename, images):
    df = pd.read_csv(filename, nrows=1)
    columns =df.columns.tolist()
    dataset = pd.read_csv(filename, usecols=columns[:len(columns) - 1])
    print("Fields in the table: ")
    for col in dataset.columns:
        print(col)
        
    filepath = lambda row: curr_dir + "\\" + row.File \
            if pd.isnull(row.RelativePath) \
            else curr_dir + "\\" + str(row.RelativePath) + "\\" + str(row.File)
            
    dataset['Filepath'] = dataset.apply(filepath, axis = 1)
    print(dataset['Filepath'][0])
    
    for index in range (0,len(images)):
            
        f = open(images[index],'rb')
         
        tags = exifread.process_file(f)
         
        note = []
        
        for item in tags['EXIF MakerNote'].values:
                note.append(item)

        csv_index = dataset.index[dataset['Filepath'] == images[index]].tolist()
        stdout.write("\r%s" % (csv_index))
        stdout.flush()
#        sleep(1)
        
        sequence = note[14]
        dataset.loc[csv_index[0],'Sequence'] =  sequence
        
        temperature = note[40]
        dataset.loc[csv_index[0],'Temperature'] = temperature
        
#        image_date = 'Image DateTime'
#        if image_date in tags.keys():
#            date_time = tags['Image DateTime']
#        else:
#            date_time = None
        
        exp_time = 'EXIF ExposureTime'
        if exp_time in tags.keys():
            Exp_time = tags['EXIF ExposureTime']
#            print(Exp_time)
        else:
            Exp_time = None
        dataset.loc[csv_index[0],'ExposureTime'] = str(Exp_time)
        
        image_make = 'Image Make'
        if image_make in tags.keys():
            Make = tags['Image Make']
        else:
            Make = None
        dataset.loc[csv_index[0],'Make'] = Make
        
        capture = 'EXIF SceneCaptureType'
        if capture in tags.keys():
            SceneCaptureType = tags['EXIF SceneCaptureType']
        else:
            SceneCaptureType = None
        dataset.loc[csv_index[0],'SceneCaptureType']= SceneCaptureType
            
        whitebalance = 'EXIF WhiteBalance'
        if whitebalance in tags.keys():
            WhiteBalance = tags['EXIF WhiteBalance']
        else:
            WhiteBalance = None
        dataset.loc[csv_index[0],'WhiteBalance']= WhiteBalance
        
        exposure = 'EXIF ExposureMode'
        if exposure in tags.keys():
            ExposureMode = tags['EXIF ExposureMode']
        else:
            ExposureMode = None
        dataset.loc[csv_index[0],'ExposureMode']= ExposureMode
            
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
        dataset.loc[csv_index[0],'Moonphase'] = moonphase[note[36]]
        
        dataset.loc[csv_index[0],'ISOSpeedRatings']= tags['EXIF ISOSpeedRatings']
        dataset.loc[csv_index[0],'ImageLength'] = tags['EXIF ExifImageLength']
        dataset.loc[csv_index[0],'ImageWidth'] = tags['EXIF ExifImageWidth']
        dataset.loc[csv_index[0],'ColorSpace'] = tags['EXIF ColorSpace']
        dataset.loc[csv_index[0],'FlashPixVersion'] = tags['EXIF FlashPixVersion']
        dataset.loc[csv_index[0],'XResolution'] = tags['Image XResolution']
        dataset.loc[csv_index[0],'YResolution'] = tags['Image YResolution']
        dataset.loc[csv_index[0],'Image_ResolutionUnit'] = tags['Image ResolutionUnit']
        dataset.loc[csv_index[0],'YCbCrPositioning'] = tags['Image YCbCrPositioning']
        dataset.loc[csv_index[0],'ExifOffset'] = tags['Image ExifOffset']
        dataset.loc[csv_index[0],'ComponentsConfiguration'] = tags['EXIF ComponentsConfiguration']
        dataset.loc[csv_index[0],'Flash'] = Flash
        dataset.loc[csv_index[0],'Saturation'] = Saturation
        dataset.loc[csv_index[0],'Contrast'] = Contrast
        dataset.loc[csv_index[0],'Sharpness'] = Sharpness
    
    
    
    dataset = dataset.drop(['Filepath'],axis = 1)
#    for col in dataset.columns:
#        print(col)
    dataset.to_csv(filename,index=False)
#        print(filepath.head(5))
#        if images[index] in filepath: 
            
#outputfile = curr_dir + "/"+ "image_metadata.csv"
#
#with open(outputfile,'w') as writeFile:
#    fieldnames = ['ID','Image','Sequence','Temperature','Time','Make',
#                  'Moonphase','ExposureTime','ISOSpeedRatings','SceneCaptureType',
#                  'WhiteBalance','ExposureMode','ImageLength','ImageWidth',
#                  'ColorSpace','FlashPixVersion','XResolution','YResolution',
#                  'ResolutionUnit','YCbCrPositioning','ExifOffset','ComponentsConfiguration',
#                  'Flash','Saturation','Contrast','Sharpness',
#                  'Detection','Score']
#    writer = csv.DictWriter(writeFile, fieldnames=fieldnames, lineterminator='\n')
#    writer.writeheader()
#writeFile.close()
            #    
#%%
def main():
    images = []
    inputfile = []
    filename = 0
    
    curr_dir = os.getcwd()
#    curr_dir = "C:/Ivory backup/animalornot/test/sub_3"
    for root, dirs, files in os.walk(curr_dir):
        for file in files:
            if file.endswith(".JPG"):
                images.append(os.path.join(root,file))
            if file.endswith(".csv"):
                inputfile.append(os.path.join(root,file))
    
    print(inputfile)
    
    for filename in inputfile:
        if filename.find("TimelapseData.csv") == -1:
            continue
        else:
            metadata(curr_dir, filename, images)
            
    if filename == 0: 
        print("Please make sure you have exported the correct csv file.")

if __name__ == '__main__':
    main()
    
