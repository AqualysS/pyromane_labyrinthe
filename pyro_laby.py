from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random

app = Ursina()

ground = Entity(
    model='plane',
    scale=(1000,1,1000),
    texture='brick',
    texture_scale=(1000,1000),
    color=color.gray,
    collider='box'
)

DirectionalLight()
AmbientLight()

player = FirstPersonController(speed=8, collider='box')
player.enabled = False

stamina = 100
display_stamina = 100

stamina_bar = Entity(
    parent=camera.ui,
    model='quad',
    scale=(0.4,0.05),
    x=-0.8,
    y=0.42,
    origin=(-0.5,0),
    color=color.lime
)

stamina_bar.enabled = False
menu = Entity(parent=camera.ui)

background = Entity(
    parent=menu,
    model='quad',
    scale=(2,1),
    color=color.dark_gray,
    z=1
)

title = Text(
    text="Pyromaniac's Labyrinth : GOTY Edition",
    parent=menu,
    y=0.3,
    scale=2.5,
    color=color.red,
    origin=(0,0)
)

def start_game():
    menu.enabled = False
    player.enabled = True
    mouse.locked = True
    stamina_bar.enabled = True

def quit_game():
    application.quit()

def create_button(txt, y, action):
    return Button(
        text=txt,
        parent=menu,
        y=y,
        scale=(0.4,0.1),
        color=color.yellow,
        highlight_color=color.orange,
        pressed_color=color.azure,
        text_color=color.red,
        on_click=action
    )

create_button("JOUER", 0.1, start_game)
create_button("OPTIONS", -0.05, lambda: print("Options"))
create_button("QUITTER", -0.2, quit_game)

def input(key):
    if key == 'escape':
        if menu.enabled:
            menu.enabled = False
            player.enabled = True
            mouse.locked = True
            stamina_bar.enabled = True
        else:
            menu.enabled = True
            player.enabled = False
            mouse.locked = False
            stamina_bar.enabled = False

def update_stamina_bar():
    global display_stamina

    display_stamina = lerp(display_stamina, stamina, time.dt * 8)
    stamina_bar.scale_x = 0.4 * display_stamina / 100

    if display_stamina > 60:
        stamina_bar.color = color.lime
        stamina_bar.x = -0.8

    elif display_stamina > 30:
        stamina_bar.color = color.yellow
        stamina_bar.x = -0.8

    elif display_stamina > 10:
        stamina_bar.color = color.orange
        stamina_bar.x = -0.8

    else:
        stamina_bar.color = color.red
        stamina_bar.x = -0.8 + random.uniform(-0.003,0.003)

def update():
    global stamina

    stamina = clamp(stamina, 0, 100)

    if player.enabled:

        if held_keys['g']:
            player.speed = 4
            camera.y = lerp(camera.y, 0.5, time.dt * 10)
            stamina += 15 * time.dt

        elif held_keys['left shift'] and stamina > 0:
            player.speed = 15
            camera.y = lerp(camera.y, 1, time.dt * 10)
            stamina -= 25 * time.dt

        else:
            player.speed = 8
            camera.y = lerp(camera.y, 1, time.dt * 10)
            stamina += 10 * time.dt

    update_stamina_bar()

app.run()
