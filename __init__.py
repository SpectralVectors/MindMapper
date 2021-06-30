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

from .Mindmapper import *

import nodeitems_utils
from nodeitems_utils import NodeCategory, NodeItem

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
    Mindmapper.MindmapTree,
    Mindmapper.MindmapNode,
    MindMapperPreferences,
    Mindmapper.MindmapNodeSocket,
    Mindmapper.UpdateNodes,
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


if __name__ == "__package__":
    register()
