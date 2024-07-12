# Halyzia© / Ladybird MRI & Medical Scanner Viewer

## Description
Halyzia©, also known as Ladybird, is a sophisticated software designed for the automatic detection of fast-ripples (FRs) in epilepsy, as described in the [doctoral thesis of L. Gardy](http://thesesups.ups-tlse.fr/5164/1/2021TOU30190.pdf) and patented under [Brevet: FR3128111](https://data.inpi.fr/brevets/FR3128111). This repository showcases a component of Halyzia© that is focused on the visualization and manipulation of 3D medical images such as MRI and PET scans. This component is designed to function independently of the complete software suite, providing standalone capabilities for medical image navigation and analysis.

### MRI viewer
The MRI viewer included in this repository offers powerful tools to navigate and interact with 3D medical images. It supports a variety of common image formats:

- NIfTI
- DICOM
- Compressed files

Users can load both clinical and research images, and several atlases are accessible within the shared database. Key functionalities include:

- Zooming in on specific anatomical planes
- Rotating images
- Applying various image processing kernels

## Installation

### Prerequisites
- Python 3.11
- Python libraries: see requirements.txt

## Usage

### Running the application
To launch the MRI viewer, you can either execute the `main.py` script from the terminal or double-click the `main.bat` file to open the GUI automatically.

```sh
python main.py  # Launches the GUI
```

![](images/image1.png)

## References
- MRI atlases: https://www.nitrc.org/projects/mricron
- Toolbar icones: https://icons8.com/

## Author
- LinkedIn: [Ludovic Gardy](https://www.linkedin.com/in/ludovic-gardy/)
- Doctoral thesis: [PDF](http://thesesups.ups-tlse.fr/5164/1/2021TOU30190.pdf)