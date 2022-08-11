import bpy
from mathutils import Color

bl_info = {
    "name": "simvertcol",
    "author": "3vilM33pl3",
    "description": "Select faces with similar vertex colors",
    "blender": (3, 2, 1),
    "location": "View3D",
    "warning": "",
    "category": "Generic"
}

classes = (

)


def select_by_vertex_color(object):
    threshold = .1
    obj = bpy.context.object

    bpy.ops.object.mode_set(mode="OBJECT")

    colors = obj.data.vertex_colors.active.data
    selected_polygons = list(filter(lambda p: p.select, obj.data.polygons))
    print(colors)

    if len(selected_polygons):
        p = selected_polygons[0]
        r = g = b = 0
        for i in p.loop_indices:
            c = colors[i].color
            r += c[0]
            g += c[1]
            b += c[2]
        r /= p.loop_total
        g /= p.loop_total
        b /= p.loop_total
        target = Color((r, g, b))

        for p in obj.data.polygons:
            r = g = b = 0
            for i in p.loop_indices:
                c = colors[i].color
                r += c[0]
                g += c[1]
                b += c[2]
            r /= p.loop_total
            g /= p.loop_total
            b /= p.loop_total
            source = Color((r, g, b))

            print(target, source)

            if (abs(source.r - target.r) < threshold and
                    abs(source.g - target.g) < threshold and
                    abs(source.b - target.b) < threshold):
                p.select = True

    bpy.ops.object.editmode_toggle()


class SelectByVertexColor(bpy.types.Operator):
    bl_idname = 'mesh.select_similar_kcl_flags'
    bl_label = 'Select By Vertex Color'
    bl_options = {'REGISTER', 'UNDO'}

    # @classmethod
    # def poll(cls, context):
    #     obj = context.active_object
    #     return (obj and obj.type == 'MESH')

    def execute(self, context):
        select_by_vertex_color(context.active_object)
        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(SelectByVertexColor.bl_idname)


def register():
    bpy.utils.register_class(SelectByVertexColor)
    bpy.types.VIEW3D_MT_edit_mesh_select_similar.append(menu_func)  # Adds the new operator to an existing menu.


def unregister():
    bpy.utils.unregister_class(SelectByVertexColor)


if __name__ == "__main__":
    register()
