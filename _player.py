import bge
from collections import OrderedDict


from collections import OrderedDict
from mathutils import Vector
from _timer import Timer

import _keys


def clamp(x, a, b):
    return min(max(a, x), b)


if not hasattr(bge, "__component__"):
    pass

class Character(bge.types.KX_PythonComponent):
    args = OrderedDict([
    
        ("Static Jump", False),
        ("Avoid Sliding", True),
        ("Align To Move Direction", True),
        ("Align Smooth", 0.5),
        ("Smooth Character Movement", 0.0),
        ("Avoid Sliding", True),
        ("Speed", 0.03),
        ("Min Speed", 0.03),
        ("Max Speed", 0.08)
    ])

    def start(self, args):
        #if not "Language" in bge.logic.globalDict:
        #    bge.logic.globalDict["Language"] = 0
            
        self._time = Timer(0)
        
        ### Character Controls:
        
        self._spd = args["Speed"]
        self._minSpd = args["Min Speed"]
        self._maxSpd = args["Max Speed"]
        
            
        self.__character = bge.constraints.getCharacter(self.object)
        self.__camLook = self.object.children["Cam_look"]
        #self.__arm = self.object.scene.objects["Armature"]
            
        self.__staticJump = args["Static Jump"]
        self.__alignMoveDir = args["Align To Move Direction"]
        self.alignSmooth = 1 - clamp(args["Align Smooth"], 0, 1)
        self.__lastPosition = self.object.worldPosition.copy()
        self.__moveDirection = None
        self.avoidSliding = args["Avoid Sliding"]
        self.__smoothLast = Vector([0, 0, 0])
        self.__lastDirection = Vector([0, 0, 0])
        self.__smoothSlidingFlag = False
        self.__smoothMov = clamp(args["Smooth Character Movement"], 0, 0.99)
        
    def avoidSlide(self):
        """Avoids the character to slide. This funtion is useful when you have
        Collision Bounds activated."""

        self.object.worldPosition.xy = self.__lastPosition.xy

        other = self.object.worldOrientation * self.__smoothLast

        if self.__lastDirection.length != 0 and other.length != 0:
            if self.__lastDirection.angle(other) > 0.3:
                if not self.__smoothSlidingFlag:
                    self.__smoothLast = Vector([0, 0, 0])
                    
    def __updateMoveDirection(self):
        """Updates the move direction"""
        self.__moveDirection = self.object.worldPosition - self.__lastPosition
        self.__lastPosition = self.object.worldPosition.copy()
    
    def movement(self):
        dir = _keys.move()
        self.__smoothSlidingFlag = False
        if dir.length != 0:
            self.__smoothSlidingFlag = True
            dir.normalize()
            dir *= self._spd
            
        smooth = 1.0 - self.__smoothMov
        vec = self.__smoothLast.lerp(dir, smooth)
        self.__smoothLast = vec
        
        vec = self.object.worldOrientation * dir
        self.__character.walkDirection = vec
        
        if vec.length != 0:

            self.__lastDirection = self.object.worldPosition - self.__lastPosition
            self.__lastPosition = self.object.worldPosition.copy()
            self.controlSpd()
            
        else:
            self._time.reset()  
            
    def controlSpd(self):
        self._spd = self._minSpd
        #print(self._time.getElapsedTime())
        if self._spd < self._maxSpd:
            if self._time.getElapsedTime() < 1.0:
                self._spd = self._minSpd + 0.01
            elif self._time.getElapsedTime() >= 1.0:
                self._spd = self._maxSpd

    def update(self):
        self.movement()

        if self.avoidSliding:
            self.avoidSlide()

        self.__updateMoveDirection()
