from PyPDF2 import PdfReader
import gradio as gr
from transformers import pipeline

classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

skillslist = ["Python","Java","Machine Learning","SQL","Data Analysis",
              "TensorFlow","Deep Learning","HTML","CSS","JavaScript",
              "Flask","React","Git","C++"]

sections = ["Education","Projects","Experience","Skills","Certifications"]

def analyze_resume(file, target_role=None, job_description=None):
    # Read PDF
    reader = PdfReader(file.name)
    text = ""
    for page in reader.pages:
        extractedtext = page.extract_text()
        if extractedtext:
            text += extractedtext

    resumetext = text[:1000]

    # Word count
    wordcount = len(text.split())

    # Experience level
    if wordcount < 150:
        experiencelevel = "Fresher"
    elif wordcount < 400:
        experiencelevel = "Intermediate"
    else:
        experiencelevel = "Experienced"

    # Detect skills
    detectedskills = [skill for skill in skillslist if skill.lower() in text.lower()]

    # Section detection
    foundsections = [sec for sec in sections if sec.lower() in text.lower()]
    missingsections = [sec for sec in sections if sec not in foundsections]

    # Role prediction with confidence scores
    labels = ["Data Scientist", "Machine Learning Engineer", "Web Developer", "Software Engineer", "Data Analyst"]
    prediction = classifier(resumetext, labels)
    role_confidences = "\n".join([f"{lbl}: {round(score*100,2)}%" for lbl, score in zip(prediction["labels"], prediction["scores"])])
    top_role = prediction["labels"][0]

    # ATS Score calculation
    ats_score = 50
    ats_score += min(len(detectedskills)*5, 20)
    if "projects" in text.lower(): ats_score += 10
    if "education" in text.lower(): ats_score += 10
    if "github" in text.lower() or "linkedin" in text.lower(): ats_score += 10
    if 200 <= wordcount <= 800: ats_score += 10
    ats_score = min(100, ats_score)

    # Resume suggestions
    suggestions = []
    if "github" not in text.lower(): suggestions.append("Add GitHub profile")
    if "linkedin" not in text.lower(): suggestions.append("Include LinkedIn profile")
    if "project" not in text.lower(): suggestions.append("Add more project descriptions")
    if "certification" not in text.lower(): suggestions.append("Mention relevant certifications")
    if wordcount < 200: suggestions.append("Expand resume with more details")

    # Outputs for each tab
    overview_text = f"""
📄 Resume Overview:
This resume belongs to a {experiencelevel} candidate.

📑 Sections Found:
{', '.join(foundsections)} | Missing: {', '.join(missingsections)}

💼 Suggested Role:
{top_role}

📊 Role Confidence Scores:
{role_confidences}

📈 ATS Score: {ats_score}/100
"""
    skills_output = [(skill, True) for skill in detectedskills]
    ats_text = f"ATS Score: {ats_score}/100\n\nSuggestions:\n" + "\n".join(suggestions)
    gap_text = ""  # you can add gap analysis here if needed

    return overview_text, skills_output, ats_text, gap_text




with gr.Blocks() as demo:
    gr.Markdown("# 🚀 AI Resume Analyzer")

    with gr.Row():
        resume_file = gr.File(label="Upload Resume PDF")
        target_role = gr.Textbox(label="Target Role (optional)")
        job_desc = gr.Textbox(label="Job Description (optional)")
        analyze_btn = gr.Button("Analyze Resume")

    with gr.Tab("Overview"):
        overview = gr.Textbox(label="Resume Overview", interactive=False)

    with gr.Tab("Skills"):
        skills = gr.HighlightedText(label="Detected Skills")

    with gr.Tab("ATS & Suggestions"):
        ats = gr.Textbox(label="ATS Score & Suggestions", interactive=False)

    with gr.Tab("Gap Analysis"):
        gap = gr.Textbox(label="Skill Gap Analysis", interactive=False)

    analyze_btn.click(
        fn=analyze_resume,
        inputs=[resume_file, target_role, job_desc],
        outputs=[overview, skills, ats, gap]
    )

demo.launch()



