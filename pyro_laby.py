from ursina import *
from ursina.prefabs.first_person_controller import *
import random
from random import randint
import json
import os
import math
import time

app = Ursina()

# MAP CONFIG

maze_entities = []
camera.fov = 80
camera.clip_plane_near = 0.01

ground = Entity(
    model='plane',
    scale=(200, 1,200),
    texture='grass',
    texture_scale=(200, 200),
    color=color.yellow,
    collider='box'
)

maze_entities.append(ground)

DirectionalLight()
AmbientLight()
Sky()

            # LE LABYRINTHE 

directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
              #Est     Ouest     Sud     Nord

mur_verticaux = []
for i in range(15):
    mur_verticaux.append([1] * 15)

mur_horizontaux = []
for i in range(15):
    mur_horizontaux.append([1] * 15)

case_visite = []
for i in range(15):
    case_visite.append([False for j in range(15)])

taille_case = 4

x_depart = randint(0, 14)
y_depart = randint(0, 14)

    # placement des coffres

def apparition_coffres(nombre_de_coffre):
    liste_coffres = []
    coffres_places = 0

    while coffres_places < nombre_de_coffre:
        x = randint(0, 14)
        y = randint(0, 14)

        if (x, y) not in liste_coffres:
            liste_coffres.append((x, y))
            coffres_places += 1
    return liste_coffres

positions_des_coffres = apparition_coffres(4)
coffres_set = set(positions_des_coffres)

    # spawn du joueur

def apparition(x_depart, y_depart, case_visite) :
	case_visite[y_depart][x_depart] = True
	pile_visite = []
	pile_visite.append((y_depart, x_depart))
	return pile_visite

pile_visite = apparition(0, 0, case_visite)

    # génération du labyrinthe

while len(pile_visite) > 0:
    case_actuelle = pile_visite[-1]
    x = case_actuelle[0]
    y = case_actuelle[1]
    voisins_valides = []
    
    for (dx, dy) in directions:
        voisin_x = x + dx
        voisin_y = y + dy
        if 0 <= voisin_x < 15 and 0 <= voisin_y < 15:
            if case_visite[voisin_y][voisin_x] == False:
                voisins_valides.append((voisin_x, voisin_y))

    if len(voisins_valides) > 0 :
        prochain_voisin = random.choice(voisins_valides)
        nv_x = prochain_voisin[0]
        nv_y = prochain_voisin[1]

        if nv_x == x + 1:
            mur_verticaux[y][x] = 0
        elif nv_x == x - 1:
            mur_verticaux[y][x - 1] = 0
        elif nv_y == y + 1:
            mur_horizontaux[y][x] = 0
        elif nv_y == y - 1:
            mur_horizontaux[y - 1][x] = 0

        case_visite[nv_y][nv_x] = True
        pile_visite.append((nv_x, nv_y))
        
    else:
        pile_visite.pop()

    #mise en forme avec ursina

decalage = taille_case / 2

for y in range(15):
    for x in range(15):

        # mur extérieur gauche
        if x == 0:
            mur = Entity(
                model='cube',
                scale=(0.1, 12, taille_case),
                position=(-decalage, 1.5, y * taille_case),
                texture='brick',
                color=color.orange,
                collider='box',
                enabled=False
            )
            maze_entities.append(mur)

        # mur extérieur haut
        if y == 0:
            mur = Entity(
                model='cube',
                scale=(taille_case, 12, 0.1),
                position=(x * taille_case, 1.5, -decalage),
                texture='brick',
                color=color.orange,
                collider='box',
                enabled=False
            )
            maze_entities.append(mur)

        # mur vertical intérieur
        if mur_verticaux[y][x] == 1:
            mur = Entity(
                model='cube',
                scale=(0.1, 12, taille_case),
                position=(x * taille_case + decalage, 1.5, y * taille_case),
                texture='brick',
                color=color.orange,
                collider='box',
                enabled=False
            )
            maze_entities.append(mur)

        # mur horizontal intérieur
        if mur_horizontaux[y][x] == 1:
            mur = Entity(
                model='cube',
                scale=(taille_case, 12, 0.1),
                position=(x * taille_case, 1.5, y * taille_case + decalage),
                texture='brick',
                color=color.orange,
                collider='box',
                enabled=False
            )
            maze_entities.append(mur)

        # coffre
        if (x, y) in positions_des_coffres:
            coffre = Entity(
                model='assets/coffre/low_poly_treasure_chest.glb',
                scale=0.02,
                color=color.gold,
                position=(x * taille_case, 0.1, y * taille_case),
                collider='box',
                enabled=False
            )
            maze_entities.append(coffre)

# PARAMETRES DU JOUEUR

x_depart = randint(0, 14)
y_depart = randint(0, 14)

player = Entity(
    model='cube',
    collider='box',
    color=color.clear,
    position=(x_depart * taille_case, 1, y_depart * taille_case)
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

maze_entities.append(arm)

# CINEMATIQUE

ground1 = Entity(
    model='plane',
    scale=(200, 1,200),
    texture='brick',
    color=color.dark_gray,
    collider='box',
    enabled=False
)

desk = Entity(
    model='cube',
    scale=(3,0.2,1.5),
    position=(0,1,3),
    color=color.brown,
    enabled=False
)

pc = Entity(
    model='cube',
    scale=(1.5,1,0.1),
    position=(0,2,2.2),
    color=color.black,
    enabled=False
)

chair = Entity(
    model='cube',
    scale=(1.5,1,1.5),
    position=(0,1,3.5),
    color=color.dark_gray,
    enabled=False
)

boy = Entity(position=(0,1,4), enabled=False)

body = Entity(parent=boy, model='cube',
              scale=(0.6,1,0.3),
              color=color.azure)

head = Entity(parent=boy, model='sphere',
              scale=0.5,
              position=(0,0.9,0),
              color=color.light_gray)

arm_l = Entity(parent=boy, model='cube',
               scale=(0.15,0.6,0.15),
               position=(-0.5,0.2,0),
               color=color.azure)

arm_r = Entity(parent=boy, model='cube',
               scale=(0.15,0.6,0.15),
               position=(0.5,0.2,0),
               color=color.azure)

leg_l = Entity(parent=boy, model='cube',
               scale=(0.2,0.8,0.2),
               position=(-0.2,-0.8,0),
               color=color.dark_gray)

leg_r = Entity(parent=boy, model='cube',
               scale=(0.2,0.8,0.2),
               position=(0.2,-0.8,0),
               color=color.dark_gray)

PointLight(position=(0,5,0), enabled=False)

cinematic = False
glitch_strength = 0

text_ui = Text(
    '',
    position=(-0.5,-0.4),
    scale=1.5,
    background=True,
    color=color.white
)

def say(msg, t=2):
    text_ui.text = msg
    invoke(lambda: setattr(text_ui, "text", ""), delay=t)


def camera_shake(intensity):
    camera.x += random.uniform(-intensity, intensity)
    camera.y += random.uniform(-intensity, intensity)


def start_cinematic():
    global cinematic

    cinematic = True

    player.enabled = False
    mouse.locked = False
    ground.enabled = False
    arm.enabled = False

    desk.enabled = True
    pc.enabled = True
    chair.enabled = True
    boy.enabled = True
    ground1.enabled = True

    camera.parent = scene
    camera.position = boy.world_position + Vec3(3,2,6)
    camera.look_at(boy)

    say("Garçon: Juste… une dernière partie...", 2)

    invoke(step_2, delay=2)


def step_2():
    say("SYSTEM: Connexion instable...", 2)

    camera.animate_position(
        pc.world_position + Vec3(2,2,2),
        duration=2
    )

    invoke(step_3, delay=2)


def step_3():
    global glitch_strength

    say("SYSTEM: SYNCHRONISATION...", 2)

    window.color = color.rgb(10,10,20)

    pc.color = color.cyan
    glitch_strength = 0.3

    camera.animate_position(
        pc.world_position + Vec3(0,0.5,0.8),
        duration=2
    )

    camera.animate_rotation(
        Vec3(10,180,0),
        duration=2
    )

    boy.animate_scale(0.1, duration=2)
    boy.animate_y(boy.y + 2, duration=2)

    arm_l.animate_rotation_z(90, duration=2)
    arm_r.animate_rotation_z(-90, duration=2)

    invoke(step_4, delay=2.2)


def step_4():
    global cinematic, cinematic_done

    desk.disable()
    pc.disable()
    chair.disable()
    boy.disable()
    ground1.disable()

    camera.parent = player
    camera.position = (0,1.6,0)

    player.enabled = True
    mouse.locked = True
    arm.enabled = True

    cinematic = False
    cinematic_done = True

    for e in maze_entities:
        e.enabled = True

    ground.enabled = True

# MINI MAP

minimap = Entity(
    parent=camera.ui,
    model='quad',
    scale=(0.25, 0.25),
    position=(0.75, 0.38),
    color=color.black66
)

mini_offset = Vec2(-0.125, -0.125)
mini_scale = 0.25 / (10 * taille_case)

def world_to_minimap(x, y):
    return Vec2(
        x * mini_scale + mini_offset.x,
        y * mini_scale + mini_offset.y
    )

mini_murs = []

for y in range(15):
    for x in range(15):

        # murs verticaux
        if mur_verticaux[y][x] == 1:
            pos = world_to_minimap(
                x * taille_case + decalage,
                y * taille_case
            )

            mini_murs.append(Entity(
                parent=minimap,
                model='quad',
                color=color.gray,
                scale=0.01,
                position=pos
            ))

        # murs horizontaux
        if mur_horizontaux[y][x] == 1:
            pos = world_to_minimap(
                x * taille_case,
                y * taille_case + decalage
            )

            mini_murs.append(Entity(
                parent=minimap,
                model='quad',
                color=color.gray,
                scale=0.01,
                position=pos
            ))

mini_coffres = []

for (x, y) in positions_des_coffres:
    pos = world_to_minimap(x * taille_case, y * taille_case)

    mini_coffres.append(Entity(
        parent=minimap,
        model='circle',
        color=color.gold,
        scale=0.02,
        position=pos
    ))

player_dot = Entity(
    parent=minimap,
    model='circle',
    color=color.red,
    scale=0.05,
    position=(0, 0)
)

world_scale = 0.01

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
    'sounds/footstep2.wav',
    loop=True,
    autoplay=False,
    volume=0.5,
    speed=50
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
    text="Pyromaniac's Labyrinth : GOTY Edition/Diractor's Cut",
    parent=main_menu,
    y=0.3,
    scale=2.5,
    color=color.red,
    origin=(0, 0),
    font = 'assets/font/IMMORTAL.ttf'
)

# MENU OPTIONS

options_background = Entity(
    parent=options_menu_ui,
    model='quad',
    scale=(2, 1),
    color=color.black66,
    z=1,
    font = 'assets/font/IMMORTAL.ttf'
)

options_title = Text(
    text="OPTIONS",
    parent=options_menu_ui,
    y=0.3,
    scale=2,
    color=color.azure,
    origin=(0, 0),
    font = 'assets/font/IMMORTAL.ttf'
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
    origin=(0, 0),
    font = 'assets/font/IMMORTAL.ttf'
)

volume_text = Text(
    text="Volume",
    parent=audio_menu_ui,
    y=0.1,
    x=-0.08,
    scale=1.5,
    font = 'assets/font/IMMORTAL.ttf'
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

cinematic = False
cinematic_done = False
glitch_strength = 0

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
        font='assets/font/IMMORTAL.ttf'
    )

    key_text = Text(
        text=controls[action_name],
        parent=parent,
        x=0,
        y=y,
        scale=1.2,
        color=color.azure,
        font='assets/font/IMMORTAL.ttf'
    )

    def change_key():
        global rebinding_action, ignorer_premiere_entree

        rebinding_action = (action_name, key_text)
        key_text.text = "..."

        ignorer_premiere_entree = True

    Button(
        text="Changer",
        text_color=color.red,
        font='assets/font/IMMORTAL.ttf',
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

    game_active = True

    if cinematic_done:
        player.enabled = True
        mouse.locked = True
        arm.enabled = True
        stamina_bar.enabled = True

        for e in maze_entities:
            e.enabled = True

        ground.enabled = True
    else:
        start_cinematic()


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
    cadre = Entity(
        parent=parent,
        model=Quad(radius=0.1),
        scale=(0.43, 0.13),
        color=color.hex('#c20000'),
        y=y
    )

    btn = Button(
        text=txt,
        parent=cadre,
        scale=(0.93, 0.82),
        color=color.hex('#ffc500'),
        highlight_color=color.hex('#ffe066'),
        pressed_color=color.gray,
        text_color=color.hex('#5c0606'),
        on_click=action,
        z=-0.02
    )

    base_scale = cadre.scale
    base_y = cadre.y

    def on_enter():
        cadre.animate_scale(base_scale * 1.1, duration=0.1)
        cadre.animate_y(base_y + 0.01, duration=0.1)

    def on_exit():
        cadre.animate_scale(base_scale, duration=0.1)
        cadre.animate_y(base_y, duration=0.1)

    def on_click_anim():
        cadre.animate_scale(base_scale * 0.95, duration=0.05)
        invoke(lambda: cadre.animate_scale(base_scale * 1.1, duration=0.05), delay=0.05)
        invoke(lambda: cadre.animate_scale(base_scale, duration=0.1), delay=0.1)
        action()

    btn.on_mouse_enter = on_enter
    btn.on_mouse_exit = on_exit
    btn.on_click = on_click_anim

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

def move_with_collision(entity, direction, speed):
    direction.y = 0

    if direction.length() == 0:
        return

    direction = direction.normalized()
    step = direction * speed * time.dt

    hit = raycast(
        entity.position + Vec3(0, 1, 0),
        direction,
        distance=0.6,
        ignore=(entity,)
    )

    future_pos = entity.position + step
    gx = int(round(future_pos.x / taille_case))
    gy = int(round(future_pos.z / taille_case))

    hit_chest = False

    for (cx, cy) in coffres_set:
        chest_pos = Vec3(cx * taille_case, 0, cy * taille_case)

        dx = future_pos.x - chest_pos.x
        dz = future_pos.z - chest_pos.z

        if (dx * dx + dz * dz) < 0.8 * 0.8 and player.y < 3:
            hit_chest = True
            break

    if (not hit.hit) and (not hit_chest):
        entity.position += step

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

    move.y = 0

    is_moving = move.length() > 0

    is_crouching = held_keys[controls["crouch"]]

    if is_crouching:
        camera.y = lerp(camera.y, crouch_height, time.dt * 10)
        stamina += 20 * time.dt
    else:
        camera.y = lerp(camera.y, stand_height, time.dt * 10)

    is_sprinting = (
        held_keys[controls["sprint"]] and
        held_keys[controls["forward"]] and
        stamina > 0 and
        not is_crouching
    )

    current_speed = sprint_speed if is_sprinting else speed

    move_with_collision(player, move, current_speed)

    if is_sprinting:
        stamina -= 25 * time.dt
    else:
        stamina += 10 * time.dt

    stamina = clamp(stamina, 0, 100)

    player.rotation_y += mouse.velocity[0] * 100
    camera.rotation_x -= mouse.velocity[1] * 100
    camera.rotation_x = clamp(camera.rotation_x, -90, 90)

    if is_moving and player.y <= 2.1:
        if not footstep_sounds.playing:
            footstep_sounds.play()

        footstep_sounds.pitch = 1.4 if is_sprinting else 1
    else:
        footstep_sounds.stop()

    player_velocity_y -= 25 * time.dt
    player.y += player_velocity_y * time.dt

    if player.y < 2:
        player.y = 2
        player_velocity_y = 0

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

    player_dot.position = world_to_minimap(player.x, player.z)

    if cinematic and glitch_strength > 0:
        camera_shake(glitch_strength)

    update_stamina_bar()

app.run()
