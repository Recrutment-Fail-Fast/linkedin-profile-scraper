from services import supabase

def get_profiles_to_scrape():
    response = supabase.table("prospects").select("linkedin_url").eq("is_scraped",False).limit(1).execute()
    if not response.data:
        raise Exception("No profiles to scrape")
    return response.data
