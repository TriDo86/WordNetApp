import streamlit as st
from nltk.corpus import wordnet as wn
import graphviz

import _utils.utils as utils

NOUN_INFO = ['synset', 'hypernyms', 'hyponyms', 'holonyms', 'meronyms']
VERB_INFO = ['synset', 'antonyms', 'hypernyms', 'troponyms', 'derivationally related', 'sentence frame', 'domain']
ADJ_INFO = ['synset', 'antonyms', 'value of']
ADV_INFO = ['synset & stem adj']

POS = {'n': 'n',
       'v': 'v',
       's': 'adj',
       'a': 'adj',
       'r': 'adv'}
POS_DICT = {'nou': 'noun',
            'ver': 'verb',
            #'sat': 'sat',
            'adj': 'adj',
            'adv': 'adv'}

# Text input
word = st.text_input("Search for a word")

# Get synsets
synsets_dict = utils.get_synsets_by_pos(word)

# Display word information
num_sense = sum([len(synsets_dict[pos]) for pos in synsets_dict.keys()])
st.write(f"The word '{word}' has **{num_sense}** {'meaning' if num_sense < 2 else 'meanings'}.\n")


# Create columns
col1, col2 = st.columns([3, 1])
pos_option = [f'{pos} ({len(synsets_dict[pos])})' for pos in synsets_dict.keys()]
with col1:
    pos = st.radio(
        "POS",
        pos_option,
        horizontal=True,
        label_visibility='collapsed'
        )
with col2:
    show_inherited = st.toggle("Show inherited")


if pos != None:
    pos = POS_DICT[pos[:3]]
# Loop through synsets and add radio buttons
if pos == 'noun':
    for i, synset in enumerate(synsets_dict[pos]):
        st.markdown(f"<div style='border: 1px solid black; padding: 10px;'><strong>Sense {i + 1} ({POS[synset.pos()]}.):</strong> {synset.definition()}</div>", unsafe_allow_html=True)

        selected_relation = st.radio("Relations", NOUN_INFO, horizontal=True, key=f'radio_{i}', label_visibility='collapsed')

        if selected_relation == "synset":
            if show_inherited:
                st.write(f"**{synset.name()}: {utils.lemma_names(synset)}**")
            else:
                st.write(f"**{utils.lemma_names(synset)}**")
        elif selected_relation == 'hypernyms':
            utils.print_relation(synset, lambda s: s.hypernyms(), 0, show_inherited)
        elif selected_relation == 'hyponyms':
            utils.print_relation(synset, lambda s: s.hyponyms(), 0, show_inherited)
        elif selected_relation == 'holonyms':
            utils.print_relation(synset, [lambda s: s.member_holonyms(), lambda s: s.substance_holonyms(), lambda s: s.part_holonyms()], 0, show_inherited)
        elif selected_relation == 'meronyms':
            utils.print_relation(synset, [lambda s: s.member_meronyms(), lambda s: s.substance_meronyms(), lambda s: s.part_meronyms()], 0, show_inherited)

elif pos == 'verb':
    for i, synset in enumerate(synsets_dict[pos]):
        st.markdown(f"<div style='border: 1px solid black; padding: 10px;'><strong>Sense {i + 1} ({POS[synset.pos()]}.):</strong> {synset.definition()}</div>", unsafe_allow_html=True)

        selected_relation = st.radio("Relations", VERB_INFO, horizontal=True, key=f'radio_{i}', label_visibility='collapsed')

        if selected_relation == "synset":
            if show_inherited:
                st.write(f"**{synset.name()}: {utils.lemma_names(synset)}**")
            else:
                st.write(f"**{utils.lemma_names(synset)}**")
        elif selected_relation == 'hypernyms':
            utils.print_relation(synset, lambda s: s.hypernyms(), 0, show_inherited)
        elif selected_relation == 'hyponyms':
            utils.print_relation(synset, lambda s: s.hyponyms(), 0, show_inherited)
        else:
            st.write('Sorry, this feature is in development :)')
elif pos == 'adj' or pos == 'sat':
    for i, synset in enumerate(synsets_dict[pos]):
        st.markdown(f"<div style='border: 1px solid black; padding: 10px;'><strong>Sense {i + 1} ({POS[synset.pos()]}.):</strong> {synset.definition()}</div>", unsafe_allow_html=True)

        selected_relation = st.radio("Relations", ADJ_INFO, horizontal=True, key=f'radio_{i}', label_visibility='collapsed')

        if selected_relation == "synset":
            if show_inherited:
                st.write(f"**{synset.name()}: {utils.lemma_names(synset)}**")
            else:
                st.write(f"**{utils.lemma_names(synset)}**")

        elif selected_relation == 'antonyms':
            st.write(f'{[l.antonyms() for l in synset.lemmas()]}')
            utils.print_relation(synset, lambda s: s.hyponyms(), 0, show_inherited)

        elif selected_relation == 'holonyms':
            utils.print_relation(synset, [lambda s: s.member_holonyms(), lambda s: s.substance_holonyms(), lambda s: s.part_holonyms()], 0, show_inherited)
        elif selected_relation == 'meronyms':
            utils.print_relation(synset, [lambda s: s.member_meronyms(), lambda s: s.substance_meronyms(), lambda s: s.part_meronyms()], 0, show_inherited)

elif pos == 'adv':
    for i, synset in enumerate(synsets_dict[pos]):
        st.markdown(f"<div style='border: 1px solid black; padding: 10px;'><strong>Sense {i + 1} ({POS[synset.pos()]}.):</strong> {synset.definition()}</div>", unsafe_allow_html=True)

        selected_relation = st.radio("Relations", ADV_INFO, horizontal=True, key=f'radio_{i}', label_visibility='collapsed')

        if selected_relation == "synset & stem adj":
            if show_inherited:
                st.write(f"**{synset.name()}: {utils.lemma_names(synset)}**")
                st.write('=> ' + ', '.join([p.synset().name() for l in synset.lemmas() for p in l.pertainyms()]))
            else:
                st.write(f"**{utils.lemma_names(synset)}**")
                st.write('=> ' + ', '.join([p.name() for l in synset.lemmas() for p in l.pertainyms()]))
                
else:
    st.write("Please enter a word.")