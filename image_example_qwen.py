import base64
from llm import call_image_api

image_path = "images/sample_photo.jpg"

# Encode image
with open(image_path, "rb") as f:
    base64_image = base64.b64encode(f.read()).decode()

# Call API
result = call_image_api(base64_image, "Describe this image.")
if result:
    print(result)