import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

st.set_page_config(page_title="أداة تحسين وحماية الصور", page_icon="🖼️", layout="centered")

st.title("🖼️ أداة تحسين وحماية صور المواقع")
st.write("حول صورك إلى صيغة WebP السريعة وأضف عليها علامتك المائية لحمايتها بضغطة زر!")

# 1. رفع الصورة
uploaded_file = st.file_uploader("اختر صورة للعمل عليها...", type=["jpg", "jpeg", "png", "webp"])

if uploaded_file is not None:
    # فتح الصورة باستخدام مكتبة Pillow
    image = Image.open(uploaded_file)
    
    # تحويل الصورة إلى مود RGB إذا كانت PNG شفافة لتجنب أخطاء الحفظ
    if image.mode in ("RGBA", "P"):
        image = image.convert("RGB")
        
    st.image(image, caption="الصورة الأصلية", use_container_width=True)
    
    # 2. خيارات المستخدم للعلامة المائية
    st.subheader("⚙️ إعدادات العلامة المائية")
    watermark_text = st.text_input("اكتب نص العلامة المائية:", "Souq Plus VIP")
    
    if st.button("معالجة الصورة وتجهيزها للتحميل ✨"):
        with st.spinner("جاري تحويل الصيغة وإضافة العلامة المائية..."):
            
            # إنشاء نسخة للعمل عليها
            img_with_watermark = image.copy()
            draw = ImageDraw.Draw(img_with_watermark)
            
            # تحديد حجم الخط بناءً على حجم الصورة تلقائياً
            width, height = img_with_watermark.size
            font_size = int(max(width, height) * 0.03) # الخط بنسبة 3% من حجم الصورة
            
            try:
                # محاولة استخدام خط افتراضي، وإذا لم يتوفر نستخدم الخط الأساسي
                font = ImageFont.load_default()
            except:
                font = ImageFont.load_default()
            
            # تحديد مكان النص (أسفل اليمين)
            # تم استخدام المتر المربع الافتراضي للنص لضمان التوافق
            text_x = width - (font_size * len(watermark_text) // 2) - 20
            text_y = height - font_size - 20
            
            # رسم خلفية خفيفة للنص لحمايته (مستطيل شفاف أو رمادي خفيف)
            draw.text((text_x, text_y), watermark_text, fill=(255, 255, 255), font=font)
            
            # 3. حفظ الصورة في الذاكرة بصيغة WebP ومضغوطة
            buffer = io.BytesIO()
            # quality=80 تعطي ضغطاً ممتازاً وحجماً صغيراً جداً بدون أي خسارة ملحوظة في الجودة
            img_with_watermark.save(buffer, format="WebP", quality=80)
            buffer.seek(0)
            
        st.success("🎉 تم تحسين الصورة وتحويلها إلى صيغة WebP بنجاح!")
        st.image(img_with_watermark, caption="الصورة الناتجة (WebP + علامة مائية)", use_container_width=True)
        
        # 4. زر التحميل
        st.download_button(
            label="تحميل الصورة المحسّنة (WebP)",
            data=buffer,
            file_name="optimized_image.webp",
            mime="image/webp"
        )