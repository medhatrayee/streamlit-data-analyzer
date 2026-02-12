import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Advanced Dataset Analyzer", layout="wide")

st.title("📊 Advanced Dynamic Dataset Analyzer")
st.write("Upload a CSV or Excel file and explore your dataset interactively.")

# File uploader
uploaded_file = st.file_uploader(
    "Upload your dataset (CSV or Excel)",
    type=["csv", "xlsx"]
)

if uploaded_file is not None:

    # Detect file type
    file_type = uploaded_file.name.split(".")[-1]

    if file_type == "csv":
        df = pd.read_csv(uploaded_file)
    elif file_type == "xlsx":
        df = pd.read_excel(uploaded_file)

    st.success("File uploaded successfully!")

    # Layout columns
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Dataset Preview")
        st.dataframe(df.head())

    with col2:
        st.subheader("Dataset Info")
        st.write("Shape:", df.shape)
        st.write("Missing Values:")
        st.write(df.isnull().sum())

    if st.button("Generate Analysis"):

        st.subheader("Statistical Summary")
        st.write(df.describe())

        numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns

        if len(numeric_cols) > 0:

            st.subheader("Visualization Section")

            plot_type = st.selectbox(
                "Select Plot Type",
                ["Histogram", "Boxplot", "Scatter Plot", "Line Plot"]
            )

            if plot_type in ["Histogram", "Boxplot", "Line Plot"]:
                column = st.selectbox("Select Column", numeric_cols)

                fig, ax = plt.subplots()

                if plot_type == "Histogram":
                    ax.hist(df[column])
                    ax.set_title(f"Histogram of {column}")

                elif plot_type == "Boxplot":
                    ax.boxplot(df[column])
                    ax.set_title(f"Boxplot of {column}")

                elif plot_type == "Line Plot":
                    ax.plot(df[column])
                    ax.set_title(f"Line Plot of {column}")

                st.pyplot(fig)

            elif plot_type == "Scatter Plot":
                col1 = st.selectbox("X-axis", numeric_cols)
                col2 = st.selectbox("Y-axis", numeric_cols)

                fig, ax = plt.subplots()
                ax.scatter(df[col1], df[col2])
                ax.set_xlabel(col1)
                ax.set_ylabel(col2)
                ax.set_title(f"{col1} vs {col2}")

                st.pyplot(fig)

            # Correlation Heatmap
            st.subheader("Correlation Matrix")

            fig, ax = plt.subplots()
            sns.heatmap(df[numeric_cols].corr(), annot=True, cmap="coolwarm")
            st.pyplot(fig)

        else:
            st.warning("No numeric columns found for visualization.")

        # Download option
        st.subheader("Download Dataset")
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download Dataset as CSV",
            data=csv,
            file_name="processed_data.csv",
            mime="text/csv",
        )

