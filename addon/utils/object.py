import bpy
from mathutils import Matrix, Vector, Quaternion

# Getter

def find(name, collection=False): # find object by name
    
    vl_objs = bpy.context.view_layer.objects

    found = None
    
    for ob in vl_objs:
        if ob.name == name:
            found = ob
        
    if collection:
        return found.users_collection
    
    return found


def get_ref(obj, reftype=False): # search object and object's bevel for reftype prop; can return obj or reftype
    
    if obj != None:
        
        if obj.get("ref_type", None) != None:
            
            if reftype == False:
                return obj 
            
            else:
                return obj.get("ref_type")
    
        elif obj.data.bevel_object != None and obj.data.bevel_object.get("ref_type", None) != None:
            
            if reftype == False:
                return obj.data.bevel_object
            
            else:
                return obj.data.bevel_object.get("ref_type")

    return None

def get_bk(obj):

    if obj.get("backup", None) != None:
        return obj["backup"] 
    
    else:
        return None


def get_sel(): # get selected object
    
    if len(bpy.context.selected_objects) == 1:
        return bpy.context.selected_objects[0]

    if bpy.context.active_object in bpy.context.selected_objects:
        return bpy.context.active_object


def get_loc_matrix(location):
    return Matrix.Translation(location)


def get_rot_matrix(rotation):
    return rotation.to_matrix().to_4x4()


def get_sca_matrix(scale):
    scale_mx = Matrix()
    
    for i in range(3):
        scale_mx[i][i] = scale[i]
    
    return scale_mx

# Setter

def set_active(obj, add=False):
    
    vl_objs = bpy.context.view_layer.objects

    if add == False:
        for ob in vl_objs:
            ob.select_set(False) 
        
    vl_objs.active = obj
    obj.select_set(True)


def makecopy(obj, collection): # copies object and object data; links new object to specified collection
    duplicate = obj.copy()
    duplicate.data = obj.data.copy()
    collection.objects.link(duplicate)
    
    return duplicate


def move(obj, collection):
    
    for col in obj.users_collection:
        col.objects.unlink(obj)
    
    collection.objects.link(obj)


def append_name(obj, name):
    obj.name = f"{obj.name.split('(')[0]}" + f"({name})"


def reset_rs_transforms(obj, rotation, scale): # resets object rotation and scale
    mx = obj.matrix_world
    loc, rot, sca = mx.decompose()

    if rotation and scale:
        meshmx = get_rot_matrix(rot) @ get_sca_matrix(sca)

    elif rotation:
        meshmx = get_rot_matrix(rot)

    elif scale:
        meshmx = get_sca_matrix(sca)

    obj.data.transform(meshmx)

    if rotation and scale:
        applymx = get_loc_matrix(loc) @ get_rot_matrix(Quaternion()) @ get_sca_matrix(Vector.Fill(3,1))

    elif rotation:
        applymx = get_loc_matrix(loc) @ get_rot_matrix(Quaternion()) @ get_sca_matrix(sca)

    elif scale:
        applymx = get_loc_matrix(loc) @ get_rot_matrix(rot) @ get_sca_matrix(Vector.Fill(3,1))

    obj.matrix_world = applymx

