from utils import get_profiles_to_scrape


profiles = get_profiles_to_scrape()

initial_actions = [{'open_tab': {'url': profiles[0]['linkedin_url']}},{'scroll_down': {'amount': 1000}}]

print(initial_actions)