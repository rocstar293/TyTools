import bpy
from . import object
import math


def bevel_to(curve, ref):
	curve.data.bevel_mode = 'OBJECT'
	curve.data.bevel_object = ref


def isBezier(curve):
	return curve.type == 'CURVE' and len(curve.data.splines) > 0 \
	and curve.data.splines[0].type == 'BEZIER' and \
	len(curve.data.splines[0].bezier_points) > 0


def set_intp(curve):
	if isBezier(curve):
		sp_len_list = [s.calc_length() for s in curve.data.splines]
		max_len = max(sp_len_list)
		curve.data.resolution_u = math.ceil(max_len)


def reset_radius(curve):
    for sp in curve.data.splines:
        for p in sp.bezier_points:
            p.radius = 1


def build_ref(coords, ref_type, refobj = None):
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

	object.get_ref_obj(refobj).data.splines.clear()

	spline = refobj.data.splines.new('POLY')
	spline.points.add(len(coords)-1)

	for i, coord in enumerate(coords):
		x, y, z = coord
		spline.points[i].co = (x, y, z, 1)

	return refobj
	
