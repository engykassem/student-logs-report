import os
import random


def get(key, default):
    val = os.environ.get(key, str(default)).strip()
    try:
        return float(val)
    except ValueError:
        return val


def score_sleep(h):
    if h >= 8:   return 100
    if h >= 7:   return 85
    if h >= 6:   return 65
    if h >= 5:   return 40
    if h >= 4:   return 20
    return max(0, h * 4)

def score_coffee(c):
    if c == 0:   return 60
    if c <= 2:   return 100
    if c <= 4:   return 70
    if c <= 6:   return 35
    return max(0, 100 - c * 10)

def score_pressure(a, exam):
    p = a + (3 if exam else 0)
    if p == 0:   return 100
    if p <= 2:   return 80
    if p <= 4:   return 55
    if p <= 6:   return 30
    return max(0, 100 - p * 12)

def score_outside(d):
    if d == 0:   return 100
    if d == 1:   return 80
    if d == 2:   return 60
    if d <= 4:   return 35
    return max(0, 100 - d * 15)

def score_meal(m):
    if m <= 3:   return 100
    if m <= 6:   return 75
    if m <= 10:  return 40
    return max(0, 100 - m * 8)


def main():
    name   = str(get("STUDENT_NAME",       "Student"))
    sleep  = get("SLEEP_HOURS",        7)
    coffee = get("COFFEE_CUPS",        0)
    assign = get("ASSIGNMENTS_DUE",    0)
    exam   = str(get("EXAM_TOMORROW",  "no")).lower() == "yes"
    out    = get("DAYS_SINCE_OUTSIDE", 0)
    meal   = get("LAST_MEAL_HOURS",    4)

    s_sleep    = score_sleep(sleep)
    s_coffee   = score_coffee(coffee)
    s_pressure = score_pressure(assign, exam)
    s_outside  = score_outside(out)
    s_meal     = score_meal(meal)

    total = (
        s_sleep    * 0.35 +
        s_coffee   * 0.20 +
        s_pressure * 0.25 +
        s_outside  * 0.10 +
        s_meal     * 0.10
    )
    if exam:
        total *= 0.85

    pct = round(max(1, min(99, total)), 1)

    if pct >= 85:
        status = "THRIVING"
        msgs = [
            "Somehow you have your life together. Suspicious.",
            "Are you actually a student or just cosplaying as one?",
            "You slept, you ate, you went outside. This is illegal.",
        ]
    elif pct >= 70:
        status = "STABLE"
        msgs = [
            "Not thriving, not dying. The student sweet spot.",
            "Like a browser with 47 tabs. Functional. For now.",
            "Could use more sleep but honestly who couldn't.",
        ]
    elif pct >= 50:
        status = "AT RISK"
        msgs = [
            "Running on caffeine and sheer stubbornness.",
            "Your body is a temple. A haunted one.",
            "Sleep is not optional. This is a threat.",
        ]
    elif pct >= 30:
        status = "CRITICAL"
        msgs = [
            str(int(coffee)) + " coffees today. Your heart is filing a formal complaint.",
            str(int(out)) + " days inside. Plants need sunlight. So do you.",
            "Survival rate lower than your Wi-Fi signal at 2am.",
        ]
    else:
        status = "SEND HELP"
        msgs = [
            str(pct) + "% survival. That is not a grade, that is a medical reading.",
            str(int(sleep)) + "h sleep and you still showed up. Respect.",
            "At this point you are not a student. You are a warning label.",
        ]

    msg    = random.choice(msgs)
    filled = round(pct / 100 * 40)
    bar    = "[" + "#" * filled + "-" * (40 - filled) + "] " + str(pct) + "%"
    sep    = "=" * 55
    sep2   = "-" * 55
    exam_n = " + exam tomorrow!" if exam else ""

    output = "\n".join([
        "",
        sep,
        "  STUDENT SURVIVAL REPORT",
        "  Saskatchewan Polytechnic  |  Code Engine Lab",
        sep,
        "",
        "  Student      : " + name,
        "  Status       : " + status,
        "",
        "  SURVIVAL RATE",
        "  " + sep2,
        "  " + bar,
        "",
        '  "' + msg + '"',
        "",
        "  BREAKDOWN",
        "  " + sep2,
        "  Sleep         : " + str(int(s_sleep))    + "/100   (" + str(sleep)  + "h slept)",
        "  Caffeine      : " + str(int(s_coffee))   + "/100   (" + str(int(coffee)) + " cups)",
        "  Academic Load : " + str(int(s_pressure)) + "/100   (" + str(int(assign)) + " assignments" + exam_n + ")",
        "  Touch Grass   : " + str(int(s_outside))  + "/100   (" + str(int(out))    + " day(s) inside)",
        "  Nutrition     : " + str(int(s_meal))     + "/100   (" + str(meal)   + "h since last meal)",
        "",
        "  " + sep2,
        "  Disclaimer: Not responsible for failed exams or",
        "  existential crises. Drink water.",
        sep,
        "",
    ])

    print(output)


if __name__ == "__main__":
    main()
