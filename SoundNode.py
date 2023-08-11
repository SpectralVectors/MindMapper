import bpy
import aud
from bpy.types import Node
from . MindmapNodeBase import MindmapTreeNode


def play_status(self, context):
    device = aud.Device()
    sound = aud.Sound(self.sound)
    if self.playing:
        device.play(sound)
    else:
        device.stopAll()


# Sound Node
class SoundNode(Node, MindmapTreeNode):
    '''A Sound file node'''
    # Optional. If not explicitly defined, the python class name is used.
    bl_idname = 'SoundNodeType'
    # Label for nice name display
    bl_label = "Sound"
    # Icon identifier
    bl_icon = 'PLAY_SOUND'

    # === Custom Properties ===
    my_title_prop: bpy.props.StringProperty(
        name='',
        default='Sound'  # noqa: F821
    )

    my_node_color: bpy.props.FloatVectorProperty(
        name='',
        default=(0.6, 0, 0),
        subtype='COLOR',  # noqa: F821
    )

    sound: bpy.props.StringProperty(
        name='Sound',  # noqa: F821
        description='Load a custom sound from your computer',
        subtype='FILE_PATH',  # noqa: F821
        default='',
        maxlen=1024,
    )

    show_in_single_node: bpy.props.BoolProperty(
        name='Show Shortcuts in Node (single)',
        default=True,
    )

    playing: bpy.props.BoolProperty(
        name='',
        default=False,
        update=play_status
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
        box = layout.box()
        box = box.column(align=True)
        box.prop(self, 'sound')
        if not self.sound == '':
            box.prop(
                self,
                'playing',
                icon='PLAY' if not self.playing else 'SNAP_FACE'
            )

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
        self.my_string_prop = self.my_string_prop
