from services import supabase

def get_job_evaluation_data(
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
            "get_job_evaluation_data",
            {"prospect_evaluation_id": prospect_evaluation_id},
        ).execute()

        result_data = response.data[0]

        profile = result_data.get("profile_text")
        evaluation_criteria = result_data.get("evaluation_criteria")
        llm_score_threshold = result_data.get("llm_score_threshold")

        if not profile or not evaluation_criteria or not llm_score_threshold:
            raise Exception(
                f"Error fetching details for prospect evaluation {prospect_evaluation_id}: Missing prospect or job position data after join."
            )

        return result_data

    except Exception as e:
        raise Exception(
            f"An unexpected error occurred while fetching details for prospect evaluation {prospect_evaluation_id}: {e}"
        )