import bge


from mathutils import Vector


mouseSense = 0.4


def move():
    keyboard = bge.logic.keyboard.inputs
    vec = Vector([0, 0, 0])
    
    vec.y = keyboard[bge.events.WKEY].active - keyboard[bge.events.SKEY].active
    vec.x = keyboard[bge.events.DKEY].active - keyboard[bge.events.AKEY].active
    
    if vec.length > 0:
        vec.normalize()
    
    return vec


def camDir():
    x = 0
    y = 0

    mousePos = Vector(bge.logic.mouse.position)

    windowSize = [bge.render.getWindowWidth() - 1, bge.render.getWindowHeight() - 1]

    mousePos[0] = ((windowSize[0] // 2) / windowSize[0]) - mousePos[0]
    mousePos[1] = ((windowSize[1] // 2) / windowSize[1]) - mousePos[1]

    vec = mousePos * mouseSense

    bge.render.setMousePosition(int(windowSize[0] // 2), int(windowSize[1] // 2))

    return vec

def run():
    keyboard = bge.logic.keyboard.inputs
    
    if keyboard[bge.events.LEFTSHIFTKEY].active:
        return keyboard[bge.events.LEFTSHIFTKEY].active

def interact():
    keyboard = bge.logic.keyboard.inputs
    
    return keyboard[bge.events.EKEY].activated
