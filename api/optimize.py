import os
import json
import requests

HF_API_KEY = os.getenv("HF_API_KEY")
if not HF_API_KEY:
    raise ValueError("❌ HF_API_KEY missing!")

API_URL = "https://api-inference.huggingface.co/models/gpt2"  # Example free model

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

            if not title or not brand:
                return {
                    "statusCode": 400,
                    "headers": {"Content-Type": "application/json"},
                    "body": json.dumps({"success": False, "error": "Title and brand required."})
                }

            prompt = f"Optimize this Depop listing for search:\nBrand: {brand}\nTitle: {title}\n"

            headers = {"Authorization": f"Bearer {HF_API_KEY}"}
            payload = {"inputs": prompt}

            response = requests.post(API_URL, headers=headers, json=payload)
            result = response.json()

            optimized_text = result[0]["generated_text"] if "generated_text" in result[0] else str(result)

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
