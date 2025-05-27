import vertexai
from vertexai.generative_models import GenerativeModel, GenerationConfig, Part
from vertexai.vision_models import ImageGenerationModel # Corrected import
import os
import base64 # Added for base64 encoding
from dotenv import load_dotenv
import google.cloud.logging # Import the logging library

# Load environment variables from .env file for local development
load_dotenv()

# Initialize Vertex AI SDK
# These will be automatically picked up if running on GCP (e.g. Cloud Run)
# or can be set in the environment for local testing.
PROJECT_ID = os.getenv("GCP_PROJECT_ID")
LOCATION = os.getenv("GCP_REGION", "us-central1")

# Initialize Google Cloud Logging client
logging_client = google.cloud.logging.Client(project=PROJECT_ID)
# The name of the log to write to
# You can choose a name that makes sense for your application
log_name = "gemini-imagen-prompts"
# Selects the log to write to
logger = logging_client.logger(log_name)

if PROJECT_ID:
    vertexai.init(project=PROJECT_ID, location=LOCATION)
else:
    print("Warning: GCP_PROJECT_ID not set. Vertex AI calls may fail if not running in a GCP environment with default credentials.")

import re # Added for parsing Gemini response

# It's good practice to specify model names, possibly from env vars too
GEMINI_MODEL_NAME = os.getenv("GEMINI_MODEL_NAME", "gemini-2.0-flash") # Using a more capable model for list generation
IMAGEN_MODEL_NAME = os.getenv("IMAGEN_MODEL_NAME", "imagen-3.0-generate-002") # Updated to a common Imagen model version


generation_config = GenerationConfig(
            temperature=1.5,
            top_p=0.9,
            max_output_tokens=2048,
        )

def parse_gemini_list_response(text_response: str, num_variations: int) -> list[str]:
    """
    Parses a text response that is expected to be a numbered list.
    """
    items = []
    # Regex to find numbered list items, allowing for some flexibility in formatting.
    # It looks for a number followed by a period or parenthesis, then captures the text.
    # Example: "1. Text" or "1) Text"
    pattern = re.compile(r"^\s*\d+\s*[\.\)]\s*(.*)", re.MULTILINE)
    matches = pattern.findall(text_response)
    
    if matches:
        items.extend(match.strip() for match in matches)
    
    # If regex doesn't find enough items, or if the response isn't a list,
    # split by newline as a fallback, assuming each line is an item.
    if not items or len(items) < num_variations:
        potential_items = [line.strip() for line in text_response.split('\n') if line.strip()]
        # Filter out lines that are likely not ad copy (e.g., just numbers, short fragments)
        # This is a heuristic and might need refinement.
        items = [item for item in potential_items if len(item.split()) > 3] # Assume ad copy has more than 3 words

    # If still no items, or not enough, and the original response is non-empty,
    # treat the whole response as a single item if num_variations was 1.
    if not items and num_variations == 1 and text_response.strip():
        items.append(text_response.strip())
    elif not items and text_response.strip(): # If multiple variations expected but not parsed
        # Fallback: return the whole block as one item, caller might need to handle this
        print(f"Warning: Could not parse {num_variations} items from Gemini response. Returning as single block.")
        items.append(text_response.strip())


    # If we have more items than requested, truncate. If fewer, the caller must handle.
    return items[:num_variations] if items else []

def generate_ad_text_with_gemini(prompt: str, num_variations: int = 1) -> list[str]:
    """Generates ad text using the Gemini model. Expects a list of strings if num_variations > 1."""
    if not PROJECT_ID:
        return [f"Error: GCP_PROJECT_ID not configured. Cannot call Gemini for {num_variations} variations."]
    try:
        # Log the prompt
        logger.log_text(f"Gemini Prompt: {prompt}")
        model = GenerativeModel(GEMINI_MODEL_NAME)
        response = model.generate_content([prompt], generation_config=generation_config)
        
        if response.candidates and response.candidates[0].content.parts:
            raw_text = response.candidates[0].content.parts[0].text
            if num_variations > 1:
                parsed_texts = parse_gemini_list_response(raw_text, num_variations)
                if len(parsed_texts) == num_variations:
                    return parsed_texts
                elif parsed_texts: # Got some, but not all
                     print(f"Warning: Expected {num_variations} ad texts, but parsed {len(parsed_texts)}. Response: {raw_text}")
                     # Pad with error messages or handle as per requirements
                     # For now, return what was parsed, router might need to check length
                     return parsed_texts 
                else: # Parsing failed completely
                    print(f"Error: Failed to parse {num_variations} ad texts from Gemini response: {raw_text}")
                    return [f"Error: Could not parse {num_variations} ad texts from response." for _ in range(num_variations)]
            else: # Single variation requested
                return [raw_text.strip()]
        else:
            print(f"Gemini response did not contain expected text: {response}")
            return [f"Sorry, I couldn't generate ad text for {num_variations} variations at this moment." for _ in range(num_variations)]
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return [f"Error generating ad text for {num_variations} variations: {e}" for _ in range(num_variations)]

def generate_ad_image_with_imagen(prompt: str, aspect_ratio: str = "1:1", number_of_images: int = 1) -> list[str]:
    """
    Generates ad images using the Imagen model and returns a list of base64 encoded data URIs.
    """
    if not PROJECT_ID:
        return [f"Error: GCP_PROJECT_ID not configured. Cannot call Imagen for {number_of_images} images."]
    
    image_data_list = []
    try:
        # Log the prompt
        logger.log_text(f"Imagen Prompt: {prompt}")
        model = ImageGenerationModel.from_pretrained(IMAGEN_MODEL_NAME)
        
        # Imagen's generate_images can take number_of_images directly
        response = model.generate_images(
            prompt=prompt,
            number_of_images=number_of_images, 
            aspect_ratio=aspect_ratio,
            # output_file_format="png", # Recommended
            # safety_filter_level="block_most", # Example
        )
        
        if response.images:
            for i in range(min(number_of_images, len(response.images))): # Ensure we don't go out of bounds
                image = response.images[i]
                if image._image_bytes:
                    image_bytes = image._image_bytes
                    base64_image = base64.b64encode(image_bytes).decode("utf-8")
                    image_data_list.append(f"data:image/png;base64,{base64_image}")
                else:
                    print(f"Warning: Image {i+1} from Imagen response did not contain image bytes. Image object: {image}")
                    image_data_list.append("Error: Image generation failed for this item (no bytes).")
            
            # If fewer images were returned than requested
            if len(image_data_list) < number_of_images:
                print(f"Warning: Requested {number_of_images} images, but Imagen returned {len(response.images)}.")
                # Pad with error messages for the missing images
                for _ in range(number_of_images - len(image_data_list)):
                    image_data_list.append("Error: Image not generated for this item (fewer returned than requested).")
            return image_data_list
        else:
            error_message = "Imagen response did not contain any images."
            print(error_message)
            return ["Error: Image generation failed or no images returned." for _ in range(number_of_images)]
            
    except Exception as e:
        print(f"Error calling Imagen API: {e}")
        # import traceback
        # print(traceback.format_exc())
        return [f"Error generating ad image: An unexpected error occurred. Details: {str(e)}" for _ in range(number_of_images)]
