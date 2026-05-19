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
menu = Entity(parent=camera.ui)

background = Entity(
    parent=menu,
    model='quad',
    texture = 'assets/menu.png',
    scale=(2,1),
    color=color.dark_gray,
    z=1
)

title = Text(
    text="Pyromaniac's Labyrinth : GOTY Edition Playstation 7 edition",
    parent=menu,
    y=0.3,
    scale=2.5,
    color=color.red,
    origin=(0,0)
)


def start_game():
    menu.enabled = False # désactive l'écran de menu principal
    player.enabled = True  # active le contrôleur du joueur pour commencer le jeu
    mouse.locked = True # verrouille la souris pour le mode première personne
    stamina_bar.enabled = True # affiche la barre d'endurance pendant le jeu
    musique_menu.volume = 0

def quit_game():
    application.quit() # quitte l'application immédiatement

def create_button(txt, y, action):
    # crée et retourne un bouton d'interface pour le menu
    return Button(
        text=txt, # texte affiché sur le bouton
        parent=menu, # parent du bouton dans l'UI du menu
        y=y, # position verticale du bouton
        scale=(0.4,0.1), # dimensions du bouton
        color=color.yellow, # couleur de base du bouton
        highlight_color=color.orange, # couleur quand le bouton est survolé
        pressed_color=color.azure, # couleur quand le bouton est cliqué
        text_color=color.red, # couleur du texte du bouton
        on_click=action # fonction appelée au clic
    )

create_button("JOUER", 0.1, start_game)
create_button("OPTIONS", -0.05, lambda: print("Options"))
create_button("QUITTER", -0.2, quit_game)

def input(key):
    # gère les événements de touches clavier
    if key == 'escape':
        # ouvre ou ferme le menu selon l'état actuel
        if menu.enabled:
            menu.enabled = False # cache le menu principal
            player.enabled = True # réactive le joueur
            mouse.locked = True # verrouille la souris pour le jeu
            stamina_bar.enabled = True # réaffiche la barre d'endurance
        else:
            menu.enabled = True # affiche le menu principal
            player.enabled = False # désactive le contrôle du joueur
            mouse.locked = False # libère la souris pour la navigation menu
            stamina_bar.enabled = False # cache la barre d'endurance
    

def update_stamina_bar():
    global display_stamina # indique que display_stamina est une variable globale modifiée ici

    display_stamina = lerp(display_stamina, stamina, time.dt * 8) # lisse la transition de l'affichage d'endurance vers la valeur réelle
    stamina_bar.scale_x = 0.4 * display_stamina / 100 # ajuste la largeur de la barre en fonction du pourcentage d'endurance

    if display_stamina > 60: # si l'endurance est haute, affiche la barre verte
        stamina_bar.color = color.lime
        stamina_bar.x = -0.8

    elif display_stamina > 30: # si l'endurance est moyenne, affiche la barre jaune
        stamina_bar.color = color.yellow
        stamina_bar.x = -0.8

    elif display_stamina > 10: # si l'endurance est faible, affiche la barre orange
        stamina_bar.color = color.orange
        stamina_bar.x = -0.8

    else: # si l'endurance est très basse, affiche la barre rouge et la secoue
        stamina_bar.color = color.red
        stamina_bar.x = -0.8 + random.uniform(-0.003,0.003)

def update():
    global stamina  # indique que stamina est une variable globale modifiée ici

    stamina = clamp(stamina, 0, 100)  # limite stamina entre 0 et 100 à chaque frame

    if player.enabled:  # si le joueur est actif, ajuste la vitesse et l'endurance

        if held_keys['g']:  # marche lente si la touche 'g' est appuyée
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

app.run()
