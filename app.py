import streamlit as st
import hashlib
from base64 import urlsafe_b64encode
from cryptography.fernet import Fernet

# إعدادات الصفحة الرئيسية
st.set_page_config(page_title="خزنة الأغاني الذكية", page_icon="🎵", layout="centered")

st.title("🎵 خزنة الأغاني والملفات الصوتية")
st.write("قم بتشفير أغانيك برقم سري لحمايتها، أو فك تشفيرها للاستماع إليها!")

# دالة توليد مفتاح التشفير
def generate_key_from_password(password: str) -> bytes:
    hasher = hashlib.sha256(password.encode())
    return urlsafe_b64encode(hasher.digest())

# القائمة الجانبية للتنقل
choice = st.sidebar.selectbox("اختر العملية:", ["تشفير وقفل أغنية", "فك قفل وتشغيل أغنية"])

# --- القسم الأول: التشفير ---
if choice == "تشفير وقفل أغنية":
    st.header("🔒 قفل ملف صوتي برقم سري")
    
    uploaded_file = st.file_uploader("اختر ملف الأغنية (MP3)", type=["mp3"])
    password = st.text_input("أدخل الرقم السري للقفل:", type="password")
    
    if uploaded_file and password:
        if st.button("تشفير الملف الآن"):
            try:
                file_bytes = uploaded_file.read()
                key = generate_key_from_password(password)
                fernet = Fernet(key)
                
                # تشفير البيانات
                encrypted_data = fernet.encrypt(file_bytes)
                
                # تجهيز اسم الملف الجديد
                new_filename = uploaded_file.name.replace(".mp3", ".vault")
                
                st.success("✔ تم تشفير الملف بنجاح! جاهز للتحميل الآن.")
                st.download_button(
                    label="📥 تحميل الملف المشفر (.vault)",
                    data=encrypted_data,
                    file_name=new_filename,
                    mime="application/octet-stream"
                )
            except Exception as e:
                st.error(f"حدث خطأ أثناء التشفير: {e}")

# --- القسم الثاني: فك التشفير والتشغيل ---
elif choice == "فك قفل وتشغيل أغنية":
    st.header("🔓 تشغيل الأغنية المشفرة")
    
    uploaded_file = st.file_uploader("ارفع الملف المشفر (.vault)", type=["vault"])
    password = st.text_input("أدخل الرقم السري للفتح:", type="password")
    
    if uploaded_file and password:
        if st.button("التحقق والتشغيل"):
            try:
                encrypted_bytes = uploaded_file.read()
                key = generate_key_from_password(password)
                fernet = Fernet(key)
                
                # محاولة فك التشفير
                decrypted_data = fernet.decrypt(encrypted_bytes)
                
                st.success("✔ الرقم السري صحيح! يمكنك الاستماع أو التحميل الآن:")
                
                # مشغل الصوت في Streamlit
                st.audio(decrypted_data, format="audio/mp3")
                
                # إمكانية إعادة تحميله كـ MP3 أصلي
                original_filename = uploaded_file.name.replace(".vault", ".mp3")
                st.download_button(
                    label="📥 تحميل الملف كـ MP3 أصلي",
                    data=decrypted_data,
                    file_name=original_filename,
                    mime="audio/mp3"
                )
            except Exception:
                st.error("✖ الرقم السري غير صحيح! لا يمكن فتح الملف.")