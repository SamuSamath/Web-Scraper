# Web-Scraper
Develop an API server capable of extracting reviews information from any given product page (e.g., Shopify, Amazon). The API should dynamically identify CSS elements of reviews and handle pagination to retrieve all reviews.

# Product Review Extractor

## Overview
This project is an API server that extracts reviews from any given product page (e.g., Shopify, Amazon). It dynamically identifies CSS elements using Mistral (a free LLM) and handles pagination to retrieve all reviews. The project includes:

- **Scraping Logic**: Extracts reviews using Selenium.
- **Dynamic CSS Identification**: Uses Mistral to identify CSS selectors for reviews.
- **API Development**: A Flask-based API to serve the extracted reviews.
- **Frontend Integration**: A Streamlit frontend to interact with the API.

## Technologies Used
- **Python**: Primary programming language.
- **Selenium**: Browser automation for scraping.
- **Mistral (LLM)**: For dynamic CSS selector identification.
- **Flask**: API server framework.
- **Streamlit**: Frontend for user interaction.
- **Hugging Face Inference API**: To interact with Mistral.

## Workflow
1. **Scraping**:
   - Use Selenium to load the product page.
   - Extract the HTML content of the page.
2. **Dynamic CSS Identification**:
   - Split the HTML content into chunks.
   - Use Mistral (via Hugging Face Inference API) to identify CSS selectors for reviews.
3. **Review Extraction**:
   - Use the identified CSS selectors to scrape reviews.
   - Handle pagination to retrieve all reviews.
4. **API Integration**:
   - Serve the extracted reviews via a Flask API.
5. **Frontend Integration**:
   - Use Streamlit to create a user-friendly interface for interacting with the API.

![image](https://github.com/user-attachments/assets/7f2009e1-865f-4977-baf4-d19bf597647b)


## Detailed Steps

### 1. Scraping Logic
The scraping logic is implemented in `api/scraper.py`. It uses Selenium to:
- Load the product page.
- Extract the HTML content.
- Use Mistral to identify CSS selectors dynamically.

#### Key Functions:
- `scrape_reviews(url)`: Extracts reviews from the given URL.
- `get_css_selectors(html_content)`: Uses Mistral to identify CSS selectors.

#### Example:
def scrape_reviews(url):
    # Configure Selenium
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    service = Service(r"C:\Users\Samath\Downloads\chromedriver-win64\chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    driver.get(url)
    time.sleep(5)  # Wait for the page to load

    # Get the page's HTML content
    html_content = driver.page_source
    driver.quit()

    return html_content
**2. Dynamic CSS Identification**
Mistral is used to identify CSS selectors dynamically. The HTML content is split into chunks, and each chunk is processed by Mistral to identify the relevant CSS selectors.
Key Functions
•	split_into_chunks(html_content, max_length=50000): Splits HTML content into manageable chunks.
•	get_css_selectors(html_content): Uses Mistral to identify CSS selectors.
Example
def get_css_selectors(html_content):
    results = []
    chunks = split_into_chunks(html_content, max_length=50000)

    for chunk in chunks:
        prompt = f"""
        [INST] Analyze the following HTML content and identify the CSS selectors for the following elements:
        - Review Container
        - Review Title
        - Review Body
        - Review Rating
        - Reviewer Name
        - Next Button
        [/INST]
        """
        response = client.chat.completions.create(
            model="mistralai/Mistral-7B-Instruct-v0.3",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=250
        )
        results.append(response.choices[0].message["content"])

    return results

**3. Frontend Integration**
The frontend is built using Streamlit in frontend/app.py. It allows users to input a product page URL and displays the extracted reviews.
Example
import streamlit as st
import requests

st.title("Product Review Extractor")
url = st.text_input("Enter the product page URL:")

if st.button("Extract Reviews"):
    if url:
        api_url = "http://127.0.0.1:8000/api/reviews"
        params = {"page": url}
        response = requests.get(api_url, params=params)

        if response.status_code == 200:
            data = response.json()
            st.success(f"Found {data['reviews_count']} reviews!")
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

**Mistral Integration**
Mistral is used for dynamic CSS identification. It is accessed via the Hugging Face Inference API.
Credentials
To use Mistral, you need a Hugging Face API key. Add it to your environment variables or directly in the code:
client = InferenceClient(api_key="hf_YOUR_API_KEY")

**Prompt Example**
The following prompt is used to instruct Mistral:
[INST] Analyze the following HTML content and identify the CSS selectors for the following elements:

1. **Review Container**: The element containing the entire review section.
2. **Review Title**: The headline summarizing the review.
3. **Review Body**: The main text written by the reviewer.
4. **Review Rating**: The numeric rating (e.g., 4 out of 5 stars) given by the reviewer, in numerical format.
5. **Reviewer Name**: The name or identifier of the person who wrote the review.
6. **Next Button for Pagination**: Identify the element that navigates to the next page.
7. **Next Page Number Element**: If the next button is not found, identify the CSS selector for the next page number element.

HTML Content:
{html_content}

Return the CSS selectors in the following format:

{
    "Review Container": "[CSS selector]",
    "Title selector": "[CSS selector]",
    "Review content selector": "[CSS selector]",
    "Ratings selector": "[CSS selector]",
    "Reviewer name selector": "[CSS selector]",
    "Next button": "[CSS selector]",
    "Next page number": "[CSS selector]"
}

Important Instructions:
- If a specific selector is not present in the HTML content, leave the field **empty** (do not make any assumptions).
- Only provide selectors that directly match the elements in the provided HTML content. Do **not** generate or assume selectors that do not exist in the HTML.
- Ensure that the output strictly follows the format provided above.
- If no selector for an element can be found in the HTML, leave the value as an empty string ("") for that field.
- Do **not** assume any CSS selector for elements like the next button or next page number if they are not explicitly found in the HTML.

[/INST]



**How to Run**
1.	Clone the repository:
git clone https://github.com/your-username/go-marble-assignment.git
cd go-marble-assignment
2.	Install dependencies:
pip install -r requirements.txt
3.	Run the API server:
python api/app.py
4.	Run the frontend:
streamlit run frontend/app.py


**Workflow Diagram**

+-------------------+       +-------------------+       +-------------------+
|                   |       |                   |       |                   |
|  User Input       | ----> |  Streamlit        | ----> |  Flask API        |
|  (Product URL)    |       |  Frontend         |       |  (/api/reviews)   |
|                   |       |                   |       |                   |
+-------------------+       +-------------------+       +-------------------+
                                                                      |
                                                                      v
+-------------------+       +-------------------+       +-------------------+
|                   |       |                   |       |                   |
|  Selenium         | <---- |  HTML Content     | <---- |  Dynamic CSS      |
|  Scraping         |       |  Extraction       |       |  Identification   |
|                   |       |                   |       |  (Mistral LLM)    |
+-------------------+       +-------------------+       +-------------------+
                                                                      |
                                                                      v
+-------------------+       +-------------------+       +-------------------+
|                   |       |                   |       |                   |
|  Review           | ----> |  API Response     | ----> |  Streamlit        |
|  Extraction       |       |  (JSON)           |       |  Frontend         |
|  & Pagination     |       |                   |       |  (Display)        |
|                   |       |                   |       |                   |
+-------------------+       +-------------------+       +-------------------+
