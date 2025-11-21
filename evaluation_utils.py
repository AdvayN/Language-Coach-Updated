import re
import math
import pandas as pd
from unidecode import unidecode
from typing import List, Tuple, Optional, Dict
from dataclasses import dataclass


LOW_CONF = 0.35  
VERY_LOW_CONF = 0.20
CSV_NAME = "evaluation.csv"
FILLERS = set("""
uh um hmm like youknow kinda sortof sorry thanks thank you next wait okay ok
yeah yea nope sorry mam pardon excuseme excuse me please
""".strip().split())


def normalize_text(s: str) -> str:
    s = unidecode(s).lower().strip()
    s = re.sub(r"[^\w'\s]", " ", s)
    s = s.replace("'", "")
    s = re.sub(r"\s+", " ", s).strip()
    return s


def tokenize(s: str) -> List[str]:
    return normalize_text(s).split()



@dataclass
class Word:
    text: str
    start: Optional[float]
    end: Optional[float]
    prob: Optional[float]


def levenshtein_align(ref: List[str], hyp: List[Word]) -> List[Tuple[str, Optional[str], Optional[Word]]]:
    n, m = len(ref), len(hyp)
    dp = [[(0, None)] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        dp[i][0] = (i, 'del')
    for j in range(1, m + 1):
        dp[0][j] = (j, 'ins')
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            cost_sub = 0 if ref[i - 1] == hyp[j - 1].text else 1
            cands = [
                (dp[i - 1][j][0] + 1, 'del'),
                (dp[i][j - 1][0] + 1, 'ins'),
                (dp[i - 1][j - 1][0] + cost_sub, 'eq' if cost_sub == 0 else 'sub')
            ]
            dp[i][j] = min(cands, key=lambda x: x[0])
    out = []
    i, j = n, m
    while i > 0 or j > 0:
        op = dp[i][j][1]
        if i > 0 and j > 0 and op in ('eq', 'sub'):
            out.append(('equal' if op == 'eq' else 'sub', ref[i - 1], hyp[j - 1]))
            i, j = i - 1, j - 1
        elif i > 0 and op == 'del':
            out.append(('del', ref[i - 1], None))
            i -= 1
        else:
            out.append(('ins', None, hyp[j - 1]))
            j -= 1
    out.reverse()
    return out


def classify_alignment(op: str, ref_tok: Optional[str], hyp: Optional[Word]) -> str:
    if op == 'equal':
        if hyp and hyp.prob is not None and hyp.prob < LOW_CONF:
            return "matched-but-unclear"
        return "match"
    if op == 'sub':
        if hyp and hyp.prob is not None and hyp.prob < VERY_LOW_CONF:
            return "mispronounced (severe)"
        return "mispronounced"
    if op == 'ins':
        if hyp and (hyp.text in FILLERS):
            return "extra-filler"
        return "extra"
    if op == 'del':
        return "missed"
    return "other"


def evaluate_pronounciations(utterances: List[dict], reference: str) -> pd.DataFrame:
    hyp_words: List[Word] = []
    # create Words list
    for utter in utterances:
        utter_words = utter["words"]
        for word_ in utter_words:
            hyp_words.append(Word(
                text = normalize_text(word_["word"].strip()),
                start = word_["start"],
                end = word_["end"],
                prob = word_.get("confidence", None)

            ))
    # create evaluation dataframe

    ref_tokens = tokenize(reference)
    alignment = levenshtein_align(ref_tokens, hyp_words)

    rows = []
    for op, ref_tok, hyp in alignment:
        label = classify_alignment(op, ref_tok, hyp)
        if label in {"mispronounced", "mispronounced (severe)", "extra", "extra-filler", "missed", "matched-but-unclear"}:
            rows.append({
                "type": label,
                "reference_word": ref_tok or "",
                "heard_word": "" if hyp is None else hyp.text,
                "start_sec": None if hyp is None else (None if hyp.start is None else round(hyp.start, 3)),
                "end_sec":   None if hyp is None else (None if hyp.end   is None else round(hyp.end,   3)),
                "confidence": None if (hyp is None or hyp.prob is None) else round(hyp.prob, 3),
            })

    df = pd.DataFrame(
        rows,
        columns=["type", "reference_word", "heard_word", "start_sec", "end_sec", "confidence"]
    )

    return df
    