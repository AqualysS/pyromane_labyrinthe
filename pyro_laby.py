from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

ground = Entity(
    model='plane',
    scale=(1000,1,1000),
    texture='brick',
    color=color.gray,
    texture_scale=(1000,1000),
    collider='box'
)

player = FirstPersonController(speed=8, collider='box')
player.enabled = False

stamina = 100
txt = Text(text="Stamina: 100", position=(-0.85, 0.45), scale=2)

DirectionalLight()
AmbientLight()

menu = Entity(parent=camera.ui)

background = Entity(
    parent=menu,
    model='quad',
    scale=(2,1),
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
    origin=(0,0),
    z=0
)

def create_button(text, y, action):
    return Button(
        text=text,
        parent=menu,
        y=y,
        scale=(0.4,0.1),
        color="#FFD429",
        highlight_color=color.orange,
        pressed_color=color.rgb(0,100,200),
        text_color=color.rgb(139,0,0),
        on_click=action
    )

def start_game():
    menu.enabled = False
    player.enabled = True
    mouse.locked = True
    txt.enabled = True

def quit_game():
    application.quit()

txt.enabled = False

create_button("JOUER", 0.1, start_game)
create_button("OPTIONS", -0.05, lambda: print("Options"))
create_button("QUITTER", -0.2, quit_game)

def input(key):
    if key == 'escape':
        if menu.enabled:
            menu.enabled = False
            player.enabled = True
            mouse.locked = True
            txt.enabled = True
        else:
            menu.enabled = True
            player.enabled = False
            mouse.locked = False
            txt.enabled = False

def jump(key):
    if key == 'space':
        player.y = 5
    else:
        player.y = 0

def update():
    global stamina

    stamina = clamp(stamina, 0, 100)
    can_sprint = stamina > 0

    if held_keys['g']:
        camera.y = lerp(camera.y, 0.5, time.dt * 10)
        player.speed = 4
        stamina += 15 * time.dt

    elif held_keys['left shift'] and can_sprint:
        camera.y = lerp(camera.y, 1, time.dt * 10)
        player.speed = 15
        stamina -= 25 * time.dt

    else:
        camera.y = lerp(camera.y, 1, time.dt * 10)
        player.speed = 8
        stamina += 10 * time.dt

    if stamina <= 0:
        stamina = 0
        player.speed = 8

    txt.text = "Stamina: " + str(int(stamina))

app.run()
