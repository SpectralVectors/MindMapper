import bpy
import textwrap
from bpy.types import Node
from . MindmapNodeBase import MindmapTreeNode
from . MindmapNodeBase import label_multiline


# Note Node
class NoteNode(Node, MindmapTreeNode):
    '''A Text-only node'''
    # Optional. If not explicitly defined, the python class name is used.
    bl_idname = 'NoteNodeType'
    # Label for nice name display
    bl_label = "Note"
    # Icon identifier
    bl_icon = 'TEXT'

    # === Custom Properties ===
    my_string_prop: bpy.props.StringProperty(
        name='',
        default='Once upon a time, a long line of text was divided into many '
        'smaller lines, the people rejoiced, and all was well in the land of '
        'Blender...',
    )

    my_title_prop: bpy.props.StringProperty(
        name='',
        default='Note'  # noqa: F821
    )

    my_node_color: bpy.props.FloatVectorProperty(
        name='',
        default=(0.6, 0.6, 0),
        subtype='COLOR',  # noqa: F821
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

    # === Optional Functions ===
    # Initialization function, called when a new node is created.
    def init(self, context):
        self.use_custom_color = True
        self.color = self.my_node_color
        self.width = 250
        j = self.outputs.new('MindmapNodeSocketType', name='>')
        j.display_shape = 'SQUARE_DOT'
        j.link_limit = 0

    # Copy function to initialize a copied node from an existing one.
    def copy(self, node):
        print("Copying from node ", node)

    # Free function to clean up on removal.
    def free(self):
        print("Removing node ", self, ", Goodbye!")

    # Additional buttons displayed on the node.
    def draw_buttons(self, context, layout):
        preferences = context.preferences
        addon_prefs = preferences.addons[__package__].preferences

        # Get the width and create a text wrapper
        characters = int(self.width / addon_prefs.WrapAmount)
        wrapper = textwrap.TextWrapper(width=characters)

        text = self.my_string_prop
        lines = text.split("\n")
        text_lines = []

        # Wrap each line separately
        for line in lines:
            text_lines += wrapper.wrap(text=line)

        box = layout.box()
        box = box.column(align=True)

        for text_line in text_lines:
            box.label(text=text_line)

        row = layout.row(align=True)
        icon = 'TRIA_DOWN' if self.show_in_single_node else 'TRIA_RIGHT'
        row.prop(self, 'show_in_single_node', icon=icon, icon_only=True)

        if self.show_in_single_node:
            row.prop(self, "my_title_prop", icon='GREASEPENCIL')
            row.prop(self, "color", text='', icon='MATERIAL')

            row = layout.row(align=True)
            row.prop(self, "my_string_prop", icon='GREASEPENCIL')

    # Detail buttons in the sidebar.
    # If function is not defined, the draw_buttons function is used instead
    def draw_buttons_ext(self, context, layout):
        column = layout.column()
        row = column.row()
        row.prop(self, "my_title_prop", icon='GREASEPENCIL')

        col = column.box().column(align=True)
        preferences = context.preferences
        addon_prefs = preferences.addons[__package__].preferences
        wrap_width = int(self.width / addon_prefs.WrapAmount)
        text = self.my_string_prop
        label_multiline(context, text, wrap_width, col)
        col.prop(self, "my_string_prop", icon='GREASEPENCIL')

    # Optional: custom label
    # Explicit user label overrides, but here we can define a label dynamically
    def draw_label(self):
        return self.my_title_prop

    def update(self):
        self.my_string_prop = self.my_string_prop
