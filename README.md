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
```


### **RGB Workflow**

```bash
0. Save all images in one folder.

1. Run:
   python bipRGBImageCheck2.py -sf <source_folder> -ext <.extension> -tf <target_folder>
   # Checks total number of images, renames and combines them into a 'renamed' folder.

2. Run:
   metashape.exe -r bipRGBImageAlignment2.py -sf <source_folder> -ext <.extension> -tf <target_folder>
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
### **multispectral Workflow**
> *(Similar workflow to RGB)*

```bash
0. Save all multispectral images in one folder.

1. Run:
   python bipRPImageCheck2.py <source_folder>

2. Run:
   metashape.exe -r bipRPImageAlignment.py -wp <project_path>

3. Run:
   metashape.exe -r bipRPImageAlignment.py -wp <project_path>
   # Generates DSM and orthomosaic.

4. Render multispectral RGB-style composite:
   python3 rasterRenderRGB.py -s <orthomosaic_path>
```
