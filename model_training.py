from pyModbusTCP.client import ModbusClient
import cv2 as cv
import numpy as np 
import os
import shutil
import image_slicer
import time
import datetime
yes=0
no=0
# TCP auto connect on first modbus request
a=1
b=1
x=1
y=1
old_status=0
status=0
camera_path='E:/Bin Picking/Input'
xx=[]
#image_counter=1
#reached=[1]

#
#import os
#import image_slicer
#source='/Users/stejasmunees/Desktop/untitled folder 2'
#source_dir=os.listdir(source)
#b=[]
#for file in source_dir:
#    if(file[0])!='.':
#        b.append(file)
#        aa=image_slicer.slice(source+'/'+b[0],56)



#0 to 320 y axis
#0 to 220 x axis

dict_coord={}
temp=0
for i in range(1,9):
    for j in range (1,8):
        temp=temp+1
        dict_coord[temp]=[41*i,33*-j]



while_flag=0
cap = cv.VideoCapture(1)
counter=0

while(True):	
    #Trigger the camera to take a picture
    #c = ModbusClient(host="192.1.1.2", port=502, auto_open=True)
    c = ModbusClient()
    c.host("192.1.1.2")
    c.port(502)
    d = ModbusClient()
    d.host("192.1.1.2")
    d.port(502)
    # managing TCP sessions with call to c.open()/c.close()
    c.open()
    if(counter>=56):
        counter=0
    else:
        counter+=1
    
   
    while(while_flag!=1):
        _, frame = cap.read()
        cv.imwrite(os.path.join(camera_path,'image.jpg'),frame)
        time.sleep(1)
        # cap.release()
        # cv.destroyAllWindows()
        while_flag=1
    
    # frame=[]
    # aa=image_slicer.slice(camera_path+'/'+'image.jpg',20)
    #Splitting the Image
    while_flag=0
    
    # while(while_flag!=1):
    #     camera_path_dir=os.listdir(camera_path)
    #     for file in camera_path_dir:
    #         if(file[0])!='.':
    #             print("flag")
    #             b=[]
    #             b.append(file)
    #             aa=image_slicer.slice(camera_path+'/'+b[0],20)
    #             while_flag=1
    #         while_flag=1
    aa=image_slicer.slice(camera_path+'/'+'image.jpg',56)   
    

    
    # Select a random co-ordinate and store its corresponding number in a variable and move the bot
    while_flag=0
    
    
    current_coord=dict_coord[counter]
    print(current_coord)
    c.close()
    d.open()
    d.write_multiple_registers(136,current_coord)
    print('sending coord')
#    c.close()
    
    d.write_multiple_registers(148,[1,1])
    time.sleep(3)
    d.close()
    c.open()
    zz=c.read_holding_registers(136, 3)
    print(zz)
    #time.sleep(0.5)
    #time.sleep(3)
	#while process_completed[0] == 0:
	#process_completed=c.read_holding_registers(135,1)
    #c.close()
#    c.open()
    xx=c.read_holding_registers(150, 1)
    while((xx[0])!=1):
        d.close()
        c.open()
        xx=c.read_holding_registers(150, 1)
        c.close()
        d.open()
        d.write_multiple_registers(149,[0])
#        c.close()
        print('wait for robo to move')
    d.close()
    c.open()
    yy=c.read_holding_registers(151, 1)
    while(yy[0]!=1):
        yy=c.read_holding_registers(151, 1)
        ax=0
        #print('wait for robo to complete')
    c.close()
        
#    c.open()
    status_of_picking=c.read_holding_registers(134, 1)
    print('reading picking status')
    image_name=str(aa[counter-1])
    image_name=image_name[11:-1]
    src=camera_path+'/'+image_name
    print('status of picking is %d'%status_of_picking[0])
    microsec=''
    if status_of_picking[0]==1:
        print('saving yes')
        yes=yes+1
        digit=str(yes).zfill(5)
        microsec=str(datetime.datetime.now().time())
        dest='E:/Bin Picking/Dataset/yes/yes_'+digit+'_'+microsec[-6:]+'.jpg'
        shutil.move(src,dest)
        for filess in os.listdir(camera_path):
            file_path=os.path.join(camera_path,filess)
            os.unlink(file_path)
            
    if status_of_picking[0]==0:
        print('saving no')
        no=no+1
        digit=str(no).zfill(5)
        microsec=str(datetime.datetime.now().time())
        dest='E:/Bin Picking/Dataset/no/no_'+digit+'_'+microsec[-6:]+'.jpg'
        shutil.move(src,dest)
        for filess in os.listdir(camera_path):
            file_path=os.path.join(camera_path,filess)
            os.unlink(file_path)
            


