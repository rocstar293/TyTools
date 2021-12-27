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
		curve.data.resolution_u = math.ceil(max_len)*2


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


def resample(obj, length=0.1, apply=False):
    
	resample_mod = [mod for mod in obj.modifiers if mod.name == "Resample"]
	
	if len(resample_mod) != 0:
		return

	geonode = obj.modifiers.new("Resample",'NODES')

	nodes = geonode.node_group.nodes
	links = geonode.node_group.links
	initial_link = links[0]

	links.remove(initial_link)

	input_node = nodes[0]
	output_node = nodes[1]

	resample = nodes.new('GeometryNodeResampleCurve')
	resample.mode = 'LENGTH'

	resample_geom_input = resample.inputs[0]
	resample_length_input = resample.inputs[3]
	resample_output = resample.outputs[0]

	geom_in = input_node.outputs[0]
	geom_out = output_node.inputs[0]

	links.new(geom_in, resample_geom_input)
	links.new(resample_output, geom_out)

	resample_length_input.default_value = length
    
	if apply:
		object.set_active(obj)
		bpy.ops.modifier_apply(obj, geonode)


