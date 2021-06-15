# MindMapper
Node-based text flowchart for Blender

![screenshot](/Mindmap.png)

## Notes
This was requested by Tobias on RightClickSelect, and made possible by a blog post from Nikita: https://b3d.interplanety.org/en/multiline-text-in-blender-interface-panels/ on how to extend Blender's Panels to display multiline text strings.

This addon gives you a custom Node Editor (just like the Shader Node Editor, or the Geometry Node Editor), which will appear in the Editor Type menu after install.

First, click 'New' to create a new node tree, then, click 'Add' > 'Mindmap' to add a new node. You can change the text and the background color of the node, as well as connect it to one or more other nodes to create a flowchart.

It works by displaying a String Property as multiple Label strings, separated by number of characters.

The complete text will display on the node, but in order to edit it, you must click in the box next to 'Text:' at the top of the node, then you can type or paste any text you like.

Line breaks are not supported, but you can paste complete paragraphs. Since they are being pasted into a small text box, it may be easier to write them in the Text Editor, then paste them in the Node Properties after you've written and edited them.

There is not currently support for Reroute nodes, multiple inputs, embedding images etc. This was a bit of a spur of the moment code, if you want more features then you can fork and extend it, I'm not sure when I'll be updating it.
