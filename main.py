from dotenv import load_dotenv
import base64
import io
import streamlit as st
import os
import google.generativeai as genai
from datetime import datetime

# Load environment variables
load_dotenv()

# Set up the frontend with the new app name
st.set_page_config(page_title='Know Your Ingredient', page_icon="🌽", layout="wide")

# Header with updated styling
st.title('Know Your Ingredient App 🌽')
st.write("Identify ingredients in your images and learn about their pros and cons!")

# Configure Google Gemini API
genai.configure(api_key=os.getenv('GOOGLE_GEMINI_KEY'))

# Function to get Gemini responses
def get_gemini_responses(input, image_data, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input, image_data[0], prompt])
    return response.text

# Function to get image uploaded
def get_image_uploaded(uploaded_image):
    if uploaded_image is not None:
        # Convert image to bytes
        image_byte_arr = io.BytesIO(uploaded_image.read()).read()

        image_parts = [
            {
                'mime_type': 'image/jpeg',
                'data': base64.b64encode(image_byte_arr).decode()
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError('Please upload your image...')

# Job description input area
job_description = st.text_input('Any specific requirements for ingredient analysis:', key='input')

# Image upload area
uploaded_file = st.file_uploader('Upload your image (* JPEG or PNG allowed)', type=['jpg', 'jpeg', 'png'])

# Image uploaded success message
if uploaded_file is not None:
    st.success('🎉 Image uploaded successfully!')
    st.image(uploaded_file, caption='Food Label Uploaded Image', use_column_width=False, width=300)

# Button with updated styling
generate_button = st.button('Analyze Ingredient', key='generate_button')

# Updated Input prompt
input_prompt = """
You are an advanced ingredient analysis model designed to provide information about the given ingredient. 
You've to generate a table, and first column would be of ingredients, and following columns would be about pros and cons about that ingredient, also add facts and figures if possible, to make your verdict more strong. Use WHO ie. world health organization's data to make your verdict more suitable.
Your goal is to analyze the provided image, identify the ingredient, and provide information about its pros and cons. In the end, please clarify, how is this food for different age groups. In the very end of result, request user to tag us on social media platforms via @ashusnapx, do them a humble request, and end the message with a quote related to health.
Please specify any specific requirements for analysis in the input field.
"""

# Button actions
if generate_button:
    if uploaded_file is not None:
        # Add a loading button while analysis is in progress
        with st.spinner('Analyzing Ingredient...'):
            # Perform analysis after clicking the button
            image_data = get_image_uploaded(uploaded_file)
            response = get_gemini_responses(input_prompt, image_data, job_description)
            st.subheader('Ingredient Analysis:')
            st.write(response)

            # Save results or perform further actions if needed
            # ...
    else:
        st.warning('Please upload your image...')

# Footer
footer = """
<hr style="border:0.5px solid #808080">
<div style="display: flex; justify-content: space-between; align-items: center; padding-top: 10px; padding-bottom: 10px;">
    <div>
         <a href="https://ashusnapx.vercel.app/" target="_blank" style="font-size: 12px; text-decoration: none; color: #1DA1F2;">Ashutosh Kumar</a><br>
        <span style="font-size: 12px;">Software Developer</span>
    </div>
    <div>
        <a href="https://twitter.com/ashusnapx" target="_blank" style="font-size: 12px; text-decoration: none; color: #1DA1F2;">Twitter</a><br>
        <a href="https://www.linkedin.com/in/ashusnapx" target="_blank" style="font-size: 12px; text-decoration: none; color: #0077B5;">LinkedIn</a>
    </div>
</div>
"""

# Add footer to the page
st.markdown(footer, unsafe_allow_html=True)