PROMPT_TEMPLATES = {
    "Marketing & Business": {
        "Product Description": {
            "template": "Write a compelling product description for {product_name}. Highlight its key features: {key_features}. Target audience: {target_audience}. Focus on benefits and create urgency.",
            "placeholders": ["product_name", "key_features", "target_audience", "previous_post_reference"],
            "description": "Generate persuasive copy that sells, focusing on features and benefits."
        },
        "Email Marketing": {
            "template": "Create an engaging email marketing campaign for {product_service}. Subject line should be catchy. Include a clear call-to-action for {desired_action}. Keep it under 200 words.",
            "placeholders": ["product_service", "desired_action", "previous_post_reference"],
            "description": "Craft concise and effective emails with a strong call-to-action."
        },
        "Sales Pitch": {
            "template": "Write a persuasive sales pitch for {product_service} targeting {target_market}. Address their main pain point: {pain_point}. Include social proof and a strong closing.",
            "placeholders": ["product_service", "target_market", "pain_point", "previous_post_reference"],
            "description": "Develop a compelling pitch that addresses customer needs and drives sales."
        },
        "Press Release": {
            "template": "Write a professional press release announcing {announcement}. Include quotes from {spokesperson_title} and highlight the impact on {industry_market}.",
            "placeholders": ["announcement", "spokesperson_title", "industry_market", "previous_post_reference"],
            "description": "Announce company news formally and professionally to the media."
        }
    },
    
    "Social Media": {
        "Instagram Caption": {
            "template": "Create an engaging Instagram caption for {post_topic}. Include relevant hashtags, ask a question to boost engagement, and match the tone to {personality}. Keep it authentic and relatable.",
            "placeholders": ["post_topic", "personality", "previous_post_reference"],
            "description": "Write catchy, engaging captions with hashtags to boost social media presence."
        },
        "LinkedIn Post": {
            "template": "Write a professional LinkedIn post about {topic}. Share insights or lessons learned, add personal experience if relevant, and end with a thought-provoking question. Target: {target_audience}.",
            "placeholders": ["topic", "target_audience", "previous_post_reference"],
            "description": "Share professional insights and stories to build your network and authority."
        },
        "Twitter Thread": {
            "template": "Create a Twitter thread (5-7 tweets) explaining {topic}. Make it informative yet engaging. Start with a hook, break down complex ideas, and end with a call-to-action or question.",
            "placeholders": ["topic", "previous_post_reference"],
            "description": "Break down a complex topic into an engaging and informative multi-tweet thread."
        },
        "YouTube Description": {
            "template": "Write a YouTube video description for '{video_title}'. Include what viewers will learn, timestamps for key sections: {key_sections}, and relevant keywords for SEO.",
            "placeholders": ["video_title", "key_sections", "previous_post_reference"],
            "description": "Optimize your video's visibility with an SEO-friendly and informative description."
        }
    },
    
    "Creative Writing": {
        "Short Story": {
            "template": "Write a {genre} short story (500-800 words) featuring {main_character} who faces {central_conflict}. Setting: {setting}. Include dialogue and a satisfying resolution.",
            "placeholders": ["genre", "main_character", "central_conflict", "setting", "previous_post_reference"],
            "description": "Craft a complete narrative with characters, conflict, and resolution."
        },
        "Character Description": {
            "template": "Create a detailed character profile for {character_name}, a {age}-year-old {profession}. Include their personality traits, backstory, motivations, and a unique quirk. Make them feel real and relatable.",
            "placeholders": ["character_name", "age", "profession", "previous_post_reference"],
            "description": "Build a multi-dimensional character with a rich backstory and personality."
        },
        "Dialogue Scene": {
            "template": "Write a dialogue scene between {character_1} and {character_2} discussing {topic}. Show their personalities through their speech patterns. Setting: {location}. Include some tension or conflict.",
            "placeholders": ["character_1", "character_2", "topic", "location", "previous_post_reference"],
            "description": "Write a compelling conversation that reveals character and advances the plot."
        },
        "Poem": {
            "template": "Write a {poem_type} poem about {subject}. Capture the emotion of {emotion} and use vivid imagery. {length} verses.",
            "placeholders": ["poem_type", "subject", "emotion", "length", "previous_post_reference"],
            "description": "Express emotions and ideas through the art of poetry and vivid imagery."
        }
    },
    
    "Educational & Explanatory": {
        "ELI5 Explanation": {
            "template": "Explain {complex_topic} like I'm 5 years old. Use simple words, fun analogies, and examples a child would understand. Make it engaging and easy to follow.",
            "placeholders": ["complex_topic", "previous_post_reference"],
            "description": "Break down a difficult subject into a simple and easy-to-understand explanation."
        },
        "How-To Guide": {
            "template": "Write a step-by-step guide on how to {task}. Include what you'll need, detailed instructions, common mistakes to avoid, and tips for success. Target audience: {skill_level}.",
            "placeholders": ["task", "skill_level", "previous_post_reference"],
            "description": "Create a clear, step-by-step guide for users of any skill level to complete a task."
        },
        "Comparison Article": {
            "template": "Compare {option_1} vs {option_2} for {use_case}. Include pros and cons of each, pricing if relevant, and a clear recommendation for different user types.",
            "placeholders": ["option_1", "option_2", "use_case", "previous_post_reference"],
            "description": "Analyze two or more options to help readers make an informed decision."
        },
        "Study Notes": {
            "template": "Create comprehensive study notes on {subject_topic}. Include key concepts, important dates/formulas, memory aids, and practice questions. Format for easy review.",
            "placeholders": ["subject_topic", "previous_post_reference"],
            "description": "Summarize a topic into organized, easy-to-review notes for learning."
        }
    },
    
    "Professional": {
        "Cover Letter": {
            "template": "Write a compelling cover letter for {job_title} position at {company_name}. Highlight relevant experience: {key_experience}. Show enthusiasm and explain why you're a perfect fit.",
            "placeholders": ["job_title", "company_name", "key_experience", "previous_post_reference"],
            "description": "Write a persuasive letter to introduce yourself and highlight your qualifications."
        },
        "Meeting Agenda": {
            "template": "Create a professional meeting agenda for {meeting_purpose}. Duration: {duration}. Key participants: {participants}. Include time allocations and desired outcomes.",
            "placeholders": ["meeting_purpose", "duration", "participants", "previous_post_reference"],
            "description": "Outline the structure and objectives of a meeting to keep it on track."
        },
        "Project Proposal": {
            "template": "Write a project proposal for {project_name}. Problem it solves: {problem}. Proposed solution, timeline: {timeline}, budget estimate, and expected outcomes.",
            "placeholders": ["project_name", "problem", "timeline", "previous_post_reference"],
            "description": "Create a detailed document to get buy-in and approval for a new project."
        },
        "Performance Review": {
            "template": "Write a constructive performance review for {role} focusing on {review_period}. Highlight achievements: {key_achievements}. Include areas for improvement and development goals.",
            "placeholders": ["role", "review_period", "key_achievements", "previous_post_reference"],
            "description": "Provide balanced and constructive feedback for employee development."
        }
    },
    
    "Personal": {
        "Love Letter": {
            "template": "Write a heartfelt love letter to {recipient} mentioning {special_memory} and expressing {main_feeling}. Make it personal, romantic, and genuine.",
            "placeholders": ["recipient", "special_memory", "main_feeling", "previous_post_reference"],
            "description": "Express deep personal feelings of love and affection in a heartfelt letter."
        },
        "Thank You Note": {
            "template": "Write a sincere thank you note to {recipient} for {reason}. Mention specific impact: {specific_impact} and express genuine gratitude.",
            "placeholders": ["recipient", "reason", "specific_impact", "previous_post_reference"],
            "description": "Show appreciation and gratitude in a thoughtful and personal note."
        },
        "Birthday Message": {
            "template": "Write a warm birthday message for {person} who is turning {age}. Include shared memories: {memory} and wishes for {upcoming_year_hopes}.",
            "placeholders": ["person", "age", "memory", "upcoming_year_hopes", "previous_post_reference"],
            "description": "Craft a personal and celebratory message for someone's special day."
        },
        "Apology Letter": {
            "template": "Write a sincere apology letter to {recipient} for {mistake_situation}. Take full responsibility, explain what you learned, and outline how you'll prevent it in the future.",
            "placeholders": ["recipient", "mistake_situation", "previous_post_reference"],
            "description": "Sincerely apologize and take responsibility for a mistake you made."
        }
    }
}

def get_template_categories():
    return list(PROMPT_TEMPLATES.keys())

def get_templates_in_category(category):
    return PROMPT_TEMPLATES.get(category, {})

def get_template_data(category, template_name):
    return PROMPT_TEMPLATES.get(category, {}).get(template_name, {})

def fill_template(template_text, **kwargs):
    try:
        # Filter out None values before formatting
        valid_kwargs = {k: v for k, v in kwargs.items() if v is not None}
        return template_text.format(**valid_kwargs)
    except KeyError as e:
        return f"Error: Missing value for {e}"