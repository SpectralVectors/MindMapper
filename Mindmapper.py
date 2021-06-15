bl_info = {
    "name": "Mind Mapper",
    "author": "Spectral Vectors",
    "version": (0, 1),
    "blender": (2, 90, 0),
    "location": "Mind Mapper - Custom Node Editor",
    "description": "A custom, node based flow chart for text",
    "warning": "",
    "doc_url": "",
    "category": "Custom Nodes",
}

import bpy, textwrap
from bpy.types import NodeTree, Node, NodeSocket

# Mindmap-style custom Node editor
# Derived from the NodeTree base type, similar to Menu, Operator, Panel, etc.
class MindmapTree(NodeTree):
    # Description string
    '''A text-only mindmap-style, node based flowchart'''
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = 'MindmapTreeType'
    # Label for nice name display
    bl_label = "Mind Mapper"
    # Icon identifier
    bl_icon = 'NODETREE'


# Mix-in class for all custom nodes in this tree type.
# Defines a poll function to enable instantiation.
class MindmapTreeNode:
    @classmethod
    def poll(cls, ntree):
        return ntree.bl_idname == 'MindmapTreeType'


# Derived from the Node base type.
class MindmapNode(Node, MindmapTreeNode):
    # === Basics ===
    # Description string
    '''A custom node'''
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = 'MindmapNodeType'
    # Label for nice name display
    bl_label = "Mindmap"
    # Icon identifier
    bl_icon = 'TEXT'
    
    # === Custom Properties ===
    my_string_prop: bpy.props.StringProperty(
        name= 'Text',
        default= 'Once upon a time, a long line of text was divided into many smaller lines, the people rejoiced, and all was well in the land of Blender...'
    )

    my_node_color: bpy.props.FloatVectorProperty(
        name='',
        default=(0,0,0.1),
        subtype='COLOR',
    )

    # === Optional Functions ===
    # Initialization function, called when a new node is created.
    def init(self, context):
        self.inputs.new('NodeSocketShader', "")
        self.outputs.new('NodeSocketShader', "")

        self.use_custom_color = True
        self.color = self.my_node_color
        self.width = 250


    # Copy function to initialize a copied node from an existing one.
    def copy(self, node):
        print("Copying from node ", node)

    # Free function to clean up on removal.
    def free(self):
        print("Removing node ", self, ", Goodbye!")

    # Additional buttons displayed on the node.
    def draw_buttons(self, context, layout):
        layout.prop(self, "my_string_prop")
        layout.prop(self, "color")

        text = self.my_string_prop
        chars = int(self.width / 6)
        wrapper = textwrap.TextWrapper(width=chars)
        text_lines = wrapper.wrap(text=text)
        box = layout.box()
        for text_line in text_lines:
            box.label(text=text_line)


    # Detail buttons in the sidebar.
    # If this function is not defined, the draw_buttons function is used instead
    def draw_buttons_ext(self, context, layout):
        layout.prop(self, "my_string_prop")

    # Optional: custom label
    # Explicit user label overrides this, but here we can define a label dynamically
    def draw_label(self):
        return "Mindmap"


### Node Categories ###
# Node categories are a python system for automatically
# extending the Add menu, toolbar panels and search operator.
# For more examples see release/scripts/startup/nodeitems_builtins.py

import nodeitems_utils
from nodeitems_utils import NodeCategory, NodeItem

# our own base class with an appropriate poll function,
# so the categories only show up in our own tree type

class MyNodeCategory(NodeCategory):
    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type == 'MindmapTreeType'

# all categories in a list
node_categories = [
    # identifier, label, items list
    MyNodeCategory('MINDMAPNODES', "Mindmapper", items=[
        # our basic node
        NodeItem("MindmapNodeType"),
    ]),
]

classes = (
    MindmapTree,
    MindmapNode,
)


def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    nodeitems_utils.register_node_categories('Mindmap', node_categories)


def unregister():
    nodeitems_utils.unregister_node_categories('Mindmap')

    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)


if __name__ == "__main__":
    register()
