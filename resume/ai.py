# from decouple import config
# from google import genai
# import json
# api_key=config("GEMINI_API_KEY")
# client = genai.Client(api_key=api_key)

# def analyze_resume(resume_text):
#     prompt=f""" 
# You are a resume analyzer. Read the resume text carefully and extract the candidate's job role and related information. 
# Return ONLY valid JSON that strictly matches the schema below. 
# Do not include any extra keys, comments, or text outside JSON. 
# If any value is missing, use an empty string "", an empty array [], or 0 as appropriate.

# Schema:
# {{
#   "detected_name": "",
#   "detected_role": "",
#   "experience_level": "",
#   "match_score": 0,
#   "matched_skills": [],
#   "missing_skills": [],
#   "suggestions": ""
# }}

# Rules:
# - detected_name: Candidate's full name if available.
# - detected_role: The primary job role/title inferred from the resume (e.g., "Full-Stack Developer").
# - experience_level: One of ["Junior", "Mid-level", "Senior"] based on years and responsibilities.
# - match_score: 0–100 overall fit for a web development role (React, Django REST, Tailwind, WebSockets, deployment).
# - matched_skills: List of skills found in resume that match the target stack.
# - missing_skills: List of important skills from target stack not found in resume.
# - suggestions: Short advice on how candidate can improve their profile (e.g., "Add more deployment details", "Highlight backend scaling experience").



# Now analyze this resume text:

# {resume_text}
# """
#     response = client.models.generate_content(
#     model="gemini-2.5-flash", contents=prompt
#     )
#     text=response.text.replace("`","").replace("json","")
#     return json.loads(text)


from decouple import config
from google import genai
import json
import re

def _extract_json(text: str):
    """
    Extract first valid JSON object from text.
    """
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError("No JSON object found")
    return json.loads(match.group())

def analyze_resume(resume_text):
    client = genai.Client(api_key=config("GEMINI_API_KEY"))

    prompt = f"""
You are a resume analyzer.

STRICT RULES:
- Output ONLY valid JSON
- No markdown
- No explanation
- No backticks
- No extra text

Schema:
{{
  "detected_name": "",
  "detected_role": "",
  "experience_level": "",
  "match_score": 0,
  "matched_skills": [],
  "missing_skills": [],
  "suggestions": ""
}}

Resume text:
{resume_text}
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
          
        )

        raw = response.text.strip()

        # 1️⃣ Try direct JSON
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            pass

        # 2️⃣ Try extracting JSON from text
        return _extract_json(raw)

    except Exception as e:
        print("Gemini error:", e)

        # 3️⃣ FINAL SAFE FALLBACK (NEVER 500)
        return {
            "detected_name": "",
            "detected_role": "",
            "experience_level": "",
            "match_score": 0,
            "matched_skills": [],
            "missing_skills": [],
            "suggestions": "AI could not reliably parse this resume. Try a clearer resume format."
        }

