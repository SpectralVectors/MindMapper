import bpy
import os


class MindMapperPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    image_folder = os.path.join(os.path.dirname(__file__), "images")

    node_images_dir: bpy.props.StringProperty(
        name="",  #
        subtype='DIR_PATH',  # noqa f821
        default=image_folder
    )

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
        column.label(text='Image Folder:')
        column.prop(self, 'node_images_dir')
