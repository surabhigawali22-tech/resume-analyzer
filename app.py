from PyPDF2 import PdfReader
import gradio as gr

# Skills list
skills_list = [
    "Python",
    "Java",
    "Machine Learning",
    "SQL",
    "Data Analysis",
    "TensorFlow",
    "Deep Learning",
    "HTML",
    "CSS",
    "JavaScript",
    "Flask",
    "React",
    "Git",
    "C++"
]

# Main function
def analyze_resume(file):

    # Read PDF
    reader = PdfReader(file.name)

    text = ""

    for page in reader.pages:
        extracted_text = page.extract_text()

        if extracted_text:
            text += extracted_text

    # Resume text
    resume_text = text[:1000]

    # Word count
    word_count = len(text.split())

    # Experience level
    if word_count < 150:
        experience_level = "Fresher"

    elif word_count < 400:
        experience_level = "Intermediate"

    else:
        experience_level = "Experienced"

    # Detect skills
    detected_skills = []

    for skill in skills_list:
        if skill.lower() in text.lower():
            detected_skills.append(skill)

    # Suggest role
    if "machine learning" in text.lower():
        role = "Machine Learning Engineer"

    elif "data analysis" in text.lower():
        role = "Data Analyst"

    elif "react" in text.lower() or "javascript" in text.lower():
        role = "Frontend Developer"

    elif "flask" in text.lower():
        role = "Backend Developer"

    else:
        role = "Software Developer"

    # Final output
    result = f"""
📄 Resume Overview:
This resume belongs to a {experience_level} candidate.

🛠 Detected Skills:
{', '.join(detected_skills)}

💼 Suggested Role:
{role}

📊 Resume Statistics:
Total Words: {word_count}
Skills Found: {len(detected_skills)}
"""

    return result


# Gradio UI
iface = gr.Interface(
    fn=analyze_resume,
    inputs=gr.File(label="Upload Resume PDF"),
    outputs=gr.Textbox(label="Analysis"),
    title="AI Resume Analyzer",
    description="Upload your resume and get AI-powered analysis instantly."
)

# Launch app
iface.launch()