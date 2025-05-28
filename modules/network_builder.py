import networkx as nx
import matplotlib.pyplot as plt
from io import BytesIO
from PyQt5.QtGui import QPixmap, QImage

def build_tf_graph(trrust_df, tf_name):
    """
    Given your TRRUST dataframe and a TF name, build a directed graph
    of all interactions where TF → target.
    Assumes trrust_df has columns ['TF','Target','Interaction'].
    """
    G = nx.DiGraph()
    # filter for rows where TF matches
    mask = trrust_df["TF"].str.upper() == tf_name.strip().upper()
    for _, row in trrust_df[mask].iterrows():
        src = row["TF"]
        tgt = row["Target"]
        sign = row.get("Interaction", "")
        G.add_edge(src, tgt, sign=sign)
    return G

def get_network_pixmap(trrust_df, tf_name, width=400, height=300):
    """
    Builds the graph, draws it into a PNG (in memory),
    and returns it as a QPixmap.
    """
    G = build_tf_graph(trrust_df, tf_name)
    # fallback: empty graph
    if G.number_of_nodes() == 0:
        # create a blank pixmap with “No data”
        pix = QPixmap(width, height)
        pix.fill()  # default white
        return pix

    # draw with matplotlib
    fig, ax = plt.subplots(figsize=(width/100, height/100), dpi=100)
    pos = nx.spring_layout(G, seed=42)
    # color edges by activation vs repression if you like
    edge_colors = [
        "green" if G[u][v].get("sign","").lower()=="activation" else "red"
        for u,v in G.edges()
    ]
    nx.draw_networkx_nodes(G, pos, ax=ax, node_size=300)
    nx.draw_networkx_labels(G, pos, ax=ax, font_size=8)
    nx.draw_networkx_edges(G, pos, ax=ax, edge_color=edge_colors, arrowsize=10)
    ax.set_axis_off()

    buf = BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight", pad_inches=0.1)
    plt.close(fig)
    buf.seek(0)

    # convert to QPixmap
    img = QImage.fromData(buf.getvalue())
    return QPixmap.fromImage(img)
