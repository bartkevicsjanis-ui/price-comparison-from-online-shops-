import re
from rapidfuzz import fuzz

def normalize_name(name: str) -> str:
    name = name.lower()
    name = re.sub(r"\d+([.,]\d+)?\s?(kg|g|l|ml)", "", name)
    name = re.sub(r"[^a-z0-9\s]", "", name)
    name = re.sub(r"\s+", " ", name)
    return name.strip()

def is_similar(a: str, b: str, threshold: int = 80) -> bool:
    return fuzz.token_sort_ratio(a, b) >= threshold
