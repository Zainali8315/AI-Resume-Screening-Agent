# AI-Resume-Screening-Agent
An AI-powered Resume Screening application built in Python that ranks and shortlists candidates using Expert System rules, Weighted Scoring, and Greedy Selection algorithms.
# AI Resume Screening Agent

A desktop-based intelligent screening system designed to evaluate, score, and rank candidate resumes automatically based on job descriptions. Built using Python, this project implements various foundational Artificial Intelligence techniques to streamline the recruitment workflow.

## 🚀 Key Features
- **Job Description Configuration:** Define required skills, experience, minimum education, and custom keywords.
- **Candidate Processing:** Input and store candidate details alongside their resume text summaries.
- **Automated Screening & Ranking:** Processes applicants instantly and populates a dynamic grading table.
- **Top Talent Shortlisting:** Filters out and highlights top-tier candidates meeting a specified score threshold (e.g., Score ≥ 70%).

## 🧠 AI Techniques Implemented
Based on Artificial Intelligence principles, the agent utilizes a combination of the following rules and heuristics:
1. **Expert System Decision Rules:** Evaluates candidates using `IF-THEN` conditional rules to check skill match adequacy, experience fulfillment, and required educational criteria.
2. **Weighted Scoring Model:** Computes a composite evaluation metric using a linear combination style allocation:
   - **Skills:** 40%
   - **Experience:** 25%
   - **Education:** 15%
   - **Keywords:** 15%
   - **Certifications:** 5%
3. **Greedy Selection Algorithm:** Optimally sorts candidates based on their final score to guarantee the highest-ranking candidates are prioritized first.
4. **Hill Climbing Optimization:** Conceptually implemented to iteratively improve scoring as missing criteria/skills are accounted for.

## 🛠️ Tech Stack & Structure
- **Language:** Python 3.14
- **Interface:** GUI Component (`gui.py`, `main.py`)
- **Data Architecture:** Structuring candidate data seamlessly using localized list/dictionary objects.

<img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/bc0c7c2a-2ad1-4223-b843-76fcb94fca6e" />

<img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/cf4b2b66-c711-4dff-a533-5017ef43c08e" />

<img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/4bde2090-8d47-482e-bebb-09540520d639" />

<img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/82243f60-344f-46da-b2be-304a7cefc410" />

<img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/699fa9e3-3dfb-421b-9637-8e038700bd9e" />

<img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/2a31d770-b5b2-4402-b575-4153fc1f9d15" />





