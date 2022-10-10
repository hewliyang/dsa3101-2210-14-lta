import numpy as np
import cv2

# function to crop cv2 image according to specified coordinates
def crop(img, coord):
    mask = np.zeros(img.shape[0:2], dtype=np.uint8)
    points = np.array([coord])
    cv2.drawContours(mask, [points], -1, (255, 255, 255), -1, cv2.LINE_AA)
    res = cv2.bitwise_and(img,img,mask = mask)
    rect = cv2.boundingRect(points)
    wbg = np.ones_like(img, np.uint8)*255
    cv2.bitwise_not(wbg,wbg, mask=mask)
    dst = wbg+res
    return dst

# function to automatically crop image into 2 directions
def auto_crop(img, coords):
    dir1 = crop(img, coords[0])
    if (coords[1]):
        dir2 = crop(img, coords[1])
    else:
        dir2 = []
    return [dir1, dir2]


# function to display the coordinates of
# of the points clicked on the image
def click_event(event, x, y, flag, coord):
    
    if event == cv2.EVENT_LBUTTONDOWN:
        coord.append((x,y))
 

# driver function
if __name__=="__main__":
 
    # reading the image
    image = input("image:")
    img = cv2.imread('images/'+image+'.jpg', 1)
 
    # displaying the image
    cv2.imshow('image', img)
    coord = []
    cv2.setMouseCallback('image', click_event, coord)
 
    # wait for a key to be pressed to exit
    cv2.waitKey(0)
    
    # close the window
    cv2.destroyAllWindows()

    mask = np.zeros(img.shape[0:2], dtype=np.uint8)

    points = np.array([coord])

    cv2.drawContours(mask, [points], -1, (255, 255, 255), -1, cv2.LINE_AA)
    res = cv2.bitwise_and(img,img,mask = mask)
    rect = cv2.boundingRect(points) 

    wbg = np.ones_like(img, np.uint8)*255
    cv2.bitwise_not(wbg,wbg, mask=mask)
    dst = wbg+res
    cv2.imshow("Samed Size White Image", dst)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # displaying the image
    cv2.imshow('image', img)
    coord2 = []
    cv2.setMouseCallback('image', click_event, coord2)
 
    # wait for a key to be pressed to exit
    cv2.waitKey(0)
    
    # close the window
    cv2.destroyAllWindows()

    mask = np.zeros(img.shape[0:2], dtype=np.uint8)

    points = np.array([coord2])

    cv2.drawContours(mask, [points], -1, (255, 255, 255), -1, cv2.LINE_AA)
    res = cv2.bitwise_and(img,img,mask = mask)
    rect = cv2.boundingRect(points) 
    
    wbg = np.ones_like(img, np.uint8)*255
    cv2.bitwise_not(wbg,wbg, mask=mask)
    dst = wbg+res
    cv2.imshow("Samed Size White Image", dst)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    print([coord, coord2])
