from Vector3 import Vector, dot_product
from PIL import Image
from math import fmod


Max_distance = 10
Min_Distance = 0.001
Max_steps = 1000


class Scene:
    def __init__(self):
        self.entities = []

    def distance(self, Position):
        minimum_distance = float('inf')
        minimum_index = -1
        for i, Entity in enumerate(self.entities):
            dis = Entity.distance(Position)
            if(dis < minimum_distance):
                minimum_distance = dis
                minimum_index = i
        return (minimum_distance, minimum_index)

    def add(self, Entity):
        self.entities.append(Entity)

    def normal(self, position, i):
        return self.entities[i].normal(position)


class Sphere:
    def __init__(self, Center, Radius):
        self.Center = Center
        self.Radius = Radius

    def distance(self, Position):

        return (Position-self.Center).size - self.Radius

    def normal(self, Position):

        return (Position - self.Center).unit()


class Plane:
    def __init__(self, normal, point):
        self.Normal = normal.unit()
        self.point = point

    def distance(self, Position):
        return abs(dot_product(Position-self.point, self.Normal))

    def normal(self, Position):
        return self.Normal


def march(u_vector, start_Position, Scene, Light):
    position = start_Position
    steps = 0
    while(steps < Max_steps):
        steps += 1

        dis, i = Scene.distance(position)
        position = position + u_vector*dis
        if(position.size > Max_distance):
            return 0
        if(dis < Min_Distance):
            light_vector = (Light - position).unit()

            color = dot_product(light_vector, Scene.normal(position, i))

            if(color > 0):
                new_start_Position = position + \
                    Scene.normal(position, i)*Min_Distance
                if(not march_is_shadow(new_start_Position, Scene, Light)):
                    return color
            return 0
    return 0


def march_is_shadow(start_Position, Scene, Light):

    u_vector = (Light - start_Position).unit()
    position = start_Position
    Max_distance = (Light-start_Position).size
    steps = 0
    while(steps < Max_steps):
        steps += 1

        dis, _ = Scene.distance(position)
        position = position + u_vector*dis
        if((position-start_Position).size >= Max_distance):

            return False
        if(dis < Min_Distance):
            return True
    return False


def main():
    screen_distance = 1.0

    screen_pwidth = 800
    screen_pheight = 800
    Light = Vector(-10.0, 10.0, -10.0)
    noramlizing_factor = 1/400
    img = Image.new('RGB', (screen_pwidth, screen_pheight), color=(0, 0, 0))
    Ball = Sphere(Vector(0.0, 0.5, 3.0), 0.25)
    Ball2 = Sphere(Vector(0.0, -0.5, 3.0), 0.25)
    Flat = Plane(Vector(0, 1, 0), Vector(0, -1, 5))
    scene = Scene()
    scene.add(Ball)
    scene.add(Ball2)
    scene.add(Flat)
    pixels = img.load()
    print("Running the Ray Marcher - This may take a while")
    for x in range(0, screen_pwidth):
        for y in range(0, screen_pheight):
            u_vector = Vector((x-screen_pwidth/2)*noramlizing_factor,
                              -(y-screen_pheight/2)*noramlizing_factor,
                              screen_distance
                              ).unit()
            color = march(u_vector, Vector(0, 0, 0), scene, Light)

            color = int(color*(color > 0)*255)

            pixels[x, y] = (color, color, color)
    img.show()
    name = input("How do you want to save the image?")
    img.save(name)


if __name__ == "__main__":
    main()
