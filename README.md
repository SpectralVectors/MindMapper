# MindMapper v0.9.3
Node-based text and image flowchart for Blender
![screenshot](/images/MindMapperUpdate.png)

## What It Is
This addon gives you an 'Extra' category in the Shader, Geometry and Compositor Node Editors __Add Menu__, as well as a custom Node Editor.

Just click __Add > Extra > Mindmap__ or __Note__ to use the nodes in any node tree.

To create a Mindmapper Node Tree, open the Mindmapper Node Editor, click 'New' to create a new node tree, then, click __Add > Mindmap__. 

You can change the text and the background color of the node, as well as connect it to one or more other nodes to create a flowchart.

## How It Works
It works by displaying a String Property as multiple Label strings, separated by number of characters.

The complete text will display on the node, but in order to edit it, you must click in the box with the __Pencil Icon__ at the bottom of the node, then you can type or paste any text you like. The top box is for the node label, the next row sets the picture, the next box sets the text for the body of the note, then the last are the controls to add/remove sockets.

Image support comes through Blender's auto-generated thumbnail previews, so images are low-res, but load quickly, and require no additional processing.

There is not currently support for renaming sockets, importing/exporting text etc.

## Acknowledgments and Thanks
Inspired by a request from __Tobias__ on RightClickSelect.

Multi-line strings c/o [Nikita of B3D Interplanety](https://b3d.interplanety.org/en/multiline-text-in-blender-interface-panels/)

__tin2tin__ contributed to the code, and also integrated it into the [Blender Screenwriter addon](https://github.com/tin2tin/Blender_Screenwriter)

__Bazza__ and __cannibalox__ contributed to the code.

__A massive thanks to everyone who has downloaded, used, and especially contributed to this addon!__
