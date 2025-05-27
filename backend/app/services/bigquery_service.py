import os
from google.cloud import bigquery

def get_persona_data():
    """
    Fetches persona data from BigQuery.

    The dataset and table are specified by environment variables:
    - BIGQUERY_DATASET
    - BIGQUERY_TABLE_PERSONA

    Returns:
        dict: A dictionary where keys are column names and values are lists of column values.
              Returns None if there's an error or if environment variables are not set.
    """
    dataset_id = os.getenv("BIGQUERY_DATASET")
    table_id = os.getenv("BIGQUERY_TABLE_PERSONA") # Using a more specific name for the table env var

    if not dataset_id or not table_id:
        print("Error: BIGQUERY_DATASET or BIGQUERY_TABLE_PERSONA environment variables not set.")
        # In a real application, you might raise an exception or handle this more gracefully.
        return None

    client = bigquery.Client()

    query = f"""
        SELECT persona_age_group_profile, persona_segment_description
        FROM `{client.project}.{dataset_id}.{table_id}`
        LIMIT 30
    """

    try:
        query_job = client.query(query)
        results = query_job.result()  # Waits for the job to complete.

        # Convert results to a dictionary of lists
        data = {}
        for row in results:
            for key, value in row.items():
                if key not in data:
                    data[key] = []
                data[key].append(value)
        return data
    except Exception as e:
        print(f"An error occurred while querying BigQuery: {e}")
        return None

if __name__ == '__main__':
    # This is for local testing of the service, requires GOOGLE_APPLICATION_CREDENTIALS
    # and the necessary environment variables to be set.
    # Example:
    # export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-file.json"
    # export BIGQUERY_DATASET="your_dataset"
    # export BIGQUERY_TABLE_PERSONA="your_persona_table"
    data = get_persona_data()
    if data:
        print("Successfully fetched data:")
        for key, values in data.items():
            print(f"- {key}: {len(values)} items")
    else:
        print("Failed to fetch data.")
