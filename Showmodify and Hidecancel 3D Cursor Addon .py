bl_info = {
    "name": "Show/Hide3D Cursor",
    "author": "ScaredyFish and Iby",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "",
    "description": "Shows and Hides the 3D Cursor and make modifications based on that",
    "warning": "",
    "wiki_url": "",
    "category": "3D Cursor",
}

import bpy


def main(context):
    for ob in context.scene.objects:
        print(ob)


class Custom3DCursorOnOperator(bpy.types.Operator):
    """Shows the 3D Cursor and modify its location"""
    bl_idname = "wm.showmodify_3dcursor"
    bl_label = "Show and modify 3D Cursor"
    bl_description = "Shows the 3D Cursor and modify its location"
    bl_options = {'REGISTER','UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        context.space_data.overlay.show_cursor = True
        bpy.ops.wm.tool_set_by_id(name='builtin.cursor')
        main(context)
        return {'FINISHED'}

class Custom3DCursorOffOperator(bpy.types.Operator):
    """Hides the 3D Cursor and switches to box select mode"""
    bl_idname = "wm.hidecancel_3dcursor"
    bl_label = "Hide and Cancel the 3D Cursor"
    bl_description = "Hides the 3D Cursor and switches to box select mode"
    bl_options = {'REGISTER','UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        context.space_data.overlay.show_cursor = False
        bpy.ops.wm.tool_set_by_id(name='builtin.select_box')
        main(context)
        return {'FINISHED'}

def register():
    bpy.utils.register_class(Custom3DCursorOnOperator)
    bpy.utils.register_class(Custom3DCursorOffOperator)


def unregister():
    bpy.utils.unregister_class(Custom3DCursorOnOperator)
    bpy.utils.unregister_class(Custom3DCursoffOnOperator)


if __name__ == "__main__":
    register()
