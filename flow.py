"""
Flow - avoid the traffic flow and cross the road.
"""
import random


WIDTH = 800
HEIGHT = 600
SPEED = 6  # Change in pixels per frame.

music.play('street_ambience1')

# The top of each "row" (pavement / road) on the screen.
rows = [56, 120, 184, 248, 312, 376, 440, 504, 568]

# Configure the hero at the bottom/middle of the screen.
player = Actor("hero1")
player.row = 8
player.frame = 1
player.pos = (368, rows[player.row])
moving = False  # A flag to show if the player is moving.

# Defines the available vehicles.
vehicles = [
    {
        'image': 'motorbike',
        'top': [1, 2, 3, ],
        'bottom': [5, 6, 7, ]
    },
    {
        'image': 'bike',
        'top': [1, 2, 3, ],
        'bottom': [5, 6, 7, ]
    },
    {
        'image': 'car',
        'top': [1, 2, ],
        'bottom': [5, 6, ]
    },
    {
        'image': 'taxi',
        'top': [1, 2, ],
        'bottom': [5, 6, ]
    },
    {
        'image': 'bus',
        'top': [1, 2, ],
        'bottom': [5, 6, ]
    },
    {
        'image': 'lorry',
        'top': [1, 2, ],
        'bottom': [5, 6, ]
    }
]


# Holds all the current traffic.
traffic = []

# Holds all the current zombies.
zombies = []
max_zombies = 3  # Max number of zombies on the screen at any one time.

def draw():
    """
    Draw the current state of the game onto the screen.
    """
    screen.blit('background', (0, 0))
    player.draw()
    for vehicle in traffic:
        vehicle.draw()
    for zombie in zombies:
        zombie.draw()

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
    if moving:
        player.image = 'hero{}'.format(player.frame)
        player.frame += 1
        if player.frame == 4:
            player.frame = 2
        clock.schedule_unique(animate_player, 0.03)
    else:
        player.image = 'hero1'
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
    
def update():
    """
    Update game state,
    """
    x, y = player.pos
    if not moving:
        # If the player isn't already moving.
        # Check the keyboard presses from the player.
        if keyboard[keys.UP]:
            player.row = max(0, player.row - 1)
            move_player(x, rows[player.row])
            if player.row == 0:
                # You've got to the top. WIN!
                print("You made it!")
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
    for vehicle in traffic:
        if vehicle.lane == 'top':
            vehicle.left += SPEED
            if vehicle.left > WIDTH:
                finished_traffic.append(vehicle)
            else:
                distance_top = min(vehicle.left, distance_top)
        else:
            vehicle.left -= SPEED
            if vehicle.right < 0:
                finished_traffic.append(vehicle)
            else:
                distance_bottom = max(vehicle.right, distance_bottom)
        if player.colliderect(vehicle):
            # Hit by traffic!
            player.image = 'splat'
            print("DEAD!")
    # Remove all the traffic that is now off the screen.
    for old_vehicle in finished_traffic:
        traffic.remove(old_vehicle)
    # Add more traffic
    chance_to_add_top = random.randint(0, 1000) > 950 
    chance_to_add_bottom = random.randint(0, 1000) > 950 
    if distance_top > 194 and chance_to_add_top:
        make_traffic('top')
    if distance_bottom < (WIDTH - 194) and chance_to_add_bottom:
        make_traffic('bottom')
    # Handle Zombies
    finished_zombies = []
    for zombie in zombies:
        if zombie.direction == 'l':
            zombie.right += SPEED // 4
            if zombie.left > WIDTH:
                finished_zombies.append(zombie)
        else:
            zombie.left -= SPEED // 4
            if zombie.right < 0:
                finished_zombies.append(zombie)
        if player.colliderect(zombie):
            player.image = 'splat'
    # Remove old Zombies
    for old_zombie in finished_zombies:
        zombies.remove(old_zombie)
    if random.randint(1, 100) == 99:
        make_zombie(random.choice(['middle', 'bottom']))

def make_traffic(lane='top'):
    """
    Create a vehicle to appear in the traffic.
    """
    global traffic
    vehicle = random.choice(vehicles)
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
    traffic.append(new_car)

def make_zombie(pavement='bottom'):
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