from services import supabase
from postgrest import APIResponse
from models import Profile
from stores.prospect_store import prospect_store

class StorageError(Exception):
    """Raised when there's an error storing data in the database"""
    pass

def store_scraped_profile(result) -> None:
    """
    Stores the scraped profile data for a prospect.
    
    Args:
        result: The result object from agent.run()
        
    Raises:
        StorageError: If storing the profile data fails
        NoProspectsAvailableError: If no prospect is available to update
    """
    try:
        # Extract data from result
        prospect_id = prospect_store.prospect["id"]
        pre_parsed_data = result.final_result()

        
        # Validate and convert the data to a Profile object
        profile: Profile = Profile.model_validate_json(pre_parsed_data)
        profile_dict = profile.model_dump()
            
        # Log the profile_dict before attempting to store it
        print(f"Attempting to store profile_dict: {profile_dict}")

        # Update the prospect with the scraped profile
        result: APIResponse = (
            supabase.table("prospect")
            .update({"scraped_profile": profile_dict})
            .eq("id", prospect_id)
            .execute()
        )
        
        if not result.data:
            raise StorageError(f"Failed to store scraped profile for prospect {prospect_id}")
            
    except Exception as e:
        raise StorageError(f"Error storing scraped profile: {str(e)}")
   

