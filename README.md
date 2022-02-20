# 1. MRI viewer
This simple app allow users to navigate through 3D medical images such as MRI or PET scans. The most common image formats are accepted:
1. NIfTI
2. DICOM
3. Compressed files

Clinical/research images can be loaded. Several atlases are also available in the shared database. On the other hand, users can either:
- Zoom in on an anatomical plan
- Rotate images
- Apply kernels

# 2. Example using the GUI
To run the program, user can either open the script "_**start_app.py**_" using the terminal, or simply double click the "_**start_app**_" file, that should automatically launch the GUI.

```
> cd root\Ladybird_MRI_viz
> python start_app.py
```

![](fullpannel_and_zoom.png)

# 3. Dependencies
cv2==4.5.5
imageio==2.14.1
pydicom==2.2.2
PyQt5==5.15.6
matplotlib==3.5.1
nibabel==3.2.1
numpy==1.21.5
scipy==1.7.3
