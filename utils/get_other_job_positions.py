from services import supabase
from stores.prospect import prospect_store

class JobPositionError(Exception):
    """Raised when there's an error fetching job positions from the database"""
    pass

def get_other_job_positions():
    """
    Calls a PostgreSQL function to get job positions associated with a specific prospect where evaluations have not been completed.
    """
    try:
        prospect_id = prospect_store.prospect["prospect_id"]
        response = supabase.rpc("get_other_job_positions_for_prospect", {"p_prospect_id": prospect_id}).execute()
        return response.data
    except Exception as e:
        raise JobPositionError(f"Error fetching job positions: {str(e)}")
