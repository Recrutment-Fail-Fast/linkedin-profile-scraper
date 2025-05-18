from utils import get_prospect_to_scrape
from stores.prospect_store import prospect_store

prospect_store.prospect = get_prospect_to_scrape()

initial_actions = [
    {'open_tab': {'url': prospect_store.prospect["linkedin_url"]}},
    {'scroll_down': {'amount': 1000}}
]
