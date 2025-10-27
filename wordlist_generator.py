"""
wordlist_generator.py
Generate a custom wordlist from user inputs with common mutations:
- case variants
- leetspeak substitutions
- append/prepend year ranges
- common suffixes/prefixes
- combine words up to a small depth (to avoid explosion)
"""

from itertools import product, permutations
import itertools
import re

LEET_MAP = {
    'a': ['a', '@', '4'],
    'b': ['b', '8'],
    'e': ['e', '3'],
    'i': ['i', '1', '!'],
    'l': ['l', '1', '|'],
    'o': ['o', '0'],
    's': ['s', '$', '5'],
    't': ['t', '7'],
    'g': ['g', '9'],
    'z': ['z', '2']
}

COMMON_SUFFIXES = ["!", "!!", "123", "1234", "2020", "2021", "2022", "2023", "2024", "2025"]
COMMON_PREFIXES = ["", "!", "#", "@"]

def sanitize_token(token: str) -> str:
    return token.strip()

def generate_case_variants(token: str):
    # yield original, lower, upper, capitalize, toggle-case (if short)
    yield token
    yield token.lower()
    yield token.upper()
    yield token.capitalize()
    # toggle every other char (only for short tokens)
    if len(token) <= 6:
        toggled = ''.join(c.upper() if i % 2 == 0 else c.lower() for i, c in enumerate(token))
        yield toggled

def leet_variants(token: str, max_variants=50):
    """
    Produce leetspeak variants by substituting characters using LEET_MAP.
    Limit total variants to avoid explosion.
    """
    token = token.lower()
    positions = [LEET_MAP.get(ch, [ch]) for ch in token]
    # Compute cartesian product but limit
    variants = []
    for combo in product(*positions):
        ent = ''.join(combo)
        variants.append(ent)
        if len(variants) >= max_variants:
            break
    return variants

def append_years(token: str, start=1970, end=2026):
    for year in range(end, start - 1, -1):
        yield f"{token}{year}"
        yield f"{year}{token}"

def common_mutations(token: str, include_leet=True, include_suffixes=True):
    seen = set()
    for case_variant in generate_case_variants(token):
        if case_variant in seen:
            continue
        seen.add(case_variant)
        yield case_variant
        if include_leet:
            for lv in leet_variants(case_variant, max_variants=20):
                if lv not in seen:
                    seen.add(lv)
                    yield lv
        if include_suffixes:
            for s in COMMON_SUFFIXES:
                cand = case_variant + s
                if cand not in seen:
                    seen.add(cand)
                    yield cand

def combine_tokens(tokens: list[str], max_join=2):
    """
    Combine tokens (permutations) up to max_join length.
    Default max_join=2 to limit explosion.
    """
    tokens = [t for t in tokens if t]
    results = set()
    for r in range(1, max_join + 1):
        for perm in permutations(tokens, r):
            results.add(''.join(perm))
    return results

def generate_wordlist(
    base_tokens: list[str],
    extra_tokens: list[str] = None,
    include_leet=True,
    include_years=(2000, 2026),
    max_combination=2,
    max_total=200000
):
    extra_tokens = extra_tokens or []
    # sanitize
    base_tokens = [sanitize_token(t) for t in base_tokens if sanitize_token(t)]
    extra_tokens = [sanitize_token(t) for t in extra_tokens if sanitize_token(t)]
    all_seeds = list(dict.fromkeys(base_tokens + extra_tokens))  # preserve order, dedupe
    # generate combos
    combined = combine_tokens(all_seeds, max_join=max_combination)
    # also include individual tokens
    combined.update(all_seeds)
    # apply mutations
    final = []
    seen = set()
    for tok in combined:
        for mut in common_mutations(tok, include_leet=include_leet):
            if mut not in seen:
                final.append(mut)
                seen.add(mut)
            # append years (only append a few common ones to avoid explosion)
            if include_years:
                start, end = include_years
                # limit to recent years for practicality
                for y in range(end, max(start, end - 10) - 1, -1):
                    cand = f"{mut}{y}"
                    if cand not in seen:
                        final.append(cand)
                        seen.add(cand)
        if len(final) >= max_total:
            break
    return final

def save_wordlist(wordlist: list[str], path: str):
    with open(path, 'w', encoding='utf-8') as f:
        for w in wordlist:
            f.write(w + "\n")
