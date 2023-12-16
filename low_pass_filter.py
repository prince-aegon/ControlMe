import matplotlib.pyplot as plt
import random


class LowPassFilter:
    def __init__(self, alpha):
        # 'alpha' is the smoothing factor, where 0 < alpha < 1
        self.alpha = alpha
        self.filtered_value = None

    def update(self, new_value):
        if self.filtered_value is None:
            self.filtered_value = new_value
        else:
            self.filtered_value = self.alpha * new_value + \
                (1 - self.alpha) * self.filtered_value

        return self.filtered_value


# Example usage:


def custom_distribution():
    weights = [1, 1, 1, 2, 3, 3, 3, 2, 1, 1, 1]
    return random.choices(range(-5, 6), weights=weights)[0]


ans, orig = [], []
curr, orig_curr = 0, 0
for i in range(1, 1000):
    random_number = custom_distribution()
    orig_curr += random_number
    orig.append(orig_curr)

    curr += random_number
    ans.append(curr)
# Simulate the dataset using the custom distribution
# raw_data = [custom_distribution() for _ in range(1000)]

# Set the smoothing factor (0 < alpha < 1)
alpha = 0.08

# Create a low-pass filter instance
low_pass_filter = LowPassFilter(alpha)

# Apply the low-pass filter to the raw data
filtered_data = [low_pass_filter.update(value) for value in ans]

# Plot the original raw data and the filtered data
plt.plot(orig, label='Raw Data')
plt.plot(filtered_data, label='Filtered Data')
plt.title('Low-Pass Filter on Custom Distribution')
plt.xlabel('Iteration')
plt.ylabel('Value')
plt.legend()
plt.show()
