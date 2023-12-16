import random
import matplotlib.pyplot as plt


class LowPassFilter:
    def __init__(self, alpha):
        self.alpha = alpha
        self.filtered_value = None

    def update(self, new_value):
        if self.filtered_value is None:
            self.filtered_value = new_value
        else:
            self.filtered_value = self.alpha * new_value + \
                (1 - self.alpha) * self.filtered_value

        return self.filtered_value


def custom_distribution():
    weights = [1, 1, 1, 2, 3, 3, 3, 2, 1, 1, 1]
    return random.choices(range(-5, 6), weights=weights)[0]


# Set the smoothing factor (0 < alpha < 1)
alpha = 0.1

# Create a low-pass filter instance
low_pass_filter = LowPassFilter(alpha)

# Simulate live data stream
live_data_stream = []

plt.ion()  # Turn on interactive mode for live plotting

for _ in range(1000):  # Adjust the number of iterations as needed for your live data
    new_data_point = custom_distribution()  # Replace with your live data source

    # Apply the low-pass filter to the live data
    filtered_value = low_pass_filter.update(new_data_point)

    # Append the filtered value to the data stream
    live_data_stream.append(filtered_value)

    # Plot the live data and the filtered data in real-time
    plt.clf()
    plt.plot(live_data_stream, label='Live Data')
    plt.plot([filtered_value] * len(live_data_stream),
             label='Filtered Data', linestyle='--')
    plt.title('Live Data with Low-Pass Filter')
    plt.xlabel('Iteration')
    plt.ylabel('Value')
    plt.legend()
    plt.pause(0.01)  # Adjust the pause time as needed for your live data rate

plt.ioff()  # Turn off interactive mode after the loop completes
plt.show()
