import streamlit as st
import requests

# Title of the app
st.title("Product Review Extractor")

# Input for the product page URL
url = st.text_input("Enter the product page URL:")

# Button to trigger the API call
if st.button("Extract Reviews"):
    if url:
        # Call the Flask API
        api_url = "http://127.0.0.1:8000/api/reviews"
        params = {"page": url}
        response = requests.get(api_url, params=params)

        if response.status_code == 200:
            data = response.json()
            st.success(f"Found {data['reviews_count']} reviews!")

            # Display the reviews
            for review in data["reviews"]:
                st.subheader(review["title"])
                st.write(f"**Rating:** {review['rating']}")
                st.write(f"**Reviewer:** {review['reviewer']}")
                st.write(review["body"])
                st.write("---")
        else:
            st.error("Failed to extract reviews. Please check the URL and try again.")
    else:
        st.warning("Please enter a valid URL.")