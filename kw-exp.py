import streamlit as st
import pandas as pd

# Streamlit app title
st.title("Keyword Exposure Analysis Tool")

# Upload your keyword data and competitor's keyword data
my_keywords_file = st.file_uploader("Upload Your Keyword Data (CSV)", type=["csv"])
competitor_keywords_file = st.file_uploader("Upload Competitor's Keyword Data (CSV)", type=["csv"])

if my_keywords_file and competitor_keywords_file:
    # Read the uploaded CSV files
    my_keywords = pd.read_csv(my_keywords_file)
    competitor_keywords = pd.read_csv(competitor_keywords_file)

    # Assuming both files have "Keyword" and "Impressions" columns
    # Merge the data to compare keywords
    merged_keywords = pd.merge(competitor_keywords, my_keywords, on='Keyword', how='left', suffixes=('_competitor', '_my'))

    # Find keywords where the competitor has higher impressions than you
    higher_exposure_keywords = merged_keywords[merged_keywords['Impressions_competitor'] > merged_keywords['Impressions_my']]

    # Find keywords that you haven't covered
    uncovered_keywords = merged_keywords[merged_keywords['Impressions_my'].isna()]

    # Display keywords where the competitor has higher impressions
    st.subheader("Keywords Where Competitor Has Higher Impressions")
    st.dataframe(higher_exposure_keywords[['Keyword', 'Impressions_competitor', 'Impressions_my']])

    # Display keywords that you haven't covered
    st.subheader("Keywords You Haven't Covered")
    st.dataframe(uncovered_keywords[['Keyword', 'Impressions_competitor', 'Traffic Share']])

    # Provide a download option for the higher exposure keywords
    st.subheader("Download Results")
    higher_exposure_keywords_download = higher_exposure_keywords[['Keyword', 'Impressions_competitor', 'Impressions_my']]
    uncovered_keywords_download = uncovered_keywords[['Keyword', 'Impressions_competitor', 'Traffic Share']]

    # Allow users to download the CSV files
    st.download_button("Download Keywords Where Competitor Has Higher Impressions", 
                       higher_exposure_keywords_download.to_csv(index=False), 
                       "higher_exposure_keywords.csv")
    st.download_button("Download Keywords You Haven't Covered", 
                       uncovered_keywords_download.to_csv(index=False), 
                       "uncovered_keywords.csv")
else:
    st.write("Please upload both your keyword data and competitor's keyword data.")
