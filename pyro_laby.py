from ursina import *
from ursina.prefabs.first_person_controller import *
import random
import json
import os
import math
import time

app = Ursina()

# MAP CONFIG

camera.fov = 90

ground = Entity(
    model='plane',
    scale=(200, 1,200),
    texture='perlin_noise',
    texture_scale=(200, 200),
    color=color.gray,
    collider='box'
)

DirectionalLight()
AmbientLight()
Sky()

# PARAMETRES DU JOUEUR

player = Entity(
    model='cube',
    collider='box',
    color=color.clear,
    position=(0, 2, 0)
)

arm = Entity(
    parent=camera,
    model='assets/arms.fbx',
    texture='assets/arms1Color.png',
    collider='box',
    color=color.white,
    position=(0.5, -0.6, 1),
    rotation=(10, -20, 5),
    scale=(-0.009, 0.009, 0.009)
)

camera.parent = player
camera.position = (0, 1.6, 0)

controls = {
    "forward": "w",
    "back": "s",
    "left": "a",
    "right": "d",
    "jump": "space",
    "sprint": "left shift",
    "crouch": "g"
}

# SAVAUGARDE DES PARAMETRES

settings_file = 'settings.json'

default_settings = {
    "volume": 1,
    "controls": controls,
}

def save_settings():
    settings = {
        "volume": volume_slider.value,
        "controls": controls,
        "music_muted": music_muted
    }

    with open(settings_file, 'w') as f:
        json.dump(settings, f, indent=4)

def load_settings():
    global controls
    global music_muted
    global last_volume

    if os.path.exists(settings_file):
        with open(settings_file, 'r') as f:
            settings = json.load(f)

            controls.update(settings.get("controls", {}))

            volume = settings.get("volume", 1)

            volume_slider.value = volume
            last_volume = volume

            music_muted = settings.get("music_muted", False)

            if music_muted:
                musique_menu.volume = 0
                mute_button.text = "UNMUTE"
            else:
                musique_menu.volume = volume
                mute_button.text = "MUTE"

# AUDIO

musique_menu = Audio('sounds/musique/epic_music.mp3', loop=True, autoplay=True)

footstep_sounds = Audio(
    'sounds/footstep1.mp3',
    loop=True,
    autoplay=False,
    volume=0.5
)

slap_sound = Audio('sounds/slap.mp3')

music_muted = False
last_volume = 1

# STAMINA CONFIG

stamina = 100
display_stamina = 100

stamina_bar = Entity(
    parent=camera.ui,
    model='quad',
    scale=(0.4, 0.05),
    x=-0.8,
    y=0.42,
    origin=(-0.5, 0),
    color=color.lime
)

stamina_bar.enabled = False

# MENUS

main_menu = Entity(parent=camera.ui)
options_menu_ui = Entity(parent=camera.ui, enabled=False)
audio_menu_ui = Entity(parent=camera.ui, enabled=False)
controles_menu_ui = Entity(parent=camera.ui, enabled=False)

# MENU PRINCIPAL

main_background = Entity(
    parent=main_menu,
    model='quad',
    texture='assets/menu.png',
    scale=(2, 1),
    color=color.dark_gray,
    z=1
)

title = Text(
    text="Pyromaniac's Labyrinth : GOTY Edition Playstation 7 edition",
    parent=main_menu,
    y=0.3,
    scale=2.5,
    color=color.red,
    origin=(0, 0)
)

# MENU OPTIONS

options_background = Entity(
    parent=options_menu_ui,
    model='quad',
    scale=(2, 1),
    color=color.black66,
    z=1
)

options_title = Text(
    text="OPTIONS",
    parent=options_menu_ui,
    y=0.3,
    scale=2,
    color=color.azure,
    origin=(0, 0)
)

# MENU AUDIO

audio_background = Entity(
    parent=audio_menu_ui,
    model='quad',
    scale=(2, 1),
    color=color.black66,
    z=1
)

audio_title = Text(
    text="AUDIO",
    parent=audio_menu_ui,
    y=0.3,
    scale=2,
    color=color.azure,
    origin=(0, 0)
)

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

# PARAMETRES DU JEU

game_active = False

height = 30
width = 40

speed = 8
sprint_speed = 15
gravity = 1
player_velocity_y = 0
stand_height = 1.6
crouch_height = 1.0

arm_base_pos = Vec3(0.5, -0.6, 1)
arm_base_rot = Vec3(10, -20, 5)

slap_timer = 0
slap_active = False

anim_t = 0

# REGLAGES AUDIO

def toggle_music():
    global music_muted, last_volume

    if not music_muted:
        last_volume = volume_slider.value
        musique_menu.volume = 0
        mute_button.text = "UNMUTE"
        music_muted = True
    else:
        musique_menu.volume = last_volume
        mute_button.text = "MUTE"
        music_muted = False

    save_settings()


mute_button = Button(
    text="MUTE",
    parent=audio_menu_ui,
    y=-0.15,
    scale=(0.3, 0.1),
    color=color.red,
    highlight_color=color.orange,
    pressed_color=color.gray,
    on_click=toggle_music
)

def on_slider_change():
    if not music_muted:
        musique_menu.volume = volume_slider.value

    save_settings()

volume_slider.on_value_changed = on_slider_change

# MENU CONTROLES

rebinding_action = None
ignorer_premiere_entree = False

def create_control_row(parent, action_name, display_name, y):

    Text(
        text=display_name,
        parent=parent,
        x=-0.3,
        y=y,
        scale=1.2,
        font='VeraMono.ttf'
    )

    key_text = Text(
        text=controls[action_name],
        parent=parent,
        x=0,
        y=y,
        scale=1.2,
        color=color.azure,
        font='VeraMono.ttf'
    )

    def change_key():
        global rebinding_action, ignorer_premiere_entree

        rebinding_action = (action_name, key_text)
        key_text.text = "..."

        ignorer_premiere_entree = True

    Button(
        text="Changer",
        text_color=color.red,
        parent=parent,
        x=0.35,
        y=y,
        scale=(0.15, 0.05),
        color=color.yellow,
        on_click=change_key
    )

def setup_controls_menu():
    create_control_row(controles_menu_ui, "forward", "Avancer", 0.4)
    create_control_row(controles_menu_ui, "back", "Reculer", 0.3)
    create_control_row(controles_menu_ui, "left", "Gauche", 0.2)
    create_control_row(controles_menu_ui, "right", "Droite", 0.1)
    create_control_row(controles_menu_ui, "jump", "Saut", 0)
    create_control_row(controles_menu_ui, "sprint", "Sprint", -0.1)
    create_control_row(controles_menu_ui, "crouch", "Accroupir", -0.2)

load_settings()
setup_controls_menu()

# MENU FUNCTIONS (IMPORTANTS)

def start_game():
    global game_active

    main_menu.enabled = False
    options_menu_ui.enabled = False

    player.enabled = True
    mouse.locked = True
    stamina_bar.enabled = True
    ground.enabled = True

    musique_menu.volume = 0

    game_active = True


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
    controles_menu_ui.enabled = False

def open_controls_menu():
    options_menu_ui.enabled = False
    controles_menu_ui.enabled = True
    mouse.locked = False

# FONCTION BOUTTONS

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

    def on_click():
        btn.animate_scale(base_scale * 0.95, duration=0.05)
        invoke(lambda: btn.animate_scale(base_scale * 1.1, duration=0.05), delay=0.05)
        invoke(lambda: btn.animate_scale(base_scale, duration=0.1), delay=0.1)

        action()

    btn.on_mouse_enter = on_enter
    btn.on_mouse_exit = on_exit
    btn.on_click = on_click

    return btn

# CREATION DES BOUTONS

create_button(main_menu, "JOUER", 0.1, start_game)
create_button(main_menu, "OPTIONS", -0.05, open_options)
create_button(main_menu, "QUITTER", -0.2, quit_game)

create_button(options_menu_ui, "AUDIO", 0.1, open_audio_menu)
create_button(options_menu_ui, "CONTROLES", -0.05, open_controls_menu)
create_button(options_menu_ui, "RETOUR", -0.2, return_to_main_menu)

create_button(audio_menu_ui, "RETOUR", -0.3, return_to_options)
create_button(controles_menu_ui, "RETOUR", -0.4, return_to_options)

def input(key):
    global player_velocity_y
    global rebinding_action
    global ignorer_premiere_entree
    global game_active

    if player.enabled and key == controls["jump"] and player.y <= 2:
        player_velocity_y = 8

    global slap_active, slap_timer

    if game_active and key == 'left mouse down':
        slap_active = True
        slap_timer = 0
        slap_sound.play()

    if rebinding_action is not None:
        action_name, key_text = rebinding_action

        if ignorer_premiere_entree:
            ignorer_premiere_entree = False
            return

        if key != 'escape':
            if action_name in controls:
                controls[action_name] = key
                key_text.text = key
                save_settings()

        rebinding_action = None
        return

    if key == 'escape':
        if main_menu.enabled:
            main_menu.enabled = False
            player.enabled = True
            mouse.locked = True
            stamina_bar.enabled = True
            player_velocity_y = 0
        else:
            main_menu.enabled = True
            player.enabled = False
            mouse.locked = False
            stamina_bar.enabled = False

# STAMINA BAR

def update_stamina_bar():
    global display_stamina

    display_stamina = lerp(display_stamina, stamina, time.dt * 8)
    stamina_bar.scale_x = 0.4 * display_stamina / 100

    if display_stamina > 60:
        stamina_bar.color = color.lime
    elif display_stamina > 30:
        stamina_bar.color = color.yellow
    elif display_stamina > 10:
        stamina_bar.color = color.orange
    else:
        stamina_bar.color = color.red
        stamina_bar.x = -0.8 + random.uniform(-0.003, 0.003)

# LE JEU EN LUI MEME

def update():
    global stamina, player_velocity_y
    global anim_t, slap_timer, slap_active

    stamina = clamp(stamina, 0, 100)

    if not player.enabled:
        return

    move = Vec3(0, 0, 0)

    if held_keys[controls["forward"]]:
        move += camera.forward
    if held_keys[controls["back"]]:
        move -= camera.forward
    if held_keys[controls["left"]]:
        move -= camera.right
    if held_keys[controls["right"]]:
        move += camera.right

    if held_keys[controls["crouch"]]:
        camera.y = lerp(camera.y, crouch_height, time.dt * 10)
        stamina += 20 * time.dt
    else:
        camera.y = lerp(camera.y, stand_height, time.dt * 10)

    move.y = 0
    move = move.normalized() if move.length() > 0 else move

    is_sprinting = held_keys[controls["sprint"]] and held_keys[controls["forward"]] and stamina > 0

    is_moving = move.length() > 0

    if is_moving and player.y <= 2.1:
        if not footstep_sounds.playing:
            footstep_sounds.play()

        if is_sprinting:
            footstep_sounds.pitch = 1.4
        else:
            footstep_sounds.pitch = 1
    else:
        footstep_sounds.stop()

    player.rotation_y += mouse.velocity[0] * 100
    camera.rotation_x -= mouse.velocity[1] * 100
    camera.rotation_x = clamp(camera.rotation_x, -90, 90)

    current_speed = sprint_speed if is_sprinting else speed

    player.position += move * current_speed * time.dt

    if is_sprinting:
        stamina -= 25 * time.dt
    else:
        stamina += 10 * time.dt

    stamina = clamp(stamina, 0, 100)

    player_velocity_y -= 25 * time.dt
    player.y += player_velocity_y * time.dt

    if player.y < 2:
        player.y = 2
        player_velocity_y = 0

    is_moving = move.length() > 0
    is_sprinting = held_keys[controls["sprint"]] and held_keys[controls["forward"]] and stamina > 0

    if not is_moving:
        anim_speed = 1.5
        amplitude = 0.003
    elif is_sprinting:
        anim_speed = 12
        amplitude = 0.06
    else:
        anim_speed = 7
        amplitude = 0.03

    anim_t += time.dt * anim_speed
    bob_y = math.sin(anim_t * 2) * amplitude

    target_pos = arm_base_pos + Vec3(0, bob_y, 0)
    target_rot = arm_base_rot

    # CLAQUE 

    slap_x = 0
    slap_rot = 0

    if slap_active:
        slap_timer += time.dt
        t = slap_timer * 10

        if t < 1:
            slap_x = lerp(0, -1.2, t)
            slap_rot = lerp(0, -100, t)
        elif t < 2:
            slap_x = lerp(-0.28, 0, t - 1)
            slap_rot = lerp(-40, 0, t - 1)
        else:
            slap_active = False

    final_pos = target_pos + Vec3(slap_x, 0, 0)
    final_rot = target_rot + Vec3(0, 0, slap_rot)

    arm.position = lerp(arm.position, final_pos, time.dt * 10)
    arm.rotation = lerp(arm.rotation, final_rot, time.dt * 10)

    update_stamina_bar()

app.run()
