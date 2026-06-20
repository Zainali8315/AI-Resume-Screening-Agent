# =============================================================================
# data.py
# Sample Data for AI Resume Screening Agent
# Contains sample job descriptions and candidate profiles for demo/testing
# =============================================================================

# ----------------------------------------------------------------------------
# SAMPLE JOB DESCRIPTIONS
# ----------------------------------------------------------------------------
SAMPLE_JOBS = {
    "Software Engineer": {
        "title":      "Software Engineer",
        "skills":     "Python, Django, REST API, Git, SQL, JavaScript",
        "experience": "2",
        "education":  "Bachelor in Computer Science",
        "keywords":   "agile, backend, software development, api, database",
    },
    "Data Scientist": {
        "title":      "Data Scientist",
        "skills":     "Python, Machine Learning, TensorFlow, Pandas, NumPy, SQL",
        "experience": "3",
        "education":  "Master in Data Science",
        "keywords":   "machine learning, data analysis, model training, statistics, visualization",
    },
    "Frontend Developer": {
        "title":      "Frontend Developer",
        "skills":     "HTML, CSS, JavaScript, React, Vue, TypeScript",
        "experience": "1",
        "education":  "Bachelor in Computer Science",
        "keywords":   "responsive design, ui, ux, web development, frontend",
    },
}

# Default job loaded on startup
DEFAULT_JOB = SAMPLE_JOBS["Software Engineer"]


# ----------------------------------------------------------------------------
# SAMPLE CANDIDATES
# ----------------------------------------------------------------------------
SAMPLE_CANDIDATES = [
    {
        "name":           "Alice Johnson",
        "skills":         "Python, Django, REST API, Git, SQL, JavaScript, Docker",
        "experience":     "4",
        "education":      "Bachelor in Computer Science",
        "certifications": "AWS Certified Developer, Google Cloud Associate, Python Institute PCEP",
        "resume_text":    (
            "Experienced software engineer with 4 years in backend development. "
            "Proficient in Python and Django framework. Worked on multiple agile teams "
            "delivering REST API services. Strong knowledge of database design and SQL. "
            "Experienced in software development life cycle and api integration."
        ),
    },
    {
        "name":           "Bob Smith",
        "skills":         "Python, Flask, Git, MySQL",
        "experience":     "1.5",
        "education":      "Bachelor in Software Engineering",
        "certifications": "Python Institute PCEP",
        "resume_text":    (
            "Junior developer with experience in Python and Flask. "
            "Worked on small-scale projects. Familiar with Git and database basics. "
            "Eager to learn backend and api development in agile environments."
        ),
    },
    {
        "name":           "Carol Davis",
        "skills":         "Java, Spring Boot, REST API, SQL, Python",
        "experience":     "5",
        "education":      "Master in Computer Science",
        "certifications": "Oracle Java Certified, AWS Solutions Architect",
        "resume_text":    (
            "Senior developer with expertise in Java and Spring Boot. "
            "5 years of experience building enterprise REST API solutions. "
            "Strong background in software development and agile methodology. "
            "Experience with database design and backend architecture."
        ),
    },
    {
        "name":           "David Lee",
        "skills":         "HTML, CSS, JavaScript, Photoshop",
        "experience":     "0",
        "education":      "Diploma in Web Design",
        "certifications": "",
        "resume_text":    (
            "Fresh graduate with basic HTML, CSS and JavaScript skills. "
            "Designed simple websites as coursework. "
            "No professional experience yet."
        ),
    },
    {
        "name":           "Eva Martinez",
        "skills":         "Python, Django, REST API, Git, SQL, React, Docker, Kubernetes",
        "experience":     "3",
        "education":      "Bachelor in Computer Science",
        "certifications": "AWS Certified Developer, Docker Certified Associate, Scrum Master",
        "resume_text":    (
            "Full-stack developer with 3 years of experience. "
            "Expert in Python, Django, and REST API development. "
            "Experienced with agile software development teams. "
            "Strong SQL and database skills. Familiar with devops and backend."
        ),
    },
]
