import streamlit as st
import datetime

# 1. إعدادات الصفحة بشكل احترافي
st.set_page_config(
    page_title="المكتبة الصوتية المتكاملة",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تخصيص واجهة المستخدم وبناء تنسيق مريح للعين
st.title("🎵 استوديو ومكتبة الأغاني الذكية")
st.write("منصة كاملة لرفع، تشغيل، تنظيم، وحذف الأغاني والمقاطع الصوتية بكل حرية وبدون قيود.")

# 2. تهيئة مخزن البيانات في الجلسة (Session State)
if "music_library" not in st.session_state:
    st.session_state.music_library = [] # مصفوفة تحتوي على قواميس لكل أغنية تفاصيلها

# دالة مساعدة لحساب حجم الملف بشكل مقروء
def get_file_size_format(b_size):
    mb_size = b_size / (1024 * 1024)
    return f"{mb_size:.2f} MB"

# 3. القائمة الجانبية: إحصائيات سريعة وأزرار التحكم العام
st.sidebar.header("📊 إحصائيات المكتبة الحالية")
total_songs = len(st.session_state.music_library)
total_size = sum([song['size_bytes'] for song in st.session_state.music_library])

st.sidebar.metric(label="عدد الأغاني المرفوعة", value=f"{total_songs} أغنية")
st.sidebar.metric(label="إجمالي حجم المكتبة", value=get_file_size_format(total_size))

st.sidebar.markdown("---")
st.sidebar.header("⚙️ تحكم سريع بالكامل")

# زر مسح المكتبة بالكامل وتصفيرها
if st.sidebar.button("🗑️ إفراغ ومسح المكتبة بالكامل", type="primary"):
    st.session_state.music_library = []
    st.sidebar.success("تم تصفير وحذف جميع الأغاني بنجاح!")
    st.rerun()

# 4. القسم الأول: شاشة رفع وإضافة الأغاني الجديدة
st.header("📥 رفع وإضافة أغاني جديدة")
uploaded_files = st.file_uploader(
    "اسحب وأفلت ملفات الـ MP3 هنا (يمكنك اختيار كمية كبيرة من الأغاني معاً):",
    type=["mp3", "wav", "m4a"],
    accept_multiple_files=True
)

if uploaded_files:
    if st.button("🚀 دمج الأغاني المحددة داخل المكتبة", use_container_width=True):
        added_count = 0
        for f in uploaded_files:
            # التحقق من أن الأغنية غير مكررة بنفس الاسم
            if not any(song['name'] == f.name for song in st.session_state.music_library):
                file_bytes = f.read()
                song_data = {
                    "id": len(st.session_state.music_library) + 1,
                    "name": f.name,
                    "bytes": file_bytes,
                    "size_bytes": len(file_bytes),
                    "date_added": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                }
                st.session_state.music_library.append(song_data)
                added_count += 1
        
        if added_count > 0:
            st.success(f"✔ تم إضافة {added_count} أغنية جديدة إلى مكتبتك الصوتية بنجاح!")
        else:
            st.warning("⚠️ جميع الملفات التي اخترتها موجودة بالفعل في المكتبة.")
        st.rerun()

st.markdown("---")

# 5. القسم الثاني: استعراض المكتبة، البحث، والتشغيل والحذف
st.header("🗂️ لوحة تحكم واستعراض الأغاني")

if not st.session_state.music_library:
    st.info("مكتبتك فارغة حالياً. قم برفع بعض الأغاني من الأعلى لتبدأ التشغيل والإدارة!")
else:
    # شريط البحث الذكي لتصفية الأغاني
    search_query = st.text_input("🔍 ابحث عن أغنية معينة داخل مكتبتك:", "").strip().lower()
    
    # تصفية قائمة الأغاني بناءً على البحث
    filtered_songs = [
        song for song in st.session_state.music_library 
        if search_query in song['name'].lower()
    ]
    
    st.write(f"عرض **{len(filtered_songs)}** أغنية من أصل **{total_songs}**")
    
    # عرض الأغاني بشكل تفاعلي ومرتب
    for index, song in enumerate(filtered_songs):
        # صندوق منبثق لكل أغنية يحتوي على المشغل والأزرار الخاصة بها
        with st.expander(f"🎵 {song['name']} | 📦 الحجم: {get_file_size_format(song['size_bytes'])} | 📅 أُضيفت: {song['date_added']}"):
            
            # مشغل الصوت الاحترافي لـ Streamlit
            st.audio(song['bytes'], format="audio/mp3")
            
            # أزرار التحكم الفرعية (تحميل وحذف)
            col1, col2 = st.columns([1, 1])
            
            with col1:
                # زر تحميل الأغنية فوراً إلى جهاز المستخدم
                st.download_button(
                    label="📥 تحميل الأغنية للجهاز",
                    data=song['bytes'],
                    file_name=song['name'],
                    mime="audio/mp3",
                    key=f"download_{song['name']}_{index}"
                )
                
            with col2:
                # زر مسح الأغنية المحددة فقط دون المساس بالباقي
                if st.button("🗑️ مسح هذه الأغنية فقط", key=f"delete_{song['name']}_{index}", type="secondary"):
                    # إيجاد الأغنية الأصلية وحذفها من المخزن الأساسي
                    st.session_state.music_library = [s for s in st.session_state.music_library if s['name'] != song['name']]
                    st.success(f"تم حذف '{song['name']}' بنجاح!")
                    st.rerun()