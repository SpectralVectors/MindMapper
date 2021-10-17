bl_info = {
    "name": "Mind Mapper",
    "author": "Spectral Vectors",
    "version": (0, 8, 3),
    "blender": (2, 90, 0),
    "location": "Mind Mapper - Custom Node Editor",
    "description": "A custom, node based flow chart for text",
    "warning": "",
    "doc_url": "",
    "category": "Custom Nodes",
}

import bpy, textwrap
from bpy.types import NodeTree, Node, NodeSocket, NodeReroute, NodeFrame

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
    '''A text and image, node based, flowchart'''
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = 'MindmapTreeType'
    # Label for nice name display
    bl_label = "Mind Mapper"
    # Icon identifier
    bl_icon = 'NETWORK_DRIVE'

# Custom socket type
class MindmapNodeSocket(NodeSocket):
    # Description string
    '''Custom node socket type'''
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = 'MindmapNodeSocketType'
    # Label for nice name display
    bl_label = "Mindmap Node Socket"

    def draw(self, context, layout, node, text):
        layout.label(text=text)
        
    # Socket color
    def draw_color(self, context, node):
        return (0.0, 1.0, 0.0, 1)


# Mix-in class for all custom nodes in this tree type.
# Defines a poll function to enable instantiation.
class MindmapTreeNode:
    @classmethod
    def poll(cls, ntree):
        return ntree.bl_idname == 'MindmapTreeType'

class UpdateNodes(bpy.types.Operator):
    bl_idname = 'node.update_nodes'
    bl_label = 'Update Node Sockets'
    bl_description = 'Updates to Node to show the correct number of Input/Output sockets'

    def execute(self, context):
        #my_node = bpy.context.active_node
        bpy.ops.node.add_node(type='MindmapNodeType')
        bpy.ops.node.delete()
        bpy.ops.node.add_node(type='MindmapNodeType')
        bpy.ops.node.delete()
        bpy.ops.node.add_node(type='MindmapNodeType')
        bpy.ops.node.delete()
        #bpy.context.active_node = my_node
        return {'FINISHED'}


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
    bl_icon = 'NETWORK_DRIVE'
    
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
        default = "Render Result",
        subtype = 'FILE_NAME'
    )

    node_inputs : bpy.props.IntProperty(
        name="Inputs",
        description="Number of Inputs on the Node",
        default=1,
        min=1,
        max=20,

    )

    node_outputs : bpy.props.IntProperty(
        name="Outputs",
        description="Number of Outputs on the Node",
        default=1,
        min=1,
        max=20,

    )    

    # === Optional Functions ===
    # Initialization function, called when a new node is created.
    def init(self, context):
        self.use_custom_color = True
        self.color = self.my_node_color
        self.width = 250
        
        for i in range(self.node_inputs):
            self.node_input_name = '1'
            i = self.inputs.new('MindmapNodeSocketType', name=self.node_input_name)
            i.display_shape = 'SQUARE_DOT'
            i.link_limit = 0 # enables multi input on a single socket
            #i.type = 'STRING'

        for j in range(self.node_outputs):
            self.node_output_name = '1'
            j = self.outputs.new('MindmapNodeSocketType', name=self.node_output_name)
            j.display_shape = 'SQUARE_DOT'
            j.link_limit = 0 # enables multi output from a single socket
            #j.type = 'STRING'

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

        text = self.my_string_prop
        characters = int(self.width / addon_prefs.WrapAmount)
        wrapper = textwrap.TextWrapper(width=characters)
        text_lines = wrapper.wrap(text=text)
        box = layout.box()

        if self.node_image:
            #nodeimage = bpy.path.basename(self.node_image)
            #bpy.data.images[self.node_image].use_fake_user = True
            box.template_icon(icon_value=bpy.data.images[self.node_image].preview.icon_id, scale=self.width / (addon_prefs.WrapAmount * 4) )

        for text_line in text_lines:
            box.label(text=text_line)

        layout.separator(factor=2)

        if addon_prefs.ShowInNode:
            if self.show_in_single_node:

                column = layout.column(align=True)
                row = column.row(align=True)
                row.prop(self, "my_title_prop", icon='GREASEPENCIL')
                row.prop(self, "color", text='', icon='MATERIAL')

                row = column.row(align=True)
                row.prop_search(self, 'node_image',  bpy.data, 'images')
                row.operator('image.open')

                row = column.row(align=True)
                row.prop(self, "my_string_prop", icon='GREASEPENCIL')

                row = column.row(align=True)
                row.prop(self, "node_inputs")
                row.prop(self, "node_outputs")

                row = column.row(align=True)
                row.operator('node.update_nodes')
    
    # Detail buttons in the sidebar.
    # If this function is not defined, the draw_buttons function is used instead
    def draw_buttons_ext(self, context, layout):
        column = layout.column(align=True)
        row = column.row()
        row.prop(self, "my_title_prop", icon='GREASEPENCIL')

        row = column.row(align=True)
        row.prop_search(self, 'node_image',  bpy.data, 'images')
        row.operator('image.open')
        
        row = column.row()
        row.prop(self, "my_string_prop", icon='GREASEPENCIL')

        row = column.row(align=True)
        row.prop(self, "node_inputs")
        row.prop(self, "node_outputs")

        row = column.row()
        row.operator('node.update_nodes')

        layout.prop(self, "show_in_single_node")

        #for i in range(self.node_inputs):
        #    layout.prop(self, "node_input_name")

    # Optional: custom label
    # Explicit user label overrides this, but here we can define a label dynamically
    def draw_label(self):
        return self.my_title_prop

    def update(self):

        if self.node_image:
            bpy.data.images[self.node_image].use_fake_user = True

        if len(self.inputs) < self.node_inputs:
            for i in range(self.node_inputs):
                if i > 0:
                    self.node_input_name = str(i + 1)
                    i = self.inputs.new('MindmapNodeSocketType', name=self.node_input_name)
                    i.display_shape = 'SQUARE_DOT'

        if len(self.inputs) > self.node_inputs:
            inputs = reversed(self.inputs)
            for input in inputs:
                while len(self.inputs) > self.node_inputs:
                    self.inputs.remove(input)

        if len(self.outputs) < self.node_outputs:
            for j in range(self.node_outputs):
                if j > 0:
                    self.node_output_name = str(j + 1)
                    j = self.outputs.new('MindmapNodeSocketType', name=self.node_output_name)
                    j.display_shape = 'SQUARE_DOT' 

        if len(self.outputs) > self.node_outputs:
            outputs = reversed(self.outputs)
            for output in outputs:
                while len(self.outputs) > self.node_outputs:
                    self.outputs.remove(output)

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
        NodeItem("NodeReroute"),
        NodeItem("NodeFrame"),
    ]),
]

classes = (
    MindmapTree,
    MindmapNode,
    MindMapperPreferences,
    MindmapNodeSocket,
    UpdateNodes,
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
