import streamlit as st
from pyvis.network import Network
from streamlit.components.v1 import html

st.title("🔗 PyVis Hello World")

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

# Add two nodes and one edge
net.add_node(1, label="Hello", shape="box", color="#97C2FC")
net.add_node(2, label="World", shape="ellipse", color="#FB7E81")
net.add_edge(1, 2, title="connects to")

# Render to HTML string and display inside Streamlit
html_str = net.generate_html(name="hello_world.html")
html(html_str, height=520, scrolling=True)
