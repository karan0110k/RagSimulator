import base64
from groq import Groq
from config import Config

client = Groq(api_key=Config.GROQ_API_KEY)

def analyze_image(image_path):

    with open(image_path, "rb") as img:
        encoded = base64.b64encode(img.read()).decode("utf-8")

    response = client.chat.completions.create(
        model="llama-3.2-11b-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Describe this image in detail."},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{encoded}"
                        }
                    }
                ]
            }
        ],
        temperature=0.3
    )

    return response.choices[0].message.content