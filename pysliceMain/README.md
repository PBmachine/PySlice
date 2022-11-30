# PySlice
 Python 3D printing slice for 15112

TP2: 
Features:
Main - currently only calls the app - will include import and export

App - views mesh, scales mesh to fit window, runs slicer
-use 'n' to cycle through given default meshes
-use 'm' to run slicer
-use 'h' to increment slice height by .25mm
-use 'c' to clear slice render
- may include final updates for control 

slicer
run from app
creates slice segments at z heights
outputs list of slices

mesh import
imports mesh and creates hash lookup for time-efficient slicing


TODO!
update file path loading
update app class organization
update user interface - height, mesh, etc

slicer search algo
slice display
export