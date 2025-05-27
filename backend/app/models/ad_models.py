from pydantic import BaseModel, Field
from enum import Enum
from typing import List, Optional

class CustomerType(str, Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"

class AdGenerationRequest(BaseModel):
    customer_type: CustomerType
    product: str
    product_description: str
    number_of_variations: Optional[int] = Field(default=1, description="Number of ad variations to generate. Frontend will send 3 if multiple are desired.")

class AdCreative(BaseModel):
    ad_text: str = Field(..., description="Generated advertisement text for one creative.")
    ad_image_data: str = Field(..., description="Generated advertisement image data as a base64 encoded string for one creative.")

class AdGenerationResponse(BaseModel):
    creatives: List[AdCreative] = Field(..., description="List of generated ad creatives.")
