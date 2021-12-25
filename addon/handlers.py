import bpy

from . utils import shader

def update_draw():
	if bpy.context.scene.TY_draw_props == True:
	
		draw_handler = bpy.types.SpaceView3D.draw_handler_add(shader.draw, (), 'WINDOW', 'POST_VIEW')
	
		for area in bpy.context.window.screen.areas:
			if area.type == 'VIEW_3D':
				area.tag_redraw()