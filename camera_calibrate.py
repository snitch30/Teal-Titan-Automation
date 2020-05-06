#!/usr/bin/env python

'''
camera calibration for distorted images with chess board samples
reads distorted images, calculates the calibration and write undistorted images

usage:
    calibrate.py [--debug <output path>] [--square_size] [<image mask>]

default values:
    --debug:    ./output/
    --square_size: 1.0
    <image mask> defaults to ../data/left*.jpg
'''

# Python 2/3 compatibility
from __future__ import print_function
import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
# local modules
from common2 import splitfn

# built-in modules
import os

if __name__ == '__main__':
    import sys
    import getopt
    from glob import glob
    

    args, img_mask = getopt.getopt(sys.argv[1:], '', ['debug=', 'square_size=', 'threads='])
    args = dict(args)
    args.setdefault('--debug', 'output/2')
    args.setdefault('--square_size', 13.75)
    args.setdefault('--threads', 4)
    if not img_mask:
        img_mask = '542.jpg'  # default
    else:
        img_mask = img_mask[0]

    img_names = glob(img_mask)
    debug_dir = args.get('--debug')
    if debug_dir and not os.path.isdir(debug_dir):
        os.mkdir(debug_dir)
    square_size = float(args.get('--square_size'))

    pattern_size = (23, 13)
    pattern_points = np.zeros((np.prod(pattern_size), 3), np.float32)
    pattern_points[:, :2] = np.indices(pattern_size).T.reshape(-1, 2)
    
    pattern_points *= square_size
    
    obj_points = []
    img_points = []
    h, w = cv.imread(img_names[0], cv.IMREAD_GRAYSCALE).shape[:2]  # TODO: use imquery call to retrieve results

    def processImage(fn):
        print('processing %s... ' % fn)
        img = cv.imread(fn, 0)
        if img is None:
            print("Failed to load", fn)
            return None

        #assert w == img.shape[1] and h == img.shape[0], ("size: %d x %d ... " % (img.shape[1], img.shape[0]))
        found, corners = cv.findChessboardCorners(img, pattern_size)
        if found:
            term = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_COUNT, 30, 0.001)
            cv.cornerSubPix(img, corners, (5, 5), (-1, -1), term)

        if debug_dir:
            vis = cv.cvtColor(img, cv.COLOR_GRAY2BGR)
            cv.drawChessboardCorners(vis, pattern_size, corners, found)
            _path, name, _ext = splitfn(fn)
            outfile = os.path.join(debug_dir, name + '_chess.png')
            cv.imwrite(outfile, vis)

        if not found:
            print('chessboard not found')
            return None

        print('           %s... OK' % fn)
        return (corners.reshape(-1, 2), pattern_points)

    threads_num = int(args.get('--threads'))
    if threads_num <= 1: 
        chessboards = [processImage(fn) for fn in img_names]
    else:
        print("Run with %d threads..." % threads_num)
        from multiprocessing.dummy import Pool as ThreadPool
        pool = ThreadPool(threads_num)
        chessboards = pool.map(processImage, img_names)

    chessboards = [x for x in chessboards if x is not None]
    for (corners, pattern_points) in chessboards:
        img_points.append(corners)
        obj_points.append(pattern_points)

    # calculate camera distortion
    #print("imag_points=\n",img_points)
    #print("obj_points=\n",obj_points)
    rms, camera_matrix, dist_coefs, rvecs, tvecs = cv.calibrateCamera(obj_points, img_points, (w, h), None, None)

    print("\nRMS:", rms)
    print("camera matrix:\n", camera_matrix)
    print("distortion coefficients: ", dist_coefs.ravel())

    # undistort the image with the calibration
    print('')
    for fn in img_names if debug_dir else []:
        path, name, ext = splitfn(fn)
        img_found = os.path.join(debug_dir, name + '_chess.png')
        outfile = os.path.join(debug_dir, name + '_undistorted.png')

        img = cv.imread(img_found)
        if img is None:
            continue
        

        h, w = img.shape[:2]
        img= cv.imread('542.jpg')
        newcameramtx, roi = cv.getOptimalNewCameraMatrix(camera_matrix, dist_coefs, (w, h), 1, (w, h))
        print("New camera matrix\n",newcameramtx)
        dst = cv.undistort(img, camera_matrix, dist_coefs, None, newcameramtx)
        mapx, mapy = cv.initUndistortRectifyMap(camera_matrix,dist_coefs,None,newcameramtx,(w,h),5)
        newimg = cv.remap(img,mapx,mapy,cv.INTER_LINEAR)
        '''
        fig, (oldimg_ax,newimg_ax) = plt.subplots(1,2) 
        oldimg_ax.imshow(img)
        oldimg_ax.set_title('Original IMAGE')
        newimg_ax.imshow
        newimg_ax.set_title('UNWRAPPED IMAGE')
        plt.show()
       
        a1=np.array([36,25,0])
        print(a1)
        a2=np.array([newcameramtx*a1])
        print("[x y w=",a2)
        k1=8.27815605e-01
        k2=-3.99548015e+00
        k3=1.05915958e+01
        p1=1.23681322e-03
        p2=-1.76362598e-01
        x1=10
        y1=20
        r=((x1**2)+(y1**2))**(0.5)
        x2 = x1*(1+(k1*(r**2))+(k2*(r**4))+(k3*(r**6)))
        y2 = y1*(1+(k1*(r**2))+(k2*(r**4))+(k3*(r**6)))
        #x3 = x2+((2*p1*x2*y2)+(p2((r**2)+2*(x2**2))))
        y3=y2+((p1*((r**2))+(2*(y2**2)))+(2*p2*x2*y2))
        print("x2=",x2)
        print("y2=",y2)
        #print("x3=",x3)
        print("y3=",y3)
        #cv.solvePnP(obj_points, img_points, camera_matrix, dist_coefs[rot_vec, rvec[trans_vec, tvec[SOLVEPNP_ITERATIVE, useExtrinsicGuess[flag, flags]]]])
        def findCameraParameters(cont):
            objectPoints = np.array([[0,0,0],[10.5,0,0],[10.5,5,0],[0,5,0]], dtype=np.float32)
            imagePoints=cont
            ret, rvec, tvec = cv2.solvePnP(objectPoints, imagePoints, np.load("mtx.npy"), np.load("dist.npy"))
            
        # crop and save the image
        
        x, y, w, h = roi
        print("x,y,w,h=", x,y,w,h)
        dst = dst[y:y+h, x:x+w]

        print('Undistorted image written to: %s' % outfile)
        cv.imwrite(outfile, dst)
        hsv = cv.cvtColor( dst, cv.COLOR_BGR2HSV) 
    
        # define range of red color in HSV 
        lower_red = np.array([30,150,50]) 
        upper_red = np.array([255,255,180]) 
        
        # create a red HSV colour boundary and  
        # threshold HSV image 
        mask = cv.inRange(hsv, lower_red, upper_red) 
    


    
        # Bitwise-AND mask and original image 
        res = cv.bitwise_and(dst,dst, mask= mask) 
    
        # Display an original image 
        cv.imshow('Original',dst)     
        # finds edges in the input image image and 
        # marks them in the output map edges 
        edges = cv.Canny(dst,100,200) 
        #x=input()
        # Display edges in a frame 
        cv.imshow('Edges',edges) 
        cv.imwrite(str(x)+'.jpg',edges)
        '''
    #ggggg
    #cv.destroyAllWindows()

var=[camera_matrix, dist_coefs, newcameramtx]
from sklearn.externals import joblib
joblib.dump(var,'variables.pkl')