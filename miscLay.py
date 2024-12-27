import bpy

from . import icons

#Show hide section with arrow, optional checkbox, and text
def createShowHide(self, context, scene, properties, showHideBool, optionalCheckboxBool, text, layout):

    if scene is not None:
        data = eval( f"scene.{properties}" )
        boolThing = eval( f"scene.{properties}.{showHideBool}" )
    else:
        data = self
        boolThing = eval( f"self.{showHideBool}")

    if boolThing:
        showHideIcon = "TRIA_DOWN"
    else:
        showHideIcon = "TRIA_RIGHT"

    row = layout.row(align=True)

    downArrow = row.column(align=True)
    downArrow.alignment = "LEFT"
    downArrow.prop(data, showHideBool, text="", icon=showHideIcon, emboss=False )

    if optionalCheckboxBool is not None:
        checkbox = row.column(align=True)
        checkbox.alignment = "LEFT"
        checkbox.prop(data, optionalCheckboxBool, text="" )

    textRow = row.column(align=True)
    textRow.alignment = "LEFT"
    textRow.prop(data, showHideBool, text=text, emboss=False )

    emptySpace = row.column(align=True)
    emptySpace.alignment = "EXPAND"
    emptySpace.prop(data, showHideBool, text=" ", emboss=False)




def createProp(self, context, scn, bEnabled, bActive, bUseCol, labelText, data, checkboxProp, propItem, scale_y, labelScale, propScale, labelAlign, propAlignment, propAlign, propText, bExpandProp, propColCount, bUseSlider, resetProp, layout):

    if bUseCol:
        propSection = layout.column(align=True)
    else:
        propSection = layout.row(align=True)

    propSection.scale_y = scale_y

    propSectionLabel = propSection.row(align=True)
    propSectionLabel.alignment="EXPAND"
    propSectionLabel.ui_units_x = labelScale

    if checkboxProp is not None:
        checkbox = propSection.row(align=True)
        checkbox.prop(self, checkboxProp, text='')

        propSection.separator()

    propSectionLabel1 = propSectionLabel.row(align=True)
    propSectionLabel1.alignment=labelAlign
    propSectionLabel1.scale_x = 1
    propSectionLabel1.enabled = bEnabled
    propSectionLabel1.active = bActive


    propSectionLabel1.label(text=labelText)

    propSectionItem = propSection.row(align=True)

    propSectionItem.enabled = bEnabled
    propSectionItem.active = bActive

    propSectionItem.alignment=propAlignment
    
    if (propColCount <= 1) or (not bExpandProp):
        propSectionItem1 = propSectionItem.row(align=propAlign)
    else:
        propSectionItem1 = propSectionItem.column_flow(columns=propColCount, align=propAlign)

    if resetProp is not None:
        propSection.separator()
        resetBtn = propSection.row(align=True)
        resetBtn.active = False
        resetBtn.prop(self, resetProp, icon="LOOP_BACK", toggle=True, emboss=False, icon_only=True)

    propSectionItem1.alignment=propAlignment
    propSectionItem1.ui_units_x = propScale
    propSectionItem1.scale_x = 100

    propSectionItem1.prop(data, propItem, text=propText, expand=bExpandProp, slider=bUseSlider)