"""@ package docstring
Virtual Camera represent view direction
"""

from common import *

# -----------------------------------------------------------------------------#
# Camera
# -----------------------------------------------------------------------------#


class Camera:
    """Virtual Camera

    """
    def __init__(self, fovy, viewport_w, viewport_h):
        self.__fovy = fovy
        self.__viewport_w = max(viewport_w, 1)
        self.__viewport_h = max(viewport_h, 1)
        self.__aspect = self.__viewport_w / self.__viewport_h
        self.__z_near = 4.0
        self.__z_far = 4096.0
        self.__eye_center = Vec3(0.0, 0.0, 0.0)
        self.__eye_pos = Vec3(0.0, -1.0, 0.0)
        self.__eye_up = Vec3(0.0, 0.0, 1.0)

    def set_pos(self, cam_pos, view_ctr, z_near, z_far):
        self.__z_near = z_near
        self.__z_far = z_far
        self.__eye_center.set(view_ctr.x, view_ctr.y, view_ctr.y)
        self.__eye_pos.set(cam_pos.x, cam_pos.y, cam_pos.z)
        self.__eye_up = Vec3(0.0, 1.0, 0.0)

    def set_fovy(self, value):
        self.__fovy = value

    @property
    def eye_pos(self):
        return self.__eye_pos

    @property
    def eye_center(self):
        return self.__eye_center

    @property
    def eye_up(self):
        return self.__eye_up

    @property
    def fovy(self):
        return self.__fovy

    @property
    def viewport_w(self):
        return self.__viewport_w

    @property
    def viewport_h(self):
        return self.__viewport_h

    @property
    def z_near(self):
        return self.__z_near

    @property
    def z_far(self):
        return self.__z_far

    def zoom(self, factor):
        """zoom in or zoom out the view"""
        eye_backward = self.__eye_pos - self.__eye_center
        cur_distance = eye_backward.normalize()
        cur_distance *= factor

        # clamp
        if cur_distance < self.__z_near:
            cur_distance = self.__z_near
        if cur_distance > self.__z_far:
            cur_distance = self.__z_far

        self.__eye_pos = self.__eye_center + eye_backward * cur_distance

    def translate(self, delta_pixel_x: int, delta_pixel_y: int):
        eye_forward = self.__eye_center - self.__eye_pos
        cur_distance = eye_forward.normalize()

        world_y = cur_distance * math.tan(math.radians(self.__fovy) * 0.5) * 2.0

        distance_per_pixel = world_y / self.__viewport_h
        side_move = delta_pixel_x * distance_per_pixel
        up_move = delta_pixel_y * distance_per_pixel

        eye_right = Vec3.cross_product(eye_forward, self.__eye_up)
        eye_right.normalize()

        delta_right = eye_right * side_move
        delta_up = self.__eye_up * up_move
        total_delta = delta_right + delta_up

        self.__eye_pos += total_delta
        self.__eye_center += total_delta

    def rotate_around_center(self, delta_yaw_in_rad: float, delta_pitch_in_rad: float):
        """rotate the camera around the viewing center"""

        eye_forward = self.__eye_center - self.__eye_pos
        cur_distance = eye_forward.normalize()

        # rotate forward vector around up vector (yaw)
        mat_rot = Mat3()
        mat_rot.rotate(delta_yaw_in_rad, self.__eye_up)
        mat_rot.transform_inplace(eye_forward)
        eye_forward.normalize()

        # calculate right vector after forward vector rotated around up vector
        eye_right = Vec3.cross_product(eye_forward, self.__eye_up)
        eye_right.normalize()

        # rotate forward vector around right vector (pitch)
        mat_rot.rotate(delta_pitch_in_rad, eye_right)
        mat_rot.transform_inplace(eye_forward)
        eye_forward.normalize()

        # calculate new up vector
        self.__eye_up = Vec3.cross_product(eye_right, eye_forward)
        self.__eye_up.normalize()

        center_to_eye = Vec3(0.0, 0.0, 0.0)
        center_to_eye.x = -eye_forward.x
        center_to_eye.y = -eye_forward.y
        center_to_eye.z = -eye_forward.z

        delta = center_to_eye * cur_distance

        # update eye position
        self.__eye_pos = self.__eye_center + delta
