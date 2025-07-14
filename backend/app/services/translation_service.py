from app.services.vertex_ai_service import GenerativeModel, generation_config
import re

def translate_korean_to_english(text: str) -> str:
    """
    Translates Korean text to English using Gemini.
    If the text doesn't contain Korean, returns it as-is.
    """
    # Check if text contains Korean characters
    if not any(ord(char) >= 0xAC00 and ord(char) <= 0xD7A3 for char in text):
        return text
    
    try:
        model = GenerativeModel("gemini-2.0-flash")
        
        prompt = f"""Translate the following Korean text to English. 
        If the text contains mixed Korean and English, translate only the Korean parts.
        Provide only the translation without any explanation.
        
        Text: {text}
        
        Translation:"""
        
        response = model.generate_content([prompt], generation_config=generation_config)
        
        if response.candidates and response.candidates[0].content.parts:
            translated = response.candidates[0].content.parts[0].text.strip()
            print(f"[DEBUG] Translation: '{text}' -> '{translated}'")
            return translated
        else:
            print(f"[WARNING] Translation failed, returning original text")
            return text
            
    except Exception as e:
        print(f"[ERROR] Translation error: {e}")
        return text

def translate_product_info(product: str, description: str) -> tuple[str, str]:
    """
    Translates product name and description from Korean to English.
    Returns a tuple of (translated_product, translated_description).
    """
    translated_product = translate_korean_to_english(product)
    translated_description = translate_korean_to_english(description)
    
    return translated_product, translated_description