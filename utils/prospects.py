from services import supabase
from postgrest import APIResponse
from models.models import Profile
from utils.models import NoProspectsAvailableError, ProspectData, ProspectError, StorageError
from stores.prospect_store import prospect_store


def get_prospect_to_scrape() -> ProspectData:
    """
    Retrieves the next prospect to be scraped from the database.
    
    Returns:
        ProspectData: Dictionary containing prospect id and linkedin_url
        
    Raises:
        NoProspectsAvailableError: If no prospects are available for scraping
    """
    try:
        response: APIResponse = (
            supabase.table("prospect")
            .select("id,linkedin_url")
            .is_("scraped_profile", None)
            .limit(1)
            .execute()
        )
        
        if not response.data:
            raise NoProspectsAvailableError("No profiles available for scraping")
            
        return {
            "id": response.data[0]["id"],
            "linkedin_url": response.data[0]["linkedin_url"]
        }
    except Exception as e:
        raise ProspectError(f"Error fetching prospect: {str(e)}")


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
            
    except NoProspectsAvailableError:
        raise
    except Exception as e:
        raise StorageError(f"Error storing scraped profile: {str(e)}")
   

