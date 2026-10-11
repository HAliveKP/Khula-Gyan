"""Decide the answer language: 'ne', 'en' or 'mixed'.

Agree with Member 2 to use this one function everywhere.
"""

import re

# Common Romanized-Nepali words. Add more as the eval set grows.
ROMAN_NEPALI = {
    "garna", "garne", "garnu", "garnuparcha", "garnuparchha", "chahincha", "chahinchha",
    "chaincha", "k", "ke", "kati", "kasari", "kaha", "kahaa", "kun", "ho", "cha", "chha",
    "ma", "lai", "ko", "le", "ra", "pani", "huncha", "hunchha", "parcha", "parchha",
    "kagaj", "kagajat", "naya", "nagarikta", "rahadani", "sulka", "shulka", "kati",
}

DEVANAGARI = re.compile(r"[ऀ-ॿ]")
LATIN = re.compile(r"[A-Za-z]")


def detect_language(text: str) -> str:
    dev = len(DEVANAGARI.findall(text))
    lat = len(LATIN.findall(text))
    if dev == 0 and lat == 0:
        return "en"
    if dev and lat:
        return "ne" if dev / (dev + lat) > 0.8 else "mixed"
    if dev:
        return "ne"
    words = re.findall(r"[a-z]+", text.lower())
    hits = sum(w in ROMAN_NEPALI for w in words)
    return "mixed" if hits >= 2 else "en"
