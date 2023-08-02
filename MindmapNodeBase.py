import bpy
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
    node.select = False
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
