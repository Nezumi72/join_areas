import bpy


areas = bpy.context.screen.areas
a_types = [
    'EMPTY',
    'VIEW_3D',
    'IMAGE_EDITOR',
    'NODE_EDITOR',
    'SEQUENCE_EDITOR',
    'CLIP_EDITOR',
    'DOPESHEET_EDITOR',
    'GRAPH_EDITOR',
    'NLA_EDITOR',
    'TEXT_EDITOR',
    'CONSOLE',
    'INFO',
    'TOPBAR',
    'STATUSBAR',
    'OUTLINER',
    'PROPERTIES',
    'FILE_BROWSER',
    'PREFERENCES',
    ]

a2_type = 'VIEW_3D'
a1_type = 'VIEW_3D'

area1 = None
area2 = None
area1_idx = None
area2_idx = None


def get_a1(area1, area1_idx):
    global areas
    global a1_type
    global a2_type
    for i, a in enumerate(areas):
        if a.type == a1_type and area1 is None:
            area1 = a
            area1_idx = i
            return area1, area1_idx


def get_a2(area2, area2_idx, area1_idx):
    global areas
    global a1_type
    global a2_type
    for i, a in enumerate(areas):
        if i == area1_idx:
            continue
        if a.type == a2_type and area2 is None:
            area2 = a
            area2_idx = i
            return area2, area2_idx
    return area2, area2_idx


def vert_join(area1, area2):
    if area1.width != area2.width:
        print('width mismatch areas not joined')
        return ('CANCELLED')
    print(f"area1.height: {area1.height} \tarea2.height: {area2.height}")
    if area1.y < area2.y:
        if (area2.y - area1.height - area1.y) > 5:
            print('No action performed areas not adjacent')
            return ('CANCELLED')
        bpy.ops.screen.area_join(
            cursor=(area2.x + int(area2.width/2), area1.y + area1.height)
            )
    else:
        if (area1.y - area2.height - area2.y) > 5:
            print('No action performed areas not adjacent')
            return ('CANCELLED') 
        bpy.ops.screen.area_join(
            cursor=(area1.x + int(area1.width/2), area2.y + area2.height)
            )


def hori_join(area1, area2):
    if area1.height != area2.height:
        print('height mismatch areas not joined')
        return ('CANCELLED')
    print(f"area1.height: {area1.height} \tarea2.height: {area2.height}")
    if area1.x < area2.x:
        if (area2.x - area1.width - area1.x) > 5:
            print('No action performed areas not adjacent')
            return ('CANCELLED')
        bpy.ops.screen.area_join(
            cursor=(area1.x + area1.width, area2.y + int(area2.height/2))
            )
    else:
        if (area1.x - area2.width - area2.x) > 5:
            print('No action performed areas not adjacent')
            return ('CANCELLED')
        bpy.ops.screen.area_join(
            cursor=(area2.x + area2.width, area1.y + int(area1.height/2)))

try:
    area1, area1_idx = get_a1(area1, area1_idx)
except TypeError:
    pass

try:
    area2, area2_idx = get_a2(area2, area2_idx, area1_idx)
except TypeError:
    pass

if area1 and area2:
    print(f"Attempting to join {a1_type}[{area1_idx}] {a2_type}[{area2_idx}]")
    print(f"area1.x: {area1.x} \tarea2.x: {area2.x}")
    print(f"area1.y: {area1.y} \tarea2.y: {area2.y}")
    if area1.x == area2.x:
        print("... using vertical join")
        vert_join(area1, area2)
    elif area1.y == area2.y:
        print("... using horizontal join")
        hori_join(area1, area2)
    else:
        print('No action performed areas not adjacent')
else:
    print('1 or more invalid area types')
    if not area1:
        print(f"{a1_type} not found")
    if not area2:
        print(f"{a2_type} not found")

# force update to windows
my_ws = bpy.context.workspace
tmp_ws = [ws for ws in bpy.data.workspaces if ws != my_ws]
bpy.context.window.workspace = tmp_ws[0]
bpy.context.window.workspace = my_ws
