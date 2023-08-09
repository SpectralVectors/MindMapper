import bpy
from bpy.types import Node
from . MindmapNodeBase import MindmapTreeNode


# Numberlist Node
class NumberlistNode(Node, MindmapTreeNode):
    '''A Numberlist node'''
    # Optional. If not explicitly defined, the python class name is used.
    bl_idname = 'NumberlistNodeType'
    # Label for nice name display
    bl_label = "Numberlist"
    # Icon identifier
    bl_icon = 'LINENUMBERS_ON'

    # === Custom Properties ===
    numberlist_length: bpy.props.IntProperty(
        name='Items',  # noqa: F821
        default=1,
        min=1,
        max=10
    )

    string_0: bpy.props.StringProperty(
        name='1',
        default=''
    )

    string_1: bpy.props.StringProperty(
        name='2',
        default=''
    )

    string_2: bpy.props.StringProperty(
        name='3',
        default=''
    )

    string_3: bpy.props.StringProperty(
        name='4',
        default=''
    )

    string_4: bpy.props.StringProperty(
        name='5',
        default=''
    )

    string_5: bpy.props.StringProperty(
        name='6',
        default=''
    )

    string_6: bpy.props.StringProperty(
        name='7',
        default=''
    )

    string_7: bpy.props.StringProperty(
        name='8',
        default=''
    )

    string_8: bpy.props.StringProperty(
        name='9',
        default=''
    )

    string_9: bpy.props.StringProperty(
        name='10',
        default=''
    )

    string_10: bpy.props.StringProperty(
        name='11',
        default=''
    )

    my_title_prop: bpy.props.StringProperty(
        name='',
        default='Numberlist'  # noqa: F821
    )

    my_node_color: bpy.props.FloatVectorProperty(
        name='',
        default=(0, 0.3, 0),
        subtype='COLOR',  # noqa: F821
    )

    # === Optional Functions ===
    # Initialization function, called when a new node is created.
    def init(self, context):
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
        column = layout.column(align=True)
        column.alignment = 'CENTER'
        for i in range(self.numberlist_length):
            text = f"string_{i}"
            column.prop(self, text)
        row = layout.row(align=True)
        row.prop(self, 'numberlist_length', icon='PRESET')
        row.prop(self, 'color', text='', icon='MATERIAL')

    # Detail buttons in the sidebar.
    # If function is not defined, the draw_buttons function is used instead
    def draw_buttons_ext(self, context, layout):
        column = layout.column()
        row = column.row()
        row.prop(self, "my_title_prop", icon='GREASEPENCIL')

    # Optional: custom label
    # Explicit user label overrides, but here we can define a label dynamically
    def draw_label(self):
        return self.my_title_prop

    def update(self):
        self.my_title_prop = self.my_title_prop
