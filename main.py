import pygame
import sys
import math
import matplotlib.pyplot as plt
import copy


def calculate_unit_vector(coord1, coord2):
    # Calculate the vector between the two coordinates
    vector = [coord2[0] - coord1[0], coord2[1] - coord1[1]]

    # Calculate the magnitude of the vector
    magnitude = math.sqrt(vector[0]**2 + vector[1]**2)
    if magnitude == 0:
        return [0, 0]
    # Calculate the unit vector
    unit_vector = [vector[0] / magnitude, vector[1] / magnitude]

    return unit_vector


def update_positions(balls):
    for ball in balls:
        ball["position"][0] += ball["velocity"][0]
        ball["position"][1] += ball["velocity"][1]
    return balls


# Initialize Pygame
pygame.init()

# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Gravity Simulator")

# Set up colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

# Set up ball properties
ball_radius = 20
ball_color = white
ball_speed = 5
gravity_constant = 900

balls = [
    {"position": [width // 4, height // 4], "velocity": [0, 0.4]},
    {"position": [3 * width // 4, 3 * height // 4], "velocity": [0, -0.4]}
]
prev_ball_posn = [copy.copy(balls[0]["position"]),
                  copy.copy(balls[1]["position"])]


frame_count = 0
position_ball_0 = []
position_ball_1 = []
ball_vel_dirn_0 = [0, 0]
ball_vel_dirn_1 = [0, 0]

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    distance = math.sqrt((balls[1]["position"][0] - balls[0]["position"][0])**2 +
                         (balls[1]["position"][1] - balls[0]["position"][1])**2)
    radial_vector = calculate_unit_vector(
        balls[0]["position"], balls[1]["position"])

    if distance > 40:
        balls[0]["velocity"][0] += ((gravity_constant * radial_vector[0]) /
                                    (distance ** 2))
        balls[1]["velocity"][0] += ((gravity_constant * -1 * radial_vector[0]) /
                                    (distance ** 2))

        balls[0]["velocity"][1] += ((gravity_constant * radial_vector[1]) /
                                    (distance ** 2))
        balls[1]["velocity"][1] += ((gravity_constant * -1 * radial_vector[1]) /
                                    (distance ** 2))
    else:
        balls[0]["velocity"][0] = -1 * balls[0]["velocity"][0]*0.85
        balls[1]["velocity"][0] = -1 * balls[1]["velocity"][0]*0.85

        balls[0]["velocity"][1] = -1 * balls[0]["velocity"][1]*0.85
        balls[1]["velocity"][1] = -1 * balls[1]["velocity"][1]*0.85

    if frame_count % 10 == 0:
        print(distance)
        print("-----")

    # Draw background
    screen.fill(black)

    balls = update_positions(balls)
    # Draw balls
    for ball in balls:
        pygame.draw.circle(screen, ball_color, (int(
            ball["position"][0]), int(ball["position"][1])), ball_radius)

    # Update display
    frame_count += 1
    pygame.display.flip()

    # Control the frames per second (FPS)
    pygame.time.Clock().tick(60)
