# 🍃 Ultra-High-Resolution Wind Blade Flow Field Quantification System
> Industrial CV project with Goldwind: 8K wind turbine blade image flow field quantification via YOLOv8-Seg & U-Net cascade architecture. *(Paper under review at **Wind Energy**)*

<!-- [这里插入图片：项目横幅或成果概览图] -->
<!-- 建议图片：放一张最具视觉冲击力的 8K 原始图像与最终提取出分离角的对比图，或者带有金风科技/项目名称的精美 Banner。 --><img width="4753" height="3172" alt="DSC_7029_1_FULL_OVERLAY" src="https://github.com/user-attachments/assets/3255d565-0b32-4733-9d55-84d2ed1403d1" />



[![Project Status](https://img.shields.io/badge/Status-Industrial%20R%26D%20Collaboration-blue)](#)
[![Target Journal](https://img.shields.io/badge/Target-Wind%20Energy%20(Top%20Journal)-orange)](#)
[![Role](https://img.shields.io/badge/Role-CV%20Algorithm%20Lead-green)](#)

---

## 📌 Project Overview
Developed in collaboration with **Goldwind (金风科技)**, this system automates high-precision measurement of deflection angles of microscopic wool yarns (10–20 pixels) on wind turbine blade surfaces using **8K high-definition inspection images**. The quantitative flow-field output directly serves wind turbine stall detection and aerodynamic optimization.

### 📊 Key Performance Indicators (KPIs)
| Metric | Performance | Remarks |
| :--- | :--- | :--- |
| **Wool Yarn Recall** | **> 95%** | Evaluated on 80 real inspection scenes (22,326 yarn targets) |
| **False Positive Rate** | **< 2%** | Robust against extreme dark/bright lighting & line-array noise |
| **Annotation Efficiency** | **20x Boost** | Reduced single-image labeling time from 10 mins to **< 30 secs** |

---

## ⚙️ Pipeline Architecture

<!-- [这里插入图片：系统全流程架构图] -->
<!-- 建议图片：放一张算法流水线图（Pipeline），展示从输入 8K 图像 -> YOLOv8 分割叶片 -> 自适应二值化 -> U-Net 提取毛线 -> 输出角度的完整流程图（如 PPT 中的架构图导出为 PNG）。 -->


<img width="1280" height="667" alt="图片1" src="https://github.com/user-attachments/assets/dd61c2a3-f733-4568-8d55-54d01778d3f2" />

🏗 Key Technical Highlights
1. Cascaded Segmentation Architecture
ROI Decoupling: Deployed YOLOv8-Seg for coarse blade localization, eliminating complex background interference. Integrated GrabCut for micro-edge refinement to retain precise blade contours in 8K downsampled spaces.

Binary-Space Topology U-Net: Innovatively shifted training from RGB space to a binary-texture space based on the premise that color/shadow is noise, structural geometry is signal.

RGB Space Accuracy: < 30% (severe overfitting to dynamic lighting)

Binary Space Accuracy: > 90% (invariant to shadows and strong reflections)

2. Interactive Semi-Automated Annotation Tool
Engineered a tailored GUI tool using Connected Component Analysis (CCA) and "click-and-draw" selection logic.

Enabled zero-threshold, pixel-level line selection, lowering dataset curation overhead by 95%.

3. Quantitative Post-Processing & Angle Calculation
Formulated projection variance maximization to calculate wool yarn orientation vectors.

Established dynamic reference coordinate systems anchored to blade edges, filtering stray noise through row/column geometric spacing constraints.

🔒 Confidentiality & NDA Notice
Notice: Due to Non-Disclosure Agreements (NDA) with corporate partners and ongoing journal review processes (Wind Energy), production source code, 8K raw datasets, and deployment models are hosted in a Private Repository.

If you are a recruiter, researcher, or engineer interested in cascaded segmentation, industrial image processing, or dynamic reference math, feel free to reach out!

📩 Contact: 2445165372@qq.com
