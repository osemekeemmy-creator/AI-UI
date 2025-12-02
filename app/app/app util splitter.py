import re

def split_questions(text: str) -> list[str]:
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    questions = []
    current = ""

    patterns = [
        r"^\d+[\.\)]",           # 1. 1)
        r"^\d+[a-zA-Z][\.\)]",   # 1a) 1b.
        r"^Question\s+\d+",      # Question 1
        r"^\d+\s*[\–\-\—]\s*",  # 1 —
        r"^[A-E]\.\s+[A-Z]",     # A. Option
    ]
    start_re = re.compile("|".join(patterns), re.IGNORECASE)

    for line in lines:
        if start_re.match(line) and current.strip():
            if len(current) > 50:
                questions.append(current.strip())
            current = line
        else:
            current += " " + line

    if current and len(current) > 50:
        questions.append(current.strip())

    return questions
