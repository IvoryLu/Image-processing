# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 12:45:34 2019

@author: Ivory.Lu
"""
import os
import exiftool
import pandas as pd
import subprocess


curr_dir = os.getcwd()

fileName = []
videos = []
tags = []
subtitle = []
contri_artist = []
title = [] 
genre = []
formatt = []

comment = []
counter = -1
layer = 0

for root, dirs, files in os.walk(curr_dir):
    for file in files:
        if file.endswith(".mov") or file.endswith(".mp4") or file.endswith(".wmv") or file.endswith(".MOV") or file.endswith(".MP4") or file.endswith(".avi") or file.endswith(".AVI") or file.endswith(".mkv"):
            fileName.append(file)
            counter = counter + 1 
            
            video = os.path.join(root,file)
            videos.append(video)
            print(video)
            
            if video.count('\\') > layer: 
                layer = video.count('\\')
            formatt.append(os.path.splitext(file)[1])
            
            with exiftool.ExifTool('exiftool.exe') as et:
                metadata = et.get_metadata(video)
                
            if metadata.get('QuickTime:Category'):
                tags.append(metadata.get('QuickTime:Category'))
            else:
                tags.append(0)
            
            if metadata.get('QuickTime:Comment'):
                comment.append(metadata.get('QuickTime:Comment'))
            elif metadata.get('QuickTime:Description'):
                comment.append(metadata.get('QuickTime:Description'))
            else:
                comment.append(0)
                
            if metadata.get('QuickTime:Subtitle'):
                subtitle.append(metadata.get('QuickTime:Subtitle'))
            else:
                subtitle.append(0)
                
            if metadata.get('QuickTime:Artist'):
                contri_artist.append(metadata.get('QuickTime:Artist'))
            else:
                contri_artist.append(0)
                
            if metadata.get('QuickTime:Title'):
                title.append(metadata.get('QuickTime:Title'))
            else:
                title.append(0)
                
            if metadata.get('QuickTime:Genre'):
                genre.append(metadata.get('QuickTime:Genre'))
            else:
                genre.append(0)
            
            metadata = 0
                
#            if counter == 5:
#                break
columns = ['root','path_1','path_2','path_3','path_4','path_5','path_6','path_7', 'path_8','path_9','path_10','path_11','path_12']

df = pd.DataFrame(videos, columns = ['filename'])
df = pd.DataFrame(df.filename.str.split('\\').tolist(),
                                   columns = columns[0:layer + 1])
    
df = df.drop(['root','path_1'], axis = 1)
df['filename'] = fileName
df['filepath'] = videos
df['Title'] = title
df['Subtitle'] = subtitle
df['Tags'] = tags
df['Comments'] = comment
df['Contributing artists'] = contri_artist
df['Formatt'] = formatt

df.to_csv(curr_dir + "/" + os.path.basename(curr_dir)+ "_video.csv")