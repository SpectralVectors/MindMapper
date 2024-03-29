import bpy
import blf
from bpy.types import Node
from . MindmapNodeBase import MindmapTreeNode


def draw_callback_px(self, context):
    space = context.space_data
    editor = space.type
    if space and editor == 'NODE_EDITOR':
        if space.node_tree:
            nodes = space.node_tree.nodes
            if self.node_name in nodes:
                node = nodes[self.node_name]
                font_id = node.my_font
                text_size = node.my_text_size
                position = node.location
                big_text = node.my_title_prop
                color = node.my_node_color
                shadow = node.shadow_color

                blf.color(font_id, *color, 1)
                blf.enable(font_id, blf.SHADOW)
                blf.shadow(font_id, 3, *shadow)
                blf.shadow_offset(font_id, 3, -3)
                for region in context.area.regions:
                    if region.type == 'WINDOW':
                        view = region.view2d
                        draw_position = view.view_to_region(*position)

                        x1, y1 = view.region_to_view(0, 0)
                        x2, y2, = view.region_to_view(
                            region.width,
                            region.height
                        )

                        view_width = x2 - x1
                        view_height = y2 - y1

                        scale_x = region.width / view_width
                        scale_y = region.height / view_height

                blf.position(
                    font_id,
                    (draw_position[0] + (node.width * scale_x)),
                    (draw_position[1] - ((node.height / 4) * scale_y)),
                    0
                )
                blf.size(font_id, text_size * scale_x)
                blf.draw(font_id, big_text)
                blf.disable(font_id, blf.SHADOW)


# BigText Node
class BigTextNode(Node, MindmapTreeNode):
    '''A Big Text only node'''
    # Optional. If not explicitly defined, the python class name is used.
    bl_idname = 'BigTextNodeType'
    # Label for nice name display
    bl_label = "BigText"
    # Icon identifier
    bl_icon = 'NONE'  # 'OUTLINER_OB_FONT'

    # === Custom Properties ===
    my_title_prop: bpy.props.StringProperty(
        name='',
        default='BigText'  # noqa: F821
    )

    my_node_color: bpy.props.FloatVectorProperty(
        name='',
        default=(0.6, 0, 0),
        min=0.0,
        max=1.0,
        subtype='COLOR',  # noqa: F821
    )

    shadow_color: bpy.props.FloatVectorProperty(
        name='',
        size=4,
        default=(0, 0, 0, 0.5),
        min=0.0,
        max=1.0,
        subtype='COLOR',  # noqa: F821
    )

    my_text_size: bpy.props.IntProperty(
        name='Size',  # noqa: F821
        default=50,
        soft_min=4,
        soft_max=300,
    )

    my_font: bpy.props.IntProperty(
        name='Font ID',
        default=0,
        soft_min=0,
        soft_max=5,
    )

    _handle = None

    # === Optional Functions ===
    # Initialization function, called when a new node is created.
    def init(self, context):
        self.use_custom_color = True
        self.color = (0.1, 0.1, 0.1)
        self.width = 20
        self.hide = True
        bpy.ops.node.draw_big_text(
            'INVOKE_DEFAULT',
            node_name=self.name,
            draw_text=self.my_title_prop
        )

    # Copy function to initialize a copied node from an existing one.
    def copy(self, node):
        print("Copying from node ", node)
        bpy.ops.node.draw_big_text(
            'INVOKE_DEFAULT',
            node_name=self.name,
            draw_text=self.my_title_prop
        )

    # Free function to clean up on removal.
    def free(self):
        if self._handle:
            bpy.context.window_manager.modal_handler_remove(self._handle)
        print("Removing node ", self, ", Goodbye!")

    # Additional buttons displayed on the node.
    def draw_buttons(self, context, layout):
        column = layout.column()
        column.prop(self, "my_title_prop", icon='GREASEPENCIL')
        column.prop(self, "my_node_color", icon='MATERIAL')
        column.prop(self, "my_text_size", icon='TEXT')
        column.prop(self, "my_font", icon='OUTLINER_OB_FONT')
        column.prop(self, "shadow_color", icon='MATERIAL')

    # Detail buttons in the sidebar.
    # If function is not defined, the draw_buttons function is used instead
    def draw_buttons_ext(self, context, layout):
        column = layout.column()
        column.prop(self, "my_title_prop", icon='GREASEPENCIL')
        column.prop(self, "my_node_color", icon='MATERIAL')
        column.prop(self, "my_text_size", icon='TEXT')
        column.prop(self, "my_font", icon='OUTLINER_OB_FONT')
        column.prop(self, "shadow_color", icon='MATERIAL')

    def update(self):
        self.my_title_prop = self.my_title_prop


class DrawBigTextOperator(bpy.types.Operator):
    bl_idname = "node.draw_big_text"
    bl_label = "Draw Big Text Operator"

    node_name: bpy.props.StringProperty()
    draw_text: bpy.props.StringProperty()

    def modal(self, context, event):
        if context.space_data is not None:
            if context.space_data.type == 'NODE_EDITOR':
                context.area.tag_redraw()
                return {'PASS_THROUGH'}  # do not block execution
        else:
            return {'PASS_THROUGH'}

    def invoke(self, context, event):
        if context.space_data.type == 'NODE_EDITOR':
            self._handle = context.space_data.draw_handler_add(
                draw_callback_px,
                (self, context),
                'WINDOW',
                'POST_PIXEL'  # BACKDROP or POST_PIXEL
            )
            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}
        elif self._handle:
            context.space_data.draw_handler_remove(self._handle, 'WINDOW')
            return {'FINISHED'}
        else:
            return {'CANCELLED'}
