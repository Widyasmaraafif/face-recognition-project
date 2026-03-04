import streamlit as st
import pandas as pd
import sqlite3
import config
import os
from datetime import datetime

st.set_page_config(page_title="Face Recognition Attendance Dashboard", layout="wide")

def get_connection():
    return sqlite3.connect(config.DB_NAME)

def load_data():
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM attendance ORDER BY timestamp DESC", conn)
    conn.close()
    return df

def load_users():
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM users", conn)
    conn.close()
    return df

st.title("📊 Face Recognition Attendance Dashboard")

# Sidebar for navigation
menu = ["Dashboard", "User Management", "Raw Data"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Dashboard":
    st.subheader("Attendance Overview")
    
    df = load_data()
    if not df.empty:
        # Metrics
        total_attendance = len(df)
        unique_users = df['user_name'].nunique()
        
        col1, col2 = st.columns(2)
        col1.metric("Total Attendance Logs", total_attendance)
        col2.metric("Unique People Identified", unique_users)
        
        # Recent Attendance Table
        st.write("### Recent Attendance")
        st.dataframe(df.head(10), use_container_width=True)
        
        # Simple Chart
        st.write("### Attendance by Person")
        user_counts = df['user_name'].value_counts()
        st.bar_chart(user_counts)
    else:
        st.info("No attendance data found yet.")

elif choice == "User Management":
    st.subheader("Registered Users")
    users_df = load_users()
    if not users_df.empty:
        st.dataframe(users_df, use_container_width=True)
        
        # Option to delete (simplified)
        st.warning("Note: Deleting users here won't delete their photos in the dataset folder.")
    else:
        st.info("No users registered yet.")
        
    st.write("---")
    st.write("### Dataset Photos")
    photos = [f for f in os.listdir(config.DATASET_DIR) if f.endswith(('.jpg', '.png', '.jpeg'))]
    if photos:
        cols = st.columns(4)
        for i, photo in enumerate(photos):
            with cols[i % 4]:
                st.image(os.path.join(config.DATASET_DIR, photo), caption=photo, use_column_width=True)
    else:
        st.info("No photos in dataset.")

elif choice == "Raw Data":
    st.subheader("Download & Export")
    df = load_data()
    if not df.empty:
        st.dataframe(df)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name=f'attendance_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv',
            mime='text/csv',
        )
    else:
        st.info("No data to export.")
