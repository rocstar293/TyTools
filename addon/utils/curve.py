import bpy
import math

# Getter

def is_bezier(curve):
	return curve.type == 'CURVE' and len(curve.data.splines) > 0 \
	and curve.data.splines[0].type == 'BEZIER' and \
	len(curve.data.splines[0].bezier_points) > 0

# Setter

def reset_radius(curve):
    for sp in curve.data.splines:
        for p in sp.bezier_points:
            p.radius = 1


def set_bevel(curve, bevel):
    curve.data.bevel_mode = 'OBJECT'
    curve.data.bevel_object = bevel


def set_intp(curve):
	if is_bezier(curve):
		sp_len_list = [s.calc_length() for s in curve.data.splines]
		max_len = max(sp_len_list)
		curve.data.resolution_u = math.ceil(max_len)*2


def resample(obj, length=0.5, apply=False):
    
	resample_mod = [mod for mod in obj.modifiers if mod.name == "Resample"]

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

