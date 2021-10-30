# -*- coding: utf-8 -*-
"""
Simple Image Wafer -- https://github.com/jorgscholvin/imagewafer
Oct 2021

This code requires phidl (see https://github.com/amccaugh/phidl)

@author: Jorg Scholvin
"""
from phidl import Device
import phidl.geometry as pg
from PIL import Image
import math

def waferlabel(mc):
    D = Device('header')
    # , font='Arial'
    # place the text messages and the ring
    D << pg.text(text=mc.label.text, size=mc.label.size, justify='center', layer=0, font=mc.label.font ).move( (0,mc.label.position) )
    D << pg.text(text=mc.label.text2, size=mc.label.size, justify='center', layer=0, font=mc.label.font).move( (0,mc.label.position - mc.label.size*1.5) )
    D << pg.arc(radius = mc.innerradius, width = mc.arcwidth, theta = 360, layer = 0)

     # add small print notes
    y = mc.notes.position
    for msg in mc.notes.randomMessages:
        D << pg.text(text=msg, size=mc.notes.size, justify='center', layer=0, font=mc.notes.font).move( (0,y) )
        y = y - mc.notes.size*2
    
    # optional random litho test structures
    D << pg.litho_steps(
            line_widths = [1,2,3,4,5,6,7,8,9,10,20,30,40],
            line_spacing = 2,
            height = 500,
            layer = 0
            ).move( (500,-zoomwafer.innerradius + 2000) )
    D << pg.litho_steps(
            line_widths = [1,2,3,4,5,6,7,8,9,10,20,30],
            line_spacing = 10,
            height = 500,
            layer = 0
            ).move( (-500,-zoomwafer.innerradius + 2000) )
    D << pg.litho_star(
            num_lines = 20,
            line_width = 2,
            diameter = 200,
            layer = 0
            ).move( (-1500,-zoomwafer.innerradius + 2000) )

    return D

# use cells for each pixel to reuse and keep the amount of data low'ish
def precalcPixels(mc):
    linectr = math.floor(mc.pixel/mc.grating.pitch)
    pixelDevices = []
    for m in range(256):
        PX = Device()
        if mc.grating.omit:
            value = pow(m/255, 0.9)
            Wline = value*(mc.pixel-mc.pixelspacing-mc.minsize)+mc.minsize
            PX << pg.rectangle(size=(Wline, Wline), layer=mc.layer)
            pixelDevices.append(PX)
        else:
            value = pow(m*1.0/255, 0.7)
            Nmax = max(2, min(linectr, math.ceil(linectr*value)))
            Wline = value*(mc.pixel-mc.pixelspacing-mc.minsize)+mc.minsize
            for n in range(Nmax):
                PX << pg.rectangle(size=(Wline, mc.grating.width), layer=mc.layer).move((-Wline/2+mc.pixel/2, n*mc.grating.pitch))
            pixelDevices.append(PX.move((-mc.pixel/2, -mc.pixel/2)))
    return pixelDevices

def drawImage(mc,im,pd):
    # draw the image, and add border. center image
    width, height = im.size
    scale = min( mc.maxwidth/mc.pixel/width , mc.maxheight/mc.pixel/height )
    im1 = im.resize(  (math.floor(scale*width),math.floor(scale*height)) )
    pix=im1.load()
    width, height = im1.size
    D = Device('image')
    for x in range(width):
        for y in range(height):
            x0 = x * mc.pixel - width*mc.pixel/2
            y0 = y * mc.pixel - height*mc.pixel/2        
            n=math.floor(pow(pix[x,height-1-y]/255,1.05)*255)
            if (abs(y0)<mc.maxY):
                if (math.sqrt(x0*x0+y0*y0)<mc.maxR):
                    D.add_ref(pd[n]).move( (x0,y0) )                    
    im1.close()
    IW  = width*mc.pixel + 2*mc.framespace
    IH = height*mc.pixel + 2*mc.framespace
    FW = mc.framewidth
    if (FW>0):
        D.add_polygon([ (0,0), (0,IH), (IW,IH), (IW,0), (0,0), (0,-FW), (IW+FW,-FW), (IW+FW,IH+FW), (-FW,IH+FW), (-FW,-FW), (0,-FW), (0,0) ] ).move( (-IW/2-mc.pixel/2, -IH/2-mc.pixel/2) )
    return D

# pass parameters in as an object
class EmptyClass:
    pass

# general parameters, modify as needed - common customized fiels marked by <<<
zoomwafer = EmptyClass()
zoomwafer.label=EmptyClass()
zoomwafer.label.text='MIT.nano 2021'   # top header <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
zoomwafer.label.text2='FAB Tour @ MIT.nano'    # 2nd line <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
zoomwafer.label.size=4000
zoomwafer.label.position = 50000
zoomwafer.label.font = 'Calibri'
zoomwafer.notes = EmptyClass()  # small print at the bottom
zoomwafer.notes.size = 1000
zoomwafer.notes.position = -50000
zoomwafer.notes.font = 'Calibri'
zoomwafer.notes.randomMessages = ['Small print at the bottom', 'For secret messages or to say hello']        # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# wafer details, innerradius is the ring of width arcwidth, make sure to pick radius so it doesn't run into the flat
zoomwafer.radius = 75000
zoomwafer.innerradius = 65000
zoomwafer.arcwidth = 1000

# pixel parameters
zoomwafer.pixel = 60                  # size of each pixel area <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
zoomwafer.pixelspacing = 1.0          # gap between pixels, should be small but printable (as pixels value 255 will have this gap)
zoomwafer.minsize = 4                 # pixel values 0 will be this size.  So pixels 0...255 will be brom minsize...pixel, to avoid washing out pixels that are too small
# also, if a dark area of the image has no metal at all, it looks weird (noticable absence)
zoomwafer.layer = 1
# area of the final image. # pixels is maxwidth/pixel. having too many pixels will make things slow/large files
# especially if grating used, so don't go crazy with trying to get super high-resolution
zoomwafer.maxwidth  = 130000 
zoomwafer.maxheight = 130000
# truncate image so it says within the circle and in the vertical range (to avoid running into other features)
zoomwafer.maxY = 40000
zoomwafer.maxR = 64000
# option to draw a frame around the image, if width not zero. frame is offset by space
zoomwafer.framewidth= 0
zoomwafer.framespace = 25
# if we want to make gratings as pixels, details here:
# pitch & width - make sure spacing is sufficient to get good litho, and width is large enough to not wash out in the wet etch
# better err on the side of caution than go overly aggressive
zoomwafer.grating = EmptyClass()
zoomwafer.grating.pitch = 5.5
zoomwafer.grating.width = 4.0
zoomwafer.grating.omit = False          # set to true if simple boxes and not gratings <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

# pre-calc pixels so we can add references
print("generating pixels")
pixelDevices = precalcPixels(zoomwafer)

# generate the layout. add labels, then the image. Image is its own device to make it
# easier to add multiple images, or to center the image
print("drawing wafer")
D = Device('wafer')
D << waferlabel(zoomwafer)
D12 = Device('images')
print("drawing image... this can take a while")
D12.add_ref(drawImage(zoomwafer,Image.open('mitnano.jpg').convert('L'),pixelDevices))
[[x_min, y_min], [x_max, y_max]] = D12.get_bounding_box()
dx = (x_max-x_min)/2 + x_min
dy = (y_max-y_min)/2 + y_min
D << D12.move(  (-dx,-dy) )

# export into gds. you can flatten manually, if MLA150 conversion gets confused or requires too many resources
#D.flatten() <<< but don't use the phidl flattening, it's too slow & resource hungry
print("exporting")
D.write_gds('imageWafer.gds')
print("please open gdsii in CAD, flatten image and remove any hierarcy or empty cells")