import bpy
from bpy.types import PropertyGroup
from bpy.props import FloatProperty, IntProperty, EnumProperty, BoolProperty

class TY_road(PropertyGroup):

	option_list = [
		"lane_width",
		"lane_cnt",
		"shoulder_width",
		"toggle_curb",
		"toggle_stripes"
	]
	
	lane_width : FloatProperty(
		name= "Lane Width",
		default= 12
	)

	lane_cnt : IntProperty(
		name = "Lane Count",
		default= 2
	)

	shoulder_width : FloatProperty(
		name= "Shoulder Width",
		default= 6
	)		

	toggle_curb : BoolProperty(
		name= "Create Curb",
		default= False
	)
	
	toggle_stripes : BoolProperty(
		name= "Create Stripes",
		default= False
	)

	def coords(self):
		
		scale = 0.3048

		lane_width = self.lane_width * scale
		shoulder_width = self.shoulder_width * scale
		curb_height = 0.5 * scale
		curb_width = 0.5 * scale
		lane_cnt = self.lane_cnt
		toggle_curb = self.toggle_curb
		
		road_top = 0
		extreme_x = lane_width * lane_cnt / 2 + shoulder_width
		shoulder_x = extreme_x - shoulder_width
		curb_s = []
		curb_f = []
		
		if toggle_curb == True:
			curb_s = [
				(-extreme_x - (2 * curb_width), road_top + curb_height, 0),
				(-extreme_x - curb_width, road_top + curb_height, 0),
				(-extreme_x - curb_width, road_top, 0)]

			curb_f = [
				(extreme_x + curb_width, road_top, 0),
				(extreme_x + curb_width, road_top + curb_height, 0),
				(extreme_x + (2 * curb_width), road_top + curb_height, 0)
		]

		road = [
			(-extreme_x, road_top, 0),	
			(extreme_x, road_top, 0)
		]
		
		coords = list(map(tuple, curb_s)) + list(map(tuple, road)) + list(map(tuple, curb_f))

		return coords


class TY_curb(PropertyGroup):

	option_list : EnumProperty(
		name = "Curb Type",
		items = [
			("c1", "Curb 1", ""),
			("c2", "Curb 2", "")
		]
	)

	c1_option_list = [
		"c1_curb_width", 
		"c1_curb_height"
	]

	c1_curb_width : FloatProperty(
		name= "Curb Width",
		default= 0.5,
		min= .125
	)

	c1_curb_height : FloatProperty(
		name= "Curb Height",
		default= 0.5,
		min= .125
	)


class TY_sidewalk(PropertyGroup):

	option_list = [
		"sidewalk_width",
		"sidewalk_height",
	]
	
	sidewalk_width : FloatProperty(
		name= "Sidewalk Width",
		default= 6,
		min= 1
	)

	sidewalk_height : FloatProperty(
		name = "Sidewalk Height",
		default= 0.5,
		min = 0
	)

	def coords(self):
		
		scale = 0.3048
		
		sidewalk_width = self.sidewalk_width * scale
		sidewalk_height = self.sidewalk_height * scale

		extreme_x = sidewalk_width / 2

		sw = [
			(-extreme_x, 0, 0),
			(-extreme_x, sidewalk_height, 0),
			(extreme_x, sidewalk_height, 0),
			(extreme_x, 0, 0)
		]
		
		if sidewalk_height == 0:
			sw.pop(0)
			sw.pop(-1)

		coords = list(map(tuple, sw))
	
		return coords

class TY_stripe(PropertyGroup):

	option_list = [
		"stripe_width",
		"stripe_offset"
	]

	stripe_width : FloatProperty(
		name = "Stripe Width",
		default = 0.5
	)

	stripe_offset : FloatProperty(
		name = "Road Offset",
		default = 0.125
	)

	def coords(self):
		
		scale = 0.3048

		stripe_width = self.stripe_width * scale
		stripe_offset = self.stripe_offset * scale

		stripe = [
			(-stripe_width / 2, stripe_offset, 0),
			(stripe_width / 2, stripe_offset, 0)
		]

		coords = list(map(tuple, stripe))

		return coords