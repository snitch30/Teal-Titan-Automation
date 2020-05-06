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
#camera_path='E:/Bin Picking/Input'
camera_path='/Users/stejasmunees/Desktop/TEAL/binphotos/test'
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


from sklearn.externals import joblib
calibrate=joblib.load('variables.pkl')
#0 to 320 y axis
#0 to 220 x axis

dict_coord={}
temp=0
for i in range(1,8):
    for j in range (1,9):
        temp=temp+1
        dict_coord[temp]=[35*i,46*j]


#c = ModbusClient(host="192.1.1.2", port=502, auto_open=True)
c = ModbusClient()
c.host("192.1.1.2")
c.port(502)
# managing TCP sessions with call to c.open()/c.close()
c.open()
while_flag=0
cap = cv.VideoCapture(0)
counter=0
time.sleep(8)
_, frame = cap.read()
camera_matrix=calibrate[0]
dist_coefs=calibrate[1]
newcameramtx=calibrate[2]

for i in range(49,57):
    dict_coord[i][0]=dict_coord[i][0]-5
while(True):	
    
    #Trigger the camera to take a picture
    
    if(counter>=56):
        counter=1
    else:
        counter+=1
    c.open()
    # Select a random co-ordinate and store its corresponding number in a variable and move the bot
    while_flag=0
    current_coord=dict_coord[counter]
    print(current_coord)
    if c.write_multiple_registers(136, current_coord):
        print("write ok1")
    else:
        print("write error")
    print('sending coord for %s'%str([dict_coord[counter][0]/35,dict_coord[counter][1]/46]))
   
    while(while_flag!=1):
#         _, frame = cap.read()
         cv.imwrite(os.path.join(camera_path,'image_temp.jpg'),frame)
         time.sleep(1)
         # cap.release()
         # cv.destroyAllWindows()
         while_flag=1
         img=cv.imread('/Users/stejasmunees/Desktop/TEAL/binphotos/test/image_temp.jpg')
         h, w = img.shape[:2]
         dst = cv.undistort(img, camera_matrix, dist_coefs, None, newcameramtx)
         mapx, mapy = cv.initUndistortRectifyMap(camera_matrix,dist_coefs,None,newcameramtx,(w,h),5)
         newimg = cv.remap(img,mapx,mapy,cv.INTER_LINEAR)
         # Crop image
         newimg = newimg[70:395, 65:525]
#         newimg = newimg[68:393, 63:528]
         rows,cols = newimg.shape[:2]

         M = cv.getRotationMatrix2D((cols/2,rows/2),180,1)
         newimg = cv.warpAffine(newimg,M,(cols,rows))
#         cv2.imwrite('cro_image.jpg',imCrop)
         cv.imwrite(os.path.join(camera_path,'image.jpg'),newimg)
         
    # frame=[]
    # aa=image_slicer.slice(camera_path+'/'+'image.jpg',20)
    #Splitting the Image
    while_flag=0
    
#    while(while_flag!=1):
#        camera_path_dir=os.listdir(camera_path)
#        for file in camera_path_dir:
#            if(file[0])!='.':
#                print("flag")
#                b=[]
#                b.append(file)
#                aa=image_slicer.slice(camera_path+'/'+b[0],20)
#                while_flag=1
#            while_flag=1
    aa=image_slicer.slice(camera_path+'/'+'image.jpg',56)   
    

#    c.open()
#    # Select a random co-ordinate and store its corresponding number in a variable and move the bot
#    while_flag=0
#    current_coord=dict_coord[counter]
#    if c.write_multiple_registers(136, current_coord):
#        print("write ok1")
#    else:
#        print("write error")
#    print('sending coord for %s'%str([dict_coord[counter][0]/35,dict_coord[counter][1]/46]))
    c.open()
    if c.write_multiple_registers(149,[1]):
        print("write ok2")
    else:
        print("write error")
       
    
    time.sleep(5)
    #time.sleep(3)
	#while process_completed[0] == 0:
	#process_completed=c.read_holding_registers(135,1)
    c.open()   
    xx=c.read_holding_registers(150, 1)
    print(xx)
    print('wait for robo to move')
    while((xx[0])!=1):
        xx=c.read_holding_registers(150, 1)
        #print(xx)
        c.open()
#        if c.write_multiple_registers(149,[0]):
#            print("write ok")
#        else:
#            print("write error")
#        
        
    c.open() 
    yy=c.read_holding_registers(151, 1)
    print(yy)
    print('wait for robo to complete')
    while(yy[0]==1):
        yy=c.read_holding_registers(151, 1)
        #print(yy)
        ax=0
        
        if c.write_multiple_registers(149,[0]):
            #print("write ok")
            adaf=0
        else:
            print("write error")
    c.open()
        
    status_of_picking=c.read_holding_registers(134, 2)
    if status_of_picking:
        print(status_of_picking[0])
    else:
        print("read Error")
    print('reading picking status')
    image_name=str(aa[counter-1])
    image_name=image_name[-16:-1]
    src=camera_path+'/'+image_name
    print('status of picking is %d'%status_of_picking[0])
    microsec=''
    _, frame = cap.read()
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
            


