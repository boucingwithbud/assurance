from PIL import Image
from io import BytesIO
import base64

def encode_image_to_base64(image_path):
    # Ouvre l'image
    with Image.open(image_path) as img:
        # Crée un objet BytesIO pour écrire l'image dans un flux mémoire
        buffered = BytesIO()
        img.save(buffered, format="PNG")  # Vous pouvez spécifier d'autres formats comme "JPEG"
        # Encode l'image en base64
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return img_str