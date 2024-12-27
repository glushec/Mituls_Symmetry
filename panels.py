import bpy
from . icons        import i as icons
from .              import misc_ot
from .              import miscLay
from .              import miscFunc

from bpy.props      import (StringProperty, BoolProperty, IntProperty, FloatProperty, FloatVectorProperty, EnumProperty, PointerProperty)
from bpy.types      import (Panel, Operator, AddonPreferences, PropertyGroup)

# -----------------------------------------------------------------------------
#   Panel
# ----------------------------------------------------------------------------- 

class NTZSYM_PT_ntzsym(Panel):

    bl_idname = "ntz_sym.panel"
    bl_label = "Symmetry v1.0"
    bl_category = "Mituls"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    bUseCompactSidebarPanel = BoolProperty(
        name="Use Compact Panel",
        description="Use Compact Panel",
        default = False
    )

    bUseCompactPopupAndPiePanel = BoolProperty(
        name="Use Compact Popup & Pie Panel",
        description="Use Compact Popup & Pie Panel",
        default = True
    )

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj and obj.type == 'MESH' and obj.mode == 'EDIT'

    def draw(self, context):

        scn = context.scene
        lay = self.layout.column(align=True)

        modeAtBegin = "OBJECT" #declare
        try:    modeAtBegin = bpy.context.object.mode
        except: pass

        selObjs = set(context.selected_objects)
        activeObj = context.view_layer.objects.active

        if modeAtBegin == "EDIT":
            editModeObjs = set(bpy.context.objects_in_mode)

            #combine selObjs and editModeObjs (useful for applying/removing modifiers in edit mode)
            selObjs = selObjs.union(editModeObjs)
        
        #determine if panel is inside of a popop/pie menu
        panelInsidePopupOrPie = context.region.type == 'WINDOW'

        if panelInsidePopupOrPie:

            if self.bUseCompactPopupAndPiePanel:
                lay.ui_units_x = 8
                lay.label(text="Symmetry")

            else:
                lay.ui_units_x = 13
                #lay.label(text="Mituls - Symmetry")


        compactPanelConditions = (panelInsidePopupOrPie and self.bUseCompactPopupAndPiePanel) or (not panelInsidePopupOrPie and self.bUseCompactSidebarPanel)

        if not compactPanelConditions:
            sepFactor = 1
            labelWidth = 2.75
        else:
            sepFactor = 0.25
            labelWidth = 1.75
        
        def opProperties(op, symType, axis, axisDir=None):
            op.symType = symType

            if not scn.ntzSym.cutLocation in ["UNSET"]: op.cutLocation = scn.ntzSym.cutLocation
            if not scn.ntzSym.cutRotation in ["UNSET"]: op.cutRotation = scn.ntzSym.cutRotation

            if scn.ntzSym.fillAfterCut == "FILL": op.use_fill = True
            else:                                 op.use_fill = False

            if scn.ntzSym.keepModifiers == "YES": op.keepModifiers = True
            else:                                 op.keepModifiers = False

            op.axis = axis

            if axisDir is not None:
                op.axisDir = axisDir

        emboss=False

        if not compactPanelConditions: labelHeight = 1.35
        else:                          labelHeight = 1

        # -----------------------------------------------------------------------------
        #   SLICE
        # -----------------------------------------------------------------------------
        main_row = lay.row(align=True)
        main_row.scale_y = 1.5
        
        # Label section
        label_section = main_row.row(align=True)
        label_section.alignment = "RIGHT"
        label_section.ui_units_x = labelWidth
        label_section.label(text="Slice:")
        
        # Button section
        button_section = main_row.grid_flow(row_major=True, columns=3, even_columns=True, align=True)
        
        # Buttons
        sop1 = button_section.operator("ntzsym.slice_x", text='', icon_value=icons['xIcon'], emboss=True)
        sop2 = button_section.operator("ntzsym.slice_y", text='', icon_value=icons['yIcon'], emboss=True)
        sop3 = button_section.operator("ntzsym.slice_z", text='', icon_value=icons['zIcon'], emboss=True)
        
        lay.separator(factor=sepFactor)

        # -----------------------------------------------------------------------------
        #   CUT
        # -----------------------------------------------------------------------------
        main_row = lay.row(align=True)
        main_row.scale_y = 1.5
        
        # Label section
        label_section = main_row.row(align=True)
        label_section.alignment = "RIGHT"
        label_section.ui_units_x = labelWidth
        label_section.label(text="Cut:")
        
        # Button section
        button_section = main_row.grid_flow(row_major=True, columns=6, even_columns=True, align=True)
        
        # Buttons
        cop1 = button_section.operator("ntzsym.cut_x_backward", text='', icon_value=icons['xIconLeft'], emboss=True)
        cop2 = button_section.operator("ntzsym.cut_x_forward", text='', icon_value=icons['xIconRight'], emboss=True)
        cop3 = button_section.operator("ntzsym.cut_y_backward", text='', icon_value=icons['yIconLeft'], emboss=True)
        cop4 = button_section.operator("ntzsym.cut_y_forward", text='', icon_value=icons['yIconRight'], emboss=True)
        cop5 = button_section.operator("ntzsym.cut_z_backward", text='', icon_value=icons['zIconLeft'], emboss=True)
        cop6 = button_section.operator("ntzsym.cut_z_forward", text='', icon_value=icons['zIconRight'], emboss=True)
        
        lay.separator(factor=sepFactor)

        # -----------------------------------------------------------------------------
        #   NEW MIRROR BUTTONS
        # -----------------------------------------------------------------------------
        main_row = lay.row(align=True)
        main_row.scale_y = 1.5
        
        # Label section
        label_section = main_row.row(align=True)
        label_section.alignment = "RIGHT"
        label_section.ui_units_x = labelWidth
        label_section.label(text="Mirror:")
        
        # Button section
        button_section = main_row.grid_flow(row_major=True, columns=6, even_columns=True, align=True)
        
        # Buttons
        mop1 = button_section.operator("ntzsym.mirror_x_backward", text='', icon_value=icons['xIconLeft'], emboss=True)
        mop2 = button_section.operator("ntzsym.mirror_x_forward", text='', icon_value=icons['xIconRight'], emboss=True)
        mop3 = button_section.operator("ntzsym.mirror_y_backward", text='', icon_value=icons['yIconLeft'], emboss=True)
        mop4 = button_section.operator("ntzsym.mirror_y_forward", text='', icon_value=icons['yIconRight'], emboss=True)
        mop5 = button_section.operator("ntzsym.mirror_z_backward", text='', icon_value=icons['zIconLeft'], emboss=True)
        mop6 = button_section.operator("ntzsym.mirror_z_forward", text='', icon_value=icons['zIconRight'], emboss=True)
        
        lay.separator(factor=sepFactor)
