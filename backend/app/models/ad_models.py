from pydantic import BaseModel, Field
# from enum import Enum # Enum is no longer needed
from typing import List, Optional

class AdGenerationRequest(BaseModel):
    # customer_type: CustomerType # Removed
    product: str
    product_description: str
    persona_description: Optional[str] = Field(None, description="Detailed description of the target persona.")
    number_of_variations: Optional[int] = Field(default=1, description="Number of ad variations to generate. Frontend will send 3 if multiple are desired.")

class AdCreative(BaseModel):
    ad_text: str = Field(..., description="Generated advertisement text for one creative.")
    ad_image_data: str = Field(..., description="Generated advertisement image data as a base64 encoded string for one creative.")

class AdGenerationResponse(BaseModel):
    creatives: List[AdCreative] = Field(..., description="List of generated ad creatives.")
