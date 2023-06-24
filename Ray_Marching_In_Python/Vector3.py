from math import sqrt
class Vector:
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z
        self.size = sqrt(x**2+y**2+z**2)
    
    def __add__(self,other):
        return Vector(
            self.x + other.x,
            self.y + other.y,
            self.z + other.z
        )
    
    def __sub__(self,other):
        return Vector(
            self.x - other.x,
            self.y - other.y,
            self.z - other.z
        )
    
    def unit(self):
        if(self.size == 0):
            return Vector(0,0,0)
        return Vector(  self.x/self.size,
                        self.y/self.size,
                        self.z/self.size,
        )
    
    def __mul__(self,scalar):

        return Vector(scalar*self.x,scalar*self.y,scalar*self.z)
        
    def __repr__(self):
        return f"({self.x}, {self.y}, {self.z})"

    def __str__(self):
        return self.__repr__()
    def __eq__(self,other):
        return (self.x == other.x and self.y == other.y and self.z == other.z)

    def __ne__(self,other):
        return not self.__eq__(other)
def dot_product(a,b):
    return (a.x*b.x+a.y*b.y+a.z*b.z)    