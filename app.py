import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Dynamic Dataset Analyzer")

st.title("Dynamic Dataset Analyzer")
st.write("Upload a CSV file and generate analysis interactively.")

# Upload CSV file
uploaded_file = st.file_uploader("Upload your dataset (CSV only)", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    if st.button("Generate Analysis"):
        st.subheader("Statistical Summary")
        st.write(df.describe())

        numeric_columns = df.select_dtypes(include=['int64', 'float64']).columns

        if len(numeric_columns) > 0:
            column = st.selectbox("Select column for histogram", numeric_columns)

            fig, ax = plt.subplots()
            ax.hist(df[column])
            ax.set_title(f"Histogram of {column}")
            ax.set_xlabel(column)
            ax.set_ylabel("Frequency")

            st.pyplot(fig)
        else:
            st.warning("No numeric columns found for visualization.")
