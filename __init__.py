bl_info = {
    "name" : "Mituls - Symmetry",
    "author" : "Neil V. Moore, Mario Ilieski",
    "description" : 'Slice, cut, or mirror a mesh object easily',
    "blender" : (4, 0, 0),
    "version" : (1, 0, 0),
    "location" : "View3D",
    "warning" : "",
    "category" : "Generic"
}

# -----------------------------------------------------------------------------
#   Import Classes and/or functions     
# -----------------------------------------------------------------------------  

import bpy

from .                      import icons

from . properties           import NTZSYM_ignitproperties
from . main_ot              import NTZSYM_OT_ntzperformsym
from . addonPrefs           import NTZSYM_OT_addonprefs
from . panels               import NTZSYM_PT_ntzsym
from . misc_ot              import NTZSYM_OT_NtzResetAllSettings
from . misc_ot              import NTZSYM_OT_applyorremovemodifier

from . main_ot import (
    NTZSYM_OT_sliceX,
    NTZSYM_OT_sliceY,
    NTZSYM_OT_sliceZ,
    NTZSYM_OT_cutX_Forward,
    NTZSYM_OT_cutX_Backward,
    NTZSYM_OT_cutY_Forward,
    NTZSYM_OT_cutY_Backward,
    NTZSYM_OT_cutZ_Forward,
    NTZSYM_OT_cutZ_Backward,
    NTZSYM_OT_mirrorX_Forward,
    NTZSYM_OT_mirrorX_Backward,
    NTZSYM_OT_mirrorY_Forward,
    NTZSYM_OT_mirrorY_Backward,
    NTZSYM_OT_mirrorZ_Forward,
    NTZSYM_OT_mirrorZ_Backward
)

from . import keymaps

PendingDeprecationWarning

bDebugModeActive = False
if bDebugModeActive:
    print("##################################################################################################################################################################")
    print("REMINDER: DEBUG MODE ACTIVE")
    print("##################################################################################################################################################################")

# -----------------------------------------------------------------------------
#    Store classes in List so that they can be easily registered/unregistered    
# -----------------------------------------------------------------------------  

classes = (
    NTZSYM_ignitproperties,
    NTZSYM_OT_ntzperformsym,
    NTZSYM_OT_addonprefs,
    NTZSYM_PT_ntzsym,
    NTZSYM_OT_NtzResetAllSettings,
    NTZSYM_OT_applyorremovemodifier,
    NTZSYM_OT_sliceX,
    NTZSYM_OT_sliceY,
    NTZSYM_OT_sliceZ,
    NTZSYM_OT_cutX_Forward,
    NTZSYM_OT_cutX_Backward,
    NTZSYM_OT_cutY_Forward,
    NTZSYM_OT_cutY_Backward,
    NTZSYM_OT_cutZ_Forward,
    NTZSYM_OT_cutZ_Backward,
    NTZSYM_OT_mirrorX_Forward,
    NTZSYM_OT_mirrorX_Backward,
    NTZSYM_OT_mirrorY_Forward,
    NTZSYM_OT_mirrorY_Backward,
    NTZSYM_OT_mirrorZ_Forward,
    NTZSYM_OT_mirrorZ_Backward
)

# -----------------------------------------------------------------------------
#    Register classes from the classes list
# -----------------------------------------------------------------------------    

addon_keymaps = []

#vscode pme workaround from iceythe (part 1 of 2)
def _reg():
    pme = bpy.utils._preferences.addons['pie_menu_editor'].preferences
    for pm in pme.pie_menus:
        if pm.key != 'NONE':
            pm.register_hotkey()
#END vscode pme workaround (part 1 of 2)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    # update panel name
    prefs = bpy.context.preferences.addons[__name__].preferences
    addonPrefs.update_panel(prefs, bpy.context)

    #add keymaps from keymaps.py
    keymaps.ntzSym_regKMs(addon_keymaps)


    #add property group to the scene
    bpy.types.Scene.ntzSym = bpy.props.PointerProperty(type=NTZSYM_ignitproperties)

    #add a pointerProperty to all objects in the scene so that the mirrorEmpty can keep track of the object --> mirror modifier it will be parented to
    bpy.types.Object.mirrorParent = bpy.props.PointerProperty(type=bpy.types.Object)

    if prefs.rememberOrientAndLocOnUndo:
        # load undo/redo handlers so that scene properties get restored on undo/redo or when adjusting operator properties
        miscFunc.load_handler()

    #vscode pme workaround from iceythe (part 2 of 2)
    #must be appended to def register() so that it is the last thing that executes
    if bDebugModeActive:
        if not bpy.app.timers.is_registered(_reg):
            bpy.app.timers.register(_reg, first_interval=1)
    #END vscode pme workaround (part 2 of 2)

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)

    #remove keymaps
    keymaps.ntzSym_unregKMs(addon_keymaps)

    # unload the undo/redo handlers for restoring scene properties
    miscFunc.unload_handler()

if __name__ == "__main__":
    register()

    # test call
    bpy.ops.ntz_sym.performsym()