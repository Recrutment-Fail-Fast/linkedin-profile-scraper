from services import supabase

def store_score_and_evaluation(*, llm_score: float, llm_evaluation: str, prospect_evaluation_id: str):
    """
    Stores a prospect evaluation in the 'prospect_evaluation' table.
    Args:
        llm_score: The score assigned by the LLM.
        llm_evaluation: The textual evaluation from the LLM.
        prospect_evaluation_id: The ID of the prospect evaluation to update.
    Returns:
        The inserted evaluation data, or None if an error occurs.
    """
    try:
        response = (
            supabase.table("prospect_evaluation")
            .update({
                "llm_score": llm_score,
                "llm_evaluation": llm_evaluation,
            })
            .eq("id", prospect_evaluation_id)
            .execute()
        )
        # The response.data will be a dictionary if successful
        if not response.data:
            raise Exception("Error storing prospect evaluation: No data returned or error in response object.")
        
        return response.data

    except Exception as e:
        print(f"Error storing prospect evaluation: {e}")
        return None
