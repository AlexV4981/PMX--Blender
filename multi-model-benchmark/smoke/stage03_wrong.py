def solve(scene):
    import bpy
    obj = bpy.data.objects["RepairMesh"]
    obj.vertex_groups["DEF_A"].add([0], 1.0, "REPLACE")  # leaves weights un-normalized; must fail
    return {"modified_vertices": 1}
