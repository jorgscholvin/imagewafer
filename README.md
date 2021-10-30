# imagewafer
Simple PY code to generate an image wafer using phidl

Install phidl first

imageWafer.py --  Conversion script
mitnano.jpg --  Sample image
imageWafer.zip --  GDS file output as example (136 MB)

Run py script, and modify the parameters to use your own image & texts, or adjust pixel sizes.

Don't use too many small pixels (harder to modulate brightness on a 5 um pixel than a 50 um pixel, and large number of pixels can cause slow conversion)

--=--=--=--=--

Tips:

GDS files can be viewed/edited with CAD (e.g. KLayout)

If file conversion on MLA150 gets stuck, use CAD software to flatten GDS and remove all hierarcy/cells.
Phidl outputs have caused some issues in the past for us with the MLA150 conversion software (clutter in the virtualbox filesystem that's slowing things down until manually cleaned up)

Before converting, know how to clean up the virtualbox on the MLA. Using offline conversion is usually faster.
