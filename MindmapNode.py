import bpy
import textwrap
from bpy.types import Node
from . MindmapNodeBase import MindmapTreeNode
from . MindmapNodeBase import label_multiline
from . MindmapNodeBase import update_nodes


# Derived from the Node base type.
class MindmapNode(Node, MindmapTreeNode):
    '''A Text and Image Flowchart node'''
    # Optional. If not explicitly defined, the python class name is used.
    bl_idname = 'MindmapNodeType'
    # Label for nice name display
    bl_label = "Mindmap"
    # Icon identifier
    bl_icon = 'NETWORK_DRIVE'

    # === Custom Properties ===
    my_string_prop: bpy.props.StringProperty(
        name='',
        default='Once upon a time, a long line of text was divided into many '
        'smaller lines, the people rejoiced, and all was well in the land of '
        'Blender...',
    )

    my_title_prop: bpy.props.StringProperty(
        name='',
        default='Mindmap'  # noqa: F821
    )

    my_node_color: bpy.props.FloatVectorProperty(
        name='',
        default=(0, 0, 0.1),
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

    node_image: bpy.props.StringProperty(
        name="",
        description="Filename of the Node's image.",
        default="Render Result",
        subtype='FILE_NAME'  # noqa: F821
    )

    node_inputs: bpy.props.IntProperty(
        name='Inputs',  # noqa: F821
        description="Number of Inputs on the Node",
        default=1,
        min=1,
        max=20,
        update=update_nodes,
    )

    node_outputs: bpy.props.IntProperty(
        name="Outputs",  # noqa: F821
        description="Number of Outputs on the Node",
        default=1,
        min=1,
        max=20,
        update=update_nodes,
    )

    # === Optional Functions ===
    # Initialization function, called when a new node is created.
    def init(self, context):
        self.use_custom_color = True
        self.color = self.my_node_color
        self.width = 250

        for i in range(self.node_inputs):
            self.node_input_name = '1'
            i = self.inputs.new(
                'MindmapNodeSocketType',
                name=self.node_input_name
            )
            i.display_shape = 'SQUARE_DOT'
            i.link_limit = 0  # enables multi input on a single socket
            # i.type = 'STRING'

        for j in range(self.node_outputs):
            self.node_output_name = '1'
            j = self.outputs.new(
                'MindmapNodeSocketType',
                name=self.node_output_name
            )
            j.display_shape = 'SQUARE_DOT'
            j.link_limit = 0  # enables multi output from a single socket
            # j.type = 'STRING'

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

        if self.node_image:
            preview = bpy.data.images[self.node_image].preview
            icon = preview.icon_id
            box.template_icon(
                icon_value=icon,
                scale=self.width / (addon_prefs.WrapAmount * 4)
            )

        for text_line in text_lines:
            box.label(text=text_line)

        if addon_prefs.ShowInNode:
            column = layout.column(align=True)
            row = column.row(align=True)
            icon = 'TRIA_DOWN' if self.show_in_single_node else 'TRIA_RIGHT'
            row.prop(self, 'show_in_single_node', icon=icon, icon_only=True)

            if self.show_in_single_node:
                row.prop(self, "my_title_prop", icon='GREASEPENCIL')
                row.prop(self, "color", text='', icon='MATERIAL')

                column = column.column(align=True)
                column.prop_search(self, 'node_image', bpy.data, 'images')
                column.operator('image.open', text='Open Image')

                row = column.row(align=True)
                row.prop(self, "my_string_prop", icon='GREASEPENCIL')

                row = column.row(align=True)
                row.prop(self, "node_inputs")
                row.prop(self, "node_outputs")

    # Detail buttons in the sidebar.
    # If the function is not defined, the draw_buttons function is used instead
    def draw_buttons_ext(self, context, layout):
        column = layout.column()
        row = column.row()
        row.prop(self, "my_title_prop", icon='GREASEPENCIL')

        row = column.row(align=True)
        row.prop_search(self, 'node_image', bpy.data, 'images')
        row.operator('image.open')

        col = column.box().column(align=True)
        preferences = context.preferences
        addon_prefs = preferences.addons[__package__].preferences
        wrap_width = int(self.width / addon_prefs.WrapAmount)
        text = self.my_string_prop
        label_multiline(context, text, wrap_width, col)
        col.prop(self, "my_string_prop", icon='GREASEPENCIL')

        row = column.row(align=True)
        row.prop(self, "node_inputs")
        row.prop(self, "node_outputs")

        layout.prop(self, "show_in_single_node")

    # Optional: custom label
    # Explicit user label overrides, but here we can define a label dynamically
    def draw_label(self):
        return self.my_title_prop

    def update(self):
        if self.node_image:
            bpy.data.images[self.node_image].use_fake_user = True

        if not len(self.inputs) == self.node_inputs:
            for input in self.inputs:
                self.inputs.remove(input)
            for i in range(self.node_inputs):
                i += 1
                self.node_input_name = str(i)
                i = self.inputs.new(
                    'MindmapNodeSocketType',
                    name=self.node_input_name
                )
                i.display_shape = 'SQUARE_DOT'

        if not len(self.outputs) == self.node_outputs:
            for output in self.outputs:
                self.outputs.remove(output)
            for j in range(self.node_outputs):
                j += 1
                self.node_output_name = str(j)
                j = self.outputs.new(
                    'MindmapNodeSocketType',
                    name=self.node_output_name
                )
                j.display_shape = 'SQUARE_DOT'
