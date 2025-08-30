PROMPT_TEMPLATES = {
    "Marketing & Business": {
        "Product Description": {
            "template": "Write a compelling product description for {product_name}. Highlight its key features: {key_features}. Target audience: {target_audience}. Focus on benefits and create urgency.",
            "placeholders": ["product_name", "key_features", "target_audience"],
            "example": "Write a compelling product description for wireless headphones. Highlight its key features: noise cancellation, 30-hour battery. Target audience: busy professionals."
        },
        "Email Marketing": {
            "template": "Create an engaging email marketing campaign for {product_service}. Subject line should be catchy. Include a clear call-to-action for {desired_action}. Keep it under 200 words.",
            "placeholders": ["product_service", "desired_action"],
            "example": "Create an engaging email marketing campaign for online fitness courses. Include a clear call-to-action for signing up for free trial."
        },
        "Sales Pitch": {
            "template": "Write a persuasive sales pitch for {product_service} targeting {target_market}. Address their main pain point: {pain_point}. Include social proof and a strong closing.",
            "placeholders": ["product_service", "target_market", "pain_point"],
            "example": "Write a persuasive sales pitch for project management software targeting small business owners. Address their main pain point: team coordination."
        },
        "Press Release": {
            "template": "Write a professional press release announcing {announcement}. Include quotes from {spokesperson_title} and highlight the impact on {industry_market}.",
            "placeholders": ["announcement", "spokesperson_title", "industry_market"],
            "example": "Write a professional press release announcing our new AI chatbot. Include quotes from CEO and highlight the impact on customer service industry."
        }
    },
    
    "Social Media": {
        "Instagram Caption": {
            "template": "Create an engaging Instagram caption for {post_topic}. Include relevant hashtags, ask a question to boost engagement, and match the tone to {personality}. Keep it authentic and relatable.",
            "placeholders": ["post_topic", "personality"],
            "example": "Create an engaging Instagram caption for morning coffee routine. Match the tone to friendly and energetic brand personality."
        },
        "LinkedIn Post": {
            "template": "Write a professional LinkedIn post about {topic}. Share insights or lessons learned, add personal experience if relevant, and end with a thought-provoking question. Target: {target_audience}.",
            "placeholders": ["topic", "target_audience"],
            "example": "Write a professional LinkedIn post about remote work productivity. Target: working professionals and managers."
        },
        "Twitter Thread": {
            "template": "Create a Twitter thread (5-7 tweets) explaining {topic}. Make it informative yet engaging. Start with a hook, break down complex ideas, and end with a call-to-action or question.",
            "placeholders": ["topic"],
            "example": "Create a Twitter thread explaining the basics of cryptocurrency for beginners."
        },
        "YouTube Description": {
            "template": "Write a YouTube video description for '{video_title}'. Include what viewers will learn, timestamps for key sections: {key_sections}, and relevant keywords for SEO.",
            "placeholders": ["video_title", "key_sections"],
            "example": "Write a YouTube video description for 'How to Start a Side Hustle'. Include timestamps for key sections: research, planning, execution."
        }
    },
    
    "Creative Writing": {
        "Short Story": {
            "template": "Write a {genre} short story (500-800 words) featuring {main_character} who faces {central_conflict}. Setting: {setting}. Include dialogue and a satisfying resolution.",
            "placeholders": ["genre", "main_character", "central_conflict", "setting"],
            "example": "Write a mystery short story featuring a detective who faces a locked-room murder. Setting: 1920s London."
        },
        "Character Description": {
            "template": "Create a detailed character profile for {character_name}, a {age}-year-old {profession}. Include their personality traits, backstory, motivations, and a unique quirk. Make them feel real and relatable.",
            "placeholders": ["character_name", "age", "profession"],
            "example": "Create a detailed character profile for Sarah, a 28-year-old librarian."
        },
        "Dialogue Scene": {
            "template": "Write a dialogue scene between {character_1} and {character_2} discussing {topic}. Show their personalities through their speech patterns. Setting: {location}. Include some tension or conflict.",
            "placeholders": ["character_1", "character_2", "topic", "location"],
            "example": "Write a dialogue scene between a strict teacher and rebellious student discussing missed homework. Setting: after-school classroom."
        },
        "Poem": {
            "template": "Write a {poem_type} poem about {subject}. Capture the emotion of {emotion} and use vivid imagery. {length} verses.",
            "placeholders": ["poem_type", "subject", "emotion", "length"],
            "example": "Write a free verse poem about autumn leaves. Capture the emotion of nostalgia and use vivid imagery. 3 verses."
        }
    },
    
    "Educational & Explanatory": {
        "ELI5 Explanation": {
            "template": "Explain {complex_topic} like I'm 5 years old. Use simple words, fun analogies, and examples a child would understand. Make it engaging and easy to follow.",
            "placeholders": ["complex_topic"],
            "example": "Explain how the internet works like I'm 5 years old."
        },
        "How-To Guide": {
            "template": "Write a step-by-step guide on how to {task}. Include what you'll need, detailed instructions, common mistakes to avoid, and tips for success. Target audience: {skill_level}.",
            "placeholders": ["task", "skill_level"],
            "example": "Write a step-by-step guide on how to start a vegetable garden. Target audience: complete beginners."
        },
        "Comparison Article": {
            "template": "Compare {option_1} vs {option_2} for {use_case}. Include pros and cons of each, pricing if relevant, and a clear recommendation for different user types.",
            "placeholders": ["option_1", "option_2", "use_case"],
            "example": "Compare iPhone vs Android for college students."
        },
        "Study Notes": {
            "template": "Create comprehensive study notes on {subject_topic}. Include key concepts, important dates/formulas, memory aids, and practice questions. Format for easy review.",
            "placeholders": ["subject_topic"],
            "example": "Create comprehensive study notes on the American Civil War."
        }
    },
    
    "Professional": {
        "Cover Letter": {
            "template": "Write a compelling cover letter for {job_title} position at {company_name}. Highlight relevant experience: {key_experience}. Show enthusiasm and explain why you're a perfect fit.",
            "placeholders": ["job_title", "company_name", "key_experience"],
            "example": "Write a compelling cover letter for Software Developer position at TechCorp. Highlight relevant experience: 3 years Python, team leadership."
        },
        "Meeting Agenda": {
            "template": "Create a professional meeting agenda for {meeting_purpose}. Duration: {duration}. Key participants: {participants}. Include time allocations and desired outcomes.",
            "placeholders": ["meeting_purpose", "duration", "participants"],
            "example": "Create a professional meeting agenda for quarterly review. Duration: 90 minutes. Key participants: team leads and manager."
        },
        "Project Proposal": {
            "template": "Write a project proposal for {project_name}. Problem it solves: {problem}. Proposed solution, timeline: {timeline}, budget estimate, and expected outcomes.",
            "placeholders": ["project_name", "problem", "timeline"],
            "example": "Write a project proposal for employee wellness app. Problem it solves: low employee engagement. Timeline: 6 months."
        },
        "Performance Review": {
            "template": "Write a constructive performance review for {role} focusing on {review_period}. Highlight achievements: {key_achievements}. Include areas for improvement and development goals.",
            "placeholders": ["role", "review_period", "key_achievements"],
            "example": "Write a constructive performance review for junior developer focusing on Q4 2024. Highlight achievements: completed 3 major features, improved code quality."
        }
    },
    
    "Personal": {
        "Love Letter": {
            "template": "Write a heartfelt love letter to {recipient} mentioning {special_memory} and expressing {main_feeling}. Make it personal, romantic, and genuine.",
            "placeholders": ["recipient", "special_memory", "main_feeling"],
            "example": "Write a heartfelt love letter to Sarah mentioning our first date at the coffee shop and expressing gratitude for her support."
        },
        "Thank You Note": {
            "template": "Write a sincere thank you note to {recipient} for {reason}. Mention specific impact: {specific_impact} and express genuine gratitude.",
            "placeholders": ["recipient", "reason", "specific_impact"],
            "example": "Write a sincere thank you note to my mentor for career guidance. Mention specific impact: helped me land my dream job."
        },
        "Birthday Message": {
            "template": "Write a warm birthday message for {person} who is turning {age}. Include shared memories: {memory} and wishes for {upcoming_year_hopes}.",
            "placeholders": ["person", "age", "memory", "upcoming_year_hopes"],
            "example": "Write a warm birthday message for Mom who is turning 55. Include shared memories: family vacations and wishes for health and happiness."
        },
        "Apology Letter": {
            "template": "Write a sincere apology letter to {recipient} for {mistake_situation}. Take full responsibility, explain what you learned, and outline how you'll prevent it in the future.",
            "placeholders": ["recipient", "mistake_situation"],
            "example": "Write a sincere apology letter to my best friend for missing their important event."
        }
    }
}


def get_template_categories():
    """Return list of template categories."""
    return list(PROMPT_TEMPLATES.keys())


def get_templates_in_category(category):
    """Return templates for a specific category."""
    return PROMPT_TEMPLATES.get(category, {})


def get_template_data(category, template_name):
    """Get template data including placeholders and example."""
    return PROMPT_TEMPLATES.get(category, {}).get(template_name, {})


def fill_template(template_text, **kwargs):
    """Fill template with provided values."""
    try:
        return template_text.format(**kwargs)
    except KeyError as e:
        return f"Error: Missing value for {e}"