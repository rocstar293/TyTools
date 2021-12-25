import bpy

from bpy.types import Panel
from .utils import collection, object

class TY_PT_profile_tools(Panel):  
    bl_label = "Profile Tools"
    bl_region_type = 'UI'
    bl_space_type = 'VIEW_3D'
    bl_category = "TyTools"

    def draw(self, context):    
        
        scene = context.scene
        TY_props = scene.TY_props 
        
        sl_obj_reftype = object.get_ref_obj(object.get_active_selected(), reftype=True)
        prop_reftype = str(f"scene.{TY_props.ref_type}")
        sel = object.get_active_selected()
        
        refprops = [op for op in eval(prop_reftype).option_list] #group ref properties by type
        numprops = []
        boolprops = []

        for prop in refprops:
            proptype = eval(f"type({prop_reftype}.{prop})")
            
            if proptype in [int, float]:
               numprops.append(prop)
            else:
                boolprops.append(prop)

        layout = self.layout
        
        box = layout.box()

        box.label(text="Settings:")
        box.prop(TY_props, "ref_col")
        box.prop(TY_props, "set_bevel")
        
        box = layout.box()

        box.label(text="Create Reference Objects:")
        box.prop(TY_props, "ref_type")
        column = box.column(align=True)

        # Dynamic Reference Parameters
        for prop in numprops:
            column.prop(eval(prop_reftype), prop)

        row = box.row(align=True)
        
        for prop in boolprops:
            row.prop(eval(prop_reftype), prop)
        
        if prop_reftype == 'scene.TY_road' and scene.TY_road.toggle_curb == True:
            
            column = box.column()

            TY_curb = scene.TY_curb
            sel_curb = TY_curb.option_list

            column.prop(TY_curb, "option_list")

            for op in eval(f"TY_curb.{sel_curb}_option_list"):
                column.prop(TY_curb, op)

        if prop_reftype == 'scene.TY_road' and scene.TY_road.toggle_stripes == True:
            TY_stripe = scene.TY_stripe
                    
            for op in TY_stripe.option_list:
                box.prop(TY_stripe, op)

            box.operator("ty.build_stripes")

        # Toggles Between Create and Update Based on Context
        
        if object.get_ref_obj(object.get_active_selected()) == None:
            op_name = "Create Reference"
        
        else:
            op_name = "Update Reference"

        box.operator("ty.set_ref", text=op_name)


class TY_PT_camera_tools(Panel):
    bl_label = "Camera Tools"
    bl_region_type = "UI"
    bl_space_type = "VIEW_3D"
    bl_category = "TyTools"

    def draw(self, context):
        sel = object.get_active_selected()
        if sel != None:
            if type(sel.data) != 'CURVE':
                pass # print("select curve")

        layout = self.layout
        box = layout.box()
        box.label(text="Create Camera")
        
        