from app.models.ad_models import CustomerType

def get_gemini_prompt(customer_type: CustomerType, product: str, product_description: str, number_of_variations: int = 1) -> str:
    markdown_format_instruction = (
        "Format the output as markdown. It should include a compelling title (H2 level, e.g., '## Title') "
        "followed by 4-5 paragraphs of detailed and engaging content. Make the copy attractive and persuasive to encourage purchase."
    )

    if number_of_variations <= 1:
        # Prompt for a single variation with markdown
        if customer_type == CustomerType.POSITIVE:
            return (
                f"You are an expert marketing copywriter. Generate a compelling and uplifting "
                f"advertisement copy for our product: '{product}' (Description: '{product_description}'). "
                f"Focus on reinforcing positive feelings, highlighting benefits, and encouraging engagement. "
                f"Tone: Enthusiastic, appreciative. "
                f"{markdown_format_instruction}"
            )
        elif customer_type == CustomerType.NEGATIVE:
            return (
                f"You are an expert marketing copywriter specializing in customer retention. "
                f"Generate an empathetic and reassuring advertisement copy "
                f"for customers who have expressed negative sentiment about our product: '{product}' (Description: '{product_description}'). "
                f"Focus on acknowledging their feelings, commitment to improvement, and rebuilding trust. "
                f"Tone: Understanding, sincere, proactive. "
                f"{markdown_format_instruction}"
            )
        else:
            raise ValueError("Invalid customer type")
    else:
        # Prompt for multiple variations with markdown
        variation_instruction = f"Generate {number_of_variations} distinct variations of a compelling advertisement copy"
        if customer_type == CustomerType.POSITIVE:
            return (
                f"You are an expert marketing copywriter. {variation_instruction} "
                f"for our product: '{product}' (Description: '{product_description}'). "
                f"Each variation should focus on reinforcing positive feelings, highlighting benefits, and encouraging engagement. "
                f"Ensure each variation is unique. "
                f"Tone: Enthusiastic, appreciative. "
                f"Format each variation as markdown, including a compelling title (H2 level, e.g., '## Title') "
                f"followed by 4-5 sentences of detailed and engaging content. Make the copy attractive and persuasive to encourage purchase. "
            )
        elif customer_type == CustomerType.NEGATIVE:
            return (
                f"You are an expert marketing copywriter specializing in customer retention. {variation_instruction} "
                f"for customers who have expressed negative sentiment about our product: '{product}' (Description: '{product_description}'). "
                f"Each variation should focus on acknowledging their feelings, commitment to improvement, and rebuilding trust. "
                f"Ensure each variation is unique. "
                f"Tone: Understanding, sincere, proactive. "
                f"Format each variation as markdown, including a compelling title (H2 level, e.g., '## Title') "
                f"followed by 4-5 sentences of detailed and engaging content. Make the copy attractive and persuasive to encourage purchase. "
            )
        else:
            raise ValueError("Invalid customer type")

def get_imagen_prompt(customer_type: CustomerType, product: str, product_description: str, number_of_variations: int = 1) -> str:
    # Imagen typically generates multiple images if the model supports it and is configured to do so.
    # The prompt itself might not need to explicitly ask for N images, but the calling service will handle requesting N images.
    # However, we can add a note about variations if it helps the model understand the intent.
    # For now, the prompt remains largely the same as Imagen's `count` parameter handles the number of images.
    # We will adjust the calling function in vertex_ai_service.py to request multiple images.
    
    # The core prompt remains focused on a single image's characteristics, 
    # as Imagen's API usually handles the generation of multiple candidates based on one core prompt.
    if customer_type == CustomerType.POSITIVE:
        return (
            f"Generate a vibrant, optimistic, high-quality advertisement image for the product: '{product}' "
            f"(Description: '{product_description}'). The image should evoke happiness and satisfaction, "
            f"showcasing the product's best features or the positive experience it offers. "
            f"Style: Clean, modern, bright. No text in image. Visual appeal. "
            f"If generating multiple variations, ensure diversity in composition and perspective."
        )
    elif customer_type == CustomerType.NEGATIVE:
        return (
            f"Generate a professional, empathetic, and hopeful advertisement image for the product: '{product}' "
            f"(Description: '{product_description}'). The image should convey understanding and reassurance, "
            f"perhaps subtly hinting at a solution or improvement related to the product or brand commitment. "
            f"Style: Calm, clear, supportive. No text in image. Visual appeal. "
            f"If generating multiple variations, ensure diversity in composition and perspective."
        )
    else:
        raise ValueError("Invalid customer type")
