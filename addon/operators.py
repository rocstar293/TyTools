import bpy

from bpy.types import Operator

from . utils import collection, curve, object
from . import ref

class TY_OT_set_ref(Operator):
    bl_idname = "ty.set_ref"
    bl_label = "Setup New Reference"
    
    def invoke(self, context, event):
        
        scene = context.scene
        TY_props = scene.TY_props
        prop_reftype = TY_props.ref_type
        
        target = object.get_sel() # set active object as target for bevel_to
        ref_obj = object.get_ref(target)
        
        collection.verify_ref() # Verify That a reference collection is set; else build one

        coords = eval(str(f"scene.{scene.TY_props.ref_type}.coords()")) # return built coords of selected ref type
        new_ref = ref.build(coords, prop_reftype, ref_obj) # build reference object with returned coords

        if target != None and TY_props.set_bevel == True and target.type == 'CURVE': # if target is curve and set bevel is enabled;
            object.reset_rs_transforms(target, rotation= True, scale= True)
            curve.reset_radius(target)
            curve.set_intp(target)
            curve.set_bevel(target, new_ref)
            object.append_name(target, new_ref.name.split(".")[0])
            new_ref['ref_type'] = TY_props.ref_type
            target.data.twist_mode = 'Z_UP'

        return {'FINISHED'}


class TY_OT_apply_ref(Operator): # Resamples curve, sets backup, and converts to mesh
    bl_idname = "ty.apply_ref"
    bl_label = "Apply"

    def invoke(self, context, event):
        
        scene = context.scene
        TY_props = scene.TY_props

        target = object.get_sel()

        collection.verify_bk()
        
        ref.apply(target)
    
        return {'FINISHED'}


class TY_OT_revert(Operator):
    bl_idname = "ty.revert"
    bl_label = "Revert"

    def invoke(self, context, event):
        target = object.get_sel()
        target_col = target.users_collection[0]
        backup = target["backup"]
        name = target.name

        bpy.data.objects.remove(target)
        object.move(backup, target_col)
        object.set_active(backup)
        backup.name = name
        return {'FINISHED'}


class TY_OT_build_stripes(Operator): # Special op for 
    bl_idname = "ty.build_stripes"
    bl_label = "Build Stripes"

    def invoke(self, context, event):
        
        target_col = object.get_sel().users_collection[0] # set stripe's target collection to active obj's collection
        
        scene = context.scene
        TY_props = scene.TY_props
        TY_stripe = scene.TY_stripe
        
        coords = TY_stripe.coords()
        new_stripe = ref.build(coords, ref_type="TY_stripe")

        target = object.get_sel()
        copy = object.makecopy(target, target_col)
        object.append_name(copy, new_stripe.name)
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
