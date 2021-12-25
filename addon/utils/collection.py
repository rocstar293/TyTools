import bpy

def find(name='Collection', parents=False, children=False):
    if parents:
        return [c for c in bpy.data.collections if name in c.children]

    if children:
        return None if name not in bpy.data.collections else bpy.data.collections[name].children[:]

    if name in bpy.data.collections:
        return bpy.data.collections[name]

    return None


def parents(name='Collection'):
    return find(name, parents=True)


def children(name='Collection'):
    return find(name, children=True)


def child_of(name='Collection', parent=None):
    if not parent:
        parent = bpy.context.scene.collection

    if name in parent.children:
        return parent.children[name]

    for sub in parent.children:
        if name in sub.children:
            return sub.children[name]

    for sub in parent.children:
        return child_of(name, sub)

    return None


def exists(name='Collection'):
    return bool(find(name))


def get(name, default=None):
    if not exists(name):
        return default

    return find(name)


def new(name='Collection', parent=None, color='', unique=True, unique_parent=False):
    color = color.lower()
    color_tags = {
        'default': 'NONE',
        'red': 'COLOR_01',
        'orange': 'COLOR_02',
        'yellow': 'COLOR_03',
        'green': 'COLOR_04',
        'blue': 'COLOR_05',
        'violet': 'COLOR_06',
        'pink': 'COLOR_07',
        'brown': 'COLOR_08',
    }

    if color not in color_tags:
        color = 'default'

    if unique and exists(name):
        collection = get(name)

        if parent:
            if unique_parent:
                for p in parents(name):
                    p.children.unlink(collection)

            if name not in parent.children:
                parent.children.link(collection)

        if hasattr(collection, 'color_tag'):
            collection.color_tag = color_tags[color]

        return collection

    collection = bpy.data.collections.new(name)

    if hasattr(collection, 'color_tag'):
        collection.color_tag = color_tags[color]

    if not parent:
        parent = bpy.context.scene.collection

    parent.children.link(collection)
    return collection


def set_active_col(collection, layer_col, found=None):
    
    if found == None:
    
        if (layer_col.name == collection.name):
            found = layer_col
        
        for layer in layer_col.children:
            set_active_col(collection, layer, found)
        
    else:
        bpy.context.view_layer.active_layer_collection = found


def verify_ref():
    scene = bpy.context.scene
    TY_props = scene.TY_props

    if TY_props.ref_col == None:
            TY_props.ref_col = new(
		        name= "Reference Lines", 
			    color= 'yellow')

def update_refs():

    items = []

    scene = bpy.context.scene
    TY_props = scene.TY_props
        
    if scene.TY_props.ref_col != None:
        for i, ob in enumerate(list(TY_props.ref_col.objects)):
            print(f"Tracking: {ob.name}")
            add_obj = (str(i), ob.name, "")
            items.append(add_obj)  
    
    return items