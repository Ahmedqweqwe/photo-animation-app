import streamlit as st
import cv2
import numpy as np
import math
import os

st.set_page_config(page_title="تطبيق مؤثرات الصور", page_icon="🎬", layout="centered")

st.title("🎬 صانع المؤثرات الحركية الضوئية")
st.write("ارفع صورتك (يفضل أن تحتوي على إضاءة أو ألوان زاهية) لتحويلها إلى فيديو ينبض بالحياة!")

# 1. رفع الصورة من قبل المستخدم
uploaded_file = st.file_uploader("اختر صورة...", type=["jpg", "jpeg", "png", "webp"])

if uploaded_file is not None:
    # قراءة الصورة وتحويلها لمصفوفة يفهمها OpenCV
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)
    
    # تصغير حجم الصورة تلقائياً لحماية رامات الاستضافة من الانهيار (مهم جداً!)
    max_size = 600
    height, width, _ = img.shape
    if max(height, width) > max_size:
        scale = max_size / max(height, width)
        img = cv2.resize(img, (int(width * scale), int(height * scale)))
        height, width, _ = img.shape

    # عرض الصورة الأصلية للمستخدم
    st.image(img, channels="BGR", caption="الصورة التي تم رفعها", use_container_width=True)
    
    # زر بدء المعالجة
    if st.button("تطبيق المؤثرات وتوليد الفيديو ✨"):
        with st.spinner("جاري معالجة الصورة وإضافة التوهج النبضي... انتظر قليلاً"):
            
            # إعدادات الفيديو
            video_path = "glowing_output.mp4"
            fps = 24
            duration = 4  # طول الفيديو 4 ثوانٍ وهو ممتاز للاستضافة
            total_frames = duration * fps
            
            # ترميز الفيديو القياسي للويب
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            video = cv2.VideoWriter(video_path, fourcc, fps, (width, height))
            
            # تحويل الصورة إلى رمادي لعمل القناع
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            _, mask = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)
            mask_blurred = cv2.GaussianBlur(mask, (21, 21), 0)
            mask_3ch = cv2.merge([mask_blurred, mask_blurred, mask_blurred]) / 255.0
            
            # توليد الإطارات
            for frame_num in range(total_frames):
                pulse = 0.4 + 0.6 * math.sin(2 * math.pi * frame_num / total_frames)
                glow_layer = cv2.GaussianBlur(img, (41, 41), 0)
                glow_layer = cv2.multiply(glow_layer, np.array([pulse, pulse * 0.9, pulse * 1.1])) # لمسة لونية سينمائية
                
                background = cv2.multiply(img, 1.0 - mask_3ch)
                foreground = cv2.multiply(glow_layer, mask_3ch)
                composite_frame = cv2.add(background, foreground)
                composite_frame = np.clip(composite_frame, 0, 255).astype(np.uint8)
                
                video.write(composite_frame)
                
            video.release()
            
        st.success("تم توليد الفيديو بنجاح!")
        
        # عرض الفيديو داخل الموقع مع إمكانية تحميله
        with open(video_path, "rb") as video_file:
            st.video(video_file.read())