# MindMapper v0.8
Node-based text and image flowchart for Blender

Mindmap with shortcuts visible:
![screenshot](/Mindmap.png)
Mindmap with shortcuts hidden:
![screenshot](/MindmapTidy.png)

## Notes
This was requested by Tobias on RightClickSelect, and made possible by a blog post from Nikita: https://b3d.interplanety.org/en/multiline-text-in-blender-interface-panels/ on how to extend Blender's Panels to display multiline text strings. Thanks also to tin2tin for suggesting some layout improvements!

This addon gives you a custom Node Editor (just like the Shader Node Editor, or the Geometry Node Editor), which will appear in the Editor Type menu after install.

First, click 'New' to create a new node tree, then, click 'Add' > 'Mindmap' to add a new node. You can change the text and the background color of the node, as well as connect it to one or more other nodes to create a flowchart.

It works by displaying a String Property as multiple Label strings, separated by number of characters.

The complete text will display on the node, but in order to edit it, you must click in the box with the __Pencil Icon__ at the bottom of the node, then you can type or paste any text you like. The top box is for the node label, the next row sets the picture, the next box sets the text for the body of the note, then the last are the controls to add/remove sockets.

Line breaks are not supported, but you can paste complete paragraphs. Since they are being pasted into a small text box, it may be easier to write them in the Text Editor, then paste them in the Node Properties after you've written and edited them.

Image support comes through Blender's auto-generated thumbnail previews, so images are low-res, but load quickly, and require no additional processing.

There is not currently support for renaming sockets, importing/exporting text etc.
