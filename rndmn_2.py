import math
import random
import pygame
import sys
import csv
import pandas as pd


def update_positions(rocket):
    rocket["position"][0] += rocket["velocity"][0]
    rocket["position"][1] += rocket["velocity"][1]
    return rocket


def rocket_end_position(rocket):
    return [rocket["position"][0], rocket["position"][1] + GRID_SIZE]


def get_color(rate):
    if rate > 0:
        # Incrementing, transition from dark green to light green
        intensity = min(255, int(50 + 20 * abs(math.log10(abs(rate) + 1))))
        return (0, intensity, 0)
    elif rate < 0:
        # Decrementing, transition from dark red to light red
        intensity = min(255, int(50 + 20 * abs(math.log10(abs(rate) + 1))))
        return (intensity, 0, 0)
    else:
        # No change
        return WHITE


def format_altitude(altitude):
    if altitude < 1000:
        return f"{altitude:.0f}"
    elif altitude < 10000:
        return f"{altitude/1000:.1f}k"
    else:
        return f"{altitude/1000:.0f}k"


# Initialize Pygame
pygame.init()

# Set up constants
WIDTH, HEIGHT = 1500, 900
GRID_SIZE = 50
GRID_COLOR = (128, 128, 128)

# Define colors using tuples
WHITE = (255, 255, 255)
BROWN = (189, 150, 123)  # Brown color
BLUE_OLD = (0, 0, 255)  # Blue color
BLUE = (106, 182, 216)
BLACK = (0, 0, 0)

image = pygame.image.load('assets/fire.png')
vab_image = pygame.image.load("assets/vab2_updated.png")
vab_image = pygame.transform.scale(vab_image, (300*1.5, 300))

# Get the image's rect and set initial coordinates
image_rect = image.get_rect()

# Create the Pygame window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rocket Controller")
font = pygame.font.Font(None, 36)
rocket_dynamics = {"position": [WIDTH // 2, 3*HEIGHT //
                                4 - GRID_SIZE], "velocity": [0, 0]}
color_switch_coordinate = 3 * HEIGHT // 4
gravity = 0.1
engine_power = 0.2
engine_status = True
velocity_values = []
displacement_values = []

# Camera variables
camera_offset = [0, 0]
zoom = 1.0
zoom_speed = 0.1
frame_count = 0
image = pygame.transform.scale(image, (20, 20))
image = pygame.transform.flip(image, False, True)

image_rect.center = (rocket_dynamics["position"][0] + camera_offset[0] + 5*GRID_SIZE + 5,
                     rocket_dynamics["position"][1] + camera_offset[1] + 2.5*GRID_SIZE + 5)  # Initial position at the center


class Rocket:
    def __init__(self, rect_x, rect_y, rect_width, rect_height, triangle_x, triangle_y, triangle_base, triangle_height, rect_color, triangle_color):
        self.rect = pygame.Rect(rect_x, rect_y, rect_width, rect_height)
        self.triangle_points = [(triangle_x, triangle_y),
                                (triangle_x + triangle_base / 2,
                                 triangle_y - triangle_height),
                                (triangle_x + triangle_base, triangle_y)]
        self.rect_color = rect_color
        self.triangle_color = triangle_color

    def draw(self, screen):
        pygame.draw.rect(screen, self.rect_color, self.rect)
        pygame.draw.polygon(screen, self.triangle_color, self.triangle_points)

    def set_position(self, new_rect_x, new_rect_y, new_triangle_x, new_triangle_y):
        self.rect.x, self.rect.y = new_rect_x, new_rect_y
        self.triangle_points[0] = (new_triangle_x, new_triangle_y)
        self.triangle_points[1] = (
            new_triangle_x + self.rect.width / 2, new_triangle_y - self.rect.height)
        self.triangle_points[2] = (
            new_triangle_x + self.rect.width, new_triangle_y)


rocket = Rocket(rocket_dynamics["position"][0] + camera_offset[0], rocket_dynamics["position"][1] + camera_offset[1],
                20, 50, rocket_dynamics["position"][0] + camera_offset[0], (rocket_dynamics)["position"][1] + camera_offset[1], 20, 30, BLACK, BLACK)

sep = False
engine_throttle_level = 0

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            csv_file_path = 'velocity_vals.csv'
            data = {'Velocity': velocity_values,
                    'Displacement': displacement_values}
            df = pd.DataFrame(data)
            df.to_csv("velocity_vals.csv")

            print(f'CSV file "{csv_file_path}" created successfully.')

            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if engine_throttle_level < 10:
                    engine_throttle_level += 1
            elif event.key == pygame.K_DOWN:
                if engine_throttle_level > 0:
                    engine_throttle_level -= 1
    keys = pygame.key.get_pressed()

    # Update the rocket's velocity and position
    if engine_power > 0:
        engine_power = engine_power - \
            (0 * (engine_throttle_level / 10)) if engine_power > 0.09 else 0
        rocket_dynamics["velocity"][1] -= engine_power * \
            (engine_throttle_level / 10)
        engine_status = True
    else:
        engine_status = False

    if frame_count % 5 == 0:
        # Define the weights for each number
        weights = [1, 1, 1, 2, 4, 6, 4, 2, 1, 1, 1]

        # Choose a random number based on the weights
        engine_throttle_level = random.choices(
            range(0, 11), weights=weights)[0]
        print(engine_throttle_level, end="")

    # if engine_power == 0 and keys[pygame.K_a] and sep == False:
    #     engine_power = 0.25
    #     sep = True

    if rocket_dynamics["position"][1] < 3 * HEIGHT // 4 - GRID_SIZE:
        rocket_dynamics["velocity"][1] += gravity

    if rocket_dynamics["position"][1] > 3 * HEIGHT // 4 - GRID_SIZE:
        # print(rocket_dynamics["velocity"][1], engine_power)
        rocket_dynamics["velocity"][1] = 0
        rocket_dynamics["position"][1] = 3 * \
            HEIGHT // 4 - GRID_SIZE

    # if frame_count % 5 == 0:
    #     print(rocket_dynamics["velocity"][1], engine_power)

    rocket_dynamics = update_positions(rocket_dynamics)

    # if frame_count % 10 == 0:
    # print(rocket_dynamics["velocity"][1])
    velocity_values.append(rocket_dynamics["velocity"][1])
    displacement_values.append(rocket_dynamics["position"][1])
    displacement_change = (displacement_values[-2] -
                           displacement_values[-1]) if len(displacement_values) > 2 else 0
    # Adjust the camera to follow the rocket
    camera_offset[0] = WIDTH // 2 - rocket_dynamics["position"][0]
    camera_offset[1] = HEIGHT // 2 - rocket_dynamics["position"][1]

    # Clear the screen
    screen.fill(BLUE)
    if engine_status:
        screen.blit(image, image_rect)
    vab_img_rect = vab_image.get_rect()
    vab_img_rect.center = [3*WIDTH//4 +
                           camera_offset[0], 3*HEIGHT // 4 - 150 + camera_offset[1]]

    screen.blit(vab_image, vab_img_rect)

    altitude_color = get_color(displacement_change)
    # print(velocity_change, altitude_color)
    # Render the text
    text_surface_1 = font.render(
        "Altitude: " + str(format_altitude(round(abs((3 * HEIGHT // 4) - rocket_dynamics["position"][1]), 1))), True, altitude_color)

    # Get the rectangle containing the text surface
    text_rect_1 = text_surface_1.get_rect()

    # Center the text on the screen
    text_rect_1.center = (WIDTH - 100, 100)

    # Blit the text surface onto the screen
    screen.blit(text_surface_1, text_rect_1)

    text_surface_2 = font.render(
        "Velocity: " + str(format_altitude(-1 * round(rocket_dynamics["velocity"][1], 1))), True, altitude_color)

    # Get the rectangle containing the text surface
    text_rect_2 = text_surface_2.get_rect()

    # Center the text on the screen
    text_rect_2.center = (WIDTH - 100, 150)

    # Blit the text surface onto the screen
    screen.blit(text_surface_2, text_rect_2)

    text_surface_3 = font.render(
        "Throttle: " + str(engine_throttle_level), True, WHITE)

    # Get the rectangle containing the text surface
    text_rect_3 = text_surface_2.get_rect()

    # Center the text on the screen
    text_rect_3.center = (WIDTH - 100, 200)

    # Blit the text surface onto the screen
    screen.blit(text_surface_3, text_rect_3)

    # Draw land partition
    pygame.draw.line(screen, GRID_COLOR, (
        0 + camera_offset[0], 3*HEIGHT//4 + camera_offset[1]), (WIDTH + camera_offset[0], 3*HEIGHT//4 + camera_offset[1]))

    # Draw the rocket
    rocket.set_position(rocket_dynamics["position"][0] + camera_offset[0], rocket_dynamics["position"][1] + camera_offset[1],
                        rocket_dynamics["position"][0] + camera_offset[0], (rocket_dynamics)["position"][1] + camera_offset[1])
    rocket.draw(screen)
    pygame.draw.rect(screen, BROWN, (0, HEIGHT * 0.75 + camera_offset[1],
                     WIDTH, 2 * HEIGHT + camera_offset[1]))

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    pygame.time.Clock().tick(30)
    frame_count += 1
