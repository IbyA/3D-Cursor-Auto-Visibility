bl_info = {
    "name": "3D Cursor Auto-Visibility+",
    "description": "Press'Back Slash' or 'C' key to Reveal and Set tool to 3D "
                    " Auto-hide 3D Cursor when you use a different tool."
                    "Cursor (Only when the 3D Cursor is already invisible "
                    "[Respects user who dont want to it Hidden or auto-hide])."
                    " Tap to toggle or Hold down/Release ';' to change the 3D "
                    "Cursor visibility and switch tools between 3D Cursor or "
                    "Previous tool." ,
    "author": "Iby and Iceythe",
    "version": (2, 0),
    "blender": (2, 80, 0),
    "location": "3D View",
    "category": "3D View",
}

import bpy
from time import perf_counter
from bpy.props import StringProperty, BoolProperty

def current_tool(context):
    tools = context.workspace.tools
    return tools.from_space_view3d_mode(context.mode).idname


class VIEW3D_3d_cursor_autovisibility_operator(bpy.types.Operator):
    bl_idname = "view3d.3dcursor_autovisibility"
    bl_label = "3D Cursor Auto-Visibility"
    bl_description = ("Reveal and Set tool to 3D Cursor. 3D Cursor Auto-hides "
                      "when you use a different tool")

    @classmethod
    def poll(cls, context):
        return context.area.type == 'VIEW_3D'

    def modal(self, context, event):
        if current_tool(context) != 'builtin.cursor':
            # Automatically Hide the 3D Cursor when you use a different tool
            context.space_data.overlay.show_cursor = False
            return {'CANCELLED'}
        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        overlay = context.space_data.overlay
        # Reveal and Set tool to 3D Cursor (Only when the 3D Cursor is already
        # invisible[Respects user who dont want to it Hidden or auto-hide])
        bpy.ops.wm.tool_set_by_id(name='builtin.cursor')
        if not overlay.show_cursor:
            overlay.show_cursor = True
        else:
            return {'FINISHED'}

        wm = context.window_manager
        wm.modal_handler_add(self)
        return {'RUNNING_MODAL'}


class VIEW3D_Tap_or_Hold_3D_Cursor_Operator(bpy.types.Operator):
    bl_idname = "wm.taporhold_3dcursor_visibility"
    bl_label = "Tap or Hold for 3D Cursor Visibility"
    bl_description = ("Tap shortcut to toggle or Hold Down/Release to control "
                      "3D Cursor visibility and previous tool")
    bl_options = {'REGISTER', 'UNDO'}

    # Poll to block the operator from repeated hotkey triggers
    @classmethod
    def poll(cls, context):
        return (context.area.type == 'VIEW_3D' and
                not getattr(cls, "running", False))

    # Clean-up when done
    def exit(self, context):
        __class__.running = False
        context.window_manager.event_timer_remove(self.handler)
        return {'FINISHED'}

    # Restore the active tool and hide the cursor on key released
    def restore(self, context, overlay):
        prev_tool = getattr(__class__, "prev_tool", "builtin.cursor")
        overlay.show_cursor = False
        bpy.ops.wm.tool_set_by_id(name=prev_tool)
        return self.exit(context)

    def modal(self, context, event):
        timeout = perf_counter() > self.timeout
        overlay = context.space_data.overlay

        if event.type == self.key_type and event.value == 'RELEASE':

            # Toggle cursor on and exit only if key is tapped
            if not overlay.show_cursor and not timeout:
                overlay.show_cursor = True
                bpy.ops.wm.tool_set_by_id(name='builtin.cursor')
                return self.exit(context)

            return self.restore(context, overlay)

        if timeout:
            # Reveal and Set tool to 3D Cursor when held down
            # Note: Dragging the 3D Cursor only works 50% of the time. There is
            # a conflict between the operator and dragging the 3D Cursor
            # function when button is held down.(requires going deep into
            # Blender's code to fix this) However, you can still move the
            # 3D Cursor's position via clicking instead of dragging the 3D
            # Cursors positon. I Was trying to make it work a bit like
            # Maya's 'D' Key)
            overlay.show_cursor = True
            bpy.ops.wm.tool_set_by_id(name='builtin.cursor')
        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        cls = __class__

        if not getattr(cls, "running", False):

            cls.running = True
            cls.prev_tool = getattr(cls, "prev_tool", None)
            cur_tool = current_tool(context)

            # Only store previous tool if it's not "builtin.cursor"
            if cur_tool != "builtin.cursor":
                cls.prev_tool = cur_tool

            # Uses perf_counter instead of event timer to set timeout
            # duration, since event timer doesn't reset and tends to bug out
            # Set hold down time speed here:  v
            self.timeout = perf_counter() + 0.25

            # Store key (from addon prefs) type on instance
            # and use it to compare event.type during modal
            p = context.preferences.addons[__name__].preferences
            self.key_type = p.kmi2_type

            wm = context.window_manager
            wm.modal_handler_add(self)

            # Still need this timer for modal refresh. makes the modal snappier
            self.handler = wm.event_timer_add(
                time_step=0.01, window=context.window)
            return {'RUNNING_MODAL'}

        return {'CANCELLED'}


# Callback function to set keymap item
# state based on preferences settings
def set_kmi_state(self, context):
    states = self.enable_auto_visibility, self.enable_toggle_cursor
    for (_, kmi), state in zip(addon_keymaps, states):
        kmi.active = state


class ToggleCursorPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    enable_auto_visibility: BoolProperty(
        name="3D Cursor Auto-Visibility",
        default=True, update=set_kmi_state)

    enable_toggle_cursor: BoolProperty(
        name="Tap or Hold for 3D Cursor Visibility",
        default=True, update=set_kmi_state)

    # for VIEW3D_3d_cursor_autovisibility_operator
    kmi1_type: StringProperty()
    kmi1_value: StringProperty()
    kmi1_alt: BoolProperty()
    kmi1_ctrl: BoolProperty()
    kmi1_shift: BoolProperty()

    # for VIEW3D_Tap_or_Hold_3D_Cursor_Operator
    kmi2_type: StringProperty()
    kmi2_value: StringProperty()
    kmi2_alt: BoolProperty()
    kmi2_ctrl: BoolProperty()
    kmi2_shift: BoolProperty()


    def draw(self, context):
        layout = self.layout
        layout.separator()

        split = layout.split()
        col_1 = split.column()
        col_2 = split.column()

        self.ensure_kmis()
        kmi1, kmi2 = addon_keymaps[0][1], addon_keymaps[1][1]

        col_1.prop(self, "enable_auto_visibility", toggle=True)

        row = col_1.row()
        if not self.enable_auto_visibility:
            row.enabled = False
        draw_kmi(kmi1, layout, row)

        col_2.prop(self, "enable_toggle_cursor", toggle=True)

        row = col_2.row()
        if not self.enable_toggle_cursor:
            row.enabled = False
        draw_kmi(kmi2, layout, row)

    # when the user changes a key, the ui is redrawn and is called to sync
    # kmi_type, kmi_alt, kmi_ctrl and kmi_shift with actual kmi values
    def ensure_kmis(self):
        kmi1_1, kmi1_2 = [kmi for km, kmi in addon_keymaps][::2]
        kmi2_1, kmi2_2 = [kmi for km, kmi in addon_keymaps][1::2]

        # object mode / mesh
        # for VIEW3D_3d_cursor_autovisibility_operator
        if self.kmi1_type != kmi1_1.type:
            self.kmi1_type = kmi1_1.type
        if kmi1_2.type != kmi1_1.type:
            kmi1_2.type = kmi1_1.type

        if self.kmi1_value != kmi1_1.value:
            self.kmi1_value = kmi1_1.value
        if kmi1_2.value != kmi1_1.value:
            kmi1_2.value = kmi1_1.value

        if self.kmi1_alt != kmi1_1.alt:
            self.kmi1_alt = kmi1_1.alt
        if kmi1_2.alt != kmi1_1.alt:
            kmi1_2.alt = kmi1_1.alt

        if self.kmi1_ctrl != kmi1_1.ctrl:
            self.kmi1_ctrl = kmi1_1.ctrl
        if kmi1_2.ctrl != kmi1_1.ctrl:
            kmi1_2.ctrl = kmi1_1.ctrl

        if self.kmi1_shift != kmi1_1.shift:
            self.kmi1_shift = kmi1_1.shift
        if kmi1_2.shift != kmi1_1.shift:
            kmi1_2.shift = kmi1_1.shift

        # for VIEW3D_Tap_or_Hold_3D_Cursor_Operator
        if self.kmi2_type != kmi2_1.type:
            self.kmi2_type = kmi2_1.type

        if kmi2_2.type != kmi2_1.type:
            kmi2_2.type = kmi2_1.type

        if self.kmi2_value != kmi2_1.value:
            self.kmi2_value = kmi2_1.value
        if kmi2_2.value != kmi2_1.value:
            kmi2_2.value = kmi2_1.value

        if self.kmi2_alt != kmi2_1.alt:
            self.kmi2_alt = kmi2_1.alt
        if kmi2_2.alt != kmi2_1.alt:
            kmi2_2.alt = kmi2_1.alt

        if self.kmi2_ctrl != kmi2_1.ctrl:
            self.kmi2_ctrl = kmi2_1.ctrl
        if kmi2_2.ctrl != kmi2_1.ctrl:
            kmi2_2.ctrl = kmi2_1.ctrl

        if self.kmi2_shift != kmi2_1.shift:
            self.kmi2_shift = kmi2_1.shift
        if kmi2_2.shift != kmi2_1.shift:
            kmi2_2.shift = kmi2_1.shift

# ui draw function for kmi
def draw_kmi(kmi, layout, col):
    col = col.column()
    col.label(text=kmi.name)
    row = col.row()
    row.scale_y = 1.3
    row.alignment = 'LEFT'
    row.label(text="Hotkey")
    row.prop(kmi, "type", text="", full_event=True)

    col.separator(factor=1)
    row = col.row()
    row.prop(kmi, "value")

    col.separator(factor=2)
    row = col.row(align=True)
    row.label(text="Modifier")

    row.prop(kmi, "any", toggle=True)
    row.prop(kmi, "shift", toggle=True)
    row.prop(kmi, "ctrl", toggle=True)

    row = col.row(align=True)
    split = row.split(align=True)
    split.separator()

    split.prop(kmi, "alt", toggle=True)
    split.prop(kmi, "oskey", text="Cmd", toggle=True)
    split.prop(kmi, "key_modifier", text="", event=True)


addon_keymaps = []
disabled = []

classes = [
    VIEW3D_3d_cursor_autovisibility_operator,
    VIEW3D_Tap_or_Hold_3D_Cursor_Operator,
    ToggleCursorPreferences,
]

# Set 3D Cursor visible state at register and unregister
def set_cursor_visible(state):
    for window in bpy.context.window_manager.windows:
        for area in window.screen.areas:
            if area.type == 'VIEW_3D':
                area.spaces.active.overlay.show_cursor = state


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    wm = bpy.context.window_manager
    p = bpy.context.preferences.addons[__name__].preferences

    # During addon registration, get the kmi values stored in preferences.
    # If they are none (usually after install), resort to default value
    # Set default keymaps for VIEW3D_3d_cursor_autovisibility_operator
    # Replace "C" if using industry compatible keymap otherwise "BACK_SLASH"
    is_industry = wm.keyconfigs.active.name == "industry_compatible"
    default1_type = (is_industry and "C") or "BACK_SLASH"
    default1_value = "PRESS"

    kmi1_type = p.kmi1_type or default1_type
    kmi1_value = p.kmi1_value or default1_value

    alt1 = p.kmi1_alt or 0
    ctrl1 = p.kmi1_ctrl or 0
    shift1 = p.kmi1_shift or 0

    # Set default keymaps for VIEW3D_Tap_or_Hold_3D_Cursor_Operator
    default2_type = "SEMI_COLON"
    default2_value = "PRESS"

    kmi2_type = p.kmi2_type or default2_type
    kmi2_value = p.kmi2_value or default2_value

    alt2 = p.kmi2_alt or 0
    ctrl2 = p.kmi2_ctrl or 0
    shift2 = p.kmi2_shift or 0

    kc = wm.keyconfigs.addon

    # Create Keymaps in Object Mode
    km = kc.keymaps.get("Object Mode")
    if not km:
        km = kc.keymaps.new("Object Mode")

    args = "view3d.3dcursor_autovisibility", kmi1_type, kmi1_value
    kmi = km.keymap_items.new(*args, alt=alt1, ctrl=ctrl1, shift=shift1)
    kmi.active = p.enable_auto_visibility
    addon_keymaps.append((km, kmi))

    args = "wm.taporhold_3dcursor_visibility", kmi2_type, kmi2_value
    kmi = km.keymap_items.new(*args, alt=alt2, ctrl=ctrl2, shift=shift2)
    kmi.active = p.enable_toggle_cursor
    addon_keymaps.append((km, kmi))

    # Create Keymaps in Edit Mode
    km = kc.keymaps.get("Mesh")
    if not km:
        km = kc.keymaps.new("Mesh")

    args = "view3d.3dcursor_autovisibility", kmi1_type, kmi1_value
    kmi = km.keymap_items.new(*args, alt=alt1, ctrl=ctrl1, shift=shift1)
    kmi.active = p.enable_auto_visibility
    addon_keymaps.append((km, kmi))

    args = "wm.taporhold_3dcursor_visibility", kmi2_type, kmi2_value
    kmi = km.keymap_items.new(*args, alt=alt2, ctrl=ctrl2, shift=shift2)
    kmi.active = p.enable_toggle_cursor
    addon_keymaps.append((km, kmi))
    # We tried to put the keymap to '3D View' but caused a lot of conflicts
    # with the default keymaps and wasn't being overrriden. So we put it
    # into 'Object Mode' and 'Mesh' (Edit Mode).

    # Hide 3D Cursor when enableing Addon
    set_cursor_visible(False)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)

    addon_keymaps.clear()

    # Show 3D Cursor when disabling Addon
    set_cursor_visible(True)
