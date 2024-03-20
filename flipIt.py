import pygame
import random
import math

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH = 1280
HEIGHT = 720

# Circle properties
NUM_CIRCLES = 300
CIRCLE_DIAMETER = 5
MOVEMENT_SPEED = 8  # Adjust speed here
GRAVITATIONAL_CONSTANT = 10  # Adjust attraction strength here - was.01

# Initialize the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Brownian Motion Circles")

# Define colors
color_toggle = True
def toggle_colors():
    global color_toggle
    color_toggle = not color_toggle

def get_colors():
    if color_toggle:
        return (255, 255, 255), (0, 0, 0)  # White circles on black background
    else:
        return (0, 0, 0), (255, 255, 255)  # Black circles on white background

# Define a Circle class
class Circle:
    def __init__(self, x, y, diameter):
        self.x = x
        self.y = y
        self.diameter = diameter

    def draw(self):
        circle_color, _ = get_colors()
        pygame.draw.circle(screen, circle_color, (self.x, self.y), self.diameter // 2)

    def move(self, force):
        # Move the circle
        self.x += random.randint(-MOVEMENT_SPEED, MOVEMENT_SPEED) + force[0]
        self.y += random.randint(-MOVEMENT_SPEED, MOVEMENT_SPEED) + force[1]
        
        # Wrap around screen edges (torus behavior)
        self.x %= WIDTH
        self.y %= HEIGHT

    def calculate_gravitational_force(self, other_circle):
        distance = max(((self.x - other_circle.x) ** 2 + (self.y - other_circle.y) ** 2) ** 0.5, 1)  # Ensure distance is at least 1 to avoid division by zero
        force_magnitude = GRAVITATIONAL_CONSTANT * (self.diameter * other_circle.diameter) / distance ** 2
        angle = math.atan2(other_circle.y - self.y, other_circle.x - self.x)
        force_x = force_magnitude * math.cos(angle)
        force_y = force_magnitude * math.sin(angle)
        return force_x, force_y

    def check_collision(self, other_circle):
        distance = ((self.x - other_circle.x) ** 2 + (self.y - other_circle.y) ** 2) ** 0.5
        if distance < (self.diameter + other_circle.diameter) / 2:
            if self.diameter >= other_circle.diameter:
                self.diameter += other_circle.diameter
                return True
            else:
                return False
        return False

# Create circles
def create_circles():
    circles = []
    for _ in range(NUM_CIRCLES):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        new_circle = Circle(x, y, CIRCLE_DIAMETER)
        # Check if the new circle overlaps with existing circles
        while any(new_circle.check_collision(circle) for circle in circles):
            new_circle.x = random.randint(0, WIDTH)
            new_circle.y = random.randint(0, HEIGHT)
        circles.append(new_circle)
    return circles

def respawn_circles():
    toggle_colors()
    return create_circles()

circles = create_circles()

# Main loop
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(get_colors()[1])  # Fill background with appropriate color

    # Move and draw circles
    for circle in circles:
        # Calculate gravitational forces from other circles
        total_force = [0, 0]
        for other_circle in circles:
            if circle != other_circle:
                force = circle.calculate_gravitational_force(other_circle)
                total_force[0] += force[0]
                total_force[1] += force[1]
        
        circle.move(total_force)
        circle.draw()
    
    # Check for collisions
    for circle in circles:
        for other_circle in circles:
            if circle != other_circle:
                if circle.check_collision(other_circle):
                    circles.remove(other_circle)

    # Respawn circles if only one left
    if len(circles) == 1:
        circles = respawn_circles()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

