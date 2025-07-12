# Cylindrical Coordinate 3D Visualizer with Stable Camera

An interactive Streamlit app to visualize points and surfaces in the cylindrical coordinate system \((r, \phi, z)\) with a stable 3D camera view.

---

## Features

- Visualizes the cylindrical surface of fixed radius \(r\).
- Displays a point at cylindrical coordinates \((r, \phi, z)\).
- Shows projection lines from the point to the base XY-plane and vertical height.
- Includes a fixed 3D reference frame with labeled \(X\), \(Y\), and \(Z\) axes and an XY grid.
- Preserves the user’s camera view angle during interaction and parameter changes.
- Optional animation to auto-rotate the angle \(\phi\).
- Responsive layout fits the visualization to the browser window.

---

## Installation

Make sure you have Python 3.x installed. Then install the required packages:

```bash
pip install streamlit numpy plotly
