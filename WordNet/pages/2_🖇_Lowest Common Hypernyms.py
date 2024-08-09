import streamlit as st
import _utils.utils as utils

input = st.text_input("Search for the Lowest Common Hyponym for a list of words", help='"table, chair, sofa" -> "furniture"')
words = utils.parse_input(input)

st.write(f"Entered {len(words)} words: {words}")

if len(words) < 2:
    st.write("Please enter at least 2 words!")
else:
    lch, can = utils.lowest_common_hypernyms(words, lambda ss1, ss2: ss1.shortest_path_distance(ss2))
    paths = utils.visualize_lch(lch, can)

    for pos in lch.keys():
        st.markdown(f"##### The meaning you are referring to:")
        for ss in can[pos]:
            st.markdown(f"- **{ss.name()}**: {utils.lemma_names(ss)} -- *{ss.definition()}*")

        ss = lch[pos][0]
        st.markdown(f"##### Lowest Common Hypernym: <span style='color:red'>{ss.name()}</span>", unsafe_allow_html=True)
        st.markdown(f"<div style='border: 1px solid black; padding: 10px;'><strong>{pos}:</strong> {ss.definition()}</div>", unsafe_allow_html=True)
        st.write(f"**{ss.name()}:** {utils.lemma_names(ss)}")

        st.graphviz_chart(paths[pos].source)
        st.markdown('---')