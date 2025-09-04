import numpy as np
import matplotlib.pyplot as plt

def get_electric_field(charges, x, y):
    """
    Calculates the electric field vector at a point (x, y) due to a list of charges.

    Args:
        charges (list): A list of tuples, where each tuple represents a charge
                        in the format (q, x_pos, y_pos). 
                        'q' is the charge magnitude.
                        '(x_pos, y_pos)' is the position of the charge.
        x (float): The x-coordinate of the point where the field is calculated.
        y (float): The y-coordinate of the point where the field is calculated.

    Returns:
        tuple: A tuple (Ex, Ey) representing the x and y components of the
               electric field vector.
    """
    Ex, Ey = 0, 0
    for q, qx, qy in charges:
        # Calculate the distance from the charge to the point
        dx = x - qx
        dy = y - qy
        r_squared = dx**2 + dy**2
        
        # Avoid division by zero at the charge's location
        if r_squared == 0:
            continue
            
        r = np.sqrt(r_squared)
        
        # Calculate the electric field components using Coulomb's Law (k=1 for simplicity)
        E = q / r_squared
        Ex += E * (dx / r)
        Ey += E * (dy / r)
        
    return Ex, Ey

def plot_electric_field(charges, x_range=(-10, 10), y_range=(-10, 10), grid_density=20):
    """
    Visualizes the electric field of a set of charges.

    Args:
        charges (list): A list of tuples, each representing a charge (q, x_pos, y_pos).
        x_range (tuple): The range of x-values for the plot.
        y_range (tuple): The range of y-values for the plot.
        grid_density (int): The number of points in each dimension of the grid.
    """
    # Create a grid of points to calculate the field at
    x = np.linspace(x_range[0], x_range[1], grid_density)
    y = np.linspace(y_range[0], y_range[1], grid_density)
    X, Y = np.meshgrid(x, y)

    # Calculate the electric field at each point on the grid
    Ex, Ey = np.zeros(X.shape), np.zeros(Y.shape)
    for i in range(X.shape[0]):
        for j in range(Y.shape[1]):
            Ex[i, j], Ey[i, j] = get_electric_field(charges, X[i, j], Y[i, j])

    # Normalize the field vectors for better visualization
    E_magnitude = np.sqrt(Ex**2 + Ey**2)
    # Avoid division by zero where magnitude is zero
    with np.errstate(divide='ignore', invalid='ignore'):
        Ex_norm = Ex / E_magnitude
        Ey_norm = Ey / E_magnitude

    # Create the plot
    plt.figure(figsize=(10, 10))
    
    # Use streamplot to show the direction of the field lines
    plt.streamplot(X, Y, Ex, Ey, color='gray', linewidth=1, density=1.5, arrowstyle='->', arrowsize=1.5)

    # Plot the charges
    for q, qx, qy in charges:
        color = 'red' if q > 0 else 'blue'
        plt.plot(qx, qy, 'o', markersize=abs(q)*10, color=color)

    # Set plot labels and title
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Electric Field Visualization')
    plt.xlim(x_range)
    plt.ylim(y_range)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.show()

if __name__ == '__main__':
    # --- Example Configurations ---
    
    # 1. A single positive charge
    # charges = [(1, 0, 0)]

    # 2. A single negative charge
    # charges = [(-1, 0, 0)]
    
    # 3. An electric dipole
    charges = [(1, -2, 0), (-1, 2, 0)]
    
    # 4. Two positive charges (repulsion)
    # charges = [(1, -2, 0), (1, 2, 0)]

    # 5. A quadrupole
    # charges = [(1, -2, -2), (-1, 2, -2), (1, 2, 2), (-1, -2, 2)]

    # 6. A more complex arrangement
    # charges = [(2, 3, 4), (-1, -5, 2), (1.5, 6, -3), (-2.5, -1, -5)]

    plot_electric_field(charges)
