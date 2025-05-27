from fastapi import APIRouter, HTTPException
from app.models.ad_models import AdGenerationRequest, AdGenerationResponse, AdCreative # CustomerType is used by services
from app.services import prompt_service, vertex_ai_service
from typing import List

router = APIRouter()

# Define the number of variations to generate
NUM_VARIATIONS = 3

@router.post("/generate_ad_content", response_model=AdGenerationResponse)
async def generate_ad_content_api(request: AdGenerationRequest):
    """
    Endpoint to generate multiple advertisement content variations (text and image)
    based on customer type, product, and product description.
    """
    try:
        num_to_generate = request.number_of_variations if request.number_of_variations is not None else NUM_VARIATIONS
        if not (1 <= num_to_generate <= 4): # Imagen 3 supports up to 4, Gemini can do more but let's cap for consistency
            raise HTTPException(status_code=400, detail="Number of variations must be between 1 and 4.")

        # 1. Get Gemini prompt for multiple variations
        gemini_prompt_text = prompt_service.get_gemini_prompt(
            request.customer_type,
            request.product,
            request.product_description,
            number_of_variations=num_to_generate
        )

        # 2. Generate ad texts using Gemini
        ad_texts = vertex_ai_service.generate_ad_text_with_gemini(gemini_prompt_text, num_variations=num_to_generate)
        
        # Basic error check for the list of texts
        if not ad_texts or len(ad_texts) < num_to_generate or any("Error:" in text or "Sorry," in text for text in ad_texts):
            # Consolidate error reporting if texts are missing or contain errors
            error_detail = "Failed to generate one or more ad texts."
            if ad_texts: # Some texts might exist, log them or provide more specific errors
                for i, text in enumerate(ad_texts):
                    if "Error:" in text or "Sorry," in text:
                        error_detail += f" Text {i+1}: {text}"
            raise HTTPException(status_code=500, detail=error_detail)

        # 3. Get Imagen prompt (it's the same prompt, Imagen service handles generating multiple images)
        imagen_prompt_text = prompt_service.get_imagen_prompt(
            request.customer_type,
            request.product,
            request.product_description,
            number_of_variations=num_to_generate # Pass for consistency, though Imagen prompt itself might not change much
        )

        # 4. Generate ad images using Imagen
        ad_image_data_list = vertex_ai_service.generate_ad_image_with_imagen(
            imagen_prompt_text,
            number_of_images=num_to_generate
        )

        # Basic error check for the list of images
        if not ad_image_data_list or len(ad_image_data_list) < num_to_generate or any("Error:" in img_data or "Failed" in img_data for img_data in ad_image_data_list):
            error_detail = "Failed to generate one or more ad images."
            if ad_image_data_list:
                 for i, img_data in enumerate(ad_image_data_list):
                    if "Error:" in img_data or "Failed" in img_data:
                        error_detail += f" Image {i+1} generation failed."
            raise HTTPException(status_code=500, detail=error_detail)

        # 5. Combine texts and images into AdCreative objects
        creatives: List[AdCreative] = []
        for i in range(num_to_generate):
            # Ensure we have both text and image for each creative
            if i < len(ad_texts) and i < len(ad_image_data_list):
                creatives.append(AdCreative(ad_text=ad_texts[i], ad_image_data=ad_image_data_list[i]))
            else:
                # This case should ideally be caught by earlier checks, but as a safeguard:
                raise HTTPException(status_code=500, detail=f"Mismatch in generated texts and images count for creative {i+1}.")
        
        return AdGenerationResponse(creatives=creatives)

    except ValueError as ve: # Catches errors from prompt_service if customer_type is invalid
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        # Log the exception for debugging
        print(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail="An internal server error occurred.")
