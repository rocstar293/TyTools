import bpy

from bpy.types import Operator

from . utils import collection, curve, shader, object


class TY_OT_set_ref(Operator): # create a new reference object 
    bl_idname = "ty.set_ref"
    bl_label = "Setup New Reference"
    
    def invoke(self, context, event):
        
        scene = context.scene
        TY_props = scene.TY_props
        atv_ref_type = TY_props.ref_type
        
        target = object.get_active_selected() # set active object as target for bevel_to
        ref_obj = object.get_ref_obj(target)
        
        collection.verify_ref() # Verify That a reference collection is set; else build one
        coords = eval(str(f"scene.{scene.TY_props.ref_type}.set_coords()")) # return built coords of selected ref type
        new_ref = curve.build_ref(coords, atv_ref_type, ref_obj) # build reference object with returned coords
        
        if target != None and TY_props.set_bevel == True and target.type == 'CURVE': # if target is curve and set bevel is enabled;
            object.reset_rs_transforms(target, rotation= True, scale= True)
            curve.reset_radius(target)
            curve.set_intp(target)                                                   # configure target path for bevel
            curve.bevel_to(target, new_ref)
            object.append_ref_name(target, new_ref)
            target.data.twist_mode = 'Z_UP'
            
        return {'FINISHED'}


class TY_OT_apply_ref(Operator):
    bl_idname = "ty.apply_ref"
    bl_label = "Apply"

    def invoke(self, context, event):
        
        scene = context.scene
        TY_props = scene.TY_props

        target = object.get_active_selected()
        bevel_obj = target.data.bevel_object

        collection.verify_bk()
        
        copy = object.makecopy(target, TY_props.bk_col)
        target.data.bevel_object = None
        
        curve.set_intp(target)                                                 # configure target path for bevel
        curve.resample(target, length=.5)

        bpy.ops.object.convert(target='MESH')
        bpy.ops.object.convert(target='CURVE')
        curve.bevel_to(target, bevel_obj)
        bpy.ops.object.convert(target='MESH')
    
        return {'FINISHED'}
        


class TY_OT_build_stripes(Operator): # Special op for 
    bl_idname = "ty.build_stripes"
    bl_label = "Build Stripes"

    def invoke(self, context, event):
        
        target_col = object.get_active_selected().users_collection[0] # set stripe's target collection to active obj's collection
        
        scene = context.scene
        TY_props = scene.TY_props
        TY_stripe = scene.TY_stripe
        
        coords = TY_stripe.set_coords()
        new_stripe = curve.build_ref(coords, ref_type="TY_stripe")

        target = object.get_active_selected()
        copy = object.makecopy(target, target_col)
        object.append_ref_name(copy, new_stripe)
        copy.data.bevel_object = new_stripe
        return {'FINISHED'}


class TY_OT_ref_editor_modal(Operator): # WIP
    bl_idname= "ty.ref_editor_modal"
    bl_label= "Reference Editor"

    def execute(self, context):
        
        if context.space_data.local_view:
            bpy.ops.view3d.localview()
        
        bpy.ops.view3d.localview()
        bpy.ops.view3d.view_axis(type='TOP')
        
        context.window_manager.modal_handler_add(self)
        
        return {'RUNNING_MODAL'}


    def modal(self, context: bpy.types.Context, event: bpy.types.Event):

        if event.type == 'MOUSEMOVE':
            print(f"{event.type}: {event.mouse_x}, {event.mouse_y}")
        
        elif event.type in {'RIGHTMOUSE', 'ESC'}:
            print(f"{event.type} -- STOPPING")
            bpy.ops.view3d.localview()
            
            return {'FINISHED'}

        return {'RUNNING_MODAL'}
