"""@ package docstring
Main business object that load, display meshes

"""

import math

from common import CanvasIntf, Vec3, Line3D
from renderer import Renderer
from camera import Camera
from ply_file import load_ply_model


# -----------------------------------------------------------------------------#
# ModelViewer
# -----------------------------------------------------------------------------#


class ModelViewer:
    def __init__(self, canvas_intf: CanvasIntf, fovy, proj_mode, viewport_w, viewport_h):
        self.__renderer = Renderer(canvas_intf)
        self.__renderer.set_proj_mode(proj_mode)
        self.__camera = Camera(fovy, viewport_w, viewport_h)
        self.__model_lines = []
        self.__model_center = Vec3(0.0, 0.0, 0.0)
        self.__model_size = Vec3(0.0, 0.0, 0.0)

    def quit(self):
        self.__renderer.quit()

    def set_fovy(self, fovy):
        self.__camera.set_fovy(fovy)
        self.draw()

    def set_proj_mode(self, proj_mode):
        self.__renderer.set_proj_mode(proj_mode)

    def zoom_camera(self, factor):
        self.__camera.zoom(factor)
        self.draw()

    def translate_camera(self, delta_pixel_x: int, delta_pixel_y: int):
        self.__camera.translate(delta_pixel_x, delta_pixel_y)
        self.draw()

    def rotate_camera_around_center(self, delta_yaw_in_deg: float, delta_pitch_in_deg: float):
        self.__camera.rotate_around_center(math.radians(delta_yaw_in_deg), math.radians(delta_pitch_in_deg))
        self.draw()

    def load_model(self, filename):
        try:
            self.__model_lines, model_min, model_max = load_ply_model(filename)
            self.__model_center = (model_min + model_max) * 0.5
            self.__model_size = model_max - model_min
            self.__init_camera_pos()
            self.draw()
        except Exception as e:
            print(f'load_model error: {e}\n')

    def load_test_cube(self):
        self.clear_model()

        # x
        self.__model_lines.append(Line3D(Vec3(1.0, -1.0, -1.0), Vec3(1.0, 1.0, -1.0)))
        self.__model_lines.append(Line3D(Vec3(1.0, -1.0, 1.0), Vec3(1.0, 1.0, 1.0)))

        self.__model_lines.append(Line3D(Vec3(-1.0, -1.0, -1.0), Vec3(-1.0, 1.0, -1.0)))
        self.__model_lines.append(Line3D(Vec3(-1.0, -1.0, 1.0), Vec3(-1.0, 1.0, 1.0)))

        # y
        self.__model_lines.append(Line3D(Vec3(-1.0, 1.0, -1.0), Vec3(1.0, 1.0, -1.0)))
        self.__model_lines.append(Line3D(Vec3(-1.0, 1.0, 1.0), Vec3(1.0, 1.0, 1.0)))

        self.__model_lines.append(Line3D(Vec3(-1.0, -1.0, -1.0), Vec3(1.0, -1.0, -1.0)))
        self.__model_lines.append(Line3D(Vec3(-1.0, -1.0, 1.0), Vec3(1.0, -1.0, 1.0)))

        # z
        self.__model_lines.append(Line3D(Vec3(-1.0, -1.0, -1.0), Vec3(-1.0, -1.0, 1.0)))
        self.__model_lines.append(Line3D(Vec3(1.0, -1.0, -1.0), Vec3(1.0, -1.0, 1.0)))

        self.__model_lines.append(Line3D(Vec3(-1.0, 1.0, -1.0), Vec3(-1.0, 1.0, 1.0)))
        self.__model_lines.append(Line3D(Vec3(1.0, 1.0, -1.0), Vec3(1.0, 1.0, 1.0)))

        self.__model_center.zero()
        self.__model_size.set(2.0, 2.0, 2.0)

        self.__init_camera_pos()
        self.draw()

    def clear_model(self):
        self.__model_lines.clear()
        self.draw()

    def draw(self):
        self.__renderer.draw(self.__camera.eye_pos,
                             self.__camera.eye_center,
                             self.__camera.eye_up,
                             self.__camera.fovy,
                             self.__camera.viewport_w,
                             self.__camera.viewport_h,
                             self.__camera.z_near,
                             self.__camera.z_far,
                             self.__model_lines)

    def __init_camera_pos(self):
        max_dim = max(self.__model_size.x, max(self.__model_size.y, self.__model_size.z))
        z_far = max_dim * 4.0       # 2.0  4.0

        cam_pos = Vec3(self.__model_center.x, self.__model_center.y, self.__model_center.z - max_dim * 2.0)
        self.__camera.set_pos(cam_pos, self.__model_center, z_far * 0.001, z_far)
