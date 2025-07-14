# from app.models.ad_models import CustomerType # Removed CustomerType import
from typing import Optional

def get_gemini_prompt(product: str, product_description: str, persona_description: Optional[str] = None, number_of_variations: int = 1) -> str: # Removed customer_type
    markdown_format_instruction = (
        "Format the output as markdown. It should include a compelling title (H2 level, e.g., '## Title') "
        "followed by 4-5 paragraphs of detailed and engaging content. Make the copy attractive and persuasive to encourage purchase."
    )
    
    base_prompt_intro = f"You are an expert marketing copywriter. Generate a compelling advertisement copy"
    if number_of_variations > 1:
        base_prompt_intro = f"You are an expert marketing copywriter. Generate {number_of_variations} distinct variations of a compelling advertisement copy"

    # Instruction to ensure only ad copy is generated
    output_only_instruction = "Provide only the advertisement copy, without any introductory phrases, explanations, or numbering for the variations. Each variation should start directly with its content."

    return (
        f"{base_prompt_intro} "
        f"for our product: '{product}' (Description: '{product_description}'). "
        f"{f'Tailor the message for the following Target Persona: {persona_description}. ' if persona_description else 'The ad should be generally appealing. '}"
        f"Focus on highlighting benefits and encouraging engagement. "
        f"Ensure each variation is unique if multiple are requested. "
        f"{output_only_instruction} " # Added instruction here
        f"Tone: Persuasive, engaging, and aligned with the product and persona. "
        f"{markdown_format_instruction if number_of_variations <=1 else 'Format each variation as markdown, including a compelling title (H2 level, e.g., ## Title) followed by 4-5 sentences of detailed and engaging content. Make the copy attractive and persuasive to encourage purchase.'}"
    )

def get_imagen_prompt(product: str, product_description: str, persona_description: Optional[str] = None, number_of_variations: int = 1) -> str: # Removed customer_type
    prompt = (
        f"Generate a high-quality advertisement image for the product: '{product}' "
        f"(Description: '{product_description}'). "
        f"{f'The image should visually resonate with the following persona: {persona_description}. ' if persona_description else 'The image should be generally appealing and highlight the product effectively. '}"
        f"The image should showcase the product's best features or the positive experience it offers. "
        f"Style: Clean, modern, visually appealing. No text in image. "
        f"If generating multiple variations, ensure diversity in composition and perspective."
    )
    
    # Debug logging for Korean text issues
    print(f"[DEBUG] Imagen prompt generated: {prompt}")
    print(f"[DEBUG] Prompt contains Korean: {any(ord(char) >= 0xAC00 and ord(char) <= 0xD7A3 for char in prompt)}")
    
    return prompt
