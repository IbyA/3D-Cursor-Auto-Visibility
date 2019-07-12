bl_info = {
    "name": "3D Cursor Auto-Visibility+",
    "author": "Iby. Thanks to assistance given by ScaredyFish and Iceythe",
    "version": (1.8, 0),
    "blender": (2, 80, 0),
    "location": "",
    "description": "Press '\' or 'C' key to reveal the 3D Cursor and sets as acive tool but then when a different shortcut for a different tool, it automatically hides. Tap or Hold and release ';' to toggle the 3D Cursor visibility and switch between 3D Cursor or Box Select tool",
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
        # Otherwise just set tool to 3D Cursor and bypass the Auto-hide 3D Cursor code (respects users who want it on permanently)
        if context.space_data.overlay.show_cursor == False:
            context.space_data.overlay.show_cursor = True
            bpy.ops.wm.tool_set_by_id(name='builtin.cursor')
        else:
            bpy.ops.wm.tool_set_by_id(name='builtin.cursor')
            return {'FINISHED'}

        wm = context.window_manager
        wm.modal_handler_add(self)
        return {'RUNNING_MODAL'}

class ToggleorHold3DCursorOperator(bpy.types.Operator):
    """Tap to toggle or Hold Down and release to control 3D Cursor visibility and active tool"""
    bl_idname = "wm.toggleorhold_3dcursor_visibility"
    bl_label = "Tap or Hold 3D Cursor Visibility"
    bl_description = "Tap to toggle or Hold Down and release to control 3D Cursor visibility and active tool"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Toggles the 3D Cursor's visibility. Also toggles active tool between 3D Cursor and Box select tool.
        if context.space_data.overlay.show_cursor == True:
            context.space_data.overlay.show_cursor = False
            bpy.ops.wm.tool_set_by_id(name='builtin.select_box')
        else:
            context.space_data.overlay.show_cursor = True
            bpy.ops.wm.tool_set_by_id(name='builtin.cursor')
        return {'FINISHED'}

    def modal(self, context, event):
        if event.type == 'SEMI_COLON' and event.value == 'PRESS':
            return {'RUNNING_MODAL'}

        elif event.type == 'SEMI_COLON' and event.value == 'RELEASE':

            if self.timeout:
                # Hide 3D Cursor on 'RELEASE' and Set current tool to Box Select
                context.space_data.overlay.show_cursor = False
                bpy.ops.wm.tool_set_by_id(name='builtin.select_box')
                return {'FINISHED'}

            wm = context.window_manager
            wm.event_timer_remove(self.handler)
            return self.execute(context)

        elif event.type == 'TIMER':
            self.timeout = True
            wm = context.window_manager
            wm.event_timer_remove(self.handler)

        if self.timeout:
            # Reveal and Set tool to 3D Cursor when held down
            # Note: Dragging the 3D Cursor only works 50% of the time. There is a conflict between operators button is held down. (requires going deep into Blender's code to fix this)
            # Note: you can still move the 3D Cursor's position via clicking instead of dragging the 3D Cursors positon
            context.space_data.overlay.show_cursor = True
            bpy.ops.wm.tool_set_by_id(name='builtin.cursor')

        return {'PASS_THROUGH'}


    def invoke(self, context, event):
        if event.value == 'PRESS':
            self.timeout = False
            wm = context.window_manager
            wm.modal_handler_add(self)
            self.handler = wm.event_timer_add(
                #Set hold down speed here
                time_step=0.25, window=context.window)
            return {'RUNNING_MODAL'}
        return {'CANCELLED'}

def register():
    bpy.utils.register_class(Auto3DCursorvisibilityOperator)
    bpy.utils.register_class(ToggleorHold3DCursorOperator)

    # add a keymap to backslash
    kc = bpy.context.window_manager.keyconfigs.addon
    km = kc.keymaps.get('Object Mode')
    if not km:
        km = kc.keymaps.new('Object Mode', space_type='EMPTY')

    if bpy.context.window_manager.keyconfigs.active.name == "industry_compatible":
        kmi = km.keymap_items.new("wm.3dcursor_autovisibility", "C", "PRESS")
    else:
        kmi = km.keymap_items.new("wm.3dcursor_autovisibility", "BACK_SLASH", "PRESS")
    # Make sure to change the shortcuts on lines 66 and 69 as well if you decide to change the shortcut below:
    kmi = km.keymap_items.new("wm.toggleorhold_3dcursor_visibility", "SEMI_COLON", "ANY")


def unregister():
    bpy.utils.unregister_class(Auto3DCursorvisibilityOperator)
    bpy.utils.unregister_class(ToggleorHold3DCursorOperator)


if __name__ == "__main__":
    register()
