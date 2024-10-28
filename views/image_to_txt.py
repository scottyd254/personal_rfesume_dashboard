import streamlit as st
from PIL import Image
import google.generativeai as genai

# Configure the API key for Google Generative AI
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

def file_validation(image_file):
    """
    Validate the uploaded image file.

    Check if the file size is less than 5 MB and if the file type is in the list of
    accepted file types.

    Parameters
    ----------
    image_file : UploadedFile
        The image file uploaded by the user.

    Returns
    -------
    bool
        True if the file is valid, False otherwise.
    """
    if image_file.size > 5 * 1024 * 1024:
        st.error("The file size is too large. Please upload a file smaller than 5 MB.")
        return False
    if image_file.type not in ["image/jpeg", "image/png", "image/webp"]:
        st.error("The file type is not supported. Please upload a JPG, PNG, or WEBP image.")
        return False
    return True

def load_image():
    """
    Handles the upload of an image file by validating it and storing in session if valid.

    Returns
    -------
    UploadedFile or None
        The uploaded image file if valid, otherwise None.
    """
    image_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png", "webp"])
    if image_file and file_validation(image_file):
        st.session_state['image_file'] = image_file
        st.success("Image uploaded successfully!")
    return image_file

def load_model():
    """
    Load the Google Generative AI model.

    Returns
    -------
    model object or None
    """
    model_name = st.secrets.get("MODEL_NAME")
    if not model_name:
        st.error("Model name is missing in secrets.")
        return None
    try:
        model = genai.GenerativeModel(model_name=model_name)
        return model
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

def extract_text(model, image_file):
    """
    Extracts text from the provided image using the specified model.

    Parameters
    ----------
    model : GenerativeAI
        The model used to extract text from the image.
    image_file : UploadedFile
        The image file from which text will be extracted.

    Returns
    -------
    str or None
        The extracted text if successful, otherwise None.
    """
    try:
        image = Image.open(image_file)
        prompt = "Extract text from the image:"
        response = model.generate_content([image, '\n\n', prompt])
        st.session_state['extracted_text'] = response.text  # Save to session state
        return response.text
    except Exception as e:
        st.error(f"Error extracting text: {e}")
        return None

# Layout sections
section = st.sidebar.radio('Go To', ["Introduction", "Upload Image", "Extracted Text", "Download"]) 

def load_layout(section):
    if section == "Introduction":
        st.title("Image to Text")
        st.markdown("This is a Streamlit app to extract text from an image file using Google AI Model.")
    
    elif section == "Upload Image":
        st.title("Upload Image")
        image_file = load_image()
        if image_file:
            st.image(image_file)
    
    elif section == "Extracted Text":
        st.title("Extracted Text")
        image_file = st.session_state.get('image_file')
        if image_file:
            model = load_model()
            if model:
                if 'extracted_text' not in st.session_state:
                    extracted_text = extract_text(model, image_file)
                else:
                    extracted_text = st.session_state['extracted_text']
                st.markdown(extracted_text)
            else:
                st.error("Model could not be loaded.")
        else:
            st.error("Please upload an image first in the 'Upload Image' section.")
    
    elif section == "Download":
        st.title("Download")
        extracted_text = st.session_state.get('extracted_text')
        if extracted_text:
            st.download_button("Download Extracted Text", extracted_text, file_name="extracted_text.txt")
            st.success("Extracted text downloaded successfully!")
            st.session_state['extracted_text'] = None
            st.session_state['image_file'] = None
        else:
            st.error("No extracted text available. Please extract text first.")

# Run the layout
load_layout(section)
