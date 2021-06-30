bl_info = {
    "name": "Mind Mapper",
    "author": "Spectral Vectors",
    "version": (0, 8, 4),
    "blender": (2, 90, 0),
    "location": "Mind Mapper - Custom Node Editor",
    "description": "A custom, node based flow chart for text",
    "warning": "",
    "doc_url": "",
    "category": "Custom Nodes",
}

from .Mindmapper import (
    MindmapTree,
    MindmapNode,
    MindMapperPreferences,
    MindmapNodeSocket,
    UpdateNodes,
    )

classes = (
    MindmapTree,
    MindmapNode,
    MindMapperPreferences,
    MindmapNodeSocket,
    UpdateNodes,
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