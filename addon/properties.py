import bpy

from bpy.types import PropertyGroup 
from bpy.props import PointerProperty, BoolProperty, EnumProperty

from . import handlers

from .utils import collection


class TY_props(PropertyGroup):
	
	ref_col : PointerProperty(
		name= "Ref Col",
		description= "Collection for new Reference Objects",
		type= bpy.types.Collection
	)

	bk_col : PointerProperty(
		name = "Backups",
		description = "Collection for backing up applied curve objects",
		type= bpy.types.Collection
	)
	
	set_bevel : BoolProperty(
		name= "Bevel to active",
		description= "Enable to set reference as bevel of active object",
		default= True
	)

	ref_type : EnumProperty(
		name= "Preset",
		description= "Type of reference to use",
		items= [
			("TY_road", "Road", ""),
			("TY_sidewalk", "Sidewalk", "")
		]
	)


# class TY_draw_props(PropertyGroup):

# 	draw_shader : bpy.props.BoolProperty(
# 		name= "draw overlay",
# 		description= "Draw Overlay",
# 		default= False,
# 		update= handlers.update_draw()
# 		)