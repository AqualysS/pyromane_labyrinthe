from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

ground = Entity(
    model='plane',
    scale=(100,1,100),
    texture='brick',
    color=color.gray,
    texture_scale=(100,100),
    collider='box')

player = FirstPersonController(speed=8, collider='box')
player.enabled = False

DirectionalLight()
AmbientLight()

menu = Entity(parent=camera.ui)

background = Entity(
    parent=menu,
    model='quad',
    scale=(2, 1),
    color=color.dark_gray,
    z=1  
)

title = Text(
    "Pyromaniac's Labyrinth : GOTY Edition",
    parent=menu,
    y=0.3,
    scale=3,
    font='VeraMono.ttf',
    color=color.red,
    origin=(0, 0),
    z=0
)

def create_button(text, y, action):
    return Button(
        text=text,
        parent=menu,
        y=y,
        scale=(0.4, 0.1),
        color="#FFD429",
        highlight_color=color.orange,
        pressed_color=color.rgb(0,100,200),
        text_color=color.rgb(139,0,0),
        z=0, 
        on_click=action
    )

def start_game():
    menu.enabled = False
    player.enabled = True
    mouse.locked = True

def quit_game():
    application.quit()

btn_play = create_button("JOUER", 0.1, start_game)
btn_options = create_button("OPTIONS", -0.05, lambda: print("Options"))
btn_quit = create_button("QUITTER", -0.2, quit_game)

def input(key):
    if key == 'escape':
        if menu.enabled:
            menu.enabled = False
            player.enabled = True
            mouse.locked = True
        else:
            menu.enabled = True
            player.enabled = False
            mouse.locked = False   

def jump(key):
    if key == 'space':
        player.y = 5
    else:
        player.y = 0

def update():
    if held_keys['g']:
        camera.y = lerp(camera.y, 0.5, time.dt * 10)
        player.speed = 4
    else:
        camera.y = lerp(camera.y, 1, time.dt * 10)
        player.speed = 8

app.run()
