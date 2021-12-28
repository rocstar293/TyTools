import bpy

from bpy.types import Panel
from .utils import collection, object

class TY_PT_profile_tools(Panel): # Panel for creating/modifying profile references
    bl_label = "Profile Tool"
    bl_region_type = 'UI'
    bl_space_type = 'VIEW_3D'
    bl_category = "TyTools"

    def draw(self, context):
        
        scene = context.scene
        TY_props = scene.TY_props
        
        sel = object.get_sel() # selected object
        
        sel_obj_ref_type = None
        create_ref_tog = False
        apply_tog = False
        revert_tog = False
        
        curb_tog = scene.TY_road.toggle_curb
        stripe_tog = scene.TY_road.toggle_stripes
        
        # Conditionals
        
        if sel: # object selected
            
            if type(sel.data) == bpy.types.Curve: # object is a curve
                
                create_ref_tog = True   
                if object.get_ref(sel): # curve has a ref obj set
                    
                    sel_obj_ref_type = object.get_ref(sel)
                    apply_tog = True

            elif type(sel.data) == bpy.types.Mesh: # object is a mesh
                
                if object.get_bk(sel) != None: # Mesh
                    revert_tog = True
                
        else: # no object selected
            
            create_ref_tog = True
        
        if create_ref_tog:
            prop_reftype = str(f"scene.{TY_props.ref_type}") # reference object set by enum in panel    
            refprops = [op for op in eval(prop_reftype).option_list] # list of properties for selected ref_type
            numprops = [] # int / float properties
            boolprops = [] # bool properties
            
            for prop in refprops:
                proptype = eval(f"type({prop_reftype}.{prop})")
                
                if proptype in [int, float]:
                    numprops.append(prop)
                
                else:
                    boolprops.append(prop)

            if prop_reftype == 'scene.TY_road' and scene.TY_road.toggle_curb == True:
                curb_tog = True

            if prop_reftype == 'scene.TY_road' and scene.TY_road.toggle_stripes == True:
                stripe_tog = True



        # Start

        layout = self.layout
        
        box = layout.box() # Profile Tool Settings

        box.label(text="Settings:")
        box.prop(TY_props, "ref_col")
        box.prop(TY_props, "bk_col")
        box.prop(TY_props, "set_bevel")

        if create_ref_tog: # Ref properties
            
            box = layout.box()

            box.label(text="Create Reference Objects:") 
            box.prop(TY_props, "ref_type")
            
            column = box.column(align=True) # Dynamic Ref parameters

            for prop in numprops:
                column.prop(eval(prop_reftype), prop)

            row = box.row(align=True)
        
            for prop in boolprops:
                row.prop(eval(prop_reftype), prop)
        
            if curb_tog: # Curb Parameters
                
                TY_curb = scene.TY_curb
                sel_curb = TY_curb.option_list
                
                column = box.column()
                column.prop(TY_curb, "option_list")

                for op in eval(f"TY_curb.{sel_curb}_option_list"):
                    column.prop(TY_curb, op)

            if stripe_tog:
                
                TY_stripe = scene.TY_stripe
                    
                for op in TY_stripe.option_list:
                    box.prop(TY_stripe, op)

                box.operator("ty.build_stripes")

            # Toggles Between Create and Update Based on Context
            
            if sel_obj_ref_type == None:
                op_name = "Create Reference"
            
            else:
                op_name = "Update Reference"

            box.operator("ty.set_ref", text=op_name)
            
            if apply_tog:
                box.operator("ty.apply_ref")

        if revert_tog:
            box.operator("ty.revert")


class TY_PT_camera_tools(Panel):
    bl_label = "Camera Tools"
    bl_region_type = "UI"
    bl_space_type = "VIEW_3D"
    bl_category = "TyTools"

    def draw(self, context):
        pass
        # sel = object.get_active_selected()
        # if sel != None:
        #     if type(sel.data) != 'CURVE':
        #         print("select curve")

        # layout = self.layout
        # box = layout.box()
        # box.label(text="Create Camera")
        
        