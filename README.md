# MindMapper v1.0.0
![A Node-based Text and Image Flowchart for Blender](/images/MindmapperLogo.png)

_(clockwise from top left: Geometry Node Editor, Mindmap Node Editor, Compositor Node Editor, Shader Node Editor)_
![screenshot](/images/MindMapperUpdate.png)
## What It Is
This addon gives you an 'Extra' category in the Shader, Geometry and Compositor Node Editors __Add Menu__, as well as a custom Node Editor.

Just click __Add > Extra > Mindmap__ or __Note__ to use the nodes in any node tree.

To create a Mindmapper Node Tree, open the Mindmapper Node Editor, click 'New' to create a new node tree, then, click __Add > Mindmap__. 

You can change the text and the background color of the node, as well as connect it to one or more other nodes to create a flowchart.

## How It Works
It works by displaying a String Property as multiple Label strings, separated by number of characters.

The complete text will display on the node, but in order to edit it, you must unhide the panel at the bottom of the node, then you can type or paste any text you like. 

The top row holds the __node label__, and the __node color__.

The next row allows you to select the __node image__.

The next allows you to select the __node image folder__.

The next holds the main __node body text__.

And, finally you can dynamically change the number of __node inputs__ and __node outputs__, however doing so will break the links, so set up your i/o before making connections!

There is not currently support for renaming sockets, importing/exporting text etc.

Image support comes through both 3dn-bip's Image Preview Generation, and Blender's auto-generated thumbnail previews.

## Acknowledgments and Thanks
Inspired by a request from __Tobias__ on RightClickSelect.

Multi-line strings c/o [Nikita of B3D Interplanety](https://b3d.interplanety.org/en/multiline-text-in-blender-interface-panels/)

__tin2tin__ contributed to the code, and also integrated it into the [Blender Screenwriter addon](https://github.com/tin2tin/Blender_Screenwriter)

__Bazza__ and __cannibalox__ contributed to the code.

__bonjorno7__ contributed the [3dn-bip library](https://github.com/bonjorno7/3dn-bip) which supports Hi-res images!

__A massive thanks to everyone who has downloaded, used, and especially contributed to this addon!__
