# Ladybird MRI & Medical Scanner Viewer

## 📄 Description

This repository showcases a component of [Ladybird](#about-ladybird) dedicated to the visualization and manipulation of 3D medical images, including MRI and PET scans. Operating independently from the complete software suite, this component provides standalone capabilities for navigating and analyzing medical images.

The MRI viewer included in this repository provides robust tools for navigating and interacting with 3D medical images. It supports a wide range of common image formats, including NIfTI (compressed `.nii.gz` and uncompressed `.nii`) and DICOM. Users can load both clinical and research images, with several atlases accessible from the shared database. Key functionalities include zooming in on specific anatomical planes, rotating images, and applying various image processing filters. This tool is designed to facilitate detailed analysis and enhance the visualization of medical imaging data.

⚠️ Please note that this MRI viewer is still under development and has not been validated by any regulatory authority. It was developed as part of research projects and is intended as a side project with no major pretensions.

🌐 Access the app and start your analysis now at [https://medviewer.sotisanalytics.com](https://medviewer.sotisanalytics.com).

## ⚒️ Installation

### Prerequisites
- Python 3.11
- Python libraries
    ```sh
    pip install -r requiremetns_local.txt  # for PyQt6 GUI, and/or,
    pip install -r requiremetns_web.txt  # for Web GUI
    ```

## 📝 Usage

### Local version (PyQt GUI)

#### Running the application
To launch the MRI viewer, you can either execute the `main.py` script from the terminal or double-click the `main.bat` file to open the GUI automatically.

```sh
python main_local.py  # Launches the local GUI
```

![](images/image1.png)

### <span style="color:red">Update!</span> The app is now available on a Web GUI
The local version of the MRI viewer has been adapted for web deployment using Streamlit. This web version offers comparable functionalities as the local version, with a user-friendly interface accessible from any web browser. To run the web version, execute the `main_web.py` script and open the provided URL in your browser.
The web version of the MRI viewer is designed to be accessible and easy to use, with a streamlined interface that simplifies the process of loading and viewing medical images. While the local version offers more advanced features and capabilities, the web version provides a convenient alternative for users who prefer a browser-based interface.

```sh
streamlit run main_web.py  # Launches the web GUI
```

![](images/image2.png)

⚠️ The PyQt (local) version being less generic and more difficult to maintain, it will not be updated in the future. Only the web version will be maintained and updated if necessary.

## 📚 References
- MRI atlases: https://www.nitrc.org/projects/mricron
- Toolbar icones: https://icons8.com/

#### About Ladybird
Ladybird, developed during [L. Gardy's doctoral research](http://thesesups.ups-tlse.fr/5164/1/2021TOU30190.pdf) under the guidance of [E. Barbeau](https://cerco.cnrs.fr/page-perso-emmanuel-j-barbeau-ph-d/) (neuroscientist, CNRS) and [C. Hurter](http://recherche.enac.fr/~hurter/presentation.html) (engineer, ENAC), is a sophisticated software designed for the automatic detection of fast-ripples (FRs) in epilepsy. Originally developed by L. Gardy, with significant input from various researchers and medical professionals the early trials in the neurology department at Toulouse Hospital, along with support from various academic and economic entities, led to widespread enthusiasm and substantial funding, allowing for further development and eventual patenting ([Brevet: FR3128111](https://data.inpi.fr/brevets/FR3128111)). Ladybird was later rebranded as Halyzia©, a name change necessitated for trademark reasons, and is now being further developed and commercialized by the French startup Avrio MedTech.

<table style="width:100%;">
  <tr>
    <td style="width:50%;"><img src="images/ladybird1_v1.jpg" alt="Image 1" style="width:100%;"></td>
    <td style="width:50%;"><img src="images/ladybird2_v1.jpg" alt="Image 2" style="width:100%;"></td>
  </tr>
  <tr>
    <td style="width:50%;"><img src="images/ladybird3_v1.jpg" alt="Image 3" style="width:100%;"></td>
    <td style="width:50%;"><img src="images/ladybird4_v1.jpg" alt="Image 4" style="width:100%;"></td>
  </tr>
  <tr>
    <td style="width:50%;"><img src="images/ladybird5_v1.jpg" alt="Image 5" style="width:100%;"></td>
    <td style="width:50%;"><img src="images/ladybird6_v1.jpg" alt="Image 6" style="width:100%;"></td>
  </tr>
</table>

## 👤 Author
- LinkedIn: [Ludovic Gardy](https://www.linkedin.com/in/ludovic-gardy/)
- Doctoral thesis: [PDF](http://thesesups.ups-tlse.fr/5164/1/2021TOU30190.pdf)