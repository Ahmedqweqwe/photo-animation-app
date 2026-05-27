import streamlit as st
import hashlib
from base64 import urlsafe_b64encode
from cryptography.fernet import Fernet

# إعدادات الصفحة
st.set_page_config(page_title="خزنة الأغاني المتعددة", page_icon="🎵", layout="centered")

st.title("🎵 خزنة الأغاني والمكتبة الصوتية الآمنة")
st.write("يمكنك الآن إضافة عدة أغاني، تشفيرها برقم سري، تشغيلها، أو مسحها في أي وقت!")

# دالة توليد مفتاح التشفير من الرقم السري
def generate_key_from_password(password: str) -> bytes:
    hasher = hashlib.sha256(password.encode())
    return urlsafe_b64encode(hasher.digest())

# تهيئة مخزن الأغاني في الجلسة إذا لم يكن موجوداً
if "vault_songs" not in st.session_state:
    st.session_state.vault_songs = {}  # قاموس لحفظ الأغاني المشفرة {اسم_الملف: البيانات_المشفرة}

# القائمة الجانبية للتنقل
choice = st.sidebar.selectbox("اختر العملية:", ["➕ إضافة وتشفير أغنية جديدة", "🗂️ استعراض وتشغيل المكتبة"])

# --- القسم الأول: إضافة وتشفير الأغاني ---
if choice == "➕ إضافة وتشفير أغنية جديدة":
    st.header("🔒 قفل وإضافة ملف صوتي للمكتبة")
    
    uploaded_files = st.file_uploader("اختر ملف أو عدة ملفات صوتية (MP3)", type=["mp3"], accept_multiple_files=True)
    password = st.text_input("أدخل الرقم السري لقفل هذه الملفات:", type="password")
    
    if uploaded_files and password:
        if st.button("🔐 تشفير وإضافة للمكتبة"):
            key = generate_key_from_password(password)
            fernet = Fernet(key)
            
            success_count = 0
            for uploaded_file in uploaded_files:
                file_bytes = uploaded_file.read()
                # تشفير الملف
                encrypted_data = fernet.encrypt(file_bytes)
                
                # تغيير الامتداد إلى .vault وحفظه في ذاكرة التطبيق
                vault_filename = uploaded_file.name.replace(".mp3", ".vault")
                
                st.session_state.vault_songs[vault_filename] = encrypted_data
                success_count += 1
                
            st.success(f"✔ تم تشفير وحفظ {success_count} ملف بنجاح في مكتبتك الحالية!")
            st.info("💡 يمكنك الآن الذهاب إلى قسم 'استعراض وتشغيل المكتبة' لإدارتها.")

# --- القسم الثاني: استعراض وتشغيل وحذف الأغاني ---
elif choice == "🗂️ استعراض وتشغيل المكتبة":
    st.header("🗂️ مكتبة الأغاني المشفرة الخاصة بك")
    
    if not st.session_state.vault_songs:
        st.info("مكتبتك فارغة حالياً. قم بإضافة بعض الأغاني من القائمة الجانبية.")
    else:
        st.write(f"تحتوي مكتبتك على: **{len(st.session_state.vault_songs)}** ملف مشفر.")
        
        # عرض الأغاني على شكل قائمة مع أزرار التحكم
        for song_name in list(st.session_state.vault_songs.keys()):
            with st.expander(f"🎵 {song_name}"):
                
                # طلب الرقم السري الخاص بكل أغنية لتشغيلها أو تحميلها
                check_password = st.text_input(f"أدخل الرقم السري لـ {song_name}:", type="password", key=f"pass_{song_name}")
                
                col1, col2, col3 = st.columns([2, 2, 1])
                
                with col1:
                    if st.button("▶ تشغيل فوري", key=f"play_{song_name}"):
                        if check_password:
                            try:
                                encrypted_bytes = st.session_state.vault_songs[song_name]
                                key = generate_key_from_password(check_password)
                                fernet = Fernet(key)
                                
                                # فك التشفير للتشغيل
                                decrypted_data = fernet.decrypt(encrypted_bytes)
                                st.audio(decrypted_data, format="audio/mp3")
                            except Exception:
                                st.error("✖ الرقم السري غير صحيح!")
                        else:
                            st.warning("الرجاء إدخال الرقم السري أولاً.")
                            
                with col2:
                    if check_password:
                        try:
                            encrypted_bytes = st.session_state.vault_songs[song_name]
                            key = generate_key_from_password(check_password)
                            fernet = Fernet(key)
                            decrypted_data = fernet.decrypt(encrypted_bytes)
                            
                            # زر تحميل الملف الأصلي كمـ MP3
                            original_name = song_name.replace(".vault", ".mp3")
                            st.download_button(
                                label="📥 تحميل MP3",
                                data=decrypted_data,
                                file_name=original_name,
                                mime="audio/mp3",
                                key=f"down_{song_name}"
                            )
                        except Exception:
                            pass
                            
                with col3:
                    # زر الحذف من المكتبة
                    if st.button("🗑️ مسح", key=f"del_{song_name}"):
                        del st.session_state.vault_songs[song_name]
                        st.rerun()