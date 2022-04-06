import pandas as pd 
from flair.models import TARSTagger
from flair.data import Sentence

df = pd.read_csv("./outputs/result/washingmachine.csv")
# print(df)

# 1. Load zero-shot NER tagger
tars = TARSTagger.load('tars-ner')

# 2. Define some classes of named entities such as "soccer teams", "TV shows" and "rivers"
labels = ["Size", "Design", "Product", "Problems", "Price", "Time", "Person", "Save", "Sustainability"]
tars.add_and_switch_to_new_task('task 1', labels, label_type='ner')


sentences = df['comments'][0]
sentences = [Sentence(f'{i}') for i in sentences]
for sentence in sentences:
    
    tars.predict(sentence)
    print(sentence.to_tagged_string("ner"))