import pygame
print(pygame.ver)

import random
import math

# Initialize Pygame
pygame.init()

# Create a Clock object
clock = pygame.time.Clock()

# Game Constants
WIDTH, HEIGHT = 1400, 800
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)

# Create Game Window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")


# Load Background Music
pygame.mixer.music.load("Graphics/Music/SoundM.mp3")  # Replace with the correct path to your music file
pygame.mixer.music.set_volume(0.5)  # Set the volume (optional)

# Load Images
player_img = pygame.image.load("Graphics/player1/set1.png")
enemy_img = pygame.image.load("Graphics/enemy.png")
bullet_img = pygame.image.load("Graphics/bullet.png")

# Resize Images
player_img = pygame.transform.scale(player_img, (90, 90))
enemy_img = pygame.transform.scale(enemy_img, (70, 50)) 
bullet_img = pygame.transform.scale(bullet_img, (10, 30))

# Load Player Animation Frames
player_frames = [
    pygame.image.load("Graphics/player1/set1.png"),
    pygame.image.load("Graphics/player1/set2.png"),
    pygame.image.load("Graphics/player1/set3.png"),
    pygame.image.load("Graphics/player1/set4.png"),
]

# Resize Player Animation Frames
player_frames = [pygame.transform.scale(frame, (90, 90)) for frame in player_frames]

# Animation Variables
player_frame_index = 0
animation_speed = 100  # Milliseconds per frame
last_animation_time = pygame.time.get_ticks()

# Load Bullet Animation Frames
bullet_frames = [
    pygame.image.load(f"Graphics/Bullet/y{i}.png") for i in range(1, 4)
]

# Resize Bullet Animation Frames
bullet_frames = [pygame.transform.scale(frame, (20, 60)) for frame in bullet_frames]  # Increased size

# Bullet Animation Variables
bullet_frame_index = 0
bullet_animation_speed = 50  # Milliseconds per frame
last_bullet_animation_time = pygame.time.get_ticks()

# Load Button Sound
button_sound = pygame.mixer.Sound("Graphics/Music/buttons.mp3")  # Replace with the correct path to your sound file
button_sound.set_volume(0.5)  # Set the volume (optional)

# Load Laser Shot Sound
laser_shot = pygame.mixer.Sound("Graphics/Music/laser-shot.mp3")
laser_shot.set_volume(0.3)  # Adjust volume as needed

# Load Enemy Death Sound
enemyD = pygame.mixer.Sound("Graphics/Music/enemyD.mp3")
enemyD.set_volume(0.6)  # Adjust volume as needed

# Player Variables
player_x = WIDTH // 2 - 35
player_y = HEIGHT - 150
player_speed = 10

# Bullet Variables
bullets = []
can_shoot = True           # Allow shooting by default
last_shot_time = 0         # Timestamp of the last shot
shoot_cooldown = 300       # Cooldown period in milliseconds (adjust as needed)
bullet_speed = 10          # Bullet movement speed (adjust as needed)

# Score and Level
score = 0
level = 1

# Load Custom Font
font = pygame.font.Font("Graphics/Font/monogram.ttf", 36)  # Adjust the path and size as needed

# Enemy Spacing
def create_enemies(rows, cols, speed):
    enemies = []
    x_spacing = (WIDTH - 600) // cols  # Reduced horizontal spacing
    y_spacing = 40  # Reduced vertical spacing
    start_x = 100  # Starting x position (adjusted for centering)
    start_y = 50  # Starting y position

    for row in range(rows):
        for col in range(cols):
            enemy_x = start_x + col * x_spacing
            enemy_y = start_y + row * y_spacing
            enemies.append([enemy_x, enemy_y, speed])
    return enemies

def draw_button(text, x, y, text_color, is_hovered):
    # Render Shadow
    shadow_color = (50, 50, 50)  # Dark gray for shadow
    shadow_offset = 2  # Offset for the shadow
    shadow_label = font.render(text, True, shadow_color)
    shadow_rect = shadow_label.get_rect(center=(x, y + shadow_offset))
    screen.blit(shadow_label, shadow_rect)

    # Render Text
    label = font.render(text, True, WHITE if is_hovered else text_color)
    text_rect = label.get_rect(center=(x, y))
    screen.blit(label, text_rect)

    # Remove arrow drawing for hovered buttons
    # (Previously, an arrow was drawn here when `is_hovered` was True)

def draw_arrow(x, text_center_y):
    # Arrow dimensions for consistent design
    arrow_width = 10  # Width of the arrow
    arrow_height = 6  # Height of the arrow
    arrow_points = [
        (x, text_center_y),                      # Tip of the arrow
        (x - arrow_width, text_center_y - arrow_height),  # Top point
        (x - arrow_width, text_center_y + arrow_height)   # Bottom point
    ]
    pygame.draw.polygon(screen, WHITE, arrow_points)

def draw_back_arrow():
    # Draw a back arrow in the top-left corner
    arrow_points = [(20, 20), (40, 30), (20, 40)]  # Arrow shape
    pygame.draw.polygon(screen, WHITE, arrow_points)

def difficulty_selection():
    # Load the background animation frames for the difficulty selection screen
    background_frames = [
        pygame.image.load(f"Graphics/BackG3/h{i}.png") for i in range(1, 13)  # Adjusted range to 1-12
    ]
    background_frames = [pygame.transform.scale(frame, (WIDTH, HEIGHT)) for frame in background_frames]

    # Animation variables
    bg_frame_index = 0
    bg_animation_speed = 100  # Milliseconds per frame
    last_bg_animation_time = pygame.time.get_ticks()

    button_spacing = 50  # Spacing between buttons
    start_y = 330

    # Arrow blinking animation variables
    arrow_visible = True
    arrow_blink_speed = 500  # Milliseconds
    last_arrow_blink_time = pygame.time.get_ticks()

    # Load a larger and bold font for the title
    title_font = pygame.font.Font("Graphics/Font/monogram.ttf", 88)

    while True:
        # Handle background animation timing
        current_time = pygame.time.get_ticks()
        if current_time - last_bg_animation_time > bg_animation_speed:
            bg_frame_index = (bg_frame_index + 1) % len(background_frames)
            last_bg_animation_time = current_time

        # Handle arrow blinking animation timing
        if current_time - last_arrow_blink_time > arrow_blink_speed:
            arrow_visible = not arrow_visible
            last_arrow_blink_time = current_time

        # Draw the current background frame
        screen.blit(background_frames[bg_frame_index], (0, 0))

        mouse_pos = pygame.mouse.get_pos()

        # Render "Choose Your Game Mode" Text
        title_text = title_font.render("Choose Your Game Mode", True, WHITE)
        title_shadow = title_font.render("Choose Your Game Mode", True, (50, 50, 50))
        title_rect = title_text.get_rect(center=(WIDTH // 2, 250))
        title_shadow_rect = title_shadow.get_rect(center=(WIDTH // 2 + 2, 252))
        screen.blit(title_shadow, title_shadow_rect)
        screen.blit(title_text, title_rect)

        # Draw Buttons for EASY, MEDIUM, and HARD modes only
        easy_text = "EASY"
        medium_text = "MEDIUM"
        hard_text = "HARD"

        easy_rect = font.render(easy_text, True, WHITE).get_rect(center=(WIDTH // 2, start_y))
        medium_rect = font.render(medium_text, True, WHITE).get_rect(center=(WIDTH // 2, start_y + button_spacing))
        hard_rect = font.render(hard_text, True, WHITE).get_rect(center=(WIDTH // 2, start_y + button_spacing * 2))

        easy_btn_hover = easy_rect.collidepoint(mouse_pos)
        medium_btn_hover = medium_rect.collidepoint(mouse_pos)
        hard_btn_hover = hard_rect.collidepoint(mouse_pos)

        draw_button(easy_text, easy_rect.centerx, easy_rect.centery, WHITE, easy_btn_hover)
        draw_button(medium_text, medium_rect.centerx, medium_rect.centery, WHITE, medium_btn_hover)
        draw_button(hard_text, hard_rect.centerx, hard_rect.centery, WHITE, hard_btn_hover)

        # Draw blinking arrow for hovered buttons
        if arrow_visible:
            if easy_btn_hover:
                draw_arrow(easy_rect.left - 15, easy_rect.centery)
            if medium_btn_hover:
                draw_arrow(medium_rect.left - 15, medium_rect.centery)
            if hard_btn_hover:
                draw_arrow(hard_rect.left - 15, hard_rect.centery)

        # Draw "Settings" Button in the Top-Right Corner
        settings_text = font.render("SETTINGS", True, WHITE)
        settings_rect = settings_text.get_rect(topright=(WIDTH - 20, 20))
        screen.blit(settings_text, settings_rect)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    start_game_screen()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if easy_btn_hover:
                    pygame.mixer.music.stop()
                    return 3, 5  # Easy mode
                if medium_btn_hover:
                    pygame.mixer.music.stop()
                    return 5, 7  # Medium mode
                if hard_btn_hover:
                    pygame.mixer.music.stop()
                    return 7, 10  # Hard mode
                if settings_rect.collidepoint(event.pos):
                    button_sound.play()
                    settings_screen()

# Music Volume Variable
music_volume = 0.5  # Default volume (50%)

def settings_screen():
    global music_volume

    # Load the background animation frames for the settings screen
    background_frames = [
        pygame.image.load(f"Graphics/BACKG2/a{i}.png") for i in range(1, 35)
    ]
    background_frames = [pygame.transform.scale(frame, (WIDTH, HEIGHT)) for frame in background_frames]

    # Animation variables
    bg_frame_index = 0
    bg_animation_speed = 100  # Milliseconds per frame
    last_bg_animation_time = pygame.time.get_ticks()

    # Slider variables
    slider_x = WIDTH // 2 - 100
    slider_y = HEIGHT // 2
    slider_width = 200
    slider_height = 10
    slider_handle_radius = 10
    slider_handle_x = slider_x + int(music_volume * slider_width)
    is_dragging = False  # Flag to track if the slider handle is being dragged

    while True:
        # Handle background animation timing
        current_time = pygame.time.get_ticks()
        if current_time - last_bg_animation_time > bg_animation_speed:
            bg_frame_index = (bg_frame_index + 1) % len(background_frames)
            last_bg_animation_time = current_time

        # Draw the current background frame
        screen.blit(background_frames[bg_frame_index], (0, 0))

        # Render "Settings" Title
        settings_title = font.render("SETTINGS", True, WHITE)
        settings_title_rect = settings_title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
        screen.blit(settings_title, settings_title_rect)

        # Draw the slider bar with a border and rounded corners
        pygame.draw.rect(screen, WHITE, (slider_x - 2, slider_y - 2, slider_width + 4, slider_height + 4), border_radius=slider_height // 2)
        pygame.draw.rect(screen, GRAY, (slider_x, slider_y, slider_width, slider_height), border_radius=slider_height // 2)
        pygame.draw.circle(screen, WHITE, (slider_handle_x, slider_y + slider_height // 2), slider_handle_radius)  # Handle

        # Render "Music Volume" Text
        volume_text = font.render(f"Music Volume: {int(music_volume * 100)}%", True, WHITE)
        volume_text_rect = volume_text.get_rect(center=(WIDTH // 2, slider_y - 30))
        screen.blit(volume_text, volume_text_rect)

        pygame.display.update()

        # Handle Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the mouse is on the slider handle
                if (slider_handle_x - slider_handle_radius <= event.pos[0] <= slider_handle_x + slider_handle_radius and
                        slider_y - slider_handle_radius <= event.pos[1] <= slider_y + slider_height + slider_handle_radius):
                    is_dragging = True  # Start dragging
            if event.type == pygame.MOUSEBUTTONUP:
                is_dragging = False  # Stop dragging
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Press ESC to go back to the start screen
                    return

        # Adjust the slider handle position while dragging
        if is_dragging:
            mouse_x = pygame.mouse.get_pos()[0]
            slider_handle_x = max(slider_x, min(mouse_x, slider_x + slider_width))  # Clamp the handle within the slider bar
            music_volume = (slider_handle_x - slider_x) / slider_width  # Calculate volume (0.0 to 1.0)
            pygame.mixer.music.set_volume(music_volume)  # Adjust music volume

def new_settings_screen():
    # Load background animation frames from BACKG4 (o1.png to o24.png)
    background_frames = [pygame.image.load(f"Graphics/BACKG4/o{i}.png") for i in range(1, 25)]
    background_frames = [pygame.transform.scale(frame, (WIDTH, HEIGHT)) for frame in background_frames]
    
    bg_frame_index = 0
    bg_animation_speed = 100  # milliseconds per frame
    last_bg_animation_time = pygame.time.get_ticks()
    
    # Slider (Music Volume) variables
    slider_x = WIDTH // 2 - 100
    slider_y = HEIGHT // 2 - 50
    slider_width = 200
    slider_height = 10
    slider_handle_radius = 10
    slider_handle_x = slider_x + int(pygame.mixer.music.get_volume() * slider_width)
    is_dragging = False
    
    # Create RESUME button
    resume_text = font.render("RESUME", True, WHITE)
    resume_rect = resume_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
    
    while True:
        current_time = pygame.time.get_ticks()
        if current_time - last_bg_animation_time > bg_animation_speed:
            bg_frame_index = (bg_frame_index + 1) % len(background_frames)
            last_bg_animation_time = current_time
        
        # Draw animated background
        screen.blit(background_frames[bg_frame_index], (0, 0))
        
        # Draw Music Volume Slider
        pygame.draw.rect(screen, WHITE, (slider_x - 2, slider_y - 2, slider_width + 4, slider_height + 4), border_radius=slider_height//2)
        pygame.draw.rect(screen, GRAY, (slider_x, slider_y, slider_width, slider_height), border_radius=slider_height//2)
        pygame.draw.circle(screen, WHITE, (slider_handle_x, slider_y + slider_height//2), slider_handle_radius)
        
        # Render Music Volume label
        volume_label = font.render("MUSIC VOLUME", True, WHITE)
        volume_label_rect = volume_label.get_rect(center=(WIDTH // 2, slider_y - 30))
        screen.blit(volume_label, volume_label_rect)
        
        # Draw RESUME button
        pygame.draw.rect(screen, GRAY, resume_rect.inflate(20, 10))
        screen.blit(resume_text, resume_rect)
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # If slider handle is clicked, start dragging
                    if (slider_handle_x - slider_handle_radius <= event.pos[0] <= slider_handle_x + slider_handle_radius and
                        slider_y - slider_handle_radius <= event.pos[1] <= slider_y + slider_height + slider_handle_radius):
                        is_dragging = True
                    # Check if RESUME is clicked: exit settings to return to gameplay
                    if resume_rect.collidepoint(event.pos):
                        button_sound.play()
                        return
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    is_dragging = False
            if event.type == pygame.MOUSEMOTION and is_dragging:
                mouse_x = event.pos[0]
                slider_handle_x = max(slider_x, min(mouse_x, slider_x + slider_width))
                volume = (slider_handle_x - slider_x) / slider_width
                pygame.mixer.music.set_volume(volume)
                    
        clock.tick(30)

def start_game_screen():
    # Load the background animation frames
    background_frames = [
        pygame.image.load(f"Graphics/BackG/b{i}.png") for i in range(1, 47)
    ]
    background_frames = [pygame.transform.scale(frame, (WIDTH, HEIGHT)) for frame in background_frames]
    title_font = pygame.font.Font("Graphics/Font/monogram.ttf", 96)  # Increase font size for bold effect

    # Animation variables
    bg_frame_index = 0
    bg_animation_speed = 100  # Milliseconds per frame
    last_bg_animation_time = pygame.time.get_ticks()

    # Arrow blinking animation variables
    arrow_visible = True
    arrow_blink_speed = 500  # Milliseconds
    last_arrow_blink_time = pygame.time.get_ticks()

    # Play background music only if it's not already playing
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.load("Graphics/Music/SoundM.mp3")  # Load the background music
        pygame.mixer.music.play(-1)  # Play the music in a loop

    while True:
        # Handle background animation timing
        current_time = pygame.time.get_ticks()
        if current_time - last_bg_animation_time > bg_animation_speed:
            bg_frame_index = (bg_frame_index + 1) % len(background_frames)
            last_bg_animation_time = current_time

        # Handle arrow blinking animation timing
        if current_time - last_arrow_blink_time > arrow_blink_speed:
            arrow_visible = not arrow_visible
            last_arrow_blink_time = current_time

        # Draw the current background frame
        screen.blit(background_frames[bg_frame_index], (0, 0))

        # Render "Space Invaders" Title
        title_text = title_font.render("SPACE INVADERS", True, WHITE)
        title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2.5))
        screen.blit(title_text, title_rect)

        # Render "Play" Text
        play_text = font.render("PLAY", True, WHITE)
        play_text_rect = play_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(play_text, play_text_rect)

        # Render "Settings" Text
        settings_text = font.render("SETTINGS", True, WHITE)
        settings_text_rect = settings_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40))
        screen.blit(settings_text, settings_text_rect)

        # Render "Exit" Text
        exit_text = font.render("EXIT", True, WHITE)
        exit_text_rect = exit_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 80))
        screen.blit(exit_text, exit_text_rect)

        # Draw a small arrow on the left side pointing to the right for "Play"
        mouse_pos = pygame.mouse.get_pos()
        if play_text_rect.collidepoint(mouse_pos) and arrow_visible:
            arrow_points = [
                (play_text_rect.left - 20, play_text_rect.centery),      # Tip
                (play_text_rect.left - 30, play_text_rect.centery - 5),  # Top point
                (play_text_rect.left - 30, play_text_rect.centery + 5)   # Bottom point
            ]
            pygame.draw.polygon(screen, WHITE, arrow_points)  # Draw the arrow

        # Draw a small arrow on the left side pointing to the right for "Settings"
        if settings_text_rect.collidepoint(mouse_pos) and arrow_visible:
            arrow_points = [
                (settings_text_rect.left - 20, settings_text_rect.centery),      # Tip
                (settings_text_rect.left - 30, settings_text_rect.centery - 5),  # Top point
                (settings_text_rect.left - 30, settings_text_rect.centery + 5)   # Bottom point
            ]
            pygame.draw.polygon(screen, WHITE, arrow_points)  # Draw the arrow

        # Draw a small arrow on the left side pointing to the right for "Exit"
        if exit_text_rect.collidepoint(mouse_pos) and arrow_visible:
            arrow_points = [
                (exit_text_rect.left - 20, exit_text_rect.centery),      # Tip
                (exit_text_rect.left - 30, exit_text_rect.centery - 5),  # Top point
                (exit_text_rect.left - 30, exit_text_rect.centery + 5)   # Bottom point
            ]
            pygame.draw.polygon(screen, WHITE, arrow_points)  # Draw the arrow

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_text_rect.collidepoint(event.pos):
                    button_sound.play()  # Play button sound
                    return  # Exit the start screen and proceed to difficulty selection
                if settings_text_rect.collidepoint(event.pos):
                    button_sound.play()  # Play button sound
                    settings_screen()  # Open the settings screen
                if exit_text_rect.collidepoint(event.pos):
                    button_sound.play()  # Play button sound
                    pygame.quit()  # Exit the game
                    exit()

def in_game_settings_screen():
    import sys, os
    # Load background animation frames (reuse BACKG4 frames)
    background_frames = [pygame.image.load(f"Graphics/BACKG4/o{i}.png") for i in range(1, 25)]
    background_frames = [pygame.transform.scale(frame, (WIDTH, HEIGHT)) for frame in background_frames]
    
    bg_frame_index = 0
    bg_animation_speed = 100  # milliseconds per frame
    last_bg_animation_time = pygame.time.get_ticks()
    
    # Slider (Music Volume) variables
    slider_x = WIDTH // 2 - 100
    slider_y = HEIGHT // 2 - 50
    slider_width = 200
    slider_height = 10
    slider_handle_radius = 10
    slider_handle_x = slider_x + int(pygame.mixer.music.get_volume() * slider_width)
    is_dragging = False
    
    # Create RESUME and HOME buttons (rendered without a solid background)
    resume_text = font.render("RESUME", True, WHITE)
    resume_rect = resume_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
    home_text = font.render("HOME", True, WHITE)
    home_rect = home_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 80))
    
    arrow_blink_speed = 500  # milliseconds
    last_arrow_blink_time = pygame.time.get_ticks()
    arrow_visible = True

    while True:
        current_time = pygame.time.get_ticks()
        if current_time - last_bg_animation_time > bg_animation_speed:
            bg_frame_index = (bg_frame_index + 1) % len(background_frames)
            last_bg_animation_time = current_time

        if current_time - last_arrow_blink_time > arrow_blink_speed:
            arrow_visible = not arrow_visible
            last_arrow_blink_time = current_time
        
        # Draw animated background
        screen.blit(background_frames[bg_frame_index], (0, 0))
        
        # Draw slider outline and handle (removed grey fill for transparency)
        pygame.draw.rect(screen, WHITE, (slider_x - 2, slider_y - 2, slider_width + 4, slider_height + 4), border_radius=slider_height//2)
        # Do not fill the slider; this keeps it transparent
        pygame.draw.circle(screen, WHITE, (slider_handle_x, slider_y + slider_height//2), slider_handle_radius)
        
        # Render Music Volume label
        volume_label = font.render(f"MUSIC VOLUME: {int(pygame.mixer.music.get_volume()*100)}%", True, WHITE)
        volume_label_rect = volume_label.get_rect(center=(WIDTH//2, slider_y - 30))
        screen.blit(volume_label, volume_label_rect)
        
        # Draw only the button texts (no background rectangles)
        screen.blit(resume_text, resume_rect)
        screen.blit(home_text, home_rect)
        
        # Blinking arrow for hovered buttons
        mouse_pos = pygame.mouse.get_pos()
        if arrow_visible:
            if resume_rect.collidepoint(mouse_pos):
                draw_arrow(resume_rect.left - 15, resume_rect.centery)
            if home_rect.collidepoint(mouse_pos):
                draw_arrow(home_rect.left - 15, home_rect.centery)

        pygame.display.update()
        
        # Handle events for in-game settings
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # Start dragging slider if clicked on slider handle
                    if (slider_handle_x - slider_handle_radius <= event.pos[0] <= slider_handle_x + slider_handle_radius and
                        slider_y - slider_handle_radius <= event.pos[1] <= slider_y + slider_height + slider_handle_radius):
                        is_dragging = True
                    # Click on RESUME: exit settings overlay
                    if resume_rect.collidepoint(event.pos):
                        button_sound.play()
                        return
                    # Click on HOME: reset the game (restart the script)
                    if home_rect.collidepoint(event.pos):
                        button_sound.play()
                        os.execl(sys.executable, sys.executable, *sys.argv)
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    is_dragging = False
            if event.type == pygame.MOUSEMOTION and is_dragging:
                mouse_x = event.pos[0]
                slider_handle_x = max(slider_x, min(mouse_x, slider_x + slider_width))
                volume = (slider_handle_x - slider_x) / slider_width
                pygame.mixer.music.set_volume(volume)
        
        clock.tick(30)

enemy_direction = 1  # 1 for right, -1 for left
# Call the start game screen before difficulty selection
start_game_screen()
enemy_speed, _ = difficulty_selection()  # Get the speed from the selected difficulty

# Now load gameplay background music with a fixed volume
pygame.mixer.music.load("Graphics/Music/pixel.mp3")
pygame.mixer.music.set_volume(0.5)  # Fixed gameplay music volume
pygame.mixer.music.play(-1)

rows = 5  # Fixed number of rows
cols = 11  # Fixed number of columns
enemies = create_enemies(rows, cols, enemy_speed)

# Load Background Animation Frames for gameplay from GAMEBACK folder (q1.png to q32.png)
bg_frames = [pygame.image.load(f"Graphics/GAMEBACK/q{i}.png") for i in range(1, 33)]
bg_frames = [pygame.transform.scale(frame, (WIDTH, HEIGHT)) for frame in bg_frames]
bg_animation_speed = 100  # Milliseconds per frame
last_bg_animation_time = pygame.time.get_ticks()
bg_frame_index = 0

# Game Loop
running = True

def draw_player(x, y):
    global player_frame_index, last_animation_time

    # Handle Animation Timing
    current_time = pygame.time.get_ticks()
    if current_time - last_animation_time > animation_speed:
        player_frame_index = (player_frame_index + 1) % len(player_frames)
        last_animation_time = current_time

    # Draw Current Frame
    screen.blit(player_frames[player_frame_index], (x, y))

def draw_enemy(x, y):
    screen.blit(enemy_img, (x, y))

def fire_bullet(x, y):
    global can_shoot, last_shot_time
    current_time = pygame.time.get_ticks()
    if can_shoot and current_time - last_shot_time > shoot_cooldown:
        # Center the bullet relative to the player's position
        bullet_x = x + (89 // 2) - (20 // 2)  # Player width: 90, Bullet width: 20
        bullet_y = y - 20  # Move the bullet slightly upward (adjusted by -20)
        bullets.append([bullet_x, bullet_y])
        last_shot_time = current_time
        laser_shot.play()  # Play the laser shot sound

def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt((enemy_x - bullet_x) ** 2 + (enemy_y - bullet_y) ** 2)
    return distance < 27

def is_player_collision(player_x, player_y, enemy_x, enemy_y):
    # Check if the distance between the player and the enemy is less than a threshold
    distance = math.sqrt((player_x - enemy_x) ** 2 + (player_y - enemy_y) ** 2)
    return distance < 50  # Adjust the threshold based on the size of the player and enemy

def game_over():
    screen.fill(BLACK)
    game_over_text = font.render("GAME OVER", True, WHITE)
    text_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(game_over_text, text_rect)
    pygame.display.update()
    pygame.time.delay(2000)
    pygame.quit()
    exit()

def increase_difficulty():
    global enemy_speed, enemies, level
    # Only increase difficulty if the maximum level hasn't been reached.
    if level >= 5:
        return
    enemy_speed += 1
    level += 1
    # Adjust enemy rows (for example, new row count could be level + 2) 
    rows = level + 2  
    cols = 11  # you can keep or adjust the number of columns as needed
    enemies = create_enemies(rows, cols, enemy_speed)

def display_score_and_level():
    # Render Shadow for Score Text
    shadow_color = (50, 50, 50)  # Dark gray for shadow
    shadow_offset = 2  # Offset for the shadow
    score_shadow_text = font.render(f"Score: {score}", True, shadow_color)
    score_shadow_rect = score_shadow_text.get_rect(center=(WIDTH // 2 + shadow_offset, 20 + shadow_offset))
    screen.blit(score_shadow_text, score_shadow_rect)

    # Render Score Text
    score_text = font.render(f"Score: {score}", True, WHITE)
    score_rect = score_text.get_rect(center=(WIDTH // 2, 20))
    screen.blit(score_text, score_rect)

    # Render Shadow for Level Text
    level_shadow_text = font.render(f"Level: {level}", True, shadow_color)
    screen.blit(level_shadow_text, (10 + shadow_offset, 10 + shadow_offset))

    # Render Level Text
    level_text = font.render(f"Level: {level}", True, WHITE)
    screen.blit(level_text, (10, 10))

while running:
    current_time = pygame.time.get_ticks()
    if current_time - last_bg_animation_time > bg_animation_speed:
        bg_frame_index = (bg_frame_index + 1) % len(bg_frames)
        last_bg_animation_time = current_time

    # Draw the animated background
    screen.blit(bg_frames[bg_frame_index], (0, 0))

    # Darken the background with a semi-transparent overlay
    dark_overlay = pygame.Surface((WIDTH, HEIGHT))
    dark_overlay.fill((0, 0, 0))
    dark_overlay.set_alpha(100)  # Adjust alpha value for darkness (0 is transparent, 255 is fully black)
    screen.blit(dark_overlay, (0, 0))

    # Draw in-game SETTINGS button (top-right corner)
    in_game_settings_text = font.render("SETTINGS", True, WHITE)
    in_game_settings_rect = in_game_settings_text.get_rect(topright=(WIDTH - 20, 20))
    screen.blit(in_game_settings_text, in_game_settings_rect)
    
    # Event Handling (including checking for in-game settings button click)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and in_game_settings_rect.collidepoint(event.pos):
                button_sound.play()
                in_game_settings_screen()
        # ...existing event handling...

    # Get Player Input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 70:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - 190:
        player_x += player_speed
    if keys[pygame.K_SPACE]:
        fire_bullet(player_x, player_y)

    # Move Enemies and process game logic
    enemy_move_down = False
    for enemy in enemies:
        enemy[0] += enemy_direction * enemy_speed
        # Check if any enemy hits the screen edges
        if enemy[0] <= 80 or enemy[0] >= WIDTH - 140:  # Adjusted to add a buffer (10 pixels on the left, 80 pixels on the right)
            enemy_direction *= -1  # Reverse direction
            enemy_move_down = True  # Move enemies down
            break

    # Move enemies down if needed
    if enemy_move_down:
        for enemy in enemies:
            enemy[1] += 30  # Adjusted to move enemies down by 50 pixels

    # Check for collision between player and enemies
    for enemy in enemies:
        if is_player_collision(player_x, player_y, enemy[0], enemy[1]):
            game_over()  # End the game if a collision is detected

    # Draw Enemies
    for enemy in enemies:
        draw_enemy(enemy[0], enemy[1])

    # Move Bullets
    current_time = pygame.time.get_ticks()

    # Handle bullet animation timing
    if current_time - last_bullet_animation_time > bullet_animation_speed:
        bullet_frame_index = (bullet_frame_index + 1) % len(bullet_frames)
        last_bullet_animation_time = current_time

    # Move Bullets
    for bullet in bullets[:]:  # Iterate over a copy of the bullets list
        bullet[1] -= bullet_speed
        # Draw the current bullet animation frame
        screen.blit(bullet_frames[bullet_frame_index], (bullet[0], bullet[1]))
        
        # Remove the bullet if it goes out of bounds
        if bullet[1] < 0:
            bullets.remove(bullet)
            continue  # Skip further checks for this bullet

        # Check for collision with enemies
        for enemy in enemies[:]:  # Iterate over a copy of the enemies list
            if is_collision(enemy[0], enemy[1], bullet[0], bullet[1]):
                if bullet in bullets:  # Ensure the bullet is still in the list
                    bullets.remove(bullet)
                enemyD.play()  # Play enemy death sound
                enemies.remove(enemy)
                score += 50  # Add points for destroying an enemy
                break  # Exit the loop after handling the collision

    # Game Over Condition: If enemy reaches bottom
    for enemy in enemies:
        if enemy[1] > HEIGHT - 80:
            game_over()
    
    # Check if all enemies are defeated and process level up
    if not enemies:
        if level < 5:
            increase_difficulty()
        else:
            # Maximum level reached; display win message and end the game
            win_text = font.render("YOU WIN!", True, WHITE)
            win_rect = win_text.get_rect(center=(WIDTH//2, HEIGHT//2))
            screen.fill(BLACK)
            screen.blit(win_text, win_rect)
            pygame.display.update()
            pygame.time.delay(3000)
            pygame.quit()
            exit()

    # Draw Player
    draw_player(player_x, player_y)

    # Display Score and Level
    display_score_and_level()

    pygame.display.update()
    clock.tick(30)

pygame.quit()