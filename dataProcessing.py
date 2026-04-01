import pandas as pd
from pypinyin import pinyin, lazy_pinyin
import re
from googletrans import Translator
import time

translator = Translator()

text = "Where is Leonard Perry Jr., the 大学 basketball player?"

translated = translator.translate(text, src='zh-cn', dest='en').text
print(translated)

chinese_pattern = re.compile(r'[\u4e00-\u9fff]+')

def convert_to_pinyin(text):
    def replace(match):
        chinese_pattern = re.compile(r'[\u4e00-\u9fff]+')
        chinese_text = match.group(0)
        
        # directly returns a flat list like ['wo', 'jue', 'de']
        py = lazy_pinyin(chinese_text)
        return ' '.join(py) + ' '
    
    return chinese_pattern.sub(replace, text)

df = pd.read_csv("/Users/cindylin/Documents/IW 06/codeMixQA_pinyin.csv")
df['answer_chinese'] = ""
for idx, row in df.iterrows():
    char_text = row['answer']
    while True:
        try:
            chinese_text = translator.translate(char_text, src='en', dest='zh-cn').text
            df.loc[idx,'answer_chinese']= chinese_text
            print(char_text)
            print(chinese_text)
            break
        except Exception as e:
            print(f"Timeout on row {idx}, retrying...")
            time.sleep(1)

df.to_csv('/Users/cindylin/Documents/IW 06/codeMixQA_pinyin.csv', index=False)