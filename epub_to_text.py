# coding: utf-8
#
# Converts the epub html files for a specified book to a single text file.
# 

import os
from bs4 import BeautifulSoup

dir_name = 'lulaby_lang_leav'
dir_open = dir_name + '/'
output   = 'lulaby.txt'
files    = os.listdir(dir_name)

def text_cleaner(text):
    clean_text = ''
    line1      = ''
    line2      = ''
    i_holder   = []
    for i in text.split('\n'):
        if not((i == 'Lullabies') or (i=='')) :
            i_holder = i.split(' ')
            if (len(i_holder) > 18):
                
                for word in i_holder[0:18]:
                    line1 += " " + word
                for word in i_holder[18::]:
                    line2 += " " + word
                        
                clean_text = clean_text + line1.lstrip() + '\n'
                clean_text = clean_text + line2.lstrip() + '\n'
               
            else:
                clean_text = clean_text + i.lstrip() + '\n'
            line1 = ''
            line2 = ''

    return clean_text

for f in files[1:]:
    soup = BeautifulSoup(open(dir_open+f),'html.parser')
    
    with open(output, "a") as myfile:
        myfile.write(text_cleaner(soup.get_text().encode('ascii', 'ignore')))
        myfile.write('\n\n')

print 'done'






