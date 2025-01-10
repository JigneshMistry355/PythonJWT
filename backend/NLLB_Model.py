from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("facebook/nllb-200-distilled-600M")
model = AutoModelForSeq2SeqLM.from_pretrained("facebook/nllb-200-distilled-600M")

article = "Hello"
inputs = tokenizer(article, return_tensors="pt")

translated_tokens = model.generate(
    **inputs, 
    forced_bos_token_id=tokenizer.convert_tokens_to_ids("spa_Latn"), 
    max_length=30
)

print(tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)[0])