import os
import cv2
import numpy as np
from pathlib import Path
from ultralytics import YOLO

# ====================== 路径直接写死 (绝对路径) ======================
INPUT_DIR = "image"
OUTPUT_DIR = "output/image"
MODEL_PATH = "yolov/runs/blade_seg_100imgs_fixed/weights/best.pt"

# 推理配置
CONF_THRES = 0.35
IMG_SIZE = 640

# 🌟 加速配置：GrabCut 的最高运算维度 (像素)
GRABCUT_MAX_DIM = 600


# ===================================================================

def run_extraction():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        print(f"📁 已创建输出目录: {OUTPUT_DIR}")

    print(f"⏳ 正在加载模型: {MODEL_PATH}")
    try:
        model = YOLO(MODEL_PATH)
    except Exception as e:
        print(f"❌ 报错：找不到模型文件，请检查路径是否正确。\n错误信息: {e}")
        return

    extensions = (".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff", ".JPG")
    img_list = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith(extensions)]

    if not img_list:
        print(f"❌ 报错：在 {INPUT_DIR} 没找到任何图片！")
        return

    print(f"🔍 找到 {len(img_list)} 张图片，开始处理多叶片提取...")

    for img_name in img_list:
        full_path = os.path.join(INPUT_DIR, img_name)
        stem_name = os.path.splitext(img_name)[0]

        raw_data = np.fromfile(full_path, dtype=np.uint8)
        img = cv2.imdecode(raw_data, cv2.IMREAD_COLOR)
        if img is None:
            print(f"⚠️ 跳过无法读取的图片: {img_name}")
            continue

        results = model.predict(source=full_path, imgsz=IMG_SIZE, conf=CONF_THRES, retina_masks=True, verbose=False)[0]

        if results.masks is None:
            print(f"💡 图片 {img_name} 未检测到叶片，跳过。")
            continue

        h_img, w_img = img.shape[:2]

        for idx, (mask_xy, box) in enumerate(zip(results.masks.xy, results.boxes.xyxy), 1):

            initial_mask = np.zeros((h_img, w_img), dtype=np.uint8)
            pts = mask_xy.astype(np.int32).reshape((-1, 1, 2))
            cv2.fillPoly(initial_mask, [pts], 255)

            x1, y1, x2, y2 = map(int, box)
            pad = 50
            x1, y1 = max(0, x1 - pad), max(0, y1 - pad)
            x2, y2 = min(w_img, x2 + pad), min(h_img, y2 + pad)

            roi_img = img[y1:y2, x1:x2]
            roi_mask = initial_mask[y1:y2, x1:x2]
            h_roi, w_roi = roi_img.shape[:2]

            # ==========================================================
            # 🚀 第三步：闪电加速核心 —— 生成缩小版“替身”
            # ==========================================================
            max_current_dim = max(h_roi, w_roi)

            if max_current_dim > GRABCUT_MAX_DIM:
                scale = GRABCUT_MAX_DIM / max_current_dim
                new_w, new_h = int(w_roi * scale), int(h_roi * scale)
                small_img = cv2.resize(roi_img, (new_w, new_h), interpolation=cv2.INTER_AREA)
                small_mask = cv2.resize(roi_mask, (new_w, new_h), interpolation=cv2.INTER_NEAREST)
            else:
                small_img, small_mask = roi_img, roi_mask
                new_w, new_h = w_roi, h_roi

            # ==========================================================
            # ✨ 第四步：带有“探索区”强制扩充的 GrabCut
            # ==========================================================
            gc_mask = np.full((new_h, new_w), cv2.GC_PR_BGD, dtype=np.uint8)

            bg_margin = max(3, int(10 * (new_w / w_roi)))
            gc_mask[:bg_margin, :] = cv2.GC_BGD
            gc_mask[-bg_margin:, :] = cv2.GC_BGD
            gc_mask[:, :bg_margin] = cv2.GC_BGD
            gc_mask[:, -bg_margin:] = cv2.GC_BGD

            # 1. 腐蚀提取核心种子 (绝对叶片)
            k_size_erode = max(3, int(7 * (new_w / w_roi)))
            k_size_erode = k_size_erode if k_size_erode % 2 != 0 else k_size_erode + 1
            core_kernel = np.ones((k_size_erode, k_size_erode), np.uint8)
            core_leaf = cv2.erode(small_mask, core_kernel, iterations=2)

            # 2. 🌟 关键新增：强行膨胀生成“探索区” (可能叶片)
            # 让算法知道：别那么早就停下！向外扩 5~15 个像素的范围内，都有可能是叶子！
            k_size_dilate = max(5, int(15 * (new_w / w_roi)))  # 动态计算膨胀核
            k_size_dilate = k_size_dilate if k_size_dilate % 2 != 0 else k_size_dilate + 1
            dilate_kernel = np.ones((k_size_dilate, k_size_dilate), np.uint8)
            search_zone = cv2.dilate(small_mask, dilate_kernel, iterations=2)

            # 3. 赋值标记：探索区为可能前景，核心区为绝对前景
            gc_mask[search_zone == 255] = cv2.GC_PR_FGD
            gc_mask[core_leaf == 255] = cv2.GC_FGD

            bgdModel = np.zeros((1, 65), np.float64)
            fgdModel = np.zeros((1, 65), np.float64)

            try:
                cv2.grabCut(small_img, gc_mask, None, bgdModel, fgdModel, iterCount=3, mode=cv2.GC_INIT_WITH_MASK)
            except Exception as e:
                print(f"⚠️ GrabCut 处理异常跳过: {e}")
                continue

            small_current_mask = np.where((gc_mask == cv2.GC_FGD) | (gc_mask == cv2.GC_PR_FGD), 255, 0).astype('uint8')

            # ==========================================================
            # 🚀 第五步：放大掩膜 + 实心填充
            # ==========================================================
            if max_current_dim > GRABCUT_MAX_DIM:
                current_mask = cv2.resize(small_current_mask, (w_roi, h_roi), interpolation=cv2.INTER_NEAREST)
            else:
                current_mask = small_current_mask

            # 寻找最外层轮廓并涂满，消灭 GrabCut 偶尔产生的内腔空洞
            contours, _ = cv2.findContours(current_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if contours:
                max_contour = max(contours, key=cv2.contourArea)
                current_mask = np.zeros_like(current_mask)
                cv2.drawContours(current_mask, [max_contour], -1, 255, thickness=cv2.FILLED)

            # === 第六步：还原到白底 ===
            white_bg = np.full((h_roi, w_roi, 3), 255, dtype=np.uint8)

            fg = cv2.bitwise_and(roi_img, roi_img, mask=current_mask)
            inv_mask = cv2.bitwise_not(current_mask)
            bg = cv2.bitwise_and(white_bg, white_bg, mask=inv_mask)
            final_crop = cv2.add(fg, bg)

            # 5. 保存结果
            # 5. 保存结果
            save_filename = f"{stem_name}_{idx}.jpg"
            save_path = os.path.join(OUTPUT_DIR, save_filename)

            _, img_encode = cv2.imencode('.jpg', final_crop)
            img_encode.tofile(save_path)
            print(f"✅ 处理完成: {save_filename} (已强制扩充探索区并填补空洞)")

            # ==================== 保存边界框（修正文件名格式） ====================
            box_filename = f"{stem_name}_{idx}_box.txt"   # 例如：DSC_3788_1_box.txt
            box_path = os.path.join(OUTPUT_DIR, box_filename)
            with open(box_path, 'w') as f:
                f.write(f"{x1} {y1} {x2} {y2}")
            print(f"   📦 已保存边界框: {box_filename}")
    print(f"\n✨ 全部任务已完成！输出位置: {OUTPUT_DIR}")


if __name__ == "__main__":
    run_extraction()