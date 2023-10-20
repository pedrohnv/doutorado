# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 09:18:54 2022

@Author Pedro H. N. Vieira

Clear and tidy bibliographic datasets
"""
import pandas as pd
from asreview import ASReviewData, io

#%% Get scopus dataset
bib = ASReviewData.from_file("scopus.ris")
print("==== Scopus dataset ====")
missing_abstract = "" == bib.abstract
print("missing abstracts:", sum(missing_abstract))

df = bib.to_dataframe()
dup_title = df['title'].duplicated()
print("duplicated titles:", sum(dup_title))

print("duplicated title & abstract:", sum(df.duplicated(subset=['title', 'abstract'])))

#%% Remove irrelevant types
df = df[df['type_of_work'] != 'Editorial']
df = df[df['type_of_work'] != 'Conference Review']
df = df[df['type_of_work'] != 'Retracted']


#%% Remove Duplicates
"""
Compare duplicated titles and decide if they are relevant based on title
and abstract and, if relevant, decide which entry to keep.
"""
entries_to_keep = []
entries_to_discard = []
ask_input = False

dup_title = df[dup_title]['title'].to_list()
for title in dup_title:
    print("================ Next duplicates ================")
    dup = df[(df['title'] == title)]
    for i in dup.index:
        entries_to_discard += [i]
        print('record_id:', i)
        for info in ['title', 'abstract', 'year', 'type_of_work']:
            print(info, ':')
            print(dup[info][i])
            print()
            
        print('================')
        
    if ask_input:
        keep_id = input("Which record_id to keep? ")
        if keep_id != '':
            entries_to_keep += [int(keep_id)]

if not ask_input:
    entries_to_keep = [105, 96]  # manually selected a posteriori
    
print("Record's id that will be kept:", entries_to_keep)
for i in entries_to_keep:
    entries_to_discard.remove(i)
    
df = df.drop(entries_to_discard)

#%% Retrieve missing abstracts, if relevant, else remove
ma = df[df['abstract'] == '']
entries_to_discard = ma.index
entries_to_keep = []  # manually selected, none relevant
for i in entries_to_keep:
    entries_to_discard.remove(i)

scopus = df.drop(entries_to_discard)

#%% Get IEEE dataset
bib = ASReviewData.from_file("ieee.ris")
print("==== IEEE dataset ====")
missing_abstract = "" == bib.abstract
print("missing abstracts:", sum(missing_abstract))

df = bib.to_dataframe()
dup_title = df['title'].duplicated()
print("duplicated titles:", sum(dup_title))

# nothing to do on IEEE dataset
ieee = df.copy()

#%% Get prior knowledge dataset
bib = ASReviewData.from_file("prior_knowledge.ris")
print("==== Prior Knowledge dataset ====")
missing_abstract = "" == bib.abstract
print("missing abstracts:", sum(missing_abstract))

df = bib.to_dataframe()
df = df.rename(columns={"primary_title": "title", "notes_abstract": "abstract"}, errors="raise")

dup_title = df['title'].duplicated()
print("duplicated titles:", sum(dup_title))

# nothing to do on Prior Knowledge dataset
pk = df.copy()

#%% Merge datasets, delete duplicates and save
df = pd.concat((pk, scopus, ieee))
print("==== Merged dataset ====")

dup_title = df.duplicated(subset='title', keep='first')
print("duplicated titles:", sum(dup_title))

df = df[~dup_title]

io.RISWriter.write_data(df, "bibliography.ris")

# Then, ASReview is used to remove non-explicit duplicates based on similar text
# The following should be run on the terminal: `asreview data dedup bibliography.ris -o bibliography_dedup.ris`
# Which outputs the following: `Removed 19 duplicates from dataset with 1349 records.`