def generate_suggestions(
    ats_score: int,
    matched_skills: list[str],
    missing_skills: list[str],
) -> list[str]:
    suggestions: list[str] = []

    if missing_skills:
        top_missing = ", ".join(missing_skills[:6])
        suggestions.append(
            f"Add relevant experience, projects, or certifications that demonstrate: {top_missing}."
        )

    if ats_score < 70:
        suggestions.append(
            "Mirror important wording from the job description where it truthfully matches your experience."
        )
        suggestions.append(
            "Add measurable impact to bullet points, such as percentages, revenue, time saved, or scale handled."
        )

    if len(matched_skills) < 5:
        suggestions.append(
            "Create a dedicated Skills section with clear technical keywords grouped by category."
        )

    suggestions.append(
        "Keep formatting ATS-friendly: use simple headings, avoid tables for core content, and export as a readable PDF."
    )

    return suggestions
