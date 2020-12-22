import bge
from collections import OrderedDict

import _keys

from mathutils import Vector
from random import randint
from _timer import Timer


def clamp(x, a, b):
    return min(max(a, x), b)


class Movement(bge.types.KX_PythonComponent):
    args = OrderedDict([

        ("Auto_cam", True),
        ("Player Name", ""),
        ("Camera Look One", ""),
        ("Camera Look Two", ""),
        ("Camera Position", ""),
        ("Armature Name", "")

    ])

    def start(self, args):
        if args["Player Name"] != "":
            try:
                self.__player = self.object.scene.objects[args["Player Name"]]
            except:
                self.__player = None
                print("Can't find any reference for the Player Name")
        #self.__player = self.object.scene.objects["Player"]
        if args["Camera Look One"] != "":
            try:
                self.__camLook = self.__player.children[args["Camera Look One"]]
            except:
                self.__camLook = None
                print("Can't find any reference for Camera One Name")
        #self.__camLook = self.__player.children["Cam_look"]
        if args["Camera Look Two"] != "":
            try:
                self.__camLook2 = self.__camLook.children[args["Camera Look Two"]]
            except:
                self.__camLook2 = None
                print("Can't find any reference for Camera Two Name")
        #self.__camLook2 = self.__camLook.children["Cam_look_2"]
        if args["Camera Position"] != "":
            try:
                self.__camPos = self.__camLook2.children[args["Camera Position"]]
            except:
                self.__camPos = None
                print("Can't find any reference for Camera Position")
        #self.__camPos = self.__camLook2.children["Cam_pos"]
        if args["Armature Name"] != "":
            try:
                self.__armature = self.object.scene.objects[args["Armature Name"]]
            except:
                self.__armature = None
                print("Can't find any reference for Camera Position")
        
        #self.__armature = self.object.scene.objects["Armature"]
        
        self._time = Timer(0)
        self.activeAutoCam = args["Auto_cam"]
        
    def movement(self):
        vec = _keys.camDir()

        #self.object.applyRotation([0, 0, vec[0]])
        self.__camLook.applyRotation([vec[1], 0, 0], True)
        self.__player.applyRotation([0, 0, vec[0]])

        # USE: .to_euler() is a function used to convert matrix(3x3) into vectors(x, y, z)

        xyz = self.__camLook.localOrientation.to_euler()
        
        if xyz[0] <= -1.10:
            xyz[0] = -1.10
        
        if xyz[0] >= 1.00:
            xyz[0] = 1.00
            
        self.object.fov = 80 + (xyz[0] * 10)

        # Após converter uma matrix em vetor, para funcionar a rotação. é necessário reverter a conversão.

        self.__camLook.localOrientation = xyz.to_matrix()
        if self.activeAutoCam:
            self.controlFocus()
        
    def controlFocus(self):
        if _keys.move().length != 0.0 and _keys.move().y != -1.0:
            if self._time.getElapsedTime() >= 3.0:
                self.__player.worldOrientation = self.__player.worldOrientation.lerp(self.__armature.worldOrientation, 0.02)
        elif _keys.move().length == 0.0 and self.__player.worldOrientation != self.__armature.worldOrientation:
            if self._time.getElapsedTime() >= 3.0:
                self.__player.worldOrientation = self.__player.worldOrientation.lerp(self.__armature.worldOrientation, 0.02)
                if self._time.getElapsedTime() >= 20.0:
                    self._time.reset()
        else:
            self._time.reset()
        
    def camCol(self):
        origin = self.__camLook.worldPosition
        track = self.__camPos.worldPosition
        
        obHit, obPos, __ = self.object.rayCast(origin, track, 0.0, "obs", 1, 0, 0)
        
        if obHit != None:
            self.object.worldPosition = obPos + Vector([0, 0, 0.1])
        else:
            self.object.worldPosition = track
    
    def update(self):
        self.movement()
        self.camCol()
