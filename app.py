import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

st.set_page_config(page_title="منصة إدارة ومحتوى المتاجر الشاملة", page_icon="🚀", layout="wide")

# --- القائمة الجانبية للتنقل بين الخدمات ---
st.sidebar.title("📌 قائمة الخدمات الشاملة")
service = st.sidebar.radio("اختر الخدمة التي تريدها:", [
    "🖼️ تحسين وحماية الصور (WebP)",
    "✍️ صانع وصف المنتجات والإعلانات",
    "🔍 فحص السيو (SEO Checker)",
    "💰 حاسبة أرباح التجارة الـ COD"
])

st.sidebar.markdown("---")
st.sidebar.caption("تم التطوير خصيصاً لإدارة المتاجر والمواقع بكفاءة وسرعة.")

# ==========================================
# الخدمة الأولى: تحسين وحماية الصور
# ==========================================
if service == "🖼️ تحسين وحماية الصور (WebP)":
    st.header("🖼️ تحسين وحماية صور المنتجات والمقالات")
    st.write("حول صورك إلى صيغة WebP السريعة وأضف علامتك المائية لحمايتها من السرقة.")
    
    uploaded_file = st.file_uploader("اختر صورة للعمل عليها...", type=["jpg", "jpeg", "png", "webp"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        if image.mode in ("RGBA", "P"):
            image = image.convert("RGB")
            
        st.image(image, caption="الصورة الأصلية", max_width=400)
        
        watermark_text = st.text_input("اكتب نص العلامة المائية:", "Souq Plus VIP")
        
        if st.button("معالجة الصورة وتجهيزها للتحميل ✨"):
            with st.spinner("جاري معالجة الصورة..."):
                img_with_watermark = image.copy()
                draw = ImageDraw.Draw(img_with_watermark)
                width, height = img_with_watermark.size
                font_size = int(max(width, height) * 0.03)
                
                font = ImageFont.load_default()
                text_x = width - (font_size * len(watermark_text) // 2) - 20
                text_y = height - font_size - 20
                
                draw.text((text_x, text_y), watermark_text, fill=(255, 255, 255), font=font)
                
                buffer = io.BytesIO()
                img_with_watermark.save(buffer, format="WebP", quality=80)
                buffer.seek(0)
                
            st.success("🎉 تم تحسين الصورة وتحويلها بنجاح!")
            st.image(img_with_watermark, caption="الصورة الناتجة جاهزة للموقع", max_width=400)
            
            st.download_button(
                label="تحميل الصورة المحسّنة (WebP)",
                data=buffer,
                file_name="optimized_image.webp",
                mime="image/webp"
            )

# ==========================================
# الخدمة الثانية: صانع وصف المنتجات والإعلانات
# ==========================================
elif service == "✍️ صانع وصف المنتجات والإعلانات":
    st.header("✍️ صانع ومولد أفكار المحتوى الإعلاني")
    st.write("اكتب بيانات منتجك وسيقوم السكريبت بصياغة نماذج جاهزة لكتابة الإعلانات أو الوصف.")
    
    product_name = st.text_input("اسم المنتج:")
    product_features = st.text_area("أهم مميزات المنتج (ميزة في كل سطر):")
    target_audience = st.text_input("الجمهور المستهدف (مثال: ربات البيوت، الشباب في السعودية):")
    
    if st.button("توليد صيغ المحتوى ✨"):
        if product_name and product_features:
            st.subheader("📋 نموذج وصف المنتج للمتجر:")
            features_list = "\n".join([f"- {f.strip()}" for f in product_features.split("\n") if f.strip()])
            
            desc_template = f"🔥 **{product_name}** هو الحل المثالي لـ {target_audience}! 🔥\n\n" \
                            f"إذا كنت تبحث عن الجودة والراحة، فهذا المنتج مصمم خصيصاً لك.\n\n" \
                            f"✨ **أهم ما يميزه:**\n{features_list}\n\n" \
                            f"🛍️ **اطلبه الآن واستمتع بتوصيل سريع ودفع عند الاستلام!**"
            st.code(desc_template, language="markdown")
            
            st.subheader("📱 نموذج إعلان قصير لمنصات التواصل (تيك توك / سناب):")
            ad_template = f"مستني إيه؟ 🤔 لكل {target_audience}، وصلنا حديثاً **{product_name}** الحصري! \n" \
                          f"الكمية محدودة جداً والشحن مجاني لفترة محدودة 📦. \n" \
                          f"اضغط على الرابط واطلب الدفع عند الاستلام الآن! 👇"
            st.code(ad_template, language="markdown")
        else:
            st.warning("الرجاء ملء اسم المنتج ومميزاته أولاً.")

# ==========================================
# الخدمة الثالثة: فحص السيو (SEO Checker)
# ==========================================
elif service == "🔍 فحص السيو (SEO Checker)":
    st.header("🔍 فحص وتحسين السيو (SEO) للمقالات والمنتجات")
    st.write("تأكد من أن صفحة منتجك أو مقالك متوافقة مع معايير جوجل لضمان ظهورها في النتائج الأولى.")
    
    title = st.text_input("عنوان الصفحة أو المنتج (Meta Title):")
    keyword = st.text_input("الكلمة المفتاحية المستهدفة (Keyword):")
    content = st.text_area("نص الوصف أو المقال بالكامل:")
    
    if st.button("ابدأ فحص السيو 🔍"):
        if title and keyword and content:
            st.subheader("📊 تقرير فحص السيو الخاص بك:")
            
            # فحص العنوان
            if keyword.lower() in title.lower():
                st.success("✅ ممتاز: الكلمة المفتاحية موجودة في عنوان الصفحة.")
            else:
                st.error("❌ خطأ: العنوان لا يحتوي على الكلمة المفتاحية المستهدفة.")
                
            if len(title) <= 60:
                st.success(f"✅ ممتاز: طول العنوان مناسب لجوجل ({len(title)} حرف).")
            else:
                st.warning(f"⚠️ تنبيه: العنوان طويل جداً ({len(title)} حرف)، يفضل أن يكون أقل من 60 حرفاً.")
                
            # فحص كثافة الكلمة المفتاحية في المحتوى
            keyword_count = content.lower().count(keyword.lower())
            if keyword_count >= 3:
                st.success(f"✅ ممتاز: تم تكرار الكلمة المفتاحية {keyword_count} مرات في الوصف، وهذا يسهل أرشفته.")
            elif keyword_count == 0:
                st.error("❌ خطأ: الكلمة المفتاحية غير موجودة تماماً داخل نص الوصف!")
            else:
                st.warning(f"⚠️ تنبيه: الكلمة المفتاحية تكررت {keyword_count} مرة فقط. يفضل زيادتها قليلاً لتصل إلى 3 مرات.")
        else:
            st.warning("الرجاء إدخال جميع البيانات لإتمام الفحص.")

# ==========================================
# الخدمة الرابعة: حاسبة أرباح التجارة الـ COD
# ==========================================
elif service == "💰 حاسبة أرباح التجارة الـ COD":
    st.header("💰 حاسبة أرباح المتاجر (الدفع عند الاستلام)")
    st.write("احسب بدقة صافي أرباح حملاتك الإعلانية بعد خصم كافة المصاريف ونسبة التوصيل المستلم.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        selling_price = st.number_input("سعر بيع المنتج للعميل:", min_value=0.0, value=150.0)
        product_cost = st.number_input("تكلفة شراء المنتج بالجملة:", min_value=0.0, value=40.0)
        shipping_cost = st.number_input("تكلفة شركة الشحن والتوصيل:", min_value=0.0, value=30.0)
        
    with col2:
        ad_cost_per_order = st.number_input("تكلفة الإعلان للطلب الواحد الناجح (CPA):", min_value=0.0, value=25.0)
        delivery_rate = st.slider("نسبة التوصيل المستلم المتوقعة (Delivery Rate %):", min_value=1, max_value=100, value=70)
    
    if st.button("احسب صافي الربح 💵"):
        # الحسابات الرياضية للـ COD
        total_revenue_per_100_orders = selling_price * delivery_rate
        total_costs_per_100_orders = (product_cost * delivery_rate) + (shipping_cost * delivery_rate) + (ad_cost_per_order * 100)
        
        net_profit_per_100_orders = total_revenue_per_100_orders - total_costs_per_100_orders
        profit_per_delivered_order = net_profit_per_100_orders / delivery_rate if delivery_rate > 0 else 0
        
        st.subheader("📊 النتيجة المالية المتوقعة (لكل 100 طلب تم شحنه):")
        
        if net_profit_per_100_orders > 0:
            st.success(f"💰 **صافي الربح الإجمالي:** {net_profit_per_100_orders:.2f}")
            st.metric(label="ربحك الصافي في كل قطعة مستلمة فعلياً", value=f"{profit_per_delivered_order:.2f}")
        else:
            st.error(f"📉 **أنت في منطقة خسارة!** صافي العجز المالي: {net_profit_per_100_orders:.2f}")
            st.write("نصيحة: حاول تقليل تكلفة الإعلان (CPA) أو رفع سعر البيع، أو تحسين جودة الاتصال لرفع نسبة التوصيل.")