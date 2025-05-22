from stores.prospect import prospect_store

def get_initial_actions():
    linkedin_url = prospect_store.prospect["linkedin_url"]
    return [
        {'open_tab': {'url': linkedin_url}},
        {'scroll_down': {'amount': 1000}}
    ]
