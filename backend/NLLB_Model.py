from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TextRequest(BaseModel):
    text: dict

@app.post('/get_text')
def translate(request: TextRequest):
    # print(request)
    # print(request.text)
    
    original_text = request.text
    print(original_text)
    for key, value in original_text.items():
        print(key, value)
        if key == 'es':
            tokenizer = AutoTokenizer.from_pretrained("facebook/nllb-200-distilled-600M")
            model = AutoModelForSeq2SeqLM.from_pretrained("facebook/nllb-200-distilled-600M")
            article = value
            inputs = tokenizer(article, return_tensors="pt")

            translated_tokens = model.generate(
                **inputs, 
                forced_bos_token_id=tokenizer.convert_tokens_to_ids("spa_Latn"), 
                max_length=30
            )

            original_text[key] =  tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)[0]
            print(original_text)
        if key == 'en':
            tokenizer = AutoTokenizer.from_pretrained("facebook/nllb-200-distilled-600M")
            model = AutoModelForSeq2SeqLM.from_pretrained("facebook/nllb-200-distilled-600M")
            article = value
            inputs = tokenizer(article, return_tensors="pt")

            translated_tokens = model.generate(
                **inputs, 
                forced_bos_token_id=tokenizer.convert_tokens_to_ids("eng_Latn"), 
                max_length=30
            )

            original_text[key] =  tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)[0]
            print(original_text)