import pandas as pd
from pypinyin import pinyin, lazy_pinyin
import re
from transformers import AutoTokenizer

def tokenize_with_offsets(tokenizer, text):
    return tokenizer(
        text,
        return_offsets_mapping=True,
        add_special_tokens=False
    )

def classify_span(text_span):
    has_zh = bool(re.search(r'[\u4e00-\u9fff]', text_span))
    has_en = bool(re.search(r'[a-zA-Z]', text_span))

    if has_zh and has_en:
        return "mixed"
    elif has_zh:
        return "zh"
    elif has_en:
        return "en"
    else:
        return "other"


def compute_ratios(tokenizer, text):
    encoding = tokenize_with_offsets(tokenizer, text)

    counts = {"en": 0, "zh": 0, "mixed": 0, "other": 0}

    for (start, end) in encoding["offset_mapping"]:
        span = text[start:end]
        label = classify_span(span)
        counts[label] += 1

    total = sum(counts.values())

    return {k: v / total for k, v in counts.items()} if total > 0 else counts

tokenizer = AutoTokenizer.from_pretrained(
    "/Users/cindylin/Documents/IW 06/Deepseek/",
    trust_remote_code=True
)

df = pd.read_csv("/Users/cindylin/Documents/IW 06/codeMixQA.csv")
df["en_prop"] = None
df["zh_prop"] = None
df["mixed_prop"] = None

for idx, row in df.iterrows():
    text = row['problem']
    ratios = compute_ratios(tokenizer, text)
    print(ratios)
    df.loc[idx,'en_prop'] = ratios['en']
    df.loc[idx,'zh_prop'] = ratios['zh']
    df.loc[idx, 'mixed_prop'] = ratios['mixed']

df.to_csv('/Users/cindylin/Documents/IW 06/codeMixQA_deepseek.csv', index=False)