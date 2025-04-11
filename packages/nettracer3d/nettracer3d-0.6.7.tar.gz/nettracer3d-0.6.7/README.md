NetTracer3D is a python package developed for both 2D and 3D analysis of microscopic images in the .tif file format. It supports generation of 3D networks showing the relationships between objects (or nodes) in three dimensional space, either based on their own proximity or connectivity via connecting objects such as nerves or blood vessels. In addition to these functionalities are several advanced 3D data processing algorithms, such as labeling of branched structures or abstraction of branched structures into networks. Note that nettracer3d uses segmented data, which can be segmented from other softwares such as ImageJ and imported into NetTracer3D, although it does offer its own segmentation via intensity and volumetric thresholding, or random forest machine learning segmentation. NetTracer3D currently has a fully functional GUI. To use the GUI, after installing the nettracer3d package via pip, enter the command 'nettracer3d' in your command prompt:


This gui is built from the PyQt6 package and therefore may not function on dockers or virtual envs that are unable to support PyQt6 displays. More advanced documentation is coming down the line, but for now please see: https://www.youtube.com/watch?v=cRatn5VTWDY
for a video tutorial on using the GUI.

NetTracer3D is free to use/fork for academic/nonprofit use so long as citation is provided, and is available for commercial use at a fee (see license file for information).

NetTracer3D was developed by Liam McLaughlin while working under Dr. Sanjay Jain at Washington University School of Medicine.

-- Version 0.6.7 updates --

1. Updated all methods to use dilation to allow the user to select between perfect distance transform based dilation (which can be slower but allows for perfect searching - and is designed to account for scaling differences), or the current pseudo-3d kernel method.

1.5. The dt dilator accounts for scaling by stretching (upsampling) images to equivalent scales before dilating with the distance transform. It will not attempt to downsample. This admittedly will ask for greater memory and some more processing. To give the user the option to use the dt dilator without dealing with this, I added two new options to the resize method. You can now have it upsample your image until its equivalently scaled, or, if you don't need the fidelity, downsample your image until it's equivalently scaled. When the scaling is equivalent, the dt dilator will always just use the regular distance transform without attempting to resize the array.

2. Fixed radius finding method to also account for scaling correctly. Previous method scaled wrong. New method predictably accounts for differing scaling in xy vs z dims as well.

3. Bug fixes.