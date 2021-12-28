import bpy
from bpy.types import Panel
from bpy.utils import register_class, unregister_class
from . import operators, properties, presets, panels

classes = [
	properties.TY_props,
	operators.TY_OT_set_ref,
	operators.TY_OT_apply_ref,
	operators.TY_OT_revert,
	operators.TY_OT_build_stripes,
	operators.TY_OT_ref_editor_modal,
	panels.TY_PT_profile_tools,
	panels.TY_PT_camera_tools,
	presets.TY_road,
	presets.TY_sidewalk,
	presets.TY_stripe,
	presets.TY_curb,
]

def register():
	for cls in classes:
		
		bpy.utils.register_class(cls)
		
		cls_split = str(cls).split(".")
		if cls_split[-2] in ["presets", "properties"]:
			prop = f"{cls_split[-2]}.{cls_split[-1]}".split("'")[-2]
			assignment = f"{prop.split('.')[-1]}"
			exec(f"bpy.types.Scene.{assignment} = bpy.props.PointerProperty(type= {prop})")

def unregister():
	for cls in classes:
		bpy.utils.unregister_class(cls)

		cls_split = str(cls).split(".")
		if cls_split[-2] in ["presets", "properties"]:
			prop = f"{cls_split[-2]}.{cls_split[-1]}".split("'")[-2]
			exec(f"del bpy.types.Scene.{prop.split('.')[-1]}")