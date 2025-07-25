# Structure-from-Motion (SfM) Processing Pipeline

This repository contains a Python-based SfM processing pipeline using [Agisoft](https://www.agisoft.com/) (or your software of choice) and custom scripts for automated photogrammetry-based reconstruction of orthomosaics DEMs from drone imagery.

The workflow includes:
- Image checking  
- Alignment  
- Model generation  
- Visualization

> *(Plot-level and batch processing will be added soon)*

---

## 📁 Repository Structure
```bash
SfM_Pipeline/
├── bip/                  # Python scripts for each pipeline stage
├── PyPlotExtraction/     # Plot-level processing scripts
└── README.md             # Project documentation

8_trait_extract_dem/
├── dem_by_plot/                 ← 1-band DEM .tif files per plot (in cm)
├── masks_overlapping/          ← binary masks for each plot image (same size/filename as DEM)
├── mulch_height/
│   └── AS_S2.xlsx              ← Excel file with ground (mulch) height reference per plot
└── metashape_report/
    └── gsd_4_all.xlsx          ← Excel file with GSD (mm/pix) per date (used to convert px² to cm²)

```


### **RGB Workflow**

```bash
0. Save all images in one folder.

1. Run:
   python bipRGBImageCheck2.py -sf <project_path> -ext <.extension> -tf <project_path>
   # Checks total number of images, renames and combines them into a 'renamed' folder.

2. Run:
   metashape.exe -r bipRGBImageAlignment2.py -sf <project_path> -ext <.extension> -tf <project_path>
   # Aligns images in Metashape.

3. For regular dataset size:
   metashape.exe -r bipRGBModelGeneration.py -wp <project_path>
   # Exports DSM and orthomosaic.

4. For large datasets (divided into sections):
   metashape.exe -r bipRGBModelGeneration2.py -wp <project_path>
   # Exports DSM and orthomosaic by region.

# 5. (Optional) Export point cloud:
#    python bipExportPointCloud.py -wp "<project_path>.psx" -pc 1

6. Render RGB orthomosaic:
   python3 rasterRenderRGB.py -s <orthofilepath>
   # Renders RGB image for visualization.
```
### **Multispectral Workflow**
> *(Similar workflow to RGB)*

```bash
0. Save all multispectral images in one folder.

1. Run:
   python bipRPImageCheck2.py <project_path>

2. Run:
   metashape.exe -r bipRPImageAlignment.py -wp <project_path>

3. Run:
   metashape.exe -r bipRPModelGeneration.py -wp <project_path>
   # Generates DSM and orthomosaic.

4. Render multispectral RGB-style composite:
   python3 rasterRenderRGB.py -s <orthofilepath>
```
