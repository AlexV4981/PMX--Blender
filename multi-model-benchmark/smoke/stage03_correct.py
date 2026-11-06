def solve(scene):
    import bpy
    obj = bpy.data.objects["RepairMesh"]
    a, b = obj.vertex_groups["DEF_A"], obj.vertex_groups["DEF_B"]
    count = 0
    for i in range(len(obj.data.vertices)):
        wa, wb = a.weight(i), b.weight(i)
        total = wa + wb
        if total > 0:
            a.add([i], wa / total, "REPLACE")
            b.add([i], wb / total, "REPLACE")
            count += 1
    return {"modified_vertices": count}
