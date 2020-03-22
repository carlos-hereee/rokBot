import cv2
import numpy as np
import pyautogui
import random
import time
import platform
import subprocess

is_retina = False


def region_grabber(region):
    '''
    grab a region (top x, top y, bottom x, bottom y)
    to the tuple (x, y, width, height)

    input : tuple containig the coordinaties of the region to capture

    output: a PIL image of the area selected
    '''
    if is_retina:
        region = [n*2 for n in region]
    x1 = region[0]
    y1 = region[1]
    width = region[2] - x1
    height = region[3] - y1

    return pyautogui.screenshot(region=(x1, y1, width, height))


def image_search_area(image, x1, y1, x2, y2, precision=.8, im=None):
    '''
    Seachs for image with an area

    input:
        image: path to the image file
        x1: top left x value
        y1: top left y value
        x2: bottom right value
        y2: bottom right y value
        precision: the higher, the lesser tolerant and fewer false positives are found default is 0.8
        im: a PIL image, usefull if you inted to search the same unchanging region for several elements

    output:
        returns: the top left corner coorinates of the element if found an an array [x,y] or [-1,-1] if not
    '''
    if im is None:
        im = region_grabber(region=(x1, y1, x2, y2))
        if is_retina:
            im.thumbnail((round(im.size[0]*.5), round(im.size[1]*.5)))
        # im.save(testare.png) usefull for debugging purposes, this will the capture region as test png

    img_rgb = np.array(im)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(image, 0)

    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    if max_val < precision:
        return [-1, -1]
    return max_loc


def click_image(image, pos, action, timestamp, offset=5):
    '''
    Click on the center of an image with a bit of random
    eg, if an image is 100*100 with an offset of 5 it may click at 52,50 the first time and then , 52,53 ect
    usefull to avoid anti-bot monitoring while staying precise

    this function doesn't search for the image, it's only ment to easy clicking on the images.

    input :
        image: path to the image file
        pos: array containing the position of the top left corner of the image[x,y]
        action: button of hte mouse to activate
        time: time taken for the mouse to move from where it was to the new
    '''
    img = cv2.imread(image)
    height, width, channels = img.shape
    pyautogui.moveTo(pos[0]+r(width/2, offset), pos[1] +
                     r(height/2, offset), timestamp)
    pyautogui.click(button=action)


def image_search(image, precision=.8):
    '''
    Searchs for an image on the screen

    input:
        image: path to the image
        precision: the higher, the lesser tolerant and fewer false positives
        im: a PIL image, usefull if you intend to search the same unchaning region for several elements

    returns:
        the top left coner coordinates of the element if found as an array [x,y] or [-1,-1] if not
    '''
    im = pyautogui.screenshot()
    if is_retina:
        im.thumbnail((round(im.size[0]*.5), round(im.size[1]*.5)))
    # im.save('test are.png') useful for debugging purposes

        img_rgb = np.array(im)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(image, 0)
    template.shape[::-1]

    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    if max_val < precision:
        return [-1, -1]
    return max_loc


def image_search_loop(image, timesample, precision=.8):
    '''
    Searchs for an image on screen continuously until it's found

    input:
        image: path to the imag
        time: watining time after failing to find the image

        presiocion:

        returns: the top left corner coordinates of the element if found as array [x,y]
    '''

    pos = image_search(image, precision)
    while pos[0] == -1:
        print(image + " not found, waiting")
        time.sleep(timesample)
        pos = image_search(image, precision)
    return pos


def image_search_num_loop(image, timesample, max_samples, precision=.8):
    '''
    Searhcer for an image on screen continuously until its found or max number of samples reached
    '''

    pos = image_search(image, precision)
    count = 0
    while pos[0] == -1:
        print(image + " not found, waiting")
        time.sleep(timesample)
        pos = image_search(image, precision)
        count += 1
        if count > max_samples:
            break
    return pos


def image_search_region_loop(image, timesample, x1, y1, x2, y2, precision=.8):
    '''
    Search for an image on a reagion of the screen continuously until its found
    '''
    pos = image_search_area(image, x1, x2, y1, y2, precision)
    while pos[0] == -1:
        time.sleep(timesample)
        pos = image_search_area(image, x1, x2, y1, y2, precision)
    return pos


def image_search_count(image, precision=.9):
    '''
    Searches for image on the screen and counts the number of occurrrences
    '''
    img_rgb = pyautogui.screenshot()
    if is_retina:
        img_rgb.thumbnail(
            (round(img_rgb.size[0]*.5), round(img_rgb.size[1] * .5)))

    img_rgb = np.array(img_rgb)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(image, 0)

    w, h = template.shape[::-1]

    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= precision)

    count = 1

    for pt in zip(*loc[::-1]):  # Swap collumns and rows
        # cv2.retangle(img_rgb, pt, (pt[0]+w+, pt[1]+h), (0,0,255), 2) // uncomment to draw boxes around found occurances
        count += 1
    # cv2.imwrite('result.png, img_rgb) // uncomment to write out put image with boxes drawn boxes around found occurences

    return count


def r(num, rand):
    return num+rand * random.random()
