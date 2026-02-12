import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
pip install xlsxwriter


# Page setup
st.set_page_config(page_title="Expense Tracker", layout="wide")
st.title("📊 Interactive Expense Tracker")

# Sidebar file upload
st.sidebar.header("Upload your dataset")
uploaded_file = st.sidebar.file_uploader(
    "Choose a CSV or Excel file", type=["csv", "xls", "xlsx"]
)

if uploaded_file:
    try:
        # Load file
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file, sheet_name=0)

        st.success("File uploaded successfully!")
        st.write("### Raw Data Preview", df.head())

        # Ensure required columns
        required_cols = ["date", "category", "amount"]
        if all(col.lower() in df.columns.str.lower() for col in required_cols):
            df.columns = [col.lower() for col in df.columns]

            # Convert date column
            df["date"] = pd.to_datetime(df["date"])

            # --- Data Analysis ---
            total_per_category = df.groupby("category")["amount"].sum()
            daily_totals = df.groupby("date")["amount"].sum()
            average_daily_spend = daily_totals.mean()
            most_expensive_day = daily_totals.idxmax()
            max_spent = daily_totals.max()

            st.write("### 🏷 Total Spent per Category")
            st.dataframe(total_per_category)

            st.write(f"### 📅 Average Daily Spend: ₹{average_daily_spend:.2f}")
            st.write(f"### 💸 Most Expensive Day: {most_expensive_day.date()} (₹{max_spent:.2f})")

            # --- Visualizations ---
            st.write("### 📈 Daily Spending Trend")
            fig1, ax1 = plt.subplots(figsize=(10, 4))
            sns.lineplot(x=daily_totals.index, y=daily_totals.values, marker="o", ax=ax1)
            ax1.set_xlabel("Date")
            ax1.set_ylabel("Amount Spent")
            ax1.set_title("Daily Spending Trend")
            st.pyplot(fig1)

            st.write("### 🥧 Category-wise Spending")
            fig2, ax2 = plt.subplots(figsize=(6, 6))
            total_per_category.plot.pie(autopct="%1.1f%%", ax=ax2, startangle=90)
            ax2.set_ylabel("")
            ax2.set_title("Category-wise Spend")
            st.pyplot(fig2)



            # Function to convert to Excel in-memory
            def to_excel(df):
                output = BytesIO()
                writer = pd.ExcelWriter(output, engine="xlsxwriter")
                df.to_excel(writer, index=True, sheet_name="Summary")
                writer.save()
                processed_data = output.getvalue()
                return processed_data

            excel_data = to_excel(summary_df)

            st.download_button(
                label="📥 Download Summary as Excel",
                data=excel_data,
                file_name="expense_summary.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        else:
            st.error(f"Dataset must contain these columns: {required_cols}")

    except Exception as e:
        st.error(f"Error loading file: {e}")

else:
    st.info("Upload a CSV or Excel file to start analyzing your expenses.")
