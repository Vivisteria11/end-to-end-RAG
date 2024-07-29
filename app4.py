
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import json
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO)

app = FastAPI()

class KeywordRequest(BaseModel):
    keyword: str

TOGETHER_AI_API_KEY = ""
TOGETHER_AI_API_URL = "https://api.together.ai/v1/generate"

@app.post("/generate")
async def generate(keyword_request: KeywordRequest):
    keyword = keyword_request.keyword

    # Example prompt for Together AI API
    prompt = f"Create a poem using the word: {keyword}"

    # Together AI API request
    try:
        response = requests.post(
            TOGETHER_AI_API_URL,
            headers={
                "Authorization": f"Bearer {TOGETHER_AI_API_KEY}",
                "Content-Type": "application/json"
            },
            data=json.dumps({
                "prompt": prompt,
                "max_tokens": 50
            })
        )
        response.raise_for_status()  # Raise an error for bad status codes
    except requests.exceptions.RequestException as e:
        logging.error(f"Together AI API request failed: {e}")
        logging.error(f"Response content: {e.response.content if e.response else 'No response'}")
        raise HTTPException(status_code=500, detail="Together AI API request failed")

    result = response.json()
    if "generated_text" in result:
        return {"generated_text": result["generated_text"]}
    else:
        logging.error(f"Invalid response from Together AI API: {result}")
        raise HTTPException(status_code=500, detail="Invalid response from Together AI API")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
