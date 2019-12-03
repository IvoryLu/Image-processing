# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 15:25:56 2019

@author: Ivory.Lu
"""

import PIL.Image
import os
import pandas as pd
from PIL.ExifTags import TAGS
import exifread
import tifffile

curr_dir = os.getcwd()

images = []
authors = []
Title = []
tmp = []
comment = []
camera_maker = []
tags = []
subject = []
fileName = []
formatt = []
metadata = 0

counter = -1
layer = 0
tif = 0
for root, dirs, files in os.walk(curr_dir):
    for file in files:
        if file.endswith(".JPG") or file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith(".png") or file.endswith(".PNG"):
            fileName.append(file)
            formatt.append(os.path.splitext(file)[1])
            counter = counter + 1
            print(file)
            image = os.path.join(root,file)
#            print(image)
            if image.count('\\') > layer: 
                layer = image.count('\\')
            images.append(image)
            img = PIL.Image.open(image)

            exif_data = img._getexif()
            
            authors.append(0)
            Title.append(0)
            comment.append(0)
            camera_maker.append(0)
            tags.append(0)
            subject.append(0)
#            if counter != 266:
#                continue

#            for tag, value in img.info.items(): 
#                key = TAGS.get(tag, tag)
#                if counter == 1:
#                    print(key)
#                    tmp.append(value)
            
            photoshop = []
            parsed_exif = []
            
            for tag, value in img.info.items(): 
                key = TAGS.get(tag, tag)
                if key == 'photoshop':
                    photoshop = value
                if key == 'parsed_exif':
                    parsed_exif = value
            
            temp_2 = []
            temp_3 = []
            temp_4 = []
            temp_last = []
            count = 0 
            total = 0
            old = 0
            if photoshop and photoshop.get(1028):
                total = photoshop.get(1028).count(b'\x1c')
                mylist = photoshop.get(1028)
                mylist = [x.to_bytes(1,byteorder='big') for x in mylist]
#                print(mylist)
                size = len(mylist)
                idx_list = [idx + 1 for idx, val in enumerate(mylist) if val == b'\x1c']
                
                res = [mylist[i: j] for i, j in zip([0] + idx_list, idx_list + ([size] if idx_list[-1] != size else []))] 
                
                for ele in res:
                    if ele[0] == b'\x02' and (ele[1] == b'P' or ele[1] == b'\x05') and (ele[3] == b'\x10' or ele[3] == b'\n' ):
                        temp_1 = []
                        for index in range(4,len(ele)-1):
                            temp_1.append(ele[index].decode("latin-1"))
                        authors[counter] = ''.join(temp_1) #ele[1] == b'\x19' or 
                    if ele[0] == b'\x02' and (ele[1] == b'x' or ele[1] == b'\x05') and (ele[3] == b'\x07' or ele[3] == b'2' or ele[3] == b'\x19' or \
                          ele[3] == b'?' or ele[3] == b'\x15' or ele[3] == b'\x1f' or ele[3] == b'\x0e' or ele[3] == b'!' or ele[3] == b',' or\
                          ele[3] == b'\n' or ele[3] == b'\x1d' or ele[3] == b'\x11' or ele[3] == b'\r' or ele[3] == b'\x18' or ele[3] == b'\t' or \
                          ele[3] == b'6' or ele[3] == b' ' or ele[3] == b'8' or ele[3] == b'"' or ele[3] == b'\x0f' or  ele[3] == b'-' or \
                          ele[3] == b')' or ele[3] == b'\x1e' or ele[3] == b'@' or ele[3] == b'\x16' or ele[3] ==  b'\x03' or ele[3] ==  b'%') and not (ele[1] == b'x' and ele[3] == b'\x03'):
                        temp_5 = []
                        for index in range(4,len(ele)-1):
                            temp_5.append(ele[index].decode("latin-1"))
                        Title[counter] = ''.join(temp_5)
                    if ele[0] == b'\x02' and ele[1] == b'\x19' and (ele[3] == b'\x0e' or ele[3] == b'\t' or ele[3] == b'\x10' or ele[3] == b'\x1f' or \
                          ele[3] == b'\x03' or ele[3] == b'\x16' or ele[3] == b'\x11' or ele[3] == b'\x08' or ele[3] == b'\x12' or  ele[3] == b'\x02' or \
                          ele[3] == b'\x11' or  ele[3] == b'\x0c' or ele[3] == b'\x07' or ele[3] == b'\x0f' or ele[3] == b'\x0b' or ele[3] == b'\x05' or \
                          ele[3] == b'\x06' or ele[3] == b'\x04' or ele[3] == b'\r'):
                        for index in range(4,len(ele)-1):
                            temp_3.append(ele[index].decode("latin-1"))
                        if temp_3 and temp_3[-1] != 0:
                            temp_3.append(';')
                        tags[counter] = ''.join(temp_3)
                    
            if parsed_exif or exif_data:
                if parsed_exif.get(40092) and comment[counter] == 0:
                    temp_3 = parsed_exif.get(40092).decode("latin-1")
                    comment[counter] = ''.join(temp_3)
                if parsed_exif.get(40094) and tags[counter] == 0:
                    temp_4 = parsed_exif.get(40094).decode("latin-1")
                    tags[counter] = ''.join(temp_4)
                if parsed_exif.get(270):
                    temp_2 = parsed_exif.get(270)
                    subject[counter] = ''.join(temp_2)
                if parsed_exif.get(40095) and subject[counter] == 0:
                    temp_2 = parsed_exif.get(40095).decode("latin-1")
                    subject[counter] = ''.join(temp_2)
                if exif_data.get(40091):
                    temp_5 = exif_data.get(40091).decode("latin-1")
                    Title[counter] = ''.join(temp_5)
#                if parsed_exif.get(40093):
#                    temp_1 = parsed_exif.get(40093).decode("latin-1")
#                    authors[counter] = ''.join(temp_1)
                camera_maker[counter] = parsed_exif.get(271)
                camera_maker[counter] = exif_data.get(271)
            if authors[counter] == 0 and parsed_exif:
                authors[counter] = parsed_exif.get(315)

            if Title[counter] != 0 and ('Australian' in Title[counter] or 'Mallee' in Title[counter] or 'Wildlife' in Title[counter]): 
                Title[counter] = 0
            if Title[counter] != 0 and tags[counter] != 0 and Title[counter] in tags[counter]:
                Title[counter] = 0

        if file.endswith('.tif') or file.endswith('.tiff') or file.endswith('.TIF'):
            fileName.append(file)
            formatt.append(os.path.splitext(file)[1])
            counter = counter + 1
            
            authors.append(0)
            Title.append(0)
            comment.append(0)
            camera_maker.append(0)
            tags.append(0)
            subject.append(0)
            
            image = os.path.join(root,file)
            images.append(image)
            
#            if counter != 3:
#                continue
#            
            print(file)

            temp_last = []
            temp_6 = []
            temp_7 = []
            with tifffile.TiffFile(image) as tif:
                tif_tags = {}
                for tag in tif.pages[0].tags.values():
                    name, value = tag.name, tag.value
                    tif_tags[name] = value
#                print(tif_tags.get('IPTCNAA'))
                
                if tif_tags.get('Make'):
                    camera_maker[counter] = tif_tags.get('Make')
                
                if tif_tags.get('Artist'):
                    authors[counter] = tif_tags.get('Artist')
                    
                if tif_tags.get('XPComment'):
                    comment[counter] = tif_tags.get('XPComment').decode("latin-1")
                    
                if tif_tags.get('ImageDescription'):
                    subject[counter] = tif_tags.get('ImageDescription')
                    
                tmp_tag = tif_tags.get('IPTCNAA')
                if tmp_tag:
                    tmp_tag = [x.to_bytes(1,byteorder='big') for x in tmp_tag]
                
                    idx_list = [idx + 1 for idx, val in enumerate(tmp_tag) if val == b'\x1c']
                
                    res_tif = [tmp_tag[i: j] for i, j in zip([0] + idx_list, idx_list + ([size] if idx_list[-1] != size else []))]
                
                    for ele in res_tif:
                        if len(ele) > 4 and ele[0] == b'\x02' and (ele[1] == b'\x19'):
                           for index in range(4,len(ele)-1):
                               temp_last.append(ele[index].decode("latin-1"))
                           if temp_last and temp_last[-1] != 0:
                               temp_last.append(';')
                           tags[counter] = ''.join(temp_last)
                        if len(ele) > 4 and ele[0] == b'\x02' and (ele[1] == b'x') and ele[3] == b'\xc2':
                           for index in range(4,len(ele)-1):
                               temp_6.append(ele[index].decode("latin-1"))
                           subject[counter] = ''.join(temp_6)
                        if len(ele) > 4 and ele[0] == b'\x02' and (ele[1] == b'\x05' ) :
                           for index in range(4,len(ele)-1):
                               temp_7.append(ele[index].decode("latin-1"))
                           Title[counter] = ''.join(temp_7)
            
columns = ['root','path_1','path_2','path_3','path_4','path_5','path_6','path_7', 'path_8','path_9','path_10','path_11','path_12']

df = pd.DataFrame(images, columns = ['filename'])
df = pd.DataFrame(df.filename.str.split('\\').tolist(),
                                   columns = columns[0:layer + 1])
    
df = df.drop(['root','path_1'], axis = 1)
df['filename'] = fileName
df['filepath'] = images
df['Title'] = Title
df['Authors'] = authors
df['Comments'] = comment
df['Camera_Maker'] = camera_maker
df['Tags'] = tags
df['Subject'] = subject
df['Formatt'] = formatt

df.to_csv(curr_dir + "/" + os.path.basename(curr_dir)+ ".csv")