import wikipedia
import re
import pandas as pd
import requests
from bs4 import BeautifulSoup
import random
import matplotlib.pyplot as plt
import numpy
import math

# Infrmation of the book
author = "Zweig, Stefan"
title = "Jeremias: Eine dramatische Dichtung in neun Bildern"
old_date = 1867 
birth = 1800
death = 1950

author = author.replace(",", "")

wikipedia.set_lang("de")

# Search for the possible wiki-websites about the author
search = wikipedia.search(author)
search += wikipedia.search(title)
print(search)

# Function to get the html of the author, for easier usage in the for loop
def gethtml(author, lang = "de"):
    # replace the spaces with the _ so it can be used in the url
    author.replace(" ", "_")
    response = requests.get(
		url="https://" + lang + ".wikipedia.org/wiki/" + author,
	)
    # get the content of the website
    soup = BeautifulSoup(response.content, 'html.parser')
    content = soup.find(id="content").__str__()
    return content

# function to check if a part of the title is in the found wikipedia page
def find_word(content, lang):
    # get the content of the website
    for p in title.split(" "):
        # check if a part of the title is in the content of the website
        if p in content:
            # add the content to the found list
            found[s + lang] = content
            # print the deatils of the search
            # print("Search: " + s + "\nWord in Text: " + p)
            break

# the content of the websites that include a part of the title of the book
found = {}
# checking if the wikiepdia wesites include the part of the title and adding them in the 'found' dictionary
for s in search:
    # get the content of the website
    # try:
    #     content = wikipedia.page(s).content
    # except:
    lang = "de"
    content = gethtml(s, lang)
    find_word(content, lang)
    lang = "en"
    content = gethtml(s, lang)
    find_word(content, lang)

# clearing the text of any html
for s in found.keys():
    soup = BeautifulSoup(found[s], 'html.parser')
    found[s] = soup.get_text()


# search for the words from the title in the given wikipedia page, and selects the surrounding paragraph and saves it under the promts array

title_clean = "Jeremias dramatische Dichtung Bildern" 

def find_all(content, word):
    n = 0
    while True:
        n = content.find(word, n)
        if n == -1:
            break
        yield n
        n += len(word)

promts = []
# search for the words from the title in the given wikipedia page, and selects the surrounding paragraph and saves it under the promts array
def find_title():

    margin = 250
    # list to store the found sentences with the title
    for s in found.keys():
        # look for the position of the title in the content
        places = numpy.empty(0, dtype=int)
        places = numpy.append(places, -margin*margin)
        for p in title_clean.split(" "):
            for gen in find_all(found[s], p):
                n = gen
                if n == -1:
                    continue
                temp = places - n
                m = math.sqrt(min(temp*temp))
                if m < margin and m > -margin:
                    continue
                places = numpy.append(places, n)
                # get the sentence and text around the title
                if n < margin:
                    text_to_check = found[s][:n+margin]
                else:
                    text_to_check = found[s][n-margin:n+margin]
                info = "Search: " + s + "; Word in Text: " + p
                info += " (" + str(n) + "):\n"
                # info += text_to_check + "\n"
                print(info)
                # add the sentence to the list
                promts.append(text_to_check)
    print(len(promts))

# selects only one row arround the found text
def selsct_row():
    for ip in range(0,len(promts)):
        enters = []
        print(promts[ip])
        for i in range(0, len(promts[ip])):
           c = promts[ip][i]
           if c == '\n':
               enters.append(i)
        print(enters)

        promt_new = ''
        if len(enters) > 1:
           first_index = min(enters, key=lambda x:abs(x-250))
           if first_index <= 250:
               if enters.index(first_index) < (len(enters) - 1):
                   promt_new = promts[ip][first_index:enters[enters.index(first_index) + 1]]
               else:
                   promt_new = promts[ip][first_index:]
           elif first_index >= 250:
               if enters.index(first_index) > 0:
                   promt_new = promts[ip][enters[enters.index(first_index) - 1]:first_index]
               else:
                   promt_new = promts[ip][:first_index]

        print(repr(promt_new))
        promts[ip] = promt_new

# searches for the dates in the generated promts
def find_title(content, word):
    for w in word.split(" "):
        pattern = re.compile(r'{}'.format(w), re.IGNORECASE)
        match = pattern.search(content)
        if match:
            return [match.start(), match.end()]
        return [None, None]

def find_dates(text: str):
    title_start, title_end = find_title(text, title_clean)

    years = pd.DataFrame(columns=['word', 'start', 'end', 'distance'])
    n = 0
    year_start, year_end = 0, 0
    year = ""
    for i in range(0, len(text)):
        c = text[i]
        if c.isnumeric():
            if n == 0:
                year_start = i
            n += 1
            year += c
        else:
            if n != 0 and n <= 4:
                year_end = i
                try:
                    year = int(year)

                    dis1, dis2, dis3, dis4 = year_start - title_start, year_start - title_end, year_end - title_start, year_end - title_end
                    dis = min(abs(dis1), abs(dis2), abs(dis3), abs(dis4))

                    years = years._append({'word': year, 'start': year_start, 'end': year_end, 'distance': dis}, ignore_index=True)
                    if dis == 1:
                        print(repr(promts[i]))
                except:
                    print("could not parse")
            n = 0
            year = ""
    return years

df = pd.DataFrame(columns=['word', 'start', 'end', 'distance'])
responses = []
length = 0
for i in range(len(promts)):
    title_start, title_end = find_title(promts[i], title_clean)
    print(str(i) + ":", title_start, title_end)

    responses.append(find_dates(promts[i]))
    print(responses[i])

    length += len(responses)
    if title_start == None or title_end == None:
        continue
    for j in range(0,len(responses[i])):
        year_start = responses[i].loc[j, 'start']
        year_end = responses[i].loc[j, 'end']
        dis1, dis2, dis3, dis4 = year_start - title_start, year_start - title_end, year_end - title_start, year_end - title_end
        dis = min(abs(dis1), abs(dis2), abs(dis3), abs(dis4))
        df = df._append({'word': responses[i].loc[j, 'word'], 'start': year_start, 'end': year_end, 'distance': dis}, ignore_index=True)
        if dis == 1:
            print(repr(promts[i]))

print(length)

# analyse the dataset

df = df[(df.word >= birth) & (df.word <= death)]
plt.figure(figsize=(10,6))

plt.scatter(df['word'], df['distance'], alpha=0.6)

plt.xlabel("year")
plt.ylabel("distance")
plt.grid(True)

plt.show()

df['distance'] = pd.to_numeric(df['distance'])
print(df.sort_values(by='distance')[0:10])


df_winners = df.sort_values(by='distance')[0:10].groupby('word')['distance'].mean().reset_index()

# Rename columns for clarity
df_winners.columns = ['year', 'average_distance']
df_winners = pd.DataFrame(df_winners)

df_year_counts = df.sort_values(by='distance')[0:10].groupby('word').count().reset_index()[['word', 'distance']]
df_year_counts.columns = ['year', 'count']

df_winners = pd.merge(df_winners, df_year_counts, on='year')

df_winners

# principal_components
# print(pca.explained_variance_ratio_)
calcs = {}
for i in df_winners.iterrows():
    # 1915: 0.99 (score) + 0.13 (count) = 1.12
    calc_count = (i[1]['count'] - df_winners.min()['count'])/(df_winners.max()['count'] - df_winners.min()['count'])
    calc_dist = 1 - (i[1]['average_distance'] - df_winners.min()['average_distance'])/(df_winners.max()['average_distance'] - df_winners.min()['average_distance'])
    calc = (calc_dist + calc_count)/2
    print(i[1]['year'],  calc_dist, '(dist' , str(round(i[1]['average_distance'])) + ')', calc_count, '(count', str(round(i[1]['count'])) + ') =', calc)
    calcs[i[1]['year']] = calc
print()
win = max(calcs, key=calcs.get)
print(win, calcs[win])

dict(sorted(calcs.items(), key=lambda item: item[1]))