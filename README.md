# basic
Basic controls for game development

### Theses Scripts were made to use together; if you try to use any of the modules separately, it won't work.

### _keys ###
  Simple Script for the keys (mouse and keyboard) inputs. 
  
### _camera.Movement ###
  Simple module for 3rd Person Character, with the option to make it "dynamic" - follows the character viewpoint.
  
  Need to be register on Main_Camera!
  
### _player.Character ###
  Simple module for Character Movement, based on WASD inputs from keyboard.
  
### _timer.Timer ###
  Simple module to control time.
  
# Important # :
  ### For these modules work, you must have a scene in upbge or bge that contains these objects:
    # Player Capsule
    # Armature parented with a vertex of Player Capsule Object
    # Empty01 parented with Player Capsule Object
    # Empty02 Parented with Empty01 and in the center of viewPoint (3D Main Camera)
    # Main Camera
    # Empty03 parented with Empty02 and located in the same position of the Camera.
###For more information, please visit LRVStudios web page for tutorials on how to use these modules:
  www.lrvstudios.com
