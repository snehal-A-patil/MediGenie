import os
import streamlit as st
from PIL import Image
import google.generativeai as genai
import io
import time

from api_key import api_key


# Configure the API key
# api_key = "your_actual_api_key_here"  # Replace with your actual API key
os.environ["GEMINI_API_KEY"] = api_key

genai.configure(api_key=api_key)

# Create the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

chat_session = model.start_chat(history=[])

# Setting the page configuration
st.set_page_config(page_title="MediGenie – AI Healthcare Assistant", page_icon="🩺", layout="wide")

# Custom CSS for styling and animations
st.markdown(
    """
    <style>
        body {
            background-color: #eef2f7;
        }
        .main-title {
            text-align: center;
            font-size: 40px;
            font-weight: bold;
            color: #2c3e50;
            animation: fadeIn 2s ease-in-out;
        }
        .sub-title {
            text-align: center;
            font-size: 20px;
            color: #7f8c8d;
            animation: fadeIn 3s ease-in-out;
        }
        @keyframes fadeIn {
            from {opacity: 0;}
            to {opacity: 1;}
        }
        .stButton>button {
            background-color: #1abc9c;
            color: white;
            font-size: 20px;
            font-weight: bold;
            padding: 10px 20px;
            border-radius: 12px;
            transition: 0.3s;
        }
        .stButton>button:hover {
            background-color: #16a085;
            transform: scale(1.1);
        }
        .uploaded-image {
            display: flex;
            justify-content: center;
            margin-top: 20px;
            animation: fadeIn 2s ease-in-out;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Setting title
st.markdown("<h1 class='main-title'>MediGenie – Your AI-Powered Healthcare Assistant</h1>", unsafe_allow_html=True)
st.markdown("<h2 class='sub-title'>Upload a medical image for AI-based analysis</h2>", unsafe_allow_html=True)

# Uploading file
uploaded_file = st.file_uploader("Upload the medical image for analysis", type=["png", "jpg", "jpeg"], help="Accepted formats: PNG, JPG, JPEG")
submit_button = st.button("🔍 Generate Analysis")

if submit_button and uploaded_file is not None:
    # Show loading animation
    with st.spinner("Analyzing the image, please wait..."):
        time.sleep(2)  # Simulating processing time
        
        # Open the image using PIL
        image = Image.open(uploaded_file)

        # Convert image to bytes
        img_byte_array = io.BytesIO()
        image.save(img_byte_array, format=image.format)  
        img_bytes = img_byte_array.getvalue()

        # Display uploaded image
        st.markdown("<div class='uploaded-image'>", unsafe_allow_html=True)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # Send both text and image to the Gemini model
        response = chat_session.send_message(
            [
                {"text": "Analyze this medical image and provide insights."},
                {
                    "inline_data": {
                        "mime_type": f"image/{image.format.lower()}",
                        "data": img_bytes,
                    }
                },
            ]
        )

        # Display the response with animation
        st.markdown("<h2 class='sub-title'>📋 Analysis Result:</h2>", unsafe_allow_html=True)
        st.success(response.text)

elif submit_button and uploaded_file is None:
    st.warning("⚠️ Please upload an image before generating analysis.")
