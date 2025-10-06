import streamlit as st
from pyvis.network import Network
from streamlit.components.v1 import html
import json

# ----------------------------
# UI
# ----------------------------
st.set_page_config(page_title="Web of Abstraction", layout="wide")
st.title("🕸️ Web of Abstraction (Abstract → Concrete)")

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
net.add_node(2, label="How might we make the pyvis render HTML?", shape="box", color="#97C2FC")
net.add_edge(1, 2, title="is stopped by")

# Render to HTML string and display inside Streamlit
html_str = net.generate_html(name="hello_world.html")
html(html_str, height=520, scrolling=True)
