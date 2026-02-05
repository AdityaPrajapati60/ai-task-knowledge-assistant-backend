from groq import Groq
import re

client = Groq()


# -----------------------------
# HELPER: Extract numeric score safely
# -----------------------------
def extract_number(text: str) -> float:
    match = re.search(r"\d*\.?\d+", text)
    if match:
        value = float(match.group())
        # Clamp to valid range
        return max(0.0, min(1.0, value))
    return 0.5


# -----------------------------
# HALLUCINATION SCORE
# -----------------------------
def hallucination_score(answer: str, context: str) -> float:
    prompt = f"""
You are scoring hallucination.

0 = answer is fully supported by the context
1 = answer is completely unsupported

Return ONLY a decimal number between 0 and 1.

Context:
{context}

Answer:
{answer}
"""
    resp = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )

    return extract_number(resp.choices[0].message.content)

# -----------------------------
# CONFIDENCE SCORE
# -----------------------------
def confidence_score(answer: str, context: str) -> float:
    prompt = f"""
You are scoring confidence.

0 = answer is not reliable
1 = answer is fully reliable and supported by context

Return ONLY a decimal number between 0 and 1.

Context:
{context}

Answer:
{answer}
"""
    resp = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )

    return extract_number(resp.choices[0].message.content)
