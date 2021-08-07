import csv
from os import POSIX_FADV_NOREUSE
import random as rand
import cli_ui
import os
import time
from PIL import Image
import requests 
from tqdm import tqdm
from io import BytesIO
from clint.textui import progress
import cv2
import numpy as np

class Pytanie:
    nr = 0
    text = ""
    odps = []
    d_odp = 1
    mult = ""

cf = open('pytania_normalne.csv')
reader = csv.reader(cf)

pytania = []
for i,x in enumerate(reader):
    if (i==0):
        continue
    
    if 'B' in x[17]:
        p = Pytanie() 
        p.text=x[1]
        p.odps=[]
        if (x[2] != ''):
            p.odps.append(x[2])
        if (x[3] != ''):
            p.odps.append(x[3])
        if (x[4] != ''):
            p.odps.append(x[4])
        p.d_odp=x[13].lower()
        p.nr=x[0]
        p.mult=x[14]
        pytania.append(p)

dobre = 0
zle = 0
while(True):
    p = rand.choice(pytania)
    tmp = input()
    os.system("clear")
    cli_ui.info_3(cli_ui.green , "DOBRE: ",dobre , cli_ui.yellow , " || " , cli_ui.red , "ŹLE: ", zle)
    cli_ui.info_1(p.text)
    #cli_ui.info_1(p.mult)
    if len(p.odps)!=0:
        cli_ui.info_section("ODPOWIEDZI")
        for x in p.odps:
            cli_ui.info_2(x)
    else:
        cli_ui.info_2(cli_ui.green, "TAK" ,cli_ui.white ,"/",cli_ui.red,"NIE")
    if p.mult!="":
        response = requests.get(f'http://buzinfo.pl/~lexu/testy/{p.mult}',stream=True)
        total_size_in_bytes= int(response.headers.get('content-length', 0))
        block_size = 1024 #1 Kibibyte
        progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True,leave=False)
        with open('test.wmv', 'wb') as file:
            for data in response.iter_content(block_size):
                progress_bar.update(len(data))
                file.write(data)
        progress_bar.close()
        if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
            print("ERROR, something went wrong")
        if p.mult[-3:]=="jpg":
            tmp = input()
            #print("ZDJ")
            os.system('mv test.wmv test.jpg')
            zdj = cv2.imread('test.jpg')
            cv2.imshow(p.mult,zdj)
            cv2.waitKey(0) 
            cv2.destroyAllWindows()
        else:
            tmp = input()
            bytes = open('test.wmv','r')
            cap = cv2.VideoCapture('test.wmv')

            # Check if camera opened successfully
            if (cap.isOpened()== False): 
              print("Error opening video  file")

            # Read until video is completed
            while(cap.isOpened()):

              # Capture frame-by-frame
              ret, frame = cap.read()
              if ret == True:
              
                # Display the resulting frame
                cv2.imshow('Frame', frame)

                # Press Q on keyboard to  exit
                if cv2.waitKey(25) & 0xFF == ord('q'):
                  break
              
              # Break the loop
              else: 
                break
            
            # When everything done, release 
            # the video capture object
            cap.release()

            # Closes all the frames
            cv2.waitKey(0) 
            cv2.destroyAllWindows()

    

    

    odp = input().lower()
    while(odp==''):
        odp = input().lower()
    if (odp =='1'):
        odp = 'a'

    if (odp =='2'):
        odp = 'b'

    if (odp =='3'):
        odp = 'c'

    if p.d_odp=="t":
        if (odp == p.d_odp or odp=="tak"):
            dobre+=1
            cli_ui.info_2(cli_ui.green , "DOBRZE\n")
            continue
    
    if p.d_odp=="n":
        if (odp == p.d_odp or odp=="nie"):
            dobre+=1
            cli_ui.info_2(cli_ui.green , "DOBRZE\n")
            continue
    
    if (p.d_odp == odp):
        dobre+=1
        cli_ui.info_2(cli_ui.green , "DOBRZE\n")
        continue

    cli_ui.info_2(cli_ui.red , "ŹLE\n")
    zle+=1
