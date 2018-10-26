"""
Flow - avoid the traffic flow and cross the road.
"""
import random


WIDTH = 800
HEIGHT = 600
music.play('street_ambience1')

# The top of each "row" (pavement / road) on the screen.
rows = [56, 120, 184, 248, 312, 376, 440, 504, 568]

# Configure the hero at the bottom/middle of the screen.
player = Actor("hero1")
player.row = 8
player.frame = 1
player.lives = 3
player.pos = (368, rows[player.row])
moving = False  # A flag to show if the player is moving.

# Define the attributes of the different levels.
levels = [
    {
        'speed': 6,
        'vehicles': ['bike', ],
        'max_zombies': 1,
        'ambience': 'park',
        'swerve': 0,
    },
    {
        'speed': 8,
        'vehicles': ['bike', 'car', 'motorbike', 'taxi', ],
        'max_zombies': 1,
        'ambience': 'park',
        'swerve': 0,
    },
    {
        'speed': 8,
        'vehicles': ['bike', 'car', 'motorbike', 'taxi', 'bus', 'lorry', ],
        'max_zombies': 2,
        'ambience': 'road',
        'swerve': 1,
    },
    {
        'speed': 10,
        'vehicles': ['bike', 'car', 'motorbike', 'taxi', 'bus', 'lorry', ],
        'max_zombies': 4,
        'ambience': 'road',
        'swerve': 2,
    },
    {
        'speed': 10,
        'vehicles': ['bike', 'car', 'motorbike', 'taxi', 'bus', 'lorry', ],
        'max_zombies': 6,
        'ambience': 'road',
        'swerve': 4,
    },
]

# Defines the available vehicles.
vehicles = {
    'motorbike': {
        'image': 'motorbike',  # Name of sprite.
        'top': [1, 2, 3, ],  # Top rows available to fill.
        'bottom': [5, 6, 7, ]  # Bottom rows available to fill.
    },
    'bike': {
        'image': 'bike',
        'top': [1, 2, 3, ],
        'bottom': [5, 6, 7, ]
    },
    'car': {
        'image': 'car',
        'top': [1, 2, ],
        'bottom': [5, 6, ]
    },
    'taxi': {
        'image': 'taxi',
        'top': [1, 2, ],
        'bottom': [5, 6, ]
    },
    'bus': {
        'image': 'bus',
        'top': [1, 2, ],
        'bottom': [5, 6, ]
    },
    'lorry': {
        'image': 'lorry',
        'top': [1, 2, ],
        'bottom': [5, 6, ]
    }
}

# Holds all the current traffic.
traffic = []

# Holds all the current zombies.
zombies = []

# Current game state. Can be one of the following:
# start, finished, level, next, dead, failed.
state = 'start'  
level_number = 0  # Current level number.

def draw():
    """
    Draw the current state of the game onto the screen for each frame
    of the game. Checks which state the game is in, in order to draw
    the correct image.
    """
    if state == 'start':
        # Show the instructions.
        screen.blit('instructions', (0, 0))
    elif state == 'finished':
        # Show the "You Won!" image.
        screen.blit('finished', (0, 0))
    else:
        # The player is in a level...
        screen.blit('background', (0, 0))  # show the road.
        # Draw the number of lives and current level.
        screen.draw.text('LIVES: {}'.format(player.lives), (32, 560),
                         fontname='zombie', fontsize=16,
                         color=(0, 0, 255), background='None')
        screen.draw.text('LEVEL: {}/5'.format(level_number + 1), (600, 560),
                         fontname='zombie', fontsize=16,
                         color=(0, 0, 255), background='None')
        # Draw the current sprite for the player, vehicles and zombies.
        player.draw()
        for vehicle in traffic:
            vehicle.draw()
        for zombie in zombies:
            zombie.draw()
        # If the state requires text on the screen, draw it!
        if state == 'next':
            screen.draw.text('YOU MADE IT', (170, 200),
                             fontname='zombie', fontsize=56,
                             color=(0, 0, 255), background='None')
            screen.draw.text('PRESS SPACE FOR NEXT LEVEL', (90, 300),
                             fontname='zombie', fontsize=32,
                             color=(0, 0, 255), background='None')
        elif state == 'dead':
            # display that the user is dead.
            screen.draw.text('YOU ARE DEAD', (150, 200),
                             fontname='zombie', fontsize=56,
                             color=(255, 0, 0), background='None')
            screen.draw.text('PRESS SPACE TO TRY AGAIN', (130, 300),
                             fontname='zombie', fontsize=32,
                             color=(255, 0, 0), background='None')
        elif state == 'failed':
            # display that the user is dead.
            screen.draw.text('YOU FAILED', (180, 200),
                             fontname='zombie', fontsize=56,
                             color=(255, 0, 0), background='None')
            screen.draw.text('PRESS ENTER TO START AGAIN', (100, 300),
                             fontname='zombie', fontsize=32,
                             color=(255, 0, 0), background='None')
            
def update():
    """
    Update the game state given user generated and in-game events.
    """
    # A bunch of global flags and states.
    global state
    global level_number
    global player
    global zombies
    global traffic
    # No lives left? You've failed.
    if player.lives < 1:
        player.lives = 0
        state = 'failed'
    if state == 'start':
        # In start state, wait to press space bar before starting level 1.
        if keyboard[keys.SPACE]:
            state = 'level'
            # Reset a bunch of state.
            level_number = 0
            player.row = 8
            player.frame = 1
            player.image = 'hero1'
            player.lives = 3
            zombies = []
            traffic = []
            player.pos = (368, rows[player.row])
    elif state == 'next':
        # Level completed OK. Next state.
        update_level()
        if keyboard[keys.SPACE]:
            state = 'level'
            level_number += 1
            if level_number == 5:
                # No more levels, so they've won!
                state = 'finished'
            # Reset player and zombies for new level.
            player.row = 8
            player.frame = 1
            player.image = 'hero1'
            zombies = []
            player.pos = (368, rows[player.row])
    elif state == 'failed':
        # Run out of lives. FAIL!
        update_level()
        if keyboard[keys.RETURN]:
            # Wait for return before returning to start state.
            level_number = 0
            state = 'start'
            player.row = 8
            player.frame = 1
            player.image = 'hero1'
            player.lives = 3
            zombies = []
            traffic = []
            player.pos = (368, rows[player.row])
    elif state == 'finished':
        # Player has won the game.
        if keyboard[keys.RETURN]:
            # Wait for return to go back to start.
            state = 'start'
    elif state == 'dead':
        # Player has lost a life.
        update_level()
        if keyboard[keys.SPACE]:
            # Start current level again.
            state = 'level'
            player.row = 8
            player.frame = 1
            player.image = 'hero1'
            player.lives -= 1  # deduct a life.
            zombies = []
            traffic = []
            player.pos = (368, rows[player.row])
    else:
        # Update the level.
        update_level()

def move_player(x, y):
    """
    Animate a move of the player to the x, y coordinates.
    """
    global moving 
    moving = True
    animate(player, pos=(x, y), 
            duration=0.1, tween='accelerate')
    player.image = 'hero2'
    clock.schedule_unique(animate_player, 0.03)
    clock.schedule_unique(stop_move_player, 0.1)
    
def animate_player():
    """
    If the player is currently moving, cycle through walking
    sprites for animation effect.
    """
    if moving:
        player.image = 'hero{}'.format(player.frame)
        player.frame += 1
        if player.frame == 4:
            player.frame = 2
        # Schedule the next frame...
        clock.schedule_unique(animate_player, 0.03)
    else:
        # No more movement, so stand still.
        player.image = 'hero1'
    # Reset angle (needed because of a bug in PyGameZero).
    player.angle = player.angle

def stop_move_player():
    """
    Called when the player has stopped moving. Right now,
    just flips the flag so keyboard input is read.
    """
    global moving 
    moving = False
    
def animate_zombies():
    """
    Updates animations of any existing Zombies.
    """
    for zombie in zombies:
        zombie.frame += 1
        if zombie.frame == 5:
            zombie.frame = 1
        zombie.image = 'zombie{}'.format(zombie.frame)
        zombie.angle = zombie.angle
    clock.schedule_unique(animate_zombies, 0.4)
    
def update_level():
    """
    Update game state for when a player is on a level.
    """
    global state
    global level_number
    level = levels[level_number]  # Get the current level.
    x, y = player.pos  # Get the current player position.
    if state == 'dead':
        player.image = 'splat'
    elif state == 'next' or state == 'failed':
        pass  # do nothing.
    elif not moving:
        # If the player isn't already moving.
        # Check the keyboard presses from the player.
        if keyboard[keys.UP]:
            player.row = max(0, player.row - 1)
            move_player(x, rows[player.row])
            if player.row == 0:
                # You've got to the top. WIN!
                state = "next"
            player.angle = 0
        if keyboard[keys.DOWN]:
            player.row = min(8, player.row + 1)
            move_player(x, rows[player.row])
            player.angle = 180
        if keyboard[keys.LEFT]:
            move_player(max(x - 64, 0), y)
            player.angle = 90
        if keyboard[keys.RIGHT]:
            move_player(min(x + 64, 800), y)
            player.angle = 270
    # Update the position of traffic.
    finished_traffic = []
    # Flags to indicate if it's possible to add a vehicle to
    # the traffic lanes.
    distance_top = WIDTH
    distance_bottom = 0
    # Update state of vehicles.
    for vehicle in traffic:
        # Vehicle swerve factor.
        if vehicle.swerve:
            if random.choice([True, False]):
                vehicle.top += vehicle.swerve
            else:
                vehicle.top -= vehicle.swerve
        if vehicle.lane == 'top':
            # Vehicles in the top lanes.
            vehicle.left += level['speed']
            if vehicle.left > WIDTH:
                finished_traffic.append(vehicle)
            else:
                distance_top = min(vehicle.left, distance_top)
        else:
            # Vehicles in the bottom lanes.
            vehicle.left -= level['speed']
            if vehicle.right < 0:
                finished_traffic.append(vehicle)
            else:
                distance_bottom = max(vehicle.right, distance_bottom)
        if player.colliderect(vehicle):
            # Hit by traffic!
            if state != 'failed':
                state = 'dead'
    # Remove all the traffic that is now off the screen.
    for old_vehicle in finished_traffic:
        traffic.remove(old_vehicle)
    # Add more traffic
    chance_to_add_top = random.randint(0, 1000) > 950 
    chance_to_add_bottom = random.randint(0, 1000) > 950 
    if distance_top > 194 and chance_to_add_top:
        make_traffic('top', level)
    if distance_bottom < (WIDTH - 194) and chance_to_add_bottom:
        make_traffic('bottom', level)
    # Handle Zombies
    finished_zombies = []
    for zombie in zombies:
        if zombie.direction == 'l':
            zombie.right += level['speed'] // 4
            if zombie.left > WIDTH:
                finished_zombies.append(zombie)
        else:
            zombie.left -= level['speed'] // 4
            if zombie.right < 0:
                finished_zombies.append(zombie)
        if player.colliderect(zombie):
            # Killed by zombie
            if state != 'failed':
                state = 'dead'
    # Remove old Zombies
    for old_zombie in finished_zombies:
        zombies.remove(old_zombie)
    # Add fresh Zombies.
    if random.randint(1, 100) == 99:
        make_zombie(random.choice(['middle', 'bottom']), level['max_zombies'])

def make_traffic(lane, level):
    """
    Create a vehicle to appear in the traffic.
    """
    global traffic
    vehicle = vehicles[random.choice(level['vehicles'])]
    new_car = Actor(vehicle['image'])
    if lane == 'top':
        new_car.right = 0
        new_car.angle = 180
        new_car.top = rows[random.choice(vehicle['top'])] - 32
        new_car.lane = lane
    else:
        new_car.left = WIDTH
        new_car.top = rows[random.choice(vehicle['bottom'])] - 32
        new_car.lane = lane
    new_car.swerve = level['swerve']
    traffic.append(new_car)

def make_zombie(pavement, max_zombies):
    """
    Create a Zombie on the bottom or middle pavement.
    """
    global zombies
    direction = random.choice(['l', 'r'])
    if len(zombies) < max_zombies:
        new_zombie = Actor('zombie1')
        new_zombie.direction = direction
        new_zombie.frame = 1
        if pavement == 'bottom':
            new_zombie.top = rows[8] - 32
        else:
            new_zombie.top = rows[4] - 32
        if direction == 'l':
            new_zombie.right = 0
        else:
            new_zombie.left = WIDTH
            new_zombie.angle = 180
        zombies.append(new_zombie)

animate_zombies()