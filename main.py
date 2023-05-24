import streamlit as st
import pandas as pd
from specklepy.api.wrapper import StreamWrapper
from specklepy.api.client import SpeckleClient
from specklepy.api import operations


def get_element_parameters(element, parameter_list):
    param_dict = {}
    for p in parameter_list:
        element["parameters"][p]


st.set_page_config(page_title="Speckle Data", page_icon="📐")

header = st.container()
data = st.container()

with header:
    st.header("Speckle Spec")
    st.info("Skapar en specifikation av valda parametrar för aktuell kategori")

with data:
    st.subheader("Input")
    commit_url = st.text_input(
        "Speckle Commit URL",
        "https://speckle.xyz/streams/678156502c/commits/19fe93184e",
    )

wrapper = StreamWrapper(commit_url)
client = wrapper.get_client()
transport = wrapper.get_transport()

commit = client.commit.get(wrapper.stream_id, wrapper.commit_id)
obj_id = commit.referencedObject
commit_data = operations.receive(obj_id, transport)

categories = commit_data.get_dynamic_member_names()

with data:
    selected_category = st.selectbox("Kategori", categories)

elements = commit_data[selected_category]
parameters = elements[0]["parameters"]
parameter_dict = {p.name: p for p in parameters}

parameter_names = sorted([p.name for p in parameters])

with data:
    selected_parameters = st.multiselect("Parametrar", parameter_names)


parameter_dict
