import bpy


class MindMapperPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__

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
