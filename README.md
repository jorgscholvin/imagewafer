# imagewafer
Simple PY code to generate an image wafer using phidl

Modify the parameters to use your own image & texts, or adjust pixel sizes.

Install phidl first

~~~

Tips:

GDS files can be viewed/edited with CAD (e.g. KLayout)

If file conversion on MLA150 gets stuck, use CAD software to flatten GDS and remove all hierarcy/cells.
Phidl outputs have caused some issues in the past for us with the MLA150 conversion software (clutter in the virtualbox filesystem that's slowing things down until manually cleaned up)

Before converting, know how to clean up the virtualbox on the MLA. Using offline conversion is usually faster.
