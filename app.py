import streamlit as st
from pyvis.network import Network
import networkx as nx
from typing import Dict, List, Optional, Tuple

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

def list_nodes_sorted() -> List[int]:
    return sorted(st.session_state.G.nodes)

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

if st.session_state.G.number_of_nodes() == 0:
    st.info("Create a root question in the left sidebar, or import a JSON to begin.")
    st.stop()

# Controls
colL, colR = st.columns([0.42, 0.58])

with colL:
    st.subheader("🧭 Navigate & Edit")
    all_nodes = list_nodes_sorted()
    labels = [node_display(n) for n in all_nodes]
    idx_default = 0
    if st.session_state.current_id in all_nodes:
        idx_default = all_nodes.index(st.session_state.current_id)

    chosen = st.selectbox("Current node", options=list(zip(labels, all_nodes)), index=idx_default, format_func=lambda x: x[0])
    current_id = chosen[1] if isinstance(chosen, tuple) else chosen
    st.session_state.current_id = current_id

    current = st.session_state.G.nodes[current_id]["data"]
    edited_text = st.text_area("Edit text", value=current.text, height=120)
    if st.button("Save text"):
        st.session_state.G.nodes[current_id]["data"].text = edited_text.strip()
        st.success("Updated.")

    st.markdown("**Add nodes**")
    new_above = st.text_input("New ABOVE (more abstract)", placeholder="How might we … ?")
    new_below = st.text_input("New BELOW (more concrete)", placeholder="How might we … ?")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("➕ Add ABOVE"):
            text = new_above.strip() if new_above.strip() else "How might we … ?"
            add_above(current_id, text, move_to_new=True)
            st.experimental_rerun()
    with c2:
        if st.button("➕ Add BELOW"):
            text = new_below.strip() if new_below.strip() else "How might we … ?"
            add_below(current_id, text, move_to_new=True)
            st.experimental_rerun()

    st.markdown("---")
    danger = st.checkbox("Enable destructive action")
    if danger and st.button("🗑️ Delete current node"):
        delete_node(current_id)
        st.warning("Node deleted.")
        st.experimental_rerun()


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
