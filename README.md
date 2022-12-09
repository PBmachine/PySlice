# PySlice
 Python 3D printing slicer for 15112:
 This program loads and displays an STL mesh in 3D and allows the user to create 2d contour slices for creating "vase style" 3d printing paths
 This project is still in progress but is functional for loading and displaying slices on low poly stls. Improvements forthcoming!
 



# How do I run this project?
1. Install the numpy module
2. Open psApp.py from the pyslicemain folder
3. Use the buttons and arrow keys to interact
4. save a custom mesh as customMesh.stl in the Mesh_Models folder to load your custom mesh

# Shortcuts
-use left and right arrow keys to rotate mesh view on the z axis
-use the up and down arrow keys to rotate by a horizontal axis
  - use 'x' and 'y' keys to switch the horizontal axis for rotation
  - click the home icon to return to the default view (ISO with Z up)
-use 'n' to cycle through provided default meshes
-use the 'h' and 'g' keys to change the slice height up or down by .5mm increments
-use 'm' to run the slicer
-use 'c' to hide/show slices


Planned Additions: There's a lot~
Soon:
improved program efficiency + speed
Contour linking algorithm
transfer motion controls
Countour offsets 
infill option


Slice analysis
Gcode export
PlugIn v Standalone mode




Function Breakdown: 
psApp: contains primary app functionality, calls other modules

psMeshImport: opens a mesh with given filepath, converts binary data to facets (3d planar triangles)

UIWidgets: classes and settings for UI functions: window, buttons, rescale etc

ps3D_Render: classes and methods for rendering 3D data to window - mesh and slice classes, isometric projection, rotation matrix, window autoscale, origin grid

psSlicer: functions for generating the mesh slices, naive facet search method, triangle/plane intersection, slice class for storing data

psExport: function to export slice 3d points to CSV, classes for additional post processing data (WIP)

