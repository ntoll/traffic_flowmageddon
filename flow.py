"""
Flow - avoid the traffic flow and cross the road.
"""
WIDTH = 800
HEIGHT = 600
SPEED = 6  # Change in pixels per frame.

# The top of each "row" (pavement / road) on the screen.
rows = [56, 120, 184, 248, 312, 376, 440, 504, 568]

# Configure the hero at the bottom/middle of the screen.
player = Actor("hero")
player.row = 8
player.pos = (368, rows[player.row])
moving = False  # A flag to show if the player is moving.

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
            duration=0.1, tween='accelerate')
    clock.schedule_unique(stop_move_player, 0.1)

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
    # If the player isn't already moving.
    if not moving:
        # Check the keyboard presses from the player.
        if keyboard[keys.UP]:
            player.row = max(0, player.row - 1)
            move_player(x, rows[player.row])
            if player.row == 0:
                # You've got to the top. WIN!
                print("You made it!")
        if keyboard[keys.DOWN]:
            player.row = min(8, player.row + 1)
            move_player(x, rows[player.row])
        if keyboard[keys.LEFT]:
            move_player(max(x - 64, 0), y)
        if keyboard[keys.RIGHT]:
            move_player(min(x + 64, 800), y)
    # Update the position of traffic.
    for vehicle in traffic:
        if vehicle.lane == 'top':
            vehicle.left += SPEED
            if vehicle.left > WIDTH:
                vehicle.right = 0
        else:
            vehicle.left -= SPEED
            if vehicle.right < 0:
                vehicle.left = WIDTH
        if player.colliderect(vehicle):
            # Hit by traffic!
            print("DEAD!")

def make_traffic(lane='top'):
    """
    Create a vehicle to appear in the traffic.
    """
    global traffic
    new_car = Actor('car')
    if lane == 'top':
        new_car.right = 0
        new_car.top = rows[1] - 32
        new_car.lane = lane
    else:
        new_car.left = WIDTH
        new_car.top = rows[6] - 32
        new_car.lane = lane
    traffic.append(new_car)

make_traffic('top')
make_traffic('bottom')