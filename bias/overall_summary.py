from llm_api import Prompt
import os

# Read the system prompt from file
prompt_file_path = os.path.join(os.path.dirname(__file__), "overall_summary_prompt.txt")
with open(prompt_file_path, "r") as f:
    SYSTEM_PROMPT = f.read()


def generate_bias_summary(title="", summary_text="", bias_score=None, reasons=None):
    """
    Generate a concise summary explaining the article's bias.
    Returns a short string. If the LLM call fails, returns a best-effort fallback string.
    """
    reasons = reasons or []
    chat = Prompt(system_message=SYSTEM_PROMPT)

    # Build a compact input payload for the model
    payload_lines = ["Summarize ONLY the bias aspect:"]
    if title:
        payload_lines.append(f"Title: {title}")
    if summary_text:
        # keep summary short when sending
        payload_lines.append(f"Summary: {summary_text[:800]}")
    if bias_score is not None:
        payload_lines.append(f"BiasScore: {bias_score}")
    if reasons:
        # include up to 3 reasons
        for i, r in enumerate(reasons[:3], 1):
            payload_lines.append(f"Reason{i}: {r}")

    user_input = "\n".join(payload_lines)

    try:
        response = chat.prompt(user_input)
        result = response.strip()
        # Only return if non-empty
        if result:
            return result
    except Exception as e:
        pass
    
    # Fallback: compose from available data
    if reasons and len(reasons) > 0:
        return f"Article contains biased language: {reasons[0]}"
    if bias_score is not None:
        return f"Bias detected at level {bias_score}/100."
    return "Bias analysis in progress."


def generate_drama_summary(summary_text="", drama_index=None):
    """
    Generate a concise summary explaining the article's drama/emotional intensity.
    Returns a short string. If the LLM call fails, returns a best-effort fallback string.
    """
    chat = Prompt(system_message=SYSTEM_PROMPT)

    # Build a compact input payload for the model
    payload_lines = ["Summarize ONLY the drama/emotional intensity aspect:"]
    if summary_text:
        # keep summary short when sending
        payload_lines.append(f"Summary: {summary_text[:800]}")
    if drama_index is not None:
        payload_lines.append(f"DramaIndex: {drama_index}")

    user_input = "\n".join(payload_lines)

    try:
        response = chat.prompt(user_input)
        result = response.strip()
        # Only return if non-empty
        if result:
            return result
    except Exception as e:
        pass
    
    # Fallback: compose from available data
    if drama_index is not None:
        if drama_index <= 20:
            return "Article is calm and measured in tone."
        elif drama_index <= 40:
            return "Article uses mild emotional language."
        elif drama_index <= 60:
            return "Article is emotionally charged in presentation."
        elif drama_index <= 80:
            return "Article uses highly dramatic language and framing."
        else:
            return "Article employs sensationalist tactics."
    return "Drama analysis in progress."


def generate_overall_summary(title="", summary_text="", bias_score=None, drama_index=None, reasons=None):
    """
    Generate both bias and drama summaries.
    Returns a tuple (bias_summary, drama_summary).
    """
    bias_summary = generate_bias_summary(title, summary_text, bias_score, reasons)
    drama_summary = generate_drama_summary(summary_text, drama_index)
    return bias_summary, drama_summary
