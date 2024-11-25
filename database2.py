import mysql.connector
import streamlit as st
from st_aggrid import AgGrid
import pandas as pd

# Establish a connection to MySQL Server
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345",
    database="student_n"
)

mycursor = mydb.cursor()
print("Connection Established")

# Streamlit App with Enhanced UI
def main():
    # Apply custom styles using HTML and CSS
    st.markdown("""
        <style>
            .main {
                background-color: #f8f9fa;
                font-family: Arial, sans-serif;
            }
            h1, h2, h3 {
                color: #6c63ff;
            }
            .stButton>button {
                color: white;
                background-color: #6c63ff;
                border-radius: 8px;
                border: none;
                font-size: 16px;
                padding: 8px 16px;
            }
            .stButton>button:hover {
                background-color: #5753d6;
            }
        </style>
    """, unsafe_allow_html=True)

    # App Title and Description
    st.title("🚀 CRUD Operations With MySQL")
    st.write("Manage your database records seamlessly with a user-friendly interface.")

    # Sidebar for CRUD Options
    st.sidebar.title("⚙️ Options")
    option = st.sidebar.radio("Select Operation", ("Create", "Read", "Update", "Delete"))

    # Perform Selected CRUD Operations
    if option == "Create":
        st.subheader("📝 Create a Record")
        name = st.text_input("Enter Name")
        email = st.text_input("Enter Email")
        if st.button("✅ Create"):
            if name and email:
                sql = "INSERT INTO student_table (name, email) VALUES (%s, %s)"
                val = (name, email)
                mycursor.execute(sql, val)
                mydb.commit()
                st.success("Record Created Successfully!")
            else:
                st.error("Please enter both Name and Email.")

    elif option == "Read":
        st.subheader("📋 Read Records")
        mycursor.execute("SELECT * FROM student_table")
        result = mycursor.fetchall()
        if result:
            df = pd.DataFrame(result, columns=["ID", "Name", "Email"])
            AgGrid(df, height=400, fit_columns_on_grid_load=True)
        else:
            st.info("No records found.")

    elif option == "Update":
        st.subheader("🔄 Update a Record")
        id = st.number_input("Enter ID", min_value=1, step=1)
        name = st.text_input("Enter New Name")
        email = st.text_input("Enter New Email")
        if st.button("📝 Update"):
            if name and email:
                sql = "UPDATE student_table SET name=%s, email=%s WHERE id=%s"
                val = (name, email, id)
                mycursor.execute(sql, val)
                mydb.commit()
                st.success("Record Updated Successfully!")
            else:
                st.error("Please enter both Name and Email.")

    elif option == "Delete":
        st.subheader("🗑️ Delete a Record")
        id = st.number_input("Enter ID", min_value=1, step=1)
        if st.button("❌ Delete"):
            sql = "DELETE FROM student_table WHERE id=%s"
            val = (id,)
            mycursor.execute(sql, val)
            mydb.commit()
            st.success("Record Deleted Successfully!")

if __name__ == "__main__":
    main()
