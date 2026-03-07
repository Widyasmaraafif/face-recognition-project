import streamlit as st
import pandas as pd
import sqlite3
import config
import os
import io
from datetime import datetime, date

st.set_page_config(page_title="Face Recognition Attendance Dashboard", layout="wide")

def get_connection():
    return sqlite3.connect(config.DB_NAME)

def load_data(start_date=None, end_date=None):
    conn = get_connection()
    query = "SELECT * FROM attendance"
    params = []
    
    if start_date and end_date:
        query += " WHERE DATE(timestamp) BETWEEN ? AND ?"
        params = [start_date, end_date]
        
    query += " ORDER BY timestamp DESC"
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df

def load_users():
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM users", conn)
    conn.close()
    return df

st.title("📊 Face Recognition Attendance Dashboard")

# Sidebar for navigation and filters
st.sidebar.title("Navigasi & Filter")
menu = ["Dashboard", "User Management", "Raw Data"]
choice = st.sidebar.selectbox("Menu Utama", menu)

# Date Filter (Global for Dashboard and Raw Data)
st.sidebar.write("---")
st.sidebar.subheader("Filter Tanggal")
today = date.today()
d_start = st.sidebar.date_input("Mulai", today)
d_end = st.sidebar.date_input("Selesai", today)

if choice == "Dashboard":
    st.subheader("Attendance Overview")
    
    df = load_data(d_start, d_end)
    users_df = load_users()
    
    if not df.empty:
        # Metrics
        total_attendance = len(df)
        unique_users = df['user_name'].nunique()
        total_registered = len(users_df)
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Kehadiran (Periode)", total_attendance)
        col2.metric("Orang Teridentifikasi", unique_users)
        col3.metric("Total User Terdaftar", total_registered)
        
        # Merge attendance with user info for better charts
        df_merged = pd.merge(df, users_df, left_on='user_name', right_on='name', how='left')
        
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.write("### Kehadiran per Orang")
            user_counts = df['user_name'].value_counts()
            st.bar_chart(user_counts)
            
        with col_right:
            st.write("### Kehadiran per Departemen")
            if 'department' in df_merged.columns:
                dept_counts = df_merged['department'].value_counts()
                st.bar_chart(dept_counts)
            else:
                st.info("Data departemen belum tersedia.")
        
        # Recent Attendance Table
        st.write("### Log Kehadiran Terbaru (Periode Ini)")
        st.dataframe(df_merged[['user_name', 'department', 'role', 'type', 'timestamp']].head(20), use_container_width=True)
        
    else:
        st.info(f"Tidak ada data kehadiran ditemukan untuk periode {d_start} s/d {d_end}.")

elif choice == "User Management":
    st.subheader("Manajemen Pengguna")
    users_df = load_users()
    
    if not users_df.empty:
        st.write(f"Total User Terdaftar: {len(users_df)}")
        st.dataframe(users_df, use_container_width=True)
    else:
        st.info("Belum ada user yang terdaftar.")
        
    st.write("---")
    st.write("### Galeri Foto Dataset")
    if os.path.exists(config.DATASET_DIR):
        photos = [f for f in os.listdir(config.DATASET_DIR) if f.endswith(('.jpg', '.png', '.jpeg'))]
        if photos:
            cols = st.columns(5)
            for i, photo in enumerate(photos):
                with cols[i % 5]:
                    st.image(os.path.join(config.DATASET_DIR, photo), caption=photo, use_column_width=True)
        else:
            st.info("Folder dataset kosong.")
    else:
        st.error(f"Direktori {config.DATASET_DIR} tidak ditemukan.")

elif choice == "Raw Data":
    st.subheader("Ekspor & Data Mentah")
    df = load_data(d_start, d_end)
    
    if not df.empty:
        # Reorder columns for better readability if they exist
        cols_to_show = ['user_name', 'type', 'timestamp']
        if all(c in df.columns for c in cols_to_show):
            df_display = df[cols_to_show]
        else:
            df_display = df
            
        st.write(f"Menampilkan {len(df)} baris data.")
        st.dataframe(df_display, use_container_width=True)
        
        # Download options
        col_dl1, col_dl2 = st.columns(2)
        
        # CSV
        csv = df.to_csv(index=False).encode('utf-8')
        col_dl1.download_button(
            label="Download as CSV",
            data=csv,
            file_name=f'attendance_{d_start}_to_{d_end}.csv',
            mime='text/csv',
        )
        
        # Excel
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Attendance')
        
        col_dl2.download_button(
            label="Download as Excel",
            data=buffer,
            file_name=f'attendance_{d_start}_to_{d_end}.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        )
    else:
        st.info("Tidak ada data untuk diekspor.")
