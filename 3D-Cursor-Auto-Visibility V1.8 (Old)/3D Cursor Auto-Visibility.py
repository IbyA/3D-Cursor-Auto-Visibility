bl_info = {
    "name": "3D Cursor Auto-Visibility",
    "author": "Iby. Thanks to assistance given by ScaredyFish and Iceythe",
    "version": (1.8, 0),
    "blender": (2, 80, 0),
    "location": "",
    "description": "Press'\' or 'C' key to reveal the 3D Cursor and sets as acive tool but then when a different shortcut for a different tool, it automatically hides. The add-on, also respects the users who prefer the 3D Cursor visibility permanently on too via an if statement checking whether the 3d cursor is already visible or not. ",
    "warning": "Remember to Hide the 3D Cursor in teh Viewport Overlays First",
    "wiki_url": "",
    "category": "Object Mode",
}

import bpy

def current_tool(context):
    tools = context.workspace.tools
    return tools.from_space_view3d_mode(context.mode).idname

class Auto3DCursorvisibilityOperator(bpy.types.Operator):
    """Reveal and Set tool to 3D Cursor and Auto-hide 3D Cursor when you use a different tool if the 3D Cursor visibility is already off"""
    bl_idname = "wm.3dcursor_autovisibility"
    bl_label = "3D Cursor Auto-Visibility"
    bl_description = "Reveal and Set tool to 3D Cursor and Auto-hide 3D Cursor when you use a different tool"

    def modal(self, context, event):
        if current_tool(context) != 'builtin.cursor':
            # Auto-hides3D Cursor when you use a different tool
            context.space_data.overlay.show_cursor = False
            return {'CANCELLED'}
        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        # Reveal and Set tool to 3D Cursor if the 3D Cursor visibility is already off
        # Otherwise just set tool to 3D Cursor as normal and bypass the Auto-hide 3D Cursor code (respects users who want it on permanently)
        if context.space_data.overlay.show_cursor == False:
            context.space_data.overlay.show_cursor = True
            bpy.ops.wm.tool_set_by_id(name='builtin.cursor')
        else:
            bpy.ops.wm.tool_set_by_id(name='builtin.cursor')
            return {'FINISHED'}

        wm = context.window_manager
        wm.modal_handler_add(self)
        return {'RUNNING_MODAL'}


def register():
    bpy.utils.register_class(Auto3DCursorvisibilityOperator)

    # Add a Keymap
    kc = bpy.context.window_manager.keyconfigs.addon
    km = kc.keymaps.get('Object Mode')
    if not km:
        km = kc.keymaps.new('Object Mode', space_type='EMPTY')

    # replace 3D Cursor Shortcut with 'C' if keymap user preference is set to Industry Compatible. (Requires Restarting Blender after setting preferences)
    if bpy.context.window_manager.keyconfigs.active.name == "industry_compatible":
        kmi = km.keymap_items.new("wm.3dcursor_autovisibility", "C", "PRESS")
    else:
        kmi = km.keymap_items.new("wm.3dcursor_autovisibility", "BACK_SLASH", "PRESS")

def unregister():
    bpy.utils.register_class(Auto3DCursorvisibilityOperator)


if __name__ == "__main__":
    register()
