# Project Ekler 

## Problem Definition

Since Turkish is an agglutinative language, memorizing all the suffixes can be problematic for new Turkish learners, especially with vowel harmony and ordering of the suffixes. So, we wanted to build a tool that can analyze the morphological structure of Turkish verbs, parse their suffixes, check for vowel harmony and suffix ordering, and correct the verbs if necessary.

## Methods & Processes

Helsinki Finite State Technology package is used for this project. Verbs are categorized into 8 groups according to their voicing features and vowel harmony, and these groups are used for writing the verb lexicons. 2 different transducers are generated: Good HFST and Bad HFST. Bad HFST accepts all entries including inacurrate verbs & suffixes. It takes a possibly badly written input, parses root and suffixes, then returns it as an output. The output of Bad HFST is then used as an input into Good HFST, which has the correct phonological rules in place. Good HFST returns the correct form of the verb as the final output.

To exemplify, it can take a word such as `yapmışdı` and return its correct form `yapmıştı`.




[Streamlit App](http://3.83.1.162:8501/)
