# PySlice
 Python 3D printing slicer for 15112:
 This program loads and displays an STL mesh in 3D and allows the user to create 2d contour slices for creating "vase style" 3d printing paths


# How do I run this project?
1. Install the numpy module
2. Open psApp.py from the pyslicemain folder
3. Use the buttons and arrow keys to interact
4. save a custom mesh as customMesh.stl in the Mesh_Models folder to load your custom mesh (above 50kb filesize may be slow when slicing!)

Shortcuts
-click the home icon to reset the mesh view
-use left and right arrow keys to rotate mesh view on the z axis
-use the up and down arrow keys to rotate mesh view on the x or y axis
    press 'x' or 'y' to swap between these axes
    press the home button to return to the default orientation
-use 'n' to cycle through provided default meshes
-use 'm' to run the slicer at selected height
-use 'h' to increment slice height by .5 mm use the increase button to incr by .1mm
-use 'g' to decrement slice height by .5 mm use the decrease button to decr by .1mm
-use 'c' to clear slice render
click the help info to display these commands and then anywhere to return




psApp: contains primary app functionality, calls other modules

psMeshImport: opens a mesh with given filepath, converts binary data to facets (3d planar triangles)

UIWidgets: classes and settings for UI functions: window, buttons, rescale etc

ps3D_Render: classes and methods for rendering 3D data to window - mesh and slice classes, isometric projection, rotation matrix, window autoscale, origin grid

psSlicer: functions for generating the mesh slices, naive facet search method, triangle/plane intersection, slice class for storing data

psExport: function to export slice 3d points to CSV, classes for additional post processing data (WIP)