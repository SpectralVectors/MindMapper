import bpy
import os
import textwrap
from bpy.types import NodeTree
from bpy.types import NodeSocket


# Mindmap-style custom Node editor
# Derived from the NodeTree base type, similar to Menu, Operator, Panel, etc.
class MindmapTree(NodeTree):
    '''A text and image, node based, flowchart'''
    # Optional. If not explicitly defined, the python class name is used.
    bl_idname = 'MindmapNodeTree'
    # Label for nice name display
    bl_label = "Mind Mapper"
    # Icon identifier
    bl_icon = 'NETWORK_DRIVE'


# Custom socket type
class MindmapNodeSocket(NodeSocket):
    '''Custom node socket type'''
    # Optional. If not explicitly defined, the python class name is used.
    bl_idname = 'MindmapNodeSocketType'
    # Label for nice name display
    bl_label = "Mindmap Node Socket"

    def draw(self, context, layout, node, text):
        layout.label(text=text)

    # Socket color
    def draw_color(self, context, node):
        return (0.1, 0.3, 0.1, 1)


# Mix-in class for all custom nodes in this tree type.
# Defines a poll function to enable instantiation.
class MindmapTreeNode:
    @classmethod
    def poll(cls, ntree):
        ntrees = [
            'MindmapNodeTree',
            'ShaderNodeTree',
            'GeometryNodeTree'
        ]
        return [ntree.bl_idname for ntree in ntrees]


def update_nodes(self, context):
    node = context.active_node
    node_tree = context.space_data.edit_tree
    nodes = node_tree.nodes
    reroute = nodes.new(type="NodeReroute")
    links = node_tree.links
    links.new(node.outputs[0], reroute.inputs[0])
    bpy.ops.node.select_all(action='DESELECT')
    reroute.select = True
    bpy.ops.node.delete()


def label_multiline(context, text, wrap_width, parent):
    chars = int(context.region.width / 7)
    print(chars)
    chars = int(wrap_width)
    print(chars)
    wrapper = textwrap.TextWrapper(width=chars)
    split = text.splitlines()
    text_lines = [
        wrap_line for line in split for wrap_line in wrapper.wrap(text=line)
    ]
    [parent.label(text=text_line) for text_line in text_lines]


def enum_previews_from_directory_items(self, context):
    """EnumProperty callback"""
    enum_items = []

    if context is None:
        return enum_items

    preferences = context.preferences
    addon_prefs = preferences.addons[__package__].preferences
    directory = addon_prefs.node_images_dir
    # Get the preview collection (defined in register func).
    pcoll = preview_collections["mindmap"]

    if directory == pcoll.node_images_dir:
        return pcoll.node_images

    print("Scanning directory: %s" % directory)

    if directory and os.path.exists(directory):
        # Scan the directory for png files
        image_paths = []
        for fn in os.listdir(directory):
            if fn.lower().endswith(".png"):
                image_paths.append(fn)

        for i, name in enumerate(image_paths):
            # generates a thumbnail preview for a file.
            filepath = os.path.join(directory, name)
            icon = pcoll.get(name)
            if not icon:
                thumb = pcoll.load(name, filepath, 'IMAGE')
            else:
                thumb = pcoll[name]
            enum_items.append((name, name, "", thumb.icon_id, i))

    pcoll.node_images = enum_items
    pcoll.node_images_dir = directory
    return pcoll.node_images


preview_collections = {}
