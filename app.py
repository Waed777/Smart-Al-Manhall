import streamlit as st
import pandas as pd
from utils.book_parser import parse_book
from utils.ai_plan_generator import generate_plan
from utils.pdf_generator import generate_pdf
from utils.email_sender import send_email

st.set_page_config(page_title="توليد ذكي – مدارس المنهل", layout="wide")

st.title("توليد ذكي – مدارس المنهل 💙")
st.sidebar.header("رفع الكتب والمعلمات")

# Load teachers list
teachers_df = pd.read_csv("data/teachers.csv")
teacher_names = teachers_df['اسم المعلمة'].tolist()
teacher_name = st.sidebar.selectbox("اختر المعلمة", teacher_names)
subject = st.sidebar.selectbox("اختر المادة", teachers_df['المادة'].tolist())

uploaded_file = st.sidebar.file_uploader("ارفع الكتاب (PDF أو DOCX)", type=["pdf","docx"])

if uploaded_file is not None:
    st.success(f"تم رفع الكتاب: {uploaded_file.name}")

    # Parse book
    book_text = parse_book(uploaded_file)

    # Generate AI plan
    plan, tests, video_links = generate_plan(teacher_name, subject, book_text)

    # Generate PDF
    pdf_path = generate_pdf(teacher_name, subject, plan, tests, video_links)

    st.success("تم توليد الخطة العلاجية PDF!")

    # Send email
    if st.sidebar.button("إرسال الإيميل الآلي"):
        send_email(teacher_name, pdf_path)
        st.success(f"تم إرسال الإيميل لـ {teacher_name} بنجاح!")

# Dashboard
st.header("لوحة الإدارة – المتابعة")
st.dataframe(teachers_df)
