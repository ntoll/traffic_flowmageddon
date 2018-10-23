"""
Flow - avoid the traffic flow and cross the road.
"""
import random


WIDTH = 800
HEIGHT = 600
SPEED = 6  # Change in pixels per frame.

# The top of each "row" (pavement / road) on the screen.
rows = [56, 120, 184, 248, 312, 376, 440, 504, 568]

# Configure the hero at the bottom/middle of the screen.
player = Actor("hero1")
player.row = 8
player.pos = (368, rows[player.row])
player.frame = 1
moving = False  # A flag to show if the player is moving.

# Defines the available vehicles.
vehicles = [
    {
        'image': 'motorbike',
        'top': [1, 2, 3, ],
        'bottom': [5, 6, 7, ]
    },
    {
        'image': 'car',
        'top': [1, 2, ],
        'bottom': [5, 6, ]
    },
    {
        'image': 'bus',
        'top': [1, 2, ],
        'bottom': [5, 6, ]
    }
]


# Holds all the current traffic.
traffic = []

def draw():
    """
    Draw the current state of the game onto the screen.
    """
    screen.blit('background', (0, 0))
    player.draw()
    for vehicle in traffic:
        vehicle.draw()

def move_player(x, y):
    """
    Animate a move of the player to the x, y coordinates.
    """
    global moving 
    moving = True
    animate(player, pos=(x, y), 
            duration=0.5, tween='accelerate')
    clock.schedule_unique(animate_player, 0.1)
    clock.schedule_unique(stop_move_player, 0.5)
    
def animate_player():
    """
    Shw the next frame in the walking sequence.
    """
    if moving:
        # Next frame for player.
        player.image = 'hero{}'.format(player.frame)
        player.frame += 1
        if player.frame == 6:
            player.frame = 1
        clock.schedule_unique(animate_player, 0.02)
    else:
        player.image = 'hero1'

def stop_move_player():
    """
    Called when the player has stopped moving. Right now,
    just flips the flag so keyboard input is read.
    """
    global moving 
    moving = False
    
def update():
    """
    Update game state,
    """
    x, y = player.pos
    if not moving:
        player.frame = 1
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
            player.angle = 270
        if keyboard[keys.RIGHT]:
            move_player(min(x + 64, 800), y)
            player.angle = 90
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
            print("DEAD!")
    # Remove all the traffic that is now off the screen.
    for old_vehicle in finished_traffic:
        traffic.remove(old_vehicle)
    chance_to_add_top = random.randint(0, 1000) > 950 
    chance_to_add_bottom = random.randint(0, 1000) > 950 
    if distance_top > 194 and chance_to_add_top:
        make_traffic('top')
    if distance_bottom < (WIDTH - 194) and chance_to_add_bottom:
        make_traffic('bottom')

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