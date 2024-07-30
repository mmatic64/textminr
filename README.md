# textminr

## 1. wiki FOLDER

Here is where the programm for finding the correct publishing date of a book will be created

### 1.x. ner_bert.ipynb

This is just a copy from https://github.com/TextminR/ai-lab (branch: main /training/notebooks/ner_bert.ipynb 23.07.2024) to better understand the model used for extracting dates, authors and titels from a given text. This model was used for a different task but seems to be okay for this one too.

### 1.x. wikipedia_scrape.ipynb

scraping the wikipedia sites using just the requestst package.

### 1.x. wikipedia.ipynb

this file is where most of the code is written for now.

using wikipedia and requests package together to better search the wikipedia sites

### 1.1. generate_promts FOLDER

used for generating the promts for training the model

#### 1.1.x. base_to_ner.py

used to tokenize the promts for the training

#### 1.1.x. wikipedia.ipynb

used for generating the promts for training