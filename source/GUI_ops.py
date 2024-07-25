import bpy
from .Enums import Operators, Rotation, Zoom
from .Rig import Rig
from .LOD import LOD
from .Sun import Sun
from .Camera import Camera
from .Renderer import Renderer
from bpy.props import StringProperty


# The OK button in the error dialog
class OkOperator(bpy.types.Operator):
    bl_idname = "error.ok"
    bl_label = "OK"

    def execute(self, context):
        return {'FINISHED'}


class MessageOperator(bpy.types.Operator):
    bl_idname = "error.message"
    bl_label = "Message"
    type: StringProperty()
    message: StringProperty()

    def execute(self, context):
        self.report({'INFO'}, self.message)
        print(self.message)
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_popup(self, width=400)

    def draw(self, context):
        self.layout.label(text="A message has arrived")
        row = self.layout.split(factor=0.25)
        row.prop(self, "type")
        row.prop(self, "message")
        row = self.layout.split(factor=0.80)
        row.label(text="")
        row.operator("error.ok")


class B4BRender(bpy.types.Operator):
    bl_idname = Operators.RENDER.value[0]
    bl_label = "Render all zooms & rotations"

    def execute(self, context):
        group = context.scene.group_id if context.scene.group_id != "default" else None
        steps = [(z, v) for z in Zoom for v in Rotation]
        for i, (z, v) in enumerate(steps):
            print(f"Step ({i+1}/{len(steps)}): zoom {z.value+1}, rotation {v.name}")
            Rig.setup(v, z)
            Renderer.generate_output(v, z, group)

        print("FINISHED")
        return {"FINISHED"}


class B4BPreview(bpy.types.Operator):
    bl_idname = Operators.PREVIEW.value[0]
    bl_label = "Preview"

    def execute(self, context):
        v = Rotation[context.window_manager.interface_vars.rotation]
        z = Zoom[context.window_manager.interface_vars.zoom]
        Rig.setup(v, z)
        # q: pass the context to the renderer? or just grab it from internals..
        Renderer.generate_preview(z)
        return {'FINISHED'}


class B4BLODExport(bpy.types.Operator):
    bl_idname = Operators.LOD_EXPORT.value[0]
    bl_label = "LODExport"

    def execute(self, context):
        LOD.export()
        return {'FINISHED'}


class B4BLODAdd(bpy.types.Operator):
    r"""Fit the LOD around all meshes that are rendered. Create the LOD if necessary"""
    bl_idname = Operators.LOD_FIT.value[0]
    bl_label = "LOD fit"

    def execute(self, context):
        Rig.lod_fit()
        return {'FINISHED'}


class B4BLODDelete(bpy.types.Operator):
    bl_idname = Operators.LOD_DELETE.value[0]
    bl_label = "LODDelete"

    def execute(self, context):
        Rig.lod_delete()
        return {'FINISHED'}


class B4BSunDelete(bpy.types.Operator):
    bl_idname = Operators.SUN_DELETE.value[0]
    bl_label = "SunDelete"

    def execute(self, context):
        Sun.delete_from_scene()
        return {'FINISHED'}


class B4BSunAdd(bpy.types.Operator):
    bl_idname = Operators.SUN_ADD.value[0]
    bl_label = "SunAdd"

    def execute(self, context):
        Sun.add_to_scene()
        return {'FINISHED'}


class B4BCamAdd(bpy.types.Operator):
    bl_idname = Operators.CAM_ADD.value[0]
    bl_label = "CamAdd"

    def execute(self, context):
        Camera.add_to_scene()
        return {'FINISHED'}


class B4BCamDelete(bpy.types.Operator):
    bl_idname = Operators.CAM_DELETE.value[0]
    bl_label = "CamDelete"

    def execute(self, context):
        Camera.delete_from_scene()
        return {'FINISHED'}
