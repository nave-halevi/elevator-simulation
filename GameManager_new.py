import pygame


from Reading_json import Reading_json
from Class_street import Street


pygame.init()
size_screen = Reading_json.get_game_manager()

# Set up the screen dimensions and create the display surface
screen = pygame.display.set_mode((size_screen["screen_width"], size_screen["screen_height"]))

# Create a Street object with specified building configurations
street = Street([(10, 2), (22, 4), (15, 3),(25,5),(7, 2)])

# Initialize the clock for controlling the frame rate
clock = pygame.time.Clock()
run = True

# Main game loop
while run:     
    screen.fill(Reading_json.get_color("white")) ## Fill the screen with white color
 
    s_time = pygame.time.get_ticks() / 1000.0  # Get the current time in seconds

    for event in pygame.event.get():  # Event handling loop
        if event.type == pygame.QUIT:  # If the quit event is triggered
            run = False  # Exit the main loop
        if event.type == pygame.MOUSEBUTTONDOWN:  # If the mouse button is pressed
            street.mouse_pos(pygame.mouse.get_pos())  # Handle mouse position

    street.update_buildings(s_time)  # Update the buildings based on the current time
    street.draw_buildings(screen)  # Draw the buildings on the screen
    pygame.display.flip()  # Update the display
    clock.tick(90)  # Cap the frame rate to 90 FPS

# Quit pygame
pygame.quit()


 #and a request for a background image for the screen
# screen.blit(screen_image, (300, 0))
# screen_image = pygame.image.load("/home/mefathim-tech-49/Documents/eievators_project_m.10/image3_988_2015-11-29_14-17-56(2).png") 