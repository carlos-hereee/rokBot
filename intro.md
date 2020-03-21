# How the modules work

## PYAUTOGUI

### KEYBOARD

1. To type one (or several) keys: auto.keyDown(key_name) # press the key

    To do more specific actions that needed some timing

    - [] auto.keyDown(key_name) # press the key
    - [] auto.keyUp(key_name) #release the key

### MOUSE

1. Controlling the mouse: auto.moveTo(x, y, duration = num_seconds)

    - moves to posion(x,y) in z seconds

    - Note: usual creen like 1080p we move from one end to the other in less
      than a second (.2 seconds or .4 seconds) games dont like if things go to
      fast, put sleep time in-between

```
    auto.click(button =button)
```

    or

```
    auto.click(x = moveToX, y = moveToY, clicks = num_of_clicks, interval =
      secs_between_clikcs, button='left')
```

## Image Searching

### Python-Imagesearch

1. Basics
    - take a screenshot of the screen
    - look for the image inside
    - return the position of said image

Example:

```
pos = imagesearch('github.png)
if pos[0]!= -1:
    print('position : ', pos[0], pos[1])
    auto.moveTo(pos[0], pos[1])
else:
    print('image not found')
```

This is how to use it but can be used to find out if an element present or not

```
auto.click(button='right')
    time.sleep(r(0.4, 0.2))
    # the r function returns .4 + .2 * random.random()
    presence = imagesearch('image_name')

    if(presence[0] == -1):
        # do things
```

Loops until something pops up.

```
pos = imagesearch_loop('image_name', 0.5)

print('image found' , pos[0], pos[1])
```

```
pos = imagesearch_loop('image_name', 0.5, 0, 0, 800,600)

print('image found' , pos[0], pos[1])
```

```
# non -optimized way :
time1 = time.clock()
for i in range(10):
    imagesearcharea("github.png", 0, 0, 800, 600)
    imagesearcharea("panda.png", 0, 0, 800, 600)
print(str(time.clock() - time1) + " seconds (non optimized)")
# optimized way :
time1 = time.clock()
im = region_grabber((0, 0, 800, 600))
for i in range(10):
    imagesearcharea("github.png", 0, 0, 800, 600, 0.8, im)
    imagesearcharea("panda.png", 0, 0, 800, 600, 0.8, im)
print(str(time.clock() - time1) + " seconds (optimized)")
# sample output :
# 1.6233619831305721 seconds (non optimized)
# 0.4075934110084374 seconds (optimized)
```
