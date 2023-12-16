import random
import matplotlib.pyplot as plt


def custom_distribution(a, b):
    # weights = [1, 1, 1, 2, 3, 3, 3, 2, 1, 1, 1]
    return random.randint(a, b)
    # return random.choices(range(a, b), weights=weights)[0]


def pid_controller(curr, setpoint, prev_error, integral):
    Kp = 0.5  # Proportional gain
    Ki = 0.1  # Integral gain
    Kd = 0.4  # Derivative gain

    error = setpoint - curr
    integral += error
    derivative = error - prev_error

    # Adjust the current value based on PID components
    correction = Kp * error + Ki * integral + Kd * derivative

    return correction, integral, error


ans = []
orig = []
curr = 0
orig_curr = 0
integral = 0
prev_error = 0
setpoint = 0  # Setpoint is the desired value (in this case, 0)
limit = 5
for i in range(1, 1000):
    # if i % 150 == 0:
    #     limit = limit ** 2
    #     print(limit)
    random_number = custom_distribution(-limit, limit + 1)
    orig_curr += random_number
    orig.append(orig_curr)
    # Use the PID controller to adjust the current value
    correction, integral, error = pid_controller(
        curr, setpoint, prev_error, integral)
    curr += random_number + correction
    ans.append(curr)

    prev_error = error

plt.plot(ans, label='Stabilized Values')
plt.plot(orig, label='Original Values')
plt.title('Stabilized Values with PID Controller')
plt.xlabel('Iteration')
plt.ylabel('Value')
plt.legend()  # Add legend to identify the lines
plt.show()
