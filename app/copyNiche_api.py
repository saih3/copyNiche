from fastapi import FastAPI, HTTPException
from copyNiche import generate_branding_snippet, generate_keywords

MAX_INPUT_LENGTH = 12

app = FastAPI()


@app.get("/generate_snippet")
async def generate_snippet_api(prompt: str):
    validate_input_length(prompt)
    snippet = generate_branding_snippet(prompt)
    return {"snippet": snippet, "keywords": []}


@app.get("/generate_keywords")
async def generate_keywords_api(prompt: str):
    validate_input_length(prompt)
    keywords = generate_keywords(prompt)
    return {"snippet": None, "keywords": keywords}


@app.get("/generate_snippet_and_keywords")
async def generate_snippet_and_keywords_api(prompt: str):
    validate_input_length(prompt)
    snippet = generate_branding_snippet(prompt)
    keywords = generate_keywords(prompt)
    return {"snippet": snippet, "keywords": keywords}


def validate_input_length(prompt: str):
    if len(prompt) > MAX_INPUT_LENGTH:
        raise HTTPException(
            status_code=400, detail=f"Length of prompt must be less than or equal to {MAX_INPUT_LENGTH} characters.")


# uvicorn copyNiche_api:app --reload
