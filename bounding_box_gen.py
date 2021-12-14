# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
    "name": "Bounding Box Gen",
    "author": "Latidoremi",
    "version": (1, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Object > Bounding Box Gen",
    "description": "Create a bounding box for each selected object",
    "category": "Add Object",
}

import bpy, bmesh
from mathutils import Vector

def calc_bound_box(verts):
    list=[]
    for i in range(3):
        list.append(max(verts, key=lambda x: x[i])[i])
        list.append(min(verts, key=lambda x: x[i])[i])
    bound_box=[
    Vector((list[1],list[3],list[5])),
    Vector((list[1],list[3],list[4])),
    Vector((list[1],list[2],list[5])),
    Vector((list[1],list[2],list[4])),
    
    Vector((list[0],list[3],list[5])),
    Vector((list[0],list[3],list[4])),
    Vector((list[0],list[2],list[5])),
    Vector((list[0],list[2],list[4]))]

    return bound_box

class OBJECT_OT_bounding_box_gen(bpy.types.Operator):
    """Create a bounding box for each selected object"""
    bl_idname = "object.bounding_box_gen"
    bl_label = "Bounding Box Gen"
    bl_options = {'REGISTER', 'UNDO'}
    
    fill_faces: bpy.props.BoolProperty(name='Fill Faces', default = False)
    
    @classmethod
    def poll(cls, context):
        return context.mode=='OBJECT' and context.selected_objects
        
    def execute(self, context):
        for ob in context.selected_objects:
            edge_list=[(0,1),(1,3),(3,2),(2,0),(4,5),(5,7),(7,6),(6,4),(0,4),(1,5),(2,6),(3,7)]
            
            bm = bmesh.new()
            me = ob.data
            bbox = calc_bound_box([ob.matrix_world @ v.co for v in me.vertices])
            for v in bbox:
                bm.verts.new(v)
            bm.verts.ensure_lookup_table()
            for e in edge_list:
                bm.edges.new((bm.verts[e[0]],bm.verts[e[1]]))
            
            if self.fill_faces:
                bmesh.ops.edgenet_fill(bm, edges=bm.edges)
            
            new_me = bpy.data.meshes.new(ob.name+"_bbox")
            bm.to_mesh(new_me)
            bm.free()
            new_ob = bpy.data.objects.new(ob.name+"_bbox", new_me)
            context.scene.collection.objects.link(new_ob)
        
        return {'FINISHED'}
    
def draw_bbox_gen_button(self, context):
    layout = self.layout
    layout.operator("object.bounding_box_gen")

def register():
    bpy.utils.register_class(OBJECT_OT_bounding_box_gen)
    bpy.types.VIEW3D_MT_object.append(draw_bbox_gen_button)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_bounding_box_gen)
    bpy.types.VIEW3D_MT_object.remove(draw_bbox_gen_button)

if __name__ == "__main__":
    register()
    

    
    
    

