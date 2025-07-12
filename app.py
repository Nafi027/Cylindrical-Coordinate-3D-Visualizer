import streamlit as st
import numpy as np
import plotly.graph_objects as go
import time

st.set_page_config(page_title="Stable Cylindrical View", layout="wide")
st.title("📐 Cylindrical Coordinate Viewer with Stable Camera")

# Initial camera
if "camera" not in st.session_state:
    st.session_state.camera = dict(eye=dict(x=1.5, y=1.5, z=1.5))

# Sidebar inputs
r_val = st.sidebar.slider("r (radius)", 0.1, 5.0, 2.0, 0.1)
phi_deg = st.sidebar.slider("φ (angle in degrees)", 0, 360, 45, 1)
z_val = st.sidebar.slider("z (height)", 0.0, 5.0, 2.5, 0.1)
animate = st.sidebar.button("🔁 Auto Rotate φ")

# Add fixed 3D reference axes
def add_reference_frame(fig):
    L = 6
    fig.add_trace(go.Scatter3d(x=[0, L], y=[0, 0], z=[0, 0],
        mode="lines+text", line=dict(color="red", width=4),
        text=["", "X"], textposition="top right", showlegend=False))
    fig.add_trace(go.Scatter3d(x=[0, 0], y=[0, L], z=[0, 0],
        mode="lines+text", line=dict(color="green", width=4),
        text=["", "Y"], textposition="top right", showlegend=False))
    fig.add_trace(go.Scatter3d(x=[0, 0], y=[0, 0], z=[0, L],
        mode="lines+text", line=dict(color="blue", width=4),
        text=["", "Z"], textposition="top right", showlegend=False))

    # XY Grid plane
    xg = np.linspace(-5, 5, 10)
    yg = np.linspace(-5, 5, 10)
    Xg, Yg = np.meshgrid(xg, yg)
    Zg = np.zeros_like(Xg)
    fig.add_trace(go.Surface(x=Xg, y=Yg, z=Zg,
        showscale=False, opacity=0.1,
        colorscale=[[0, 'gray'], [1, 'gray']], hoverinfo='skip'))

def plot_scene(r_val, phi_deg, z_val):
    phi_rad = np.deg2rad(phi_deg)
    x = r_val * np.cos(phi_rad)
    y = r_val * np.sin(phi_rad)

    theta = np.linspace(0, 2*np.pi, 100)
    z_cyl = np.linspace(0, 5, 100)
    TH, Z = np.meshgrid(theta, z_cyl)
    Xcyl = r_val * np.cos(TH)
    Ycyl = r_val * np.sin(TH)

    fig = go.Figure()

    fig.add_trace(go.Surface(
        x=Xcyl, y=Ycyl, z=Z,
        colorscale='Blues', opacity=0.4, showscale=False
    ))

    fig.add_trace(go.Scatter3d(
        x=[x], y=[y], z=[z_val],
        mode="markers+text",
        marker=dict(size=6, color="red"),
        text=[f"(r={r_val}, φ={phi_deg}°, z={z_val})"],
        textposition="top center"
    ))

    fig.add_trace(go.Scatter3d(
        x=[0, x], y=[0, y], z=[0, 0],
        mode="lines", line=dict(color="gray", dash="dash"), showlegend=False))
    fig.add_trace(go.Scatter3d(
        x=[x, x], y=[y, y], z=[0, z_val],
        mode="lines", line=dict(color="gray", dash="dash"), showlegend=False))

    add_reference_frame(fig)

    fig.update_layout(
        scene=dict(
            xaxis_title='X', yaxis_title='Y', zaxis_title='Z',
            aspectmode='cube', camera=st.session_state.camera
        ),
        margin=dict(l=0, r=0, b=0, t=40),
        height=750
    )
    return fig

# Animate or show static
if animate:
    container = st.empty()
    for phi in range(0, 361, 3):
        fig = plot_scene(r_val, phi, z_val)
        container.plotly_chart(fig, use_container_width=True)
        time.sleep(0.03)
else:
    fig = plot_scene(r_val, phi_deg, z_val)
    chart = st.plotly_chart(fig, use_container_width=True, key="chart")

    # Store new camera angle if user interacted
    if hasattr(chart, "relayout_data") and chart.relayout_data:
        cam_data = chart.relayout_data.get("scene.camera", None)
        if cam_data:
            st.session_state.camera = cam_data
