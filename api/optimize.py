import os
import json
import requests

# -------------------------------
# Hugging Face API key
# -------------------------------
HF_API_KEY = os.getenv("HF_API_KEY")
if not HF_API_KEY:
    raise ValueError("❌ HF_API_KEY is missing!")

# Example free Hugging Face model
API_URL = "https://api-inference.huggingface.co/models/gpt2"

# -------------------------------
# Serverless function
# -------------------------------
def handler(request):
    try:
        if request.method == "GET":
            return {
                "statusCode": 200,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"message": "✅ Depop AI Bot (Hugging Face) is running!"})
            }

        if request.method == "POST":
            data = json.loads(request.body)
            title = data.get("title", "")
            brand = data.get("brand", "")
            size = data.get("size", "")
            color = data.get("color", "")

            if not title or not brand:
                return {
                    "statusCode": 400,
                    "headers": {"Content-Type": "application/json"},
                    "body": json.dumps({"success": False, "error": "Title and brand required."})
                }

            prompt = (
                f"Optimize this Depop listing for search:\n"
                f"Brand: {brand}\nTitle: {title}\nSize: {size}\nColor: {color}\n\n"
                "Provide an optimized title under 60 characters and 10 tags."
            )

            headers = {"Authorization": f"Bearer {HF_API_KEY}"}
            payload = {"inputs": prompt}

            response = requests.post(API_URL, headers=headers, json=payload)
            result = response.json()

            # Parse generated text
            optimized_text = ""
            if isinstance(result, list) and "generated_text" in result[0]:
                optimized_text = result[0]["generated_text"]
            else:
                optimized_text = str(result)

            return {
                "statusCode": 200,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"success": True, "optimized_output": optimized_text})
            }

        return {
            "statusCode": 405,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"success": False, "error": "Method not allowed"})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"success": False, "error": str(e)})
        }
