# -*- coding: utf-8 -*-
"""
Get relevant references and, if url is a scopus link, clear it.
"""
import pandas as pd
import bibtexparser


filepath = "relevant_references.bib"
with open(filepath, 'r', encoding='utf-8') as f:
    bib = bibtexparser.load(f)

df = pd.DataFrame.from_dict(bib.entries)
for i, url in enumerate(df.loc[:, ('url')]):
    try:
        if 'scopus' in url:
            df.loc[:, ('url')][i] = ""
            
    except TypeError:
        next


with open('relevant_references_clean.bib', 'w') as bibtex_file:
    bibtexparser.dump(bibtex_database, bibtex_file)