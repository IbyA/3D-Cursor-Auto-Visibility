bl_info = {
    "name": "Show/Hide3D Cursor",
    "author": "Iby. Thanks to help given from ScaredyFish and Iceythe and Nick0",
    "version": (1.2, 0),
    "blender": (2, 80, 0),
    "location": "",
    "description": "Shows and Hides the 3D Cursor and make modifications based on that",
    "warning": "",
    "wiki_url": "",
    "category": "3D Cursor",
}

import bpy

def current_tool(context):
    tools = context.workspace.tools
    return tools.from_space_view3d_mode(context.mode).idname

#Reveal the 3D Cursor and set as active tool. Hides automatically when tool is changed
class Custom3DCursorOperator(bpy.types.Operator):
    """Reveal the 3D Cursor and set as active tool. Hides automatically when tool is changed"""
    bl_idname = "wm.custom3dcursor"
    bl_label = "Custom 3D Cursor"
    bl_description = "Reveal the 3D Cursor and set as active tool. Hides automatically when tool is changed"

    def modal(self, context, event):
        if current_tool(context) != 'builtin.cursor':
            context.space_data.overlay.show_cursor = False
            return {'CANCELLED'}
        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        context.space_data.overlay.show_cursor = True
        bpy.ops.wm.tool_set_by_id(name='builtin.cursor')
        
        wm = context.window_manager
        wm.modal_handler_add(self)
        return {'RUNNING_MODAL'}
    
def main(context):
    for ob in context.scene.objects:
        print(ob)

#Reveal the 3D Cursor and modify its location.    
class Custom3DCursorOnOperator(bpy.types.Operator):
    """Shows the 3D Cursor and modify its location"""
    bl_idname = "wm.showmodify_custom3dcursor"
    bl_label = "Show and Modify 3D Cursor"
    bl_description = "Shows the 3D Cursor and modify its location"
    bl_options = {'REGISTER','UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        context.space_data.overlay.show_cursor = True
        bpy.ops.wm.tool_set_by_id(name='builtin.cursor')
        return {'FINISHED'}
    
#Hide the 3D Cursor and set box select a sactive tool. 
class Custom3DCursorOffOperator(bpy.types.Operator):
    """Hides the 3D Cursor and switches to box select mode"""
    bl_idname = "wm.hidecancel_custom3dcursor"
    bl_label = "Hide and Cancel 3D Cursor"
    bl_description = "Hides the 3D Cursor and switches to box select mode"
    bl_options = {'REGISTER','UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        context.space_data.overlay.show_cursor = False
        bpy.ops.wm.tool_set_by_id(name='builtin.select_box')
        return {'FINISHED'}
    
#Toggle the 3D Cursor and toggle 3D Cursor or box select as active tool.  
class Custom3DCursorToggleOperator(bpy.types.Operator):
    """Works a bit like the previous Operators but toggles between them instead"""
    bl_idname = "wm.toggle_custom3dcursor"
    bl_label = "Toggle 3D Cursor"
    bl_description = "Toggles 3D Cursor - Showsandmodify/Hideandcancel"
    bl_options = {'REGISTER','UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        if context.space_data.overlay.show_cursor == True:
            context.space_data.overlay.show_cursor = False
            bpy.ops.wm.tool_set_by_id(name='builtin.select_box')
        else:
            context.space_data.overlay.show_cursor = True
            bpy.ops.wm.tool_set_by_id(name='builtin.cursor')
        return {'FINISHED'}
    
def register():
    bpy.utils.register_class(Custom3DCursorOperator)
    bpy.utils.register_class(Custom3DCursorOnOperator)
    bpy.utils.register_class(Custom3DCursorOffOperator)
    bpy.utils.register_class(Custom3DCursorToggleOperator)
    


def unregister():
    bpy.utils.unregister_class(Custom3DCursorOperator)
    bpy.utils.unregister_class(Custom3DCursorOnOperator)
    bpy.utils.unregister_class(Custom3DCursorffOnOperator)
    bpy.utils.unregister_class(Custom3DCursorToggleOperator)


if __name__ == "__main__":
    register()
