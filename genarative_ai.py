
import os
import google.generativeai as genai
from flask import Flask, request, jsonify,render_template
# from generativeai import callingai
from werkzeug.utils import secure_filename
from PIL import Image  # Added for image processing
# Your API key directly assigned
api_key_value = "'***"
key="***"
model_name = 'gemini-2.0-flash' # Using a different variable name to avoid conflict

def generate_ai_response(prompt):
    # print("yes")
    genai.configure(api_key=key) # Use the directly assigned variable
    model = genai.GenerativeModel(model_name)
    response = model.generate_content(prompt)
    if response.candidates and response.candidates[0].content and response.candidates[0].content.parts:
        result= response.candidates[0].content.parts[0].text
        print(result)
        return result.replace('**', '').replace('\\n', '\n').replace('* ','-').strip()
    else:
        return "No content generated or unexpected response format."

    # return response


def generate_ai_response_for_image(prompt, image_path):
    os.environ['GOOGLE_API_KEY'] = key  # Replace with your actual API key
    genai.configure(api_key=os.environ['GOOGLE_API_KEY'])
    model = genai.GenerativeModel('gemini-1.5-flash-8b')

    # Read image data
    try:
        img = Image.open(image_path)
        img = img.convert('RGB')  # Ensure image is in RGB mode if necessary
    except FileNotFoundError:
        return jsonify({"message": "Error: Image file not found"}), 500

    # Generate AI response using the image and prompt
    response = model.generate_content([prompt, img])

    # Extract necessary data from response (assuming response.text contains the relevant info)
    # print(response)
    result=response.candidates[0].content.parts[0].text  # Adjust this based on the actual response object structure
    result=result.replace('**', '').replace('\\n', '\n').strip()
    # print(response)
    return result



# result=generate_ai_response_for_image("describe about img ",'Hanumanji.jpeg')
# print(result)