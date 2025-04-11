
---

# SUN-DIC

**Stellenbosch University Digital Image Correlation (DIC) Code**

---

## Important Notice

This is an early release of the Stellenbosch University DIC Code, referred to as **SUN-DIC**. The code includes the following features and limitations. If you encounter issues or have suggestions for improvement, please contact the author. Additional documentation will be provided in future updates.

---

## Limitations

1. Currently supports only 2D planar problems (a stereo version is under development).
2. Only rectangular regions of interest (ROI) can be specified. However, subsets with an all-black background (based on a user-defined threshold) is ignored thus allowing the code to handle irregularly shaped domains.
3. Limited documentation.  Please see the `settings.ini` file for complete documentation on on the options and the `test_sundic.ipynb` file as a working example of using the API.

---

## Key Features

1. Fully open-source, utilizing standard Python libraries wherever possible.
2. Offers both a user-friendly GUI and an API for interaction.
3. Implements the Zero-Mean Normalized Sum of Squared Differences (ZNSSD) correlation criterion.
4. Features an advanced starting strategy using the AKAZE feature detection algorithm for initial guess generation.
5. Supports both linear (affine) and quadratic shape functions.
6. Includes Inverse Compositional Gauss-Newton (IC-GN) and Inverse Compositional Levenberg-Marquardt (IC-LM) solvers.
7. Provides absolute and relative update strategies for handling multiple image pairs.
8. Computes displacements and strains.
9. Utilizes Savitzky-Golay smoothing for strain calculations.  Displacements can also be smoothed using the same algorithm.
10. Supports parallel computing for improved performance.
11. Easy installation via [PyPI](https://pypi.org/project/SUN-DIC/).

---

## Installation

Although installation can be performed without creating a virtual environment, it is highly recommended to use one for easier dependency management.

### General Steps

1. Create a virtual environment.
2. Activate the virtual environment.
3. Install the package from [PyPI](https://pypi.org/project/SUN-DIC/).
4. Optionally, download the following files and folders for a complete working example:
   - `test_sundic.ipynb`
   - `settings.ini`
   - `planar_images` folder
   These can be found in this repository and provide a practical starting point for using both the API or GUI.

---

### Using `pip`

1. Create a virtual environment (e.g., `sundic`):
   ```
   python3 -m venv sundic
   ```
2. Activate the virtual environment:
   ```
   source sundic/bin/activate
   ```
3. Install the package:
   ```
   pip install SUN-DIC
   ```

---

### Using `conda`

1. Create a virtual environment (e.g., `sundic`) with Python pre-installed:
   ```
   conda create -n sundic python=3.11
   ```
2. Activate the virtual environment:
   ```
   conda activate sundic
   ```
3. Install the package:
   ```
   pip install SUN-DIC
   ```

---

### Installing Directly from GitHub (Advanced users only)

1. Create and activate a virtual environment using either `pip` or `conda` as outlined above.
2. Clone the repository and install the package:
   ```
   git clone https://github.com/gventer/SUN-DIC.git
   pip install ./SUN-DIC
   ```

---

## Usage

Make sure the virtual environment where `SUN-DIC` is installed is active before proceeding.

### Starting the GUI

1. Type `sundic` in the terminal to launch the GUI.
2. Download the `planar_images` folder from this repository for example image data.
3. Follow the workflow outlined on the left-hand side of the GUI. Hovering over any entry provides helpful tooltips.

<img src="screenshots/settings.png" width="450"> <img src="screenshots/image_set.png" width="450"> <img src="screenshots/roi.png" width="450">
<img src="screenshots/analyze.png" width="450"> <img src="screenshots/results.png" width="450">

---

### Using the API

1. Download the following files from this repository:
   - `test_sundic.ipynb`
   - `settings.ini`
   - `planar_images` folder
2. Open the `test_sundic.ipynb` Jupyter Notebook for a detailed working example.
3. The typical workflow involves:
   - Modifying the `settings.ini` file.
   - Running the DIC analysis.
   - Post-processing the results.
4. While the example uses a Jupyter Notebook, the API can also be used in standard Python `.py` scripts.

---

## API Documentation

Detailed API documentation is available at:

[https://gventer.github.io/SUN-DIC](https://gventer.github.io/SUN-DIC/)

---

## Acknowledgments

- **SUN-DIC Analysis Code**: Based on work by Ed Brisley as part of his MEng degree at Stellenbosch University. His thesis is available at the [Stellenbosch University Library](https://scholar.sun.ac.za/items/7a519bf5-e62b-45cb-82f1-11f4969da23a).
- **Interpolator**: Utilizes `fast_interp` by David Stein, licensed under Apache 2.0. Repository: [fast_interp](https://github.com/dbstein/fast_interp).
- **Smoothing Algorithm**: Implements the 2D Savitzky-Golay algorithm from the [SciPy Cookbook](https://scipy-cookbook.readthedocs.io/items/SavitzkyGolay.html).
- **GUI Development**: Developed by [Elijah Stockhall](https://github.com/EMStockhall/).

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Authors

Developed by [Gerhard Venter](https://github.com/gventer/).

---
