from services import supabase

async def get_evaluation_criteria_and_prospect_profile(
    prospect_evaluation_id: str,
) -> dict:
    """
    Fetches the scraped profile of a prospect and the evaluation criteria of a job position
    associated with a specific prospect evaluation.
    Args:
        prospect_evaluation_id: The ID of the prospect evaluation (UUID).
    Returns:
        An object containing the prospect's scraped profile and job's evaluation criteria,
        or None if not found or an error occurs.
    """


    try:
        response = supabase.rpc(
            "get_evaluation_criteria_and_prospect_profile",
            {"prospect_evaluation_id": prospect_evaluation_id},
        ).execute()

        result_data = response.data[0]

        profile = result_data.get("profile_text")
        evaluation_criteria = result_data.get("evaluation_criteria")

        if not profile or not evaluation_criteria:
            raise Exception(
                f"Error fetching details for prospect evaluation {prospect_evaluation_id}: Missing prospect or job position data after join."
            )

        return result_data

    except Exception as e:
        raise Exception(
            f"An unexpected error occurred while fetching details for prospect evaluation {prospect_evaluation_id}: {e}"
        )