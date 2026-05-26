import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

st.set_page_config(page_title="منصة إدارة ومحتوى المتاجر الشاملة", page_icon="🚀", layout="wide")

# --- 1. القائمة الجانبية للتنقل بين الخدمات ---
st.sidebar.title("📌 قائمة الخدمات الشاملة")
service = st.sidebar.radio("اختر الخدمة التي تريدها:", [
    "🖼️ تحسين وحماية الصور (WebP)",
    "✍️ صانع وصف المنتجات والإعلانات",
    "🔍 فحص السيو (SEO Checker)",
    "💰 حاسبة أرباح التجارة الـ COD",
    "🎨 صانع صفحات الهبوط الذكي"  # أضفنا الخدمة هنا في القائمة
])

st.sidebar.markdown("---")
st.sidebar.caption("تم التطوير خصيصاً لإدارة المتاجر والمواقع بكفاءة وسرعة.")

# ==========================================
# الجملة الشرطية الأولى الأساسية (if)
# ==========================================
if service == "🖼️ تحسين وحماية الصور (WebP)":
    st.header("🖼️ تحسين وحماية صور المنتجات والمقالات")
    st.write("حول صورك إلى صيغة WebP السريعة وأضف علامتك المائية لحمايتها من السرقة.")
    
    uploaded_file = st.file_uploader("اختر صورة للعمل عليها...", type=["jpg", "jpeg", "png", "webp"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        if image.mode in ("RGBA", "P"):
            image = image.convert("RGB")
            
        st.image(image, caption="الصورة الأصلية", width=400)
        
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
            st.image(img_with_watermark, caption="الصورة الناتجة جاهزة للموقع", width=400)
            
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
            
            if keyword.lower() in title.lower():
                st.success("✅ ممتاز: الكلمة المفتاحية موجودة في عنوان الصفحة.")
            else:
                st.error("❌ خطأ: العنوان لا يحتوي على الكلمة المفتاحية المستهدفة.")
                
            if len(title) <= 60:
                st.success(f"✅ ممتاز: طول العنوان مناسب لجوجل ({len(title)} حرف).")
            else:
                st.warning(f"⚠️ تنبيه: العنوان طويل جداً ({len(title)} حرف)، يفضل أن يكون أقل من 60 حرفاً.")
                
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

# ==========================================
# الخدمة الخامسة: صانع صفحات الهبوط (تم ضبط الشرط هنا)
# ==========================================
elif service == "🎨 صانع صفحات الهبوط الذكي":
    st.header("🎨 صانع صفحات الهبوط الاحترافية للمنتجات")
    st.write("أدخل بيانات منتجك واختر الألوان لتوليد صفحة هبوط جاهزة ومتوافقة مع الهواتف.")

    col1, col2 = st.columns(2)
    
    with col1:
        store_name = st.text_input("اسم المتجر أو الماركة:", "سوق بلس VIP")
        headline = st.text_input("العنوان الرئيسي الجذاب:", "احصل على المنتج الأكثر مبيعاً في الخليج اليوم!")
        subheadline = st.text_input("العنوان الفرعي:", "توصيل سريع مجاني ودفع عند الاستلام 📦")
        cta_text = st.text_input("نص زر الشراء (CTA):", "اطلب الآن - الدفع عند الاستلام")
        whatsapp_number = st.text_input("رقم الواتساب لاستقبال الطلبات (مع رمز الدولة بدون +):", "201000000000")

    with col2:
        product_img_url = st.text_input("رابط صورة المنتج (رابط مباشر للـ Image):", "https://via.placeholder.com/500")
        features_input = st.text_area("مميزات المنتج (اكتب كل ميزة في سطر منفصل):", "خامات عالية الجودة ومضمونة\nتصميم عصري يناسب الجميع\nضمان استبدال واسترجاع مجاني خلال 14 يوم")
        
        st.write("🎨 **إعدادات ألوان الصفحة:**")
        primary_color = st.color_picker("اللون الرئيسي (للأزرار والعناوين):", "#25D366")
        bg_color = st.color_picker("لـون خلفية الصفحة:", "#F8F9FA")

    features_list = "".join([f"<li>✅ {f.strip()}</li>" for f in features_input.split("\n") if f.strip()])

    html_code = f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{headline}</title>
    <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap" rel="stylesheet">
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: 'Tajawal', sans-serif; }}
        body {{ background-color: {bg_color}; color: #333; line-height: 1.6; text-align: center; }}
        header {{ background: #fff; padding: 15px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }}
        .logo {{ font-size: 20px; font-weight: bold; color: {primary_color}; }}
        .container {{ max-width: 600px; margin: 20px auto; background: #fff; padding: 25px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }}
        h1 {{ font-size: 24px; margin-bottom: 15px; color: #111; font-weight: 700; }}
        .sub {{ font-size: 16px; color: #666; margin-bottom: 25px; }}
        .product-img {{ max-width: 100%; border-radius: 8px; margin-bottom: 25px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
        .features {{ text-align: right; margin-bottom: 30px; background: #f9f9f9; padding: 20px; border-radius: 8px; }}
        .features ul {{ list-style: none; }}
        .features li {{ margin-bottom: 12px; font-size: 16px; font-weight: bold; }}
        .btn {{ display: block; background-color: {primary_color}; color: #fff; text-decoration: none; padding: 15px; border-radius: 8px; font-size: 18px; font-weight: bold; box-shadow: 0 4px 10px rgba(0,0,0,0.15); transition: 0.3s; }}
        .btn:hover {{ transform: translateY(-2px); box-shadow: 0 6px 15px rgba(0,0,0,0.2); }}
        footer {{ margin-top: 40px; padding: 20px; font-size: 14px; color: #888; }}
    </style>
</head>
<body>
    <header><div class="logo">{store_name}</div></header>
    <div class="container">
        <h1>{headline}</h1>
        <p class="sub">{subheadline}</p>
        <img class="product-img" src="{product_img_url}" alt="Product Image">
        <div class="features"><ul>{features_list}</ul></div>
        <a href="https://wa.me/{whatsapp_number}?text=أريد%20طلب%20منتج" target="_blank" class="btn">{cta_text}</a>
    </div>
    <footer>جميع الحقوق محفوظة &copy; {store_name}</footer>
</body>
</html>"""

    st.markdown("---")
    st.subheader("👀 معاينة كود الصفحة وتنزيلها:")
    
    st.download_button(
        label="📥 تحميل صفحة الهبوط الآن (index.html)",
        data=html_code,
        file_name="index.html",
        mime="text/html",
        key="download_lp"
    )
    
    with st.expander("اضغط هنا لعرض كود الـ HTML الناتج"):
        st.code(html_code, language="html")