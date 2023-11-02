# UrbanChaosUtils
Repo containing various scripts for Urban Chaos game.

# 3D Model Viewer
Tool used to convert nprim data to .obj & .mtl format as shown in:
[https://youtu.be/sdvsI-QBcZ0 https://youtu.be/sdvsI-QBcZ0](https://youtu.be/sdvsI-QBcZ0)

# Requirements
You will need to have a full version of **Urban Chaos** game to be able to use nprim_visualizer script. 


Textures can be exported by using tools from [https://github.com/Fire-Head/UCTxcTools/tree/master ](https://github.com/Fire-Head/UCTxcTools/tree/master)

nprim_visualizer script has hardcoded path to textures at line 175:

            map_Kd = f"map_Kd C:/Games/Urban Chaos/server/textures/shared/prims/tex{key:03d}hi.tga\n"

You will need to change this path accordingly, as this is the path to textures used to do UV mapping. 
Additionally I copied all nprims (so I don't accidentally modify original) to res/nprims in the directory where python script is located. 
