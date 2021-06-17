bl_info = {
    "name": "Mind Mapper",
    "author": "Spectral Vectors",
    "version": (0, 6),
    "blender": (2, 90, 0),
    "location": "Mind Mapper - Custom Node Editor",
    "description": "A custom, node based flow chart for text",
    "warning": "",
    "doc_url": "",
    "category": "Custom Nodes",
}

import bpy, textwrap
from bpy.types import NodeTree, Node, NodeSocket
from bpy_extras.io_utils import ImportHelper

class MindMapperPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    ShowInNode: bpy.props.BoolProperty(
        name='Show Shortcuts in Node (Global)',
        description='They will remain visible in the Node properties panel.',
        default=True,
    )

    WrapAmount: bpy.props.IntProperty(
        name='Text Wrap Amount',
        description='Bigger numbers mean shorter lines',
        default=6,
        soft_max=10,
        soft_min=1,
    )

    def draw(self, context):    
        layout = self.layout
        box = layout.box()
        column = box.column()
        row = column.row()
        row.prop(self, 'ShowInNode')
        row.prop(self, 'WrapAmount')


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
        name= '',
        default= 'Once upon a time, a long line of text was divided into many smaller lines, the people rejoiced, and all was well in the land of Blender...',
    )

    my_title_prop: bpy.props.StringProperty(
        name= '',
        default= 'Mindmap'
    )

    my_node_color: bpy.props.FloatVectorProperty(
        name='',
        default=(0,0,0.1),
        subtype='COLOR',
    )

    my_text_size: bpy.props.IntProperty(
        name='Text Size',
        default=12,
        soft_min=8,
        soft_max=64,
    )

    show_in_single_node: bpy.props.BoolProperty(
        name='Show Shortcuts in Node (single)',
        default=True,
    )

    node_image : bpy.props.StringProperty(
        name = "",
        description = "Filename of the Node's image.",
        default = "",
        subtype = 'FILE_NAME'
    )


    # === Optional Functions ===
    # Initialization function, called when a new node is created.
    def init(self, context):
        self.use_custom_color = True
        self.color = self.my_node_color
        self.width = 250
        
        self.inputs.new('NodeSocketShader', "")
        
        self.outputs.new('NodeSocketShader', "")

    # Copy function to initialize a copied node from an existing one.
    def copy(self, node):
        print("Copying from node ", node)

    # Free function to clean up on removal.
    def free(self):
        print("Removing node ", self, ", Goodbye!")

    # Additional buttons displayed on the node.
    def draw_buttons(self, context, layout):
        preferences = context.preferences
        addon_prefs = preferences.addons[__name__].preferences

        if addon_prefs.ShowInNode:
            if self.show_in_single_node:

                box = layout.box()

                row = box.row()
                row.prop(self, "my_title_prop", icon='GREASEPENCIL')
                row.prop(self, "color", text='', icon='MATERIAL')

                row = box.row()
                row.prop_search(self, 'node_image',  bpy.data, 'images')
                row.operator('image.open')

                row = box.row()
                row.prop(self, "my_string_prop", icon='GREASEPENCIL')
                

                layout.separator(factor=2)

        text = self.my_string_prop
        characters = int(self.width / addon_prefs.WrapAmount)
        wrapper = textwrap.TextWrapper(width=characters)
        text_lines = wrapper.wrap(text=text)
        box = layout.box()

        if self.node_image:
            nodeimage = bpy.path.basename(self.node_image)
            box.template_icon(icon_value=bpy.data.images[nodeimage].preview.icon_id, scale=self.width / (addon_prefs.WrapAmount * 4) )

        for text_line in text_lines:
            box.label(text=text_line)
    
    # Detail buttons in the sidebar.
    # If this function is not defined, the draw_buttons function is used instead
    def draw_buttons_ext(self, context, layout):
        row = layout.row()
        row.prop(self, "my_title_prop", icon='GREASEPENCIL')
        row = layout.row()
        row.prop_search(self, 'node_image',  bpy.data, 'images')
        row.operator('image.open')
        row = layout.row()
        row.prop(self, "my_string_prop", icon='GREASEPENCIL')
        
        layout.prop(self, "show_in_single_node")

    # Optional: custom label
    # Explicit user label overrides this, but here we can define a label dynamically
    def draw_label(self):
        return self.my_title_prop

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
    MindMapperPreferences,
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
