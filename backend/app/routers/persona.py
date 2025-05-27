from fastapi import APIRouter, HTTPException
from app.services import bigquery_service

router = APIRouter()

@router.get("/persona-segments", tags=["Persona"])
async def get_persona_segments():
    """
    Retrieves persona segment data from BigQuery.
    """
    try:
        data = bigquery_service.get_persona_data()
        if data is None:
            # This could be due to missing env vars or a query error.
            # The service function already prints a more specific error.
            raise HTTPException(status_code=500, detail="Failed to retrieve persona data from BigQuery. Check server logs for details.")
        return data
    except Exception as e:
        # Catch any other unexpected errors
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
