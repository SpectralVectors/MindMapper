from nodeitems_utils import NodeCategory
from nodeitems_utils import NodeItem
from nodeitems_utils import register_node_categories
from nodeitems_utils import unregister_node_categories

from . Preferences import MindMapperPreferences
from . MindmapNodeBase import MindmapTree, MindmapNodeSocket
from . MindmapNode import MindmapNode
from . NoteNode import NoteNode

bl_info = {
    "name": "MindMapper",
    "author": "Spectral Vectors, tin2tin, Bazza, cannibalox",
    "version": (0, 9, 3),
    "blender": (2, 90, 0),
    "location": "Custom Node Editor, and Shader, Geometry, Compositor Nodes",
    "description": "A multi-line text and image flow chart node",
    "warning": "",
    "doc_url": "",
    "category": "Node",
}


# our own base class with an appropriate poll function,
# so the categories only show up in our own tree type
class MyNodeCategory(NodeCategory):
    @classmethod
    def poll(cls, context):
        ntrees = [
            'MindmapNodeTree',
            'ShaderNodeTree',
            'GeometryNodeTree'
        ]
        return [context.space_data.tree_type for ntree in ntrees]


class LayoutCategory(NodeCategory):
    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type == 'MindmapNodeTree'


# all categories in a list
node_categories = [
    # identifier, label, items list
    # This list will show up in all Node Editors
    MyNodeCategory('EXTRA', "Extra", items=[
        # our basic node
        NodeItem("MindmapNodeType"),
        NodeItem("NoteNodeType"),
    ]),
    # This is to add the Layout nodes to the Mindmapper Node Editor
    LayoutCategory('LAYOUT', "Layout", items=[
        NodeItem("NodeReroute"),
        NodeItem("NodeFrame"),
    ]),
]

classes = (
    MindmapTree,
    MindmapNode,
    MindMapperPreferences,
    MindmapNodeSocket,
    NoteNode,
)


def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    register_node_categories('Mindmap', node_categories)


def unregister():
    unregister_node_categories('Mindmap')

    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)


if __name__ == "__main__":
    register()
