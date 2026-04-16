from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

ground = Entity(
    model='plane',
    scale=(100,1,100),
    texture='white_cube',
    texture_scale=(100,100),
    collider='box')

player = FirstPersonController()

DirectionalLight()
AmbientLight()

app.run()
