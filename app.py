import streamlit as st
from pyvis.network import Network
import networkx as nx

from streamlit.components.v1 import html
import json

# ----------------------------
# UI
# ----------------------------
st.set_page_config(page_title="Web of Abstraction", layout="wide")
st.title("🕸️ Web of Abstraction (Abstract → Concrete)")

def init_state():
    if "G" not in st.session_state:
        st.session_state.G = nx.DiGraph()
    if "id_counter" not in st.session_state:
        st.session_state.id_counter = 0
    if "root_id" not in st.session_state:
        st.session_state.root_id = None
    if "current_id" not in st.session_state:
        st.session_state.current_id = None

init_state()

# New or load
with st.sidebar:
    st.header("🔧 Setup / Import / Export")

    if st.session_state.root_id is None:
        default_root = "How might we launch a memorable first podcast episode?"
        root_text = st.text_input("Root 'How might we…?' question:", default_root)
        if st.button("Create Root"):
            if root_text.strip():
                set_root(root_text.strip())

    uploaded = st.file_uploader("Import JSON", type=["json"])
    if uploaded is not None:
        try:
            data = json.load(uploaded)
            load_from_dict(data)
            st.success("Imported JSON successfully.")
        except Exception as e:
            st.error(f"Failed to load JSON: {e}")

    if st.session_state.G.number_of_nodes() > 0:
        export_json = json.dumps(to_dict(), ensure_ascii=False, indent=2)
        st.download_button(
            "Export JSON",
            data=export_json.encode("utf-8"),
            file_name="web_of_abstraction.json",
            mime="application/json",
        )

    st.markdown("---")
    st.caption("Tip: Edges point from **more abstract → more concrete**. Use ABOVE to go abstract, BELOW to go concrete.")
    
# Build a tiny graph
net = Network(
    height="500px",
    width="100%",
    directed=True,
    bgcolor="#ffffff",
    font_color="#000000",
    notebook=False,
    cdn_resources="in_line",  # keeps JS/CSS bundled so Streamlit Cloud works
)
options = {
    "physics": {"enabled": True, "stabilization": {"iterations": 120}},
    "layout": {"hierarchical": {"enabled": True, "direction": "UD"}},
    "edges": {"arrows": {"to": {"enabled": True}}, "smooth": {"enabled": True, "type": "dynamic"}},
}
net.set_options(json.dumps(options))

# Add two nodes and one edge
net.add_node(1, label="How might we make the tool work?", shape="ellipse", color="#FB7E81")
#net.add_node(2, label="How might we make the pyvis render HTML?", shape="box", color="#97C2FC")
#net.add_edge(1, 2, title="is stopped by")

# Render to HTML string and display inside Streamlit
html_str = net.generate_html(name="hello_world.html")
html(html_str, height=520, scrolling=True)
