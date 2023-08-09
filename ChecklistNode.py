import bpy
from bpy.types import Node
from . MindmapNodeBase import MindmapTreeNode


# Checklist Node
class ChecklistNode(Node, MindmapTreeNode):
    '''A Checklist node'''
    # Optional. If not explicitly defined, the python class name is used.
    bl_idname = 'ChecklistNodeType'
    # Label for nice name display
    bl_label = "Checklist"
    # Icon identifier
    bl_icon = 'CHECKMARK'

    # === Custom Properties ===
    checklist_length: bpy.props.IntProperty(
        name='Items',  # noqa: F821
        default=1,
        # update=update_checklist,
        min=1,
        max=10
    )

    item_0: bpy.props.BoolProperty(
        name='',
        default=False
    )

    item_1: bpy.props.BoolProperty(
        name='',
        default=False
    )

    item_2: bpy.props.BoolProperty(
        name='',
        default=False
    )

    item_3: bpy.props.BoolProperty(
        name='',
        default=False
    )

    item_4: bpy.props.BoolProperty(
        name='',
        default=False
    )

    item_5: bpy.props.BoolProperty(
        name='',
        default=False
    )

    item_6: bpy.props.BoolProperty(
        name='',
        default=False
    )

    item_7: bpy.props.BoolProperty(
        name='',
        default=False
    )

    item_8: bpy.props.BoolProperty(
        name='',
        default=False
    )

    item_9: bpy.props.BoolProperty(
        name='',
        default=False
    )

    item_10: bpy.props.BoolProperty(
        name='',
        default=False
    )

    string_0: bpy.props.StringProperty(
        name='',
        default=''
    )

    string_1: bpy.props.StringProperty(
        name='',
        default=''
    )

    string_2: bpy.props.StringProperty(
        name='',
        default=''
    )

    string_3: bpy.props.StringProperty(
        name='',
        default=''
    )

    string_4: bpy.props.StringProperty(
        name='',
        default=''
    )

    string_5: bpy.props.StringProperty(
        name='',
        default=''
    )

    string_6: bpy.props.StringProperty(
        name='',
        default=''
    )

    string_7: bpy.props.StringProperty(
        name='',
        default=''
    )

    string_8: bpy.props.StringProperty(
        name='',
        default=''
    )

    string_9: bpy.props.StringProperty(
        name='',
        default=''
    )

    string_10: bpy.props.StringProperty(
        name='',
        default=''
    )

    my_title_prop: bpy.props.StringProperty(
        name='',
        default='Checklist'  # noqa: F821
    )

    my_node_color: bpy.props.FloatVectorProperty(
        name='',
        default=(0, 0, 0.6),
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
        for i in range(self.checklist_length):
            split = column.split(factor=0.05, align=True)
            name = f"item_{i}"
            text = f"string_{i}"
            split.prop(self, name)
            row = split.row(align=True)
            row.prop(self, text)
            row.enabled = not eval(f'self.item_{i}')
        row = layout.row(align=True)
        row.prop(self, 'checklist_length', icon='PRESET')
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
