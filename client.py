import pygame
from network import Network
from player import Player
import time
from wall import Wall
from powerup import PowerUp

pygame.init()

# Setting up the window dimensions and title
width = 1000
height = 800
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")
font = pygame.font.Font(None, 36)

# Drawing walls from the txt file
def initialize_walls_from_file(file_name):
    walls = []
    with open(file_name, 'r') as file:
        lines = file.readlines()
        total_lines = len(lines)
        total_characters = len(lines[0].strip())
        wall_width = 1000 // total_characters
        wall_height = (800 - 49) // total_lines  # Subtracting 49 pixels for the exclusion at the top

        for y, line in enumerate(lines):
            for x, char in enumerate(line.strip()):
                if char == '#':  # '#' represents a wall in the file
                    walls.append(Wall(x * wall_width, y * wall_height + 50, wall_width, wall_height))

    return walls

# Call initialize_walls_from_file() to create walls based on the map file
walls = initialize_walls_from_file('map.txt')

def redrawWindow(win, player_id, players, walls, power_ups):
    # Function to redraw the game window

    # Fill the window with white color
    win.fill((255, 255, 255))

    # Drawing a line at the top of the window
    pygame.draw.line(win, (0, 0, 0), (0, 49), (1000, 49))

    # Font setup for displaying player health information
    font = pygame.font.Font(None, 24)

    # Initializing variables to hold player health and eliminated players
    player_health_line = ""
    eliminated_players = []

    for wall in walls:
        wall.draw(win)

    for power_up in power_ups:
        power_up.draw(win)

    # Iterating through the players to display their information
    for i, player in enumerate(players):
        if player.get_health() > 0:
            player.draw(win)  # Drawing the player character
            # Adding player health information to the horizontal line
            player_health_line += f"Player {i + 1} Health: {player.get_health()}            "
        else:
            eliminated_players.append(player)

        # Moving and drawing bullets for each player
        for bullet in player.bullets[:]:
            bullet.move()
            # Removing bullets that are out of the screen bounds
            if not (0 <= bullet.x <= width and 0 <= bullet.y <= height):
                player.bullets.remove(bullet)
            else:
                bullet.draw(win)

        player.update_hitbox()  # Updating player hitbox for collision detection

    # Calculating the center position for the text
    text_width = font.size(player_health_line)[0]
    center_x = (width - text_width) // 2

    # Displaying the player health line centered on the screen with smaller font
    player_health_text = font.render(player_health_line, True, (0, 0, 0))
    win.blit(player_health_text, (center_x, 10))

    bullets_to_remove = []  # Create a list to store bullets to be removed

    for player in players:
        for bullet in player.bullets[:]:
            for other_player in players:
                if other_player != player and other_player.get_health() > 0:
                    # Check for bullet collision with other players' hitbox
                    if (
                        other_player.hitbox[0] + other_player.hitbox[2] > bullet.x > other_player.hitbox[0]
                        and other_player.hitbox[1] + other_player.hitbox[3] > bullet.y > other_player.hitbox[1]
                    ):
                        # If a bullet hits a player, deal damage to the player and remove the bullet
                        bullets_to_remove.append((player, bullet))
                        other_player.hit()  # Reduce the player's health

    # Remove bullets that hit players
    for player, bullet in bullets_to_remove:
        if bullet in player.bullets:
            player.bullets.remove(bullet)

    # Display "X" for eliminated players
    for eliminated_player in eliminated_players:
        if eliminated_player.game_over:
            x_text = font.render("X", True, (255, 0, 0))
            win.blit(
                x_text,
                (eliminated_player.x + eliminated_player.width // 2 - x_text.get_width() // 2,
                 eliminated_player.y - x_text.get_height() - 10)
            )

    # Check for the winning player
    winning_player = None
    for p in players:
        if not p.game_over:
            if winning_player is not None:
                winning_player = None  # More than one player still alive, so no winner yet
                break
            winning_player = p

    if winning_player and player_id == players.index(winning_player):
        # Display which player won
        winning_message = font.render(f"Player {player_id} Won!", True, (128, 128, 128))
        winning_player.victory = True
        #p.victory = True
        win.blit(
            winning_message,
            (width // 2 - winning_message.get_width() // 2, 425)
        )
        
    for player in players:
        player.update_hitbox()  # Update player hitbox
        if player.game_over:
            player.bullets = []  # Remove bullets of eliminated players

    pygame.display.update()  # Update the display to show changes

def main_menu():
    # Function to display the main menu

    # Font setup for menu options
    menu_font = pygame.font.Font(None, 72)
    title_text = menu_font.render("Main Menu", True, (0, 0, 0))
    play_text = menu_font.render("Play Game", True, (0, 0, 0))
    quit_text = menu_font.render("Quit", True, (0, 0, 0))

    while True:
        win.fill((255, 255, 255))  # Clear the window with white color
        # Displaying menu options centered on the screen
        win.blit(title_text, (width // 2 - title_text.get_width() // 2, 100))
        win.blit(play_text, (width // 2 - play_text.get_width() // 2, 300))
        win.blit(quit_text, (width // 2 - quit_text.get_width() // 2, 400))
        pygame.display.update()  # Update the display to show changes

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    x, y = pygame.mouse.get_pos()
                    # Check for mouse click on Play Game or Quit options
                    if width // 2 - play_text.get_width() // 2 <= x <= width // 2 + play_text.get_width() // 2 \
                            and 300 <= y <= 300 + play_text.get_height():
                        return True  # Start the game
                    elif width // 2 - quit_text.get_width() // 2 <= x <= width // 2 + quit_text.get_width() // 2 \
                            and 400 <= y <= 400 + quit_text.get_height():
                        pygame.quit()
                        quit()

# Check how many players have clicked start
def how_many_ready(players):
    ready_num = 0
    for player in players:
        if player.ready:
            ready_num += 1
    return ready_num

def main():
    # Initializing variables and setting up the game
    run = True
    in_game = False
    n = Network()  # Creating a network instance
    clock = pygame.time.Clock()
    players = []  # Initialize an empty list to store player objects
    player_id = None  # Store the current player's ID
    power_ups = []  # Initialize an empty list to store power_up objects
    waiting_displayed = False  # Flag to track if waiting text is displayed

    while run:
        if not in_game:
            # Displaying the main menu and handling player readiness
            ready = main_menu()

            if ready:
                player_id, p = n.getP()  # Get player ID and initial player object from the server
                p.ready = n.send('PLAYER_READY', None)
                n.send('PLAYER_DATA', p)  # Sending the player object to the server
                players = n.send('GET_PLAYERS', None)  # Receiving the list of players from the server

        while not in_game:
            players = n.send('GET_PLAYERS', None)  # Sending the player object and receiving updated player list

            if n.send('READY_CHECK', players) == True: # Check if all players are ready
                print("All players are ready to start the game!")
                n.send('INITIALIZE_POWERUPS', None) # Spawn the powerups
                in_game = True
            else:
                print("Some players are not ready yet!")

                # Display waiting text if not already displayed
                if not waiting_displayed:
                    # Displaying "Waiting for other players" text
                    win.fill((255, 255, 255))  # Clear the screen
                    wait_font = pygame.font.Font(None, 72)
                    wait_text = wait_font.render("Waiting for other players", True, (0, 0, 0))
                    num_ready_text = wait_font.render(f"{how_many_ready(players)}/4 ready", True, (0, 0, 0))
                    win.blit(wait_text, (225, 300))
                    win.blit(num_ready_text, (400, 375))
                    pygame.display.update()
                    waiting_displayed = True  # Set the waiting flag to true
                    
        clock.tick(60)
        n.send('PLAYER_DATA', p) # Sending current client data
        players = n.send('GET_PLAYERS', None)  # updated player information
        p = players[player_id]  # Getting the current player object from the list of players
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if in_game:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        # Handling mouse click for shooting bullets
                        target_x, target_y = pygame.mouse.get_pos()
                        p.shoot(target_x, target_y)  # Shooting a bullet towards the clicked position
                if event.type == pygame.USEREVENT:
                    p.vel = 3  # Restore the player's original speed after the boost duration
            

        if in_game:
            # Getting the current player object from the list of players
            player_id, p = n.getP()
            p = players[player_id]  # Updating the current player object

            p.move(walls)  # Handling player movement
            n.send('PLAYER_DATA', p)
            power_ups = n.send('GET_POWER_UPS', None)

            for power_up in power_ups[:]: # Drawing power ups in game
                power_up.draw(win) 

            for player in players:
                for bullet in player.bullets:
                    bullet.move()  # Moving bullets for each player

            for power_up in power_ups:
                if power_up.check_collision(p):
                    if power_up.type == 'speed_boost':
                        p.vel = 6  # Double the player's speed
                        n.send('PLAYER_COLLECTED_POWER_UP', power_ups.index(power_up))
                        pygame.time.set_timer(pygame.USEREVENT, 5000)  # Set a timer for 5 seconds
                    elif power_up.type == 'triple_shot':
                        p.bullet_burst = True  
                        n.send('PLAYER_COLLECTED_POWER_UP', power_ups.index(power_up))
                    elif power_up.type == 'med_pack':
                        p.health  = 100
                        n.send('PLAYER_COLLECTED_POWER_UP', power_ups.index(power_up))
                    elif power_up.type == 'shield':
                        p.has_shield = True
                        n.send('PLAYER_COLLECTED_POWER_UP', power_ups.index(power_up))

            victory_check = n.send('PLAYER_WON', players) # Checking if a player has won

            if victory_check == True:
                print("Returning to Main Menu")
                time.sleep(5)
                in_game = False
                waiting_displayed = False
                n.send('RESET_GAME_STATE', None)

            # Redrawing the game window with updated information
            redrawWindow(win, player_id, players, walls, power_ups)

    pygame.quit()  # Exiting the pygame environment when the game loop ends

if __name__ == "__main__":
    main()