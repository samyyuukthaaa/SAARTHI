
import re
import json


def extract_section(text: str, label: str) -> str:
    pattern = rf"{label}\s*:\s*(.*?)(?=\n\s*[A-Za-z][A-Za-z /_-]*\s*:|$)"
    match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
    return match.group(1).strip() if match else ""


def parse_cv(cv_text: str) -> dict:

    cv_text = (cv_text or "").strip()

    if not cv_text:
        return {
            "error": "CV text is empty",
            "skills": [],
            "projects": [],
            "education": ""
        }

    # Extract explicitly mentioned skills
    skills_section = extract_section(cv_text, "Skills")

    skills = [
        item.strip(" -•")
        for item in re.split(r"[,;\n|]", skills_section)
        if item.strip(" -•")
    ] if skills_section else []

    # Extract projects
    projects_section = extract_section(cv_text, "Projects")

    projects = [
        item.strip(" -•")
        for item in re.split(r"[,;\n|]", projects_section)
        if item.strip(" -•")
    ] if projects_section else []

    # Extract education
    education_section = extract_section(cv_text, "Education")

    if not education_section:
        degree_match = re.search(
            r"\b(?:B\.?Tech|B\.?E\.?|M\.?Tech|M\.?S\.?|BCA|MCA|"
            r"B\.?Sc|M\.?Sc|Bachelor|Master|Diploma|Ph\.?D\.?)"
            r"[^,\n]*",
            cv_text,
            re.IGNORECASE
        )
        education_section = degree_match.group(0).strip() if degree_match else ""

    return {
        "skills": skills,
        "projects": projects,
        "education": education_section
    }


if __name__ == "__main__":
    sample = """
    Education: B.Tech CSE
    Skills: Python, Java, SQL, React
    Projects: Weather App, Portfolio Website
    """

    print(json.dumps(parse_cv(sample), indent=2))
