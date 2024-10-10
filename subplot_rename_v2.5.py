####Chromosome png sorter. Paste this file in the parent directory of the directories whos contents you wish to sort.

import os
import shutil
from pathlib import Path
import cv2
#from PIL import image
import numpy as np

font = cv2.FONT_HERSHEY_SIMPLEX
listdirectory = os.listdir() ###create list of folders/files to search through
chr_out = 'new_chromX'
Path(chr_out).mkdir()
for a in listdirectory:

    if os.path.isdir(a) is False: ###check we are scanning a directory. if not, pass onto next loop iteration.
        print('{} is not a directory'.format(a))
        continue
    file_list = os.listdir(a)
    a_clean = a.replace(" ","_")
    a_clean = a.replace('.','_') ###remove spaces and periods
    for b in file_list:
        unique_sep = '___' ###set unique separator to split the identifier name (parent directory) from chromosome number. we can search for this without risking picking up more commonly used separators
        new_png_name=a_clean+unique_sep+b ###generate new name for PNG which has unique identifier, pulled from its parent directory name
        pref,exten = os.path.splitext(new_png_name)
        pref=pref.strip()
        new_png_name = new_png_name.replace(' ','_')
        chrom_num = pref[(pref.find(unique_sep))+len(unique_sep):] ###the files were created as 'chromosome number.png' so pull chromosome number from the end of the name, sans extension and any prefixes. Find the unique separator we created, and take the index number in the string from after the unique seprator
        
        print(chrom_num)
        
        chrom_dir = chr_out+'/'+'chrom_'+chrom_num
        old_png_path = a+'/'+b ###old path. the relative path for where this .py file is being run from. 
        new_png_path = chrom_dir+'/'+new_png_name ###new path (the copied file with name change. relative path)
        
        if os.path.exists(chrom_dir) == False: ###generate folders based on chromosome number. Here we check if the folder already exists. If it does not, create it.
            Path(chrom_dir).mkdir()
        shutil.copy(old_png_path,new_png_path) ###copy and rename into relevant chromsome folder
        

chr_out_ls = os.listdir(chr_out)
print(chr_out_ls)

for c in chr_out_ls:
    chrom_dir = chr_out+'/'+c
    if os.path.isdir(chrom_dir) is False: ###check we are scanning a directory. if not, pass onto next loop iteration.
        print('{} is not a directory'.format(c))
        continue
    image_list = os.listdir(chrom_dir)
    print(image_list)
    image_list_len = len(image_list)
    print(image_list_len)
    
    ###
    ###HQ Update v2.5 2024-10-09
    ##add in logic if im_row_len > image_list_len then say im_row_len is too high, try again.
    ###provide user input for im_row_len. cannot be less than 1
    ##make  it work so it will accept im_row_len = 1. Currenly this state just results in printing just 1 image.
    ###
    
    im_row_len = 3 ###intended length of image rows. user defined.
    
    
    timer = 0
    row_count = 0
    for d in image_list:
        im_path = chrom_dir+'/'+d
        if timer == 0:
            print('first image')
            ###turn into function
            curr_im = cv2.imread(im_path)
            ht,wt,dp=curr_im.shape
            
            first_im = cv2.imread(im_path)
            cv2.putText(first_im,d,(int(ht*0.1),int(wt-(wt*0.9))),font,2,(0,0,0)) ###add title to top of image
            
            
            ###function to check if last image and wrap up image.
            if timer==image_list_len:
                print('end image')
                curr_im = first_im
                break ###exit for loop to save image as is
            
            timer+=1
            
            
        elif timer>0 and timer%im_row_len==0:
            ###have filled row and start new line in graphic 
            print('start new line')
            prev_row_count=row_count
            
            if prev_row_count > 0: ###if still on first row of images, no need to concaternate anything otherwise concatenate rows
                print('save row')                               
                prev_row_im = cv2.vconcat([prev_row_im,first_im])
                print(prev_row_im.shape,' ',first_im.shape) 
            else:
                prev_row_im  = first_im
            
            ###function to check if last image and wrap up image.
            ###if images end on row end
            if timer==image_list_len:
                print('end image')
                curr_im=prev_row_im
                break ###exit for loop to save image as is
                
            curr_im = cv2.imread(im_path)
            ht,wt,dp=curr_im.shape
            first_im = cv2.imread(im_path)
            cv2.putText(first_im,d,(int(ht*0.1),int(wt-(wt*0.9))),font,2,(0,0,0)) ###add title to top of image
            #cv2.imwrite(chrom_dir+'concat.png', first_im)

                
            
            timer+=1
            row_count+=1
            
        
        else:
            curr_im = cv2.imread(im_path)
            ht,wt,dp=curr_im.shape
            print(ht,' ',wt)
            cv2.putText(curr_im,d,(int(ht*0.1),int(wt-(wt*0.9))),font,2,(0,0,0))

            print('along same row')
            curr_im=cv2.hconcat([first_im,curr_im])

            first_im=curr_im
            im_shape = first_im.shape
            f_ht,f_wt,f_dp=im_shape
            print('im_shape = ',im_shape)
            
            
            if timer==image_list_len-1:
                print('end image')
                p_ht,p_wt,p_dp=prev_row_im.shape
                print(prev_row_im.shape)
                print(first_im.shape)
                padding_image = np.uint8(np.zeros((ht,(p_wt-f_wt),f_dp))) ###create padding to even out row length with previous rows. remember to ensure bit detph is the same accross images as well as dimensions
                padding_image[:,0:(p_wt-f_wt)] = (255,255,255)
                
                print(first_im.dtype,padding_image.dtype)
                print('first_im = {} padding_image = {}'.format(first_im.shape,padding_image.shape))
                
                curr_im = cv2.hconcat([first_im,padding_image])
                #print('padded image = ',curr_im.shape)
                curr_im = cv2.vconcat([prev_row_im,curr_im])
                break
                
                
            
            
            print('count = ',timer)
            timer+=1
    cv2.imwrite(chrom_dir+'concat.png',curr_im)
        
