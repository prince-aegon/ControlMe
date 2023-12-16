import pandas as pd
import matplotlib.pyplot as plt

# Read data from the CSV file
csv_file = "velocity_vals.csv"
data = pd.read_csv(csv_file)

# Extract velocity and displacement data
velocity_data = data["Velocity"]
displacement_data = data["Displacement"]
velocity_data = [-50 * i for i in velocity_data]
displacement_data = [abs(((3 * 900) / 4) - i) for i in displacement_data]
# Plot both velocity and displacement on the same graph
plt.plot(velocity_data, label="Velocity", color="blue")
plt.plot(displacement_data, label="Displacement", color="red")

# Add labels and a legend
plt.xlabel("Time")
plt.ylabel("Values")
plt.title("Velocity and Displacement over Time")
plt.legend()

# Show the plot
plt.show()
