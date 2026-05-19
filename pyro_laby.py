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

musique_menu = Audio('sounds/musique/epic_music.mp3', loop=True, autoplay=True)

player = FirstPersonController(speed=8, collider='box')
player.enabled = False

stamina = 100
display_stamina = 100

height = 30
width = 40

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

main_menu = Entity(parent=camera.ui)
options_menu_ui = Entity(parent=camera.ui, enabled=False)
audio_menu_ui = Entity(parent=camera.ui, enabled=False)
controles_menu_ui = Entity(parent=camera.ui, enabled=False)

# MENU PRINCIPAL

main_background = Entity(
    parent=main_menu,
    model='quad',
    texture = 'assets/menu.png',
    scale=(2,1),
    color=color.dark_gray,
    z=1
)

title = Text(
    text="Pyromaniac's Labyrinth : GOTY Edition Playstation 7 edition",
    parent=main_menu,
    y=0.3,
    scale=2.5,
    color=color.red,
    origin=(0,0)
)

# MENU OPTIONS

options_background = Entity(
    parent=options_menu_ui,
    model='quad',
    scale=(2,1),
    color=color.black66,
    z=1
)

options_title = Text(
    text="OPTIONS",
    parent=options_menu_ui,
    y=0.3,
    scale=2,
    color=color.azure,
    origin=(0,0)
)

# MENU AUDIO

audio_background = Entity(
    parent=audio_menu_ui,
    model='quad',
    scale=(2,1),
    color=color.black66,
    z=1
)

audio_title = Text(
    text="AUDIO",
    parent=audio_menu_ui,
    y=0.3,
    scale=2,
    color=color.azure,
    origin=(0,0)
)

# SLIDER VOLUME

volume_text = Text(
    text="Volume",
    parent=audio_menu_ui,
    y=0.1,
    x=-0.08,
    scale=1.5
)

volume_slider = Slider(
    min=0,
    max=1,
    default=1,
    step=0.01,
    parent=audio_menu_ui,
    y=0,
    x=-0.25,
    scale=1
)

music_muted = False

def toggle_music():
    global music_muted

    if not music_muted:
        musique_menu.volume = 0
        volume_slider.value = 0
        mute_button.text = "UNMUTE"
        music_muted = True

    else:
        musique_menu.volume = 1
        volume_slider.value = 1
        mute_button.text = "MUTE"
        music_muted = False

mute_button = Button(
    text="MUTE",
    parent=audio_menu_ui,
    y=-0.15,
    scale=(0.3,0.1),
    color=color.red,
    highlight_color=color.orange,
    pressed_color=color.gray,
    on_click=toggle_music
)

def start_game():
    main_menu.enabled = False
    options_menu_ui.enabled = False

    player.enabled = True
    mouse.locked = True 

    stamina_bar.enabled = True 
    ground.enabled = True

    musique_menu.volume = 0

def quit_game():
    application.quit()

def open_options():
    main_menu.enabled = False
    options_menu_ui.enabled = True

    player.enabled = False
    mouse.locked = False

def return_to_main_menu():
    options_menu_ui.enabled = False
    main_menu.enabled = True

    player.enabled = False
    mouse.locked = False

def open_audio_menu():
    options_menu_ui.enabled = False
    audio_menu_ui.enabled = True

def return_to_options():
    audio_menu_ui.enabled = False
    options_menu_ui.enabled = True

def update_volume():
    global music_muted

    if not music_muted:
        musique_menu.volume = volume_slider.value

def create_button(parent, txt, y, action):
    btn = Button(
        text=txt,
        parent=parent,
        y=y,
        scale=(0.4, 0.1),
        color=color.yellow,
        highlight_color=color.orange,
        pressed_color=color.gray,
        text_color=color.red,
        on_click=action
    )

    base_scale = btn.scale
    base_y = btn.y

    def on_enter():
        btn.animate_scale(base_scale * 1.1, duration=0.1)
        btn.animate_y(base_y + 0.01, duration=0.1)

    def on_exit():
        btn.animate_scale(base_scale, duration=0.1)
        btn.animate_y(base_y, duration=0.1)

    btn.on_mouse_enter = on_enter
    btn.on_mouse_exit = on_exit

    def on_click():
        btn.animate_scale(base_scale * 0.95, duration=0.05)
        invoke(lambda: btn.animate_scale(base_scale * 1.1, duration=0.05), delay=0.05)
        invoke(lambda: btn.animate_scale(base_scale, duration=0.1), delay=0.1)

        action()

    btn.on_click = on_click

    return btn

create_button(main_menu, "JOUER", 0.1, start_game)
create_button(main_menu, "OPTIONS", -0.05, open_options)
create_button(main_menu, "QUITTER", -0.2, quit_game)

create_button(options_menu_ui, "AUDIO", 0.1, open_audio_menu)
create_button(options_menu_ui, "CONTROLES", -0.05, Func(print, "Controles"))
create_button(options_menu_ui, "RETOUR", -0.2, return_to_main_menu) # retour menu principal
create_button(audio_menu_ui, "RETOUR", -0.3, return_to_options) # retour menu options

def input(key):
    if key == 'escape':
        if main_menu.enabled:
            main_menu.enabled = False
            player.enabled = True
            mouse.locked = True
            stamina_bar.enabled = True
        else:
            main_menu.enabled = True
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
            stamina += 20 * time.dt

        if held_keys['left shift'] and held_keys['w'] and stamina > 0:
            player.speed = 15
            camera.y = lerp(camera.y, 1, time.dt * 10)
            stamina -= 25 * time.dt
        
        elif stamina < 0:
            player.speed = 6
            camera.y = lerp(camera.y, 1, time.dt * 10)
        
        else:
            player.speed = 8
            camera.y = lerp(camera.y, 1, time.dt * 10)
            stamina += 10 * time.dt

    update_stamina_bar()
    update_volume()

app.run()
