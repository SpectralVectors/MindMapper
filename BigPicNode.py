import bpy
import gpu
import os
from gpu_extras.batch import batch_for_shader
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
                pic_size = node.my_pic_size
                position = node.location
                filepath = node.my_pic
                image_name = bpy.path.basename(filepath)
                image = bpy.data.images[image_name]
                texture = gpu.texture.from_image(image)

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

                width = image.size[0] * pic_size * scale_x
                height = image.size[1] * pic_size * scale_y

                x = draw_position[0] + (node.width * scale_x)
                y = draw_position[1] - height

                try:
                    shader = gpu.shader.from_builtin('IMAGE')
                except NameError:
                    shader = gpu.shader.from_builtin('2D_IMAGE')

                batch = batch_for_shader(
                    shader, 'TRI_FAN',
                    {
                        "pos": (
                            (x, y),
                            (x + width, y),
                            (x + width, y + height),
                            (x, y + height)
                        ),
                        "texCoord": (
                            (0, 0),
                            (1, 0),
                            (1, 1),
                            (0, 1)
                        ),
                    },
                )
                shader.bind()
                shader.uniform_sampler("image", texture)
                batch.draw(shader)


def add_pic(self, context):
    filepath = self.my_pic
    bpy.ops.image.open(filepath=filepath)
    bpy.ops.image.pack()


# BigPic Node
class BigPicNode(Node, MindmapTreeNode):
    '''A Big Picture only node'''
    # Optional. If not explicitly defined, the python class name is used.
    bl_idname = 'BigPicNodeType'
    # Label for nice name display
    bl_label = "BigPic"
    # Icon identifier
    bl_icon = 'NONE'  # 'OUTLINER_OB_FONT'

    # === Custom Properties ===
    my_title_prop: bpy.props.StringProperty(
        name='',
        default='BigPic'  # noqa: F821
    )

    my_node_color: bpy.props.FloatVectorProperty(
        name='',
        default=(0.6, 0, 0),
        min=0.0,
        max=1.0,
        subtype='COLOR',  # noqa: F821
    )

    my_pic_size: bpy.props.FloatProperty(
        name='Size',  # noqa: F821
        default=1.0,
        soft_min=0.01,
        soft_max=10,
    )

    default_image = os.path.join(
        os.path.dirname(__file__),
        "images//SVAvatar.png"
    )

    my_pic: bpy.props.StringProperty(
        name='',  # noqa: F821
        default=default_image,  # noqa: F821
        subtype='FILE_PATH',  # noqa: F821
        update=add_pic
    )

    _handle = None

    # === Optional Functions ===
    # Initialization function, called when a new node is created.
    def init(self, context):
        self.use_custom_color = True
        self.color = (0.2, 0.2, 0.2)
        self.width = 20
        self.hide = True
        filepath = self.my_pic
        bpy.ops.image.open(filepath=filepath)
        bpy.ops.image.pack()
        bpy.ops.node.draw_big_pic(
            'INVOKE_DEFAULT',
            node_name=self.name,
        )

    # Copy function to initialize a copied node from an existing one.
    def copy(self, node):
        print("Copying from node ", node)
        bpy.ops.node.draw_big_pic(
            'INVOKE_DEFAULT',
            node_name=self.name,
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
        column.prop(self, "my_pic", icon='IMAGE')
        column.prop(self, "my_pic_size", icon='UV_SYNC_SELECT')

    # Detail buttons in the sidebar.
    # If function is not defined, the draw_buttons function is used instead
    def draw_buttons_ext(self, context, layout):
        column = layout.column()
        column.prop(self, "my_title_prop", icon='GREASEPENCIL')
        column.prop(self, "my_pic", icon='IMAGE')
        column.prop(self, "my_pic_size", icon='UV_SYNC_SELECT')

    def update(self):
        self.my_title_prop = self.my_title_prop


class DrawBigPicOperator(bpy.types.Operator):
    bl_idname = "node.draw_big_pic"
    bl_label = "Draw Big Picture Operator"

    node_name: bpy.props.StringProperty()
    # draw_text: bpy.props.StringProperty()

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
                'BACKDROP'  # BACKDROP or POST_PIXEL
            )
            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}
        elif self._handle:
            context.space_data.draw_handler_remove(self._handle, 'WINDOW')
            return {'FINISHED'}
        else:
            return {'CANCELLED'}
