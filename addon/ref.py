import bpy
from . utils import object, collection, curve

def build(coords, ref_type, refobj = None):
    scene = bpy.context.scene
    TY_props = scene.TY_props

    if refobj == None :
        new_ref_curve = bpy.data.curves.new(ref_type, type='CURVE')
        new_ref_curve.dimensions = '2D'
		
        new_ref = bpy.data.objects.new(f"{ref_type.split('_')[1]}", new_ref_curve)
		
        TY_props.ref_col.objects.link(new_ref)
        refobj = new_ref
	
    else:
        pass
    refobj["ref_type"] = ref_type
    refobj.name =f"{ref_type.split('_')[1]}"
	
    for option in eval(f"scene.{ref_type}.option_list"):
        refobj[option] = eval(f"scene.{ref_type}.{option}")

    object.get_ref(refobj).data.splines.clear()

    spline = refobj.data.splines.new('POLY')
    spline.points.add(len(coords)-1)

    for i, coord in enumerate(coords):
        x, y, z = coord
        spline.points[i].co = (x, y, z, 1)
    
    return refobj

def backup(obj):
    scene = bpy.context.scene
    TY_props = scene.TY_props
    
    copy = object.makecopy(obj, TY_props.bk_col)
    obj["backup"] = copy
    object.append_name(copy, "backup")

def apply(target):
    backup(target)
    
    bevel = target.data.bevel_object
    target.data.bevel_object = None

    curve.set_intp(target)
    curve.resample(target)
    object.set_active(target)
    bpy.ops.object.convert(target='MESH')
    bpy.ops.object.convert(target='CURVE')
    curve.set_bevel(target, bevel)
    target.data.twist_mode = 'Z_UP'
    bpy.ops.object.convert(target='MESH')
