bl_info = {
	'name' : 'TyTools',
	'description' : 'Tools for workflow improvments',
	'author': 'Tyler Beaird',
	'version': (1, 0, 0),
	'blender': (3, 1, 0),
	'location': ('view3D'),
	'catagory': '3D View'}


from . import addon

def register():
	addon.register()

def unregister():
	addon.unregister()
