import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# --- Page Configuration ---
st.set_page_config(
    page_title="Electric Field Simulator",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.title("⚡ Interactive Electric Field Simulator")
st.write(
    "Use the sidebar to add or remove point charges and see how they "
    "affect the electric field in real-time."
)

# --- Functions for E-Field Calculation and Plotting ---

def get_electric_field(charges, x, y):
    """
    Calculates the electric field vector at a point (x, y) due to a list of charges.
    """
    Ex, Ey = 0, 0
    # Use a small epsilon to prevent division by zero at the charge's exact location
    epsilon = 1e-6
    for q, qx, qy in charges:
        dx = x - qx
        dy = y - qy
        r_squared = dx**2 + dy**2
        
        if r_squared < epsilon**2:
            continue
            
        r = np.sqrt(r_squared)
        E = q / r_squared
        Ex += E * (dx / r)
        Ey += E * (dy / r)
        
    return Ex, Ey

def create_plot(charges, x_range, y_range, grid_density):
    """
    Generates and returns the matplotlib figure for the electric field.
    """
    fig, ax = plt.subplots(figsize=(10, 10))
    
    x = np.linspace(x_range[0], x_range[1], grid_density)
    y = np.linspace(y_range[0], y_range[1], grid_density)
    X, Y = np.meshgrid(x, y)

    Ex, Ey = np.zeros(X.shape), np.zeros(Y.shape)
    for i in range(X.shape[0]):
        for j in range(Y.shape[1]):
            Ex[i, j], Ey[i, j] = get_electric_field(charges, X[i, j], Y[i, j])

    E_magnitude = np.sqrt(Ex**2 + Ey**2)
    
    # Use streamplot to show the direction of the field lines
    ax.streamplot(X, Y, Ex, Ey, color=E_magnitude, cmap='viridis', linewidth=1, density=1.5, arrowstyle='->', arrowsize=1.5)

    # Plot the charges
    for q, qx, qy in charges:
        color = 'red' if q > 0 else 'blue'
        ax.plot(qx, qy, 'o', markersize=max(6, min(20, abs(q) * 5)), color=color)

    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title('Electric Field Visualization')
    ax.set_xlim(x_range)
    ax.set_ylim(y_range)
    ax.set_aspect('equal', adjustable='box')
    ax.grid(True, linestyle='--', alpha=0.6)
    
    return fig

# --- Sidebar for User Inputs ---

st.sidebar.header("Controls")

# Initialize charges in session state if they don't exist
if 'charges' not in st.session_state:
    # Default to an electric dipole
    st.session_state.charges = [[1.0, -2.0, 0.0], [-1.0, 2.0, 0.0]]

# Sliders for plot settings
st.sidebar.subheader("Plot Settings")
grid_density = st.sidebar.slider("Grid Density", 10, 50, 25)
plot_range = st.sidebar.slider("Plot Range", 1, 20, 10)
x_range = (-plot_range, plot_range)
y_range = (-plot_range, plot_range)

# UI for adding a new charge
st.sidebar.subheader("Add a Charge")
q = st.sidebar.number_input("Charge (q)", value=1.0, step=0.5)
qx = st.sidebar.number_input("x-coordinate", value=0.0, step=0.5)
qy = st.sidebar.number_input("y-coordinate", value=0.0, step=0.5)

if st.sidebar.button("Add Charge"):
    st.session_state.charges.append([q, qx, qy])
    st.rerun()

# --- Main App Area ---

# Display the plot
if not st.session_state.charges:
    st.warning("No charges to display. Please add a charge using the sidebar.")
else:
    # Create and display the plot
    field_plot = create_plot(st.session_state.charges, x_range, y_range, grid_density)
    st.pyplot(field_plot)

# Display and manage current charges
st.sidebar.subheader("Current Charges")
if not st.session_state.charges:
    st.sidebar.info("No charges added yet.")
else:
    # Use a DataFrame for a cleaner look
    charges_df = pd.DataFrame(st.session_state.charges, columns=['q', 'x', 'y'])
    charges_df['Remove'] = [f'rm_{i}' for i in range(len(st.session_state.charges))]
    
    edited_df = st.sidebar.data_editor(
        charges_df,
        column_config={
            "Remove": st.column_config.CheckboxColumn(
                "Remove?",
                default=False,
            )
        },
        hide_index=True,
    )
    
    # Find which charges were marked for removal
    charges_to_remove_indices = edited_df[edited_df['Remove']].index
    
    if len(charges_to_remove_indices) > 0:
        # Filter out the charges marked for removal
        st.session_state.charges = [
            charge for i, charge in enumerate(st.session_state.charges)
            if i not in charges_to_remove_indices
        ]
        st.rerun()

