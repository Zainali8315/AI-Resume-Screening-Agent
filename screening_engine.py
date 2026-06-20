# =============================================================================
# screening_engine.py
# AI Resume Screening Engine
# Contains: Expert System Rules, Weighted Scoring, Greedy Ranking
# =============================================================================

# ----------------------------------------------------------------------------
# SCORING WEIGHTS (Linear Regression-inspired weighted model)
# These weights determine how much each factor contributes to the final score.
# ----------------------------------------------------------------------------
WEIGHTS = {
    "skills":        0.40,   # 40% - Most important factor
    "experience":    0.25,   # 25% - Years of experience
    "education":     0.15,   # 15% - Degree/qualification match
    "keywords":      0.15,   # 15% - Important keywords in resume
    "certifications": 0.05,  # 5%  - Additional certifications
}

# ----------------------------------------------------------------------------
# STATUS THRESHOLDS (Expert System decision boundaries)
# ----------------------------------------------------------------------------
def get_status(score):
    """
    Expert System Rule:
    Based on final score, assign a recommendation status.
    This is a classic rule-based decision (like an expert system).
    """
    if score >= 90:
        return "Highly Recommended", "#1a7a1a"   # Dark green
    elif score >= 70:
        return "Recommended", "#2d862d"           # Green
    elif score >= 50:
        return "Average", "#cc8800"               # Orange
    else:
        return "Not Recommended", "#cc2200"       # Red


# ----------------------------------------------------------------------------
# SKILL MATCH (Expert System Rule 1)
# ----------------------------------------------------------------------------
def calculate_skill_match(required_skills_str, candidate_skills_str):
    """
    Expert System Rule:
    IF a required skill is found in candidate skills → increase score.
    
    Returns: (percentage_float, matched_list, missing_list)
    """
    if not required_skills_str.strip():
        return 100.0, [], []

    # Parse comma-separated skill lists, make lowercase for comparison
    required = [s.strip().lower() for s in required_skills_str.split(",") if s.strip()]
    candidate = [s.strip().lower() for s in candidate_skills_str.split(",") if s.strip()]

    if not required:
        return 100.0, [], []

    matched = []
    missing = []

    for skill in required:
        # Check if skill appears anywhere in candidate's skills (partial match allowed)
        found = any(skill in c or c in skill for c in candidate)
        if found:
            matched.append(skill)
        else:
            missing.append(skill)

    percentage = (len(matched) / len(required)) * 100
    return percentage, matched, missing


# ----------------------------------------------------------------------------
# EXPERIENCE MATCH (Expert System Rule 2)
# ----------------------------------------------------------------------------
def calculate_experience_match(required_exp_str, candidate_exp_str):
    """
    Expert System Rule:
    IF candidate experience >= required experience → full score.
    IF candidate experience < required → partial score based on ratio.
    
    Returns: (percentage_float, reason_string)
    """
    try:
        required = float(required_exp_str)
    except (ValueError, TypeError):
        required = 0.0

    try:
        candidate = float(candidate_exp_str)
    except (ValueError, TypeError):
        candidate = 0.0

    if required <= 0:
        return 100.0, "No experience requirement set."

    if candidate >= required:
        return 100.0, f"Has {candidate} yrs experience (required: {required} yrs). ✓"
    else:
        ratio = candidate / required
        pct = ratio * 100
        return pct, f"Has {candidate} yrs experience (required: {required} yrs). Partial match."


# ----------------------------------------------------------------------------
# EDUCATION MATCH (Expert System Rule 3)
# ----------------------------------------------------------------------------
# Education levels ranked from lowest to highest
EDUCATION_LEVELS = {
    "high school": 1,
    "diploma": 2,
    "associate": 3,
    "bachelor": 4,
    "bs": 4,
    "be": 4,
    "bsc": 4,
    "btech": 4,
    "b.tech": 4,
    "b.e.": 4,
    "ba": 4,
    "master": 5,
    "ms": 5,
    "msc": 5,
    "mba": 5,
    "mtech": 5,
    "m.tech": 5,
    "phd": 6,
    "doctorate": 6,
}

def get_education_level(edu_str):
    """Helper: Get numeric level for an education string."""
    edu_lower = edu_str.lower()
    for key, level in EDUCATION_LEVELS.items():
        if key in edu_lower:
            return level
    return 0  # Unknown

def calculate_education_match(required_edu_str, candidate_edu_str):
    """
    Expert System Rule:
    IF degree matches or exceeds required degree → full score.
    IF below required → reduced score.
    
    Returns: (percentage_float, reason_string)
    """
    if not required_edu_str.strip():
        return 100.0, "No education requirement set."

    req_level   = get_education_level(required_edu_str)
    cand_level  = get_education_level(candidate_edu_str)

    if req_level == 0:
        # Can't determine required level — do a simple string match
        if required_edu_str.lower() in candidate_edu_str.lower():
            return 100.0, f"Education matches: {candidate_edu_str} ✓"
        else:
            return 50.0, f"Education mismatch. Required: {required_edu_str}, Has: {candidate_edu_str}"

    if cand_level >= req_level:
        return 100.0, f"Education sufficient: {candidate_edu_str} (Required: {required_edu_str}) ✓"
    elif cand_level > 0:
        ratio = cand_level / req_level
        return ratio * 100, f"Education below requirement. Has: {candidate_edu_str}, Required: {required_edu_str}"
    else:
        return 30.0, f"Education level unclear. Required: {required_edu_str}"


# ----------------------------------------------------------------------------
# KEYWORD MATCH (Expert System Rule 4)
# ----------------------------------------------------------------------------
def calculate_keyword_match(keywords_str, resume_text, candidate_skills_str=""):
    """
    Expert System Rule:
    IF important keywords are missing → reduce score.
    
    Searches keywords in both resume text and skills.
    Returns: (percentage_float, found_list, missing_list)
    """
    if not keywords_str.strip():
        return 100.0, [], []

    keywords = [k.strip().lower() for k in keywords_str.split(",") if k.strip()]
    if not keywords:
        return 100.0, [], []

    # Search in resume text + candidate skills combined
    search_space = (resume_text + " " + candidate_skills_str).lower()

    found   = [k for k in keywords if k in search_space]
    missing = [k for k in keywords if k not in search_space]

    percentage = (len(found) / len(keywords)) * 100
    return percentage, found, missing


# ----------------------------------------------------------------------------
# CERTIFICATION MATCH (Expert System Rule 5)
# ----------------------------------------------------------------------------
def calculate_certification_match(certifications_str):
    """
    Expert System Rule:
    IF candidate has certifications → bonus score.
    Simple presence-based scoring.
    
    Returns: (percentage_float, reason_string)
    """
    if not certifications_str.strip():
        return 0.0, "No certifications listed."

    # Count certifications
    certs = [c.strip() for c in certifications_str.split(",") if c.strip()]
    if len(certs) >= 3:
        return 100.0, f"{len(certs)} certifications found ✓"
    elif len(certs) == 2:
        return 75.0, f"{len(certs)} certifications found"
    elif len(certs) == 1:
        return 50.0, f"1 certification found"
    else:
        return 0.0, "No valid certifications."


# ----------------------------------------------------------------------------
# MAIN SCREENING FUNCTION
# ----------------------------------------------------------------------------
def screen_candidate(job, candidate):
    """
    Main function: Screens a single candidate against the job description.
    
    Uses:
    - Expert System Rules (rule-based scoring)
    - Weighted Scoring Model (like Linear Regression with fixed weights)
    
    Parameters:
        job       : dict with keys: title, skills, experience, education, keywords
        candidate : dict with keys: name, skills, experience, education, certifications, resume_text
    
    Returns:
        dict with score, status, reasons, and component scores
    """
    reasons = []

    # --- Rule 1: Skills Match ---
    skill_pct, matched_skills, missing_skills = calculate_skill_match(
        job.get("skills", ""),
        candidate.get("skills", "")
    )
    if matched_skills:
        reasons.append(f"✓ Skills matched: {', '.join(matched_skills)}")
    if missing_skills:
        reasons.append(f"✗ Missing skills: {', '.join(missing_skills)}")

    # --- Rule 2: Experience Match ---
    exp_pct, exp_reason = calculate_experience_match(
        job.get("experience", "0"),
        candidate.get("experience", "0")
    )
    reasons.append(exp_reason)

    # --- Rule 3: Education Match ---
    edu_pct, edu_reason = calculate_education_match(
        job.get("education", ""),
        candidate.get("education", "")
    )
    reasons.append(edu_reason)

    # --- Rule 4: Keyword Match ---
    kw_pct, found_kw, missing_kw = calculate_keyword_match(
        job.get("keywords", ""),
        candidate.get("resume_text", ""),
        candidate.get("skills", "")
    )
    if found_kw:
        reasons.append(f"✓ Keywords found: {', '.join(found_kw)}")
    if missing_kw:
        reasons.append(f"✗ Missing keywords: {', '.join(missing_kw)}")

    # --- Rule 5: Certification Match ---
    cert_pct, cert_reason = calculate_certification_match(
        candidate.get("certifications", "")
    )
    reasons.append(cert_reason)

    # --- Weighted Final Score (Linear Regression-style model) ---
    final_score = (
        skill_pct * WEIGHTS["skills"] +
        exp_pct   * WEIGHTS["experience"] +
        edu_pct   * WEIGHTS["education"] +
        kw_pct    * WEIGHTS["keywords"] +
        cert_pct  * WEIGHTS["certifications"]
    )

    # Clamp to 0-100
    final_score = max(0.0, min(100.0, final_score))

    # --- Expert System Decision ---
    status, color = get_status(final_score)

    return {
        "name":         candidate.get("name", "Unknown"),
        "score":        round(final_score, 1),
        "status":       status,
        "color":        color,
        "reasons":      reasons,
        "skill_pct":    round(skill_pct, 1),
        "exp_pct":      round(exp_pct, 1),
        "edu_pct":      round(edu_pct, 1),
        "kw_pct":       round(kw_pct, 1),
        "cert_pct":     round(cert_pct, 1),
    }


# ----------------------------------------------------------------------------
# GREEDY RANKING ALGORITHM
# ----------------------------------------------------------------------------
def rank_candidates(results):
    """
    Greedy Algorithm:
    Sort candidates by highest suitability score (greedy: pick the best first).
    This mimics a greedy selection strategy — always pick the highest-ranked
    candidate at each step.
    
    Parameters:
        results : list of candidate result dicts (from screen_candidate)
    
    Returns:
        Sorted list from highest score to lowest (greedy ranking)
    """
    # Greedy sort: always prefer higher score
    return sorted(results, key=lambda x: x["score"], reverse=True)


# ----------------------------------------------------------------------------
# SCREEN ALL CANDIDATES (Main entry point)
# ----------------------------------------------------------------------------
def screen_all(job, candidates):
    """
    Screen all candidates and return greedy-ranked results.
    
    Parameters:
        job        : job description dict
        candidates : list of candidate dicts
    
    Returns:
        Ranked list of result dicts with added 'rank' field
    """
    results = []
    for candidate in candidates:
        result = screen_candidate(job, candidate)
        results.append(result)

    # Apply Greedy Algorithm to rank
    ranked = rank_candidates(results)

    # Add rank numbers
    for i, r in enumerate(ranked):
        r["rank"] = i + 1

    return ranked
