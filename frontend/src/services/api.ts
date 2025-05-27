import axios from 'axios';

// The base URL for the API. Since the frontend is served by the same FastAPI
// backend, relative paths can be used.
const API_BASE_URL = '/api/v1'; // Adjust if your FastAPI prefix is different

export interface AdGenerationRequestPayload {
  customer_type: 'positive' | 'negative';
  product: string;
  product_description: string;
  number_of_variations?: number; // Added to specify how many ads to generate
}

export interface AdCreative {
  ad_text: string;
  ad_image_data: string; 
}

export interface AdGenerationResponseData {
  creatives: AdCreative[]; // Expects a list of ad creatives
}

/**
 * Calls the backend API to generate ad content.
 * @param payload - The customer type, product, description, and number of variations.
 * @returns A promise that resolves to an array of ad creatives.
 */
export const generateAdContent = async (payload: AdGenerationRequestPayload): Promise<AdGenerationResponseData> => {
  try {
    // Ensure number_of_variations is included in the payload sent to the backend.
    // The backend will default if not provided, but explicit is better.
    const requestPayload = { ...payload, number_of_variations: payload.number_of_variations || 3 };
    const response = await axios.post<AdGenerationResponseData>(`${API_BASE_URL}/generate_ad_content`, requestPayload);
    return response.data;
  } catch (error) {
    console.error('Error generating ad content:', error);
    if (axios.isAxiosError(error) && error.response) {
      // Attempt to parse and throw a more specific error message from the backend if available
      const errorDetail = error.response.data?.detail || 'Failed to generate ad content due to a server error.';
      throw new Error(errorDetail);
    }
    throw new Error('Failed to generate ad content. An unknown error occurred.');
  }
};
