def calculate_risk(app, status):
    if status == "PATCHED_UPSTREAM":
        return 0

    if status == "POTENTIALLY_VULNERABLE":
        score = 50
    elif status == "UNSUPPORTED":
        score = 40
    else:
        return None

    if app["exposure"] == "internet":
        score += 25

    criticality_points = {
        "critical": 25,
        "high": 15,
        "medium": 5,
        "low": 0,
    }

    score += criticality_points[app["business_criticality"]]

    return min(score, 100)
