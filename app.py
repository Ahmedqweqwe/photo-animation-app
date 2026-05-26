# ضع هذا الجزء كخدمة جديدة في القائمة الجانبية بملف app.py
elif service == "🎨 صانع صفحات الهبوط الذكي":
    st.header("🎨 صانع صفحات الهبوط الاحترافية للمنتجات")
    st.write("أدخل بيانات منتجك واختر الألوان لتوليد صفحة هبوط جاهزة ومتوافقة مع الهواتف.")

    # تقسيم المدخلات في أعمدة لشكل منظم
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
        
        # اختيار الألوان للتصميم
        st.write("🎨 **إعدادات ألوان الصفحة:**")
        primary_color = st.color_picker("اللون الرئيسي (للأزرار والعناوين):", "#25D366") # الافتراضي أخضر واتساب
        bg_color = st.color_picker("لـون خلفية الصفحة:", "#F8F9FA")

    # تحويل المميزات إلى قائمة HTML
    features_list = "".join([f"<li>✅ {f.strip()}</li>" for f in features_input.split("\n") if f.strip()])

    # قالب صفحة الهبوط (HTML & CSS)
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

    <header>
        <div class="logo">{store_name}</div>
    </header>

    <div class="container">
        <h1>{headline}</h1>
        <p class="sub">{subheadline}</p>
        
        <img class="product-img" src="{product_img_url}" alt="Product Image">
        
        <div class="features">
            <ul>
                {features_list}
            </ul>
        </div>
        
        <a href="https://wa.me/{whatsapp_number}?text=أريد%20طلب%20منتج:%20{headline}" target="_blank" class="btn">
            {cta_text}
        </a>
    </div>

    <footer>
        جميع الحقوق محفوظة &copy; {store_name}
    </footer>

</body>
</html>
"""

    st.markdown("---")
    st.subheader("👀 معاينة كود الصفحة وتنزيلها:")
    
    # زر لتحميل ملف الـ HTML مباشرة
    st.download_button(
        label="📥 تحميل صفحة الهبوط الآن (index.html)",
        data=html_code,
        file_name="index.html",
        mime="text/html",
        key="download_lp"
    )
    
    # عرض الكود البرمجي للمستخدم لمن يحب نسخه يدوياً
    with st.expander("اضغط هنا لعرض كود الـ HTML الناتج"):
        st.code(html_code, language="html")