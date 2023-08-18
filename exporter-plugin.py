# Blender Add-on Template
# Contributor(s): Lok Lok (lok@agape.games)
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
"name": "Exporter Plugin",
"description": "Export to nodejs",
"author": "Lok Lok",
"version": (1, 0),
"blender": (2, 80, 0),
"location": "Properties > Render > My Exporter Panel",
"warning": "", # used for warning icon and text in add-ons panel
"wiki_url": "https://agape.games",
"tracker_url": "https://agape.games",
"support": "COMMUNITY",
"category": "Render"
}

import requests
import bpy

def server_start():
    url = 'http://localhost:3001/file'

    filePath = bpy.app.tempdir + 'temp.glb'

    bpy.ops.export_scene.gltf(
      filepath=filePath,
    #  export_format='GLTF_EMBEDDED',
        use_selection=True,
        export_draco_mesh_compression_enable=True
    )

    with open(filePath, 'rb') as f:
        data = f.read()
        x = requests.post(
            url,
            data = data,
            headers={'Content-Type': 'application/octet-stream'}
        )

def server_stop():
    print('stop')


class ExportGLBFile(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.simple_operator1"
    bl_label = "ExportGLBFile"

    def execute(self, context):
        server_start();
        return {'FINISHED'}

class StopServer(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.simple_operator2"
    bl_label = "StopServer"

    def execute(self, context):
        server_stop();
        return {'FINISHED'}


class HelloWorldPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Blender Live Link"
    bl_idname = "SCENE_PT_layout"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.operator(ExportGLBFile.bl_idname)

        row = layout.row()
        row.operator(StopServer.bl_idname)


def register():
    bpy.utils.register_class(HelloWorldPanel)
    bpy.utils.register_class(ExportGLBFile)
    # bpy.utils.register_class(StopServer)


def unregister():
    bpy.utils.unregister_class(HelloWorldPanel)
    bpy.utils.unregister_class(ExportGLBFile)
    # bpy.utils.unregister_class(StopServer)

if __name__ == "__main__":
    register()
