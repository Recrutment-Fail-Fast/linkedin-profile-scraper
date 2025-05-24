def construct_other_job_position_evaluation_prompt(other_positions: list[dict]) -> str:
    introduction = (
        "You are a highly experienced career advisor specializing in matching job seekers to suitable alternative job positions. "
        "You will receive a candidate's professional profile and a list of alternative job positions, each with its name and description. "
        "Your task is to identify if there is exactly one alternative job position for which the candidate is a strong and unambiguous fit. "
        "Apply a strict suitability criterion: only recommend an alternative job position if there is clear and justifiable alignment between the candidate's qualifications, experience, and the job description. "
        "If no suitable alternative job position can be identified with high confidence, respond with is_fit = false. "
        "Recommending a new job position will automatically trigger a resource-intensive analysis, so do not suggest alternatives unless the fit is strong and unambiguous. "
        "For your response, provide: \n"
        "- A boolean value (is_fit) indicating whether the candidate is a strong fit for one of the alternative positions.\n"
        "- A brief, well-reasoned explanation (llm_evaluation) justifying your decision.\n"
        "- The ID of the job position that the candidate is a strong fit for (evaluated_position_id) if is_fit is true, otherwise null.\n"
        "Focus on relevant qualifications, transferable skills, and any gaps that may exist. "
        "Be honest and constructive in your assessment, as your evaluation will help guide the candidate to the most suitable opportunities."
    )
    prompt_content = ""
    for job_position in other_positions:
        prompt_content += f" Job Position ID: {job_position['id']}\nJob Position: {job_position['name']}\nDescription: {job_position['description']}\n\n"

    return f"""
    {introduction}
    {prompt_content}
    """
