# High-Res-Blade-CV-System
Industrial CV project with Goldwind: 8K wind blade image flow field quantification using YOLOv8-Seg &amp; U-Net cascade architecture. (Paper under review)
# Ultra-High-Resolution Wind Blade Image Flow Field Quantification System

[![Project Status](https://img.shields.io/badge/Status-Industrial%20Collaboration-blue)]()
[![Target Journal](https://img.shields.io/badge/Target-Wind%20Energy%20(Top%20Journal)-orange)]()
[![Role](https://img.shields.io/badge/Role-CV%20Algorithm%20Lead-green)]()

## 📌 Project Overview
This project is an industrial R&D collaboration with **Goldwind (金风科技)**. The goal is to achieve automated, high-precision measurement of deflection angles of extremely fine wool yarns on wind turbine blade surfaces using **8K high-definition inspection images**, providing core quantitative data for wind turbine stall analysis.

### 🎯 Key Challenges Addressed
- **Extreme Resolution Interference:** Processing 8K images while capturing microscopic features (fine wool yarns) against complex and dynamic lighting backgrounds[cite: 1].
- **High Computational Overhead:** Balancing real-time/efficient inference with heavy semantic segmentation loads[cite: 1].
- **High Annotation Costs:** Overcoming the scarcity and high cost of pixel-level labels for tiny, complex structures[cite: 1].

---

## 🏗 System Architecture & Technical Highlights

### 1. Cascade Recognition Architecture (YOLOv8-Seg + U-Net)
- **ROI Localization & Decoupling:** Leveraged **YOLOv8-Seg** for robust blade region-of-interest (ROI) extraction, successfully decoupling the blade from complex background interference[cite: 1].
- **Topology Modeling via "Feature Dimensionality Reduction":** Innovatively proposed an adaptive binarization-guided U-Net framework to strip away complex shadow/lighting noise, achieving pixel-level segmentation of extremely fine wool yarns[cite: 1].
- **Performance Metrics:** Achieved a **95% recall rate** with a **false positive rate of less than 2%** on real-world industrial test sets[cite: 1].

### 2. Engineering Efficiency: Interactive Semi-Auto Annotation Tool
- Developed an in-house interactive semi-automatic annotation program based on **connected component analysis (连通域分析)**[cite: 1].
- Implemented an intuitive "click-and-draw" selection logic[cite: 1].
- **Result:** Boosted single-image annotation efficiency by **20x**[cite: 1], drastically lowering data curation overhead for the team.

### 3. Quantitative Analysis & Dynamic Reference Systems
- Implemented spatial clustering algorithms for wool yarns.
- Established a dynamic reference coordinate system to automatically compute precise deflection angles[cite: 1].
- Validated rigorously through Goldwind's business and operational standards[cite: 1].

---

## 🔒 Confidentiality Notice
> **Note:** Due to strict Non-Disclosure Agreements (NDA) with corporate partners and pending academic submissions (*Wind Energy*), the production-level source code, proprietary 8K datasets, and deployment scripts are kept in a **Private Repository**. 
> 
> If you are a recruiter or researcher interested in discussing the algorithm design (Cascade Segmentation, Feature Dimensionality Reduction, or Industrial CV Engineering), feel free to contact me at **2445165372@qq.com**[cite: 1]!
