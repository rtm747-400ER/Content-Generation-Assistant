def build_prompt(user_input, tone="Default", style="Default", format_type="Default"):
    """
    Preprocess user input with style instructions.
    Returns system + user messages for Groq API.
    """

    instructions = []

    if tone != "Default":
        instructions.append(f"Use a {tone.lower()} tone.")
    if style != "Default":
        instructions.append(f"Follow a {style.lower()} writing style.")
    
    if format_type != "Default":
        if format_type.lower() == "email":
            instructions.append("Write this as a professional email.")
        elif format_type.lower() == "linkedin post":
            instructions.append("Write this as a concise, professional LinkedIn post.")
        elif format_type.lower() == "tweet / thread":
            instructions.append("Write this as a short, attention-grabbing tweet or thread.")
        elif format_type.lower() == "blog post":
            instructions.append("Write this as a detailed, engaging blog post.")
        elif format_type.lower() == "journal / diary entry":
            instructions.append("Write this as a personal journal or diary entry.")
        elif format_type.lower() == "story / fiction":
            instructions.append("Write this as a creative story or fiction piece.")
        elif format_type.lower() == "summary / report":
            instructions.append("Write this as a clear and concise summary or report.")
        else:
            instructions.append(f"Format the response as a {format_type.lower()}.")

    system_msg = " ".join(instructions) if instructions else "Respond helpfully to the user."

    return [
        {"role": "system", "content": system_msg},
        {"role": "user", "content": user_input},
    ]
