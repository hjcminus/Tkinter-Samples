"""@ package docstring
mathlib etc.

"""

import math
from abc import ABC, abstractmethod
from threading import Thread
from queue import Queue     # python built-in thread-safe queue


# ------------------------------------------------------------------------------#
# math
# ------------------------------------------------------------------------------#


def inv(f):
    if math.fabs(f) > 0.00000001:
        return 1.0 / f
    else:
        if f > 0.0:
            return math.inf
        else:
            return -math.inf


# ------------------------------------------------------------------------------#
# Vec2
# ------------------------------------------------------------------------------#
class Vec2:
    
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f'({self.x},{self.y})'

    def set(self, x, y):
        self.x = x
        self.y = y

    def zero(self):
        self.x = 0.0
        self.y = 0.0

    def inv(self):
        return Vec2(inv(self.x), inv(self.y))
    
    def __sub__(self, other):
        return Vec2(self.x - other.x, self.y - other.y)
    
    def __add__(self, other):
        return Vec2(self.x + other.x, self.y + other.y)
    
    def __mul__(self, factor):
        return Vec2(self.x * factor, self.y * factor)
    
    def length(self):
        return math.sqrt(self.x * self.x + self.y * self.y)
    
    def normalize(self):
        l_ = self.length()
        if l_ > 0.0:
            f = 1.0 / l_
            self.x *= f
            self.y *= f
        return l_

    @staticmethod
    def dot_product(v1, v2):
        return v1.x * v2.x + v1.y * v2.y

    
# ------------------------------------------------------------------------------#
# Vec3
# ------------------------------------------------------------------------------#


class Vec3:

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return f'({self.x},{self.y},{self.z})'

    def set(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def zero(self):
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0

    def inv(self):
        return Vec3(inv(self.x), inv(self.y), inv(self.z))

    def __sub__(self, other):
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __add__(self, other):
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __mul__(self, factor):
        return Vec3(self.x * factor, self.y * factor, self.z * factor)

    def length(self):
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def normalize(self):
        l_ = self.length()
        if l_ > 0.0:
            f = 1.0 / l_
            self.x *= f
            self.y *= f
            self.z *= f
        return l_

    @staticmethod
    def dot_product(v1, v2):
        return v1.x * v2.x + v1.y * v2.y + v1.z * v2.z

    @staticmethod
    def cross_product(v1, v2):
        r = Vec3(0.0, 0.0, 0.0)

        r.x = v1.y * v2.z - v1.z * v2.y
        r.y = v1.z * v2.x - v1.x * v2.z
        r.z = v1.x * v2.y - v1.y * v2.x

        return r

    
# ------------------------------------------------------------------------------#
# Vec4
# ------------------------------------------------------------------------------#


class Vec4:

    def __init__(self, x, y, z, w):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def __str__(self):
        return f'({self.x},{self.y},{self.z},{self.w})'
        
    def set(self, x, y, z, w):
        self.x = x
        self.y = y
        self.z = z
        self.w = w
        
    def zero(self):
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        self.w = 0.0

    def inv(self):
        return Vec4(inv(self.x), inv(self.y), inv(self.z), inv(self.w))

    def __sub__(self, other):
        return Vec4(self.x - other.x, self.y - other.y, self.z - other.z, self.w - other.w)

    def __add__(self, other):
        return Vec4(self.x + other.x, self.y + other.y, self.z + other.z, self.w + other.w)

    def __mul__(self, factor):
        return Vec4(self.x * factor, self.y * factor, self.z * factor, self.w * factor)
  
# ------------------------------------------------------------------------------#
# Mat3
# ------------------------------------------------------------------------------#


class Mat3:
    def __init__(self):
        self.elem = [Vec3(1.0, 0.0, 0.0),
                     Vec3(0.0, 1.0, 0.0),
                     Vec3(0.0, 0.0, 1.0)]

    def identity(self):
        self.elem[0].set(1.0, 0.0, 0.0)
        self.elem[1].set(0.0, 1.0, 0.0)
        self.elem[2].set(0.0, 0.0, 1.0)

    def zero(self):
        self.elem[0].zero()
        self.elem[1].zero()
        self.elem[2].zero()

    def __mul__(self, other):
        r = Mat3()

        # x
        r.elem[0].x = \
            self.elem[0].x * other.elem[0].x + \
            self.elem[1].x * other.elem[0].y + \
            self.elem[2].x * other.elem[0].z

        r.elem[1].x = \
            self.elem[0].x * other.elem[1].x + \
            self.elem[1].x * other.elem[1].y + \
            self.elem[2].x * other.elem[1].z

        r.elem[2].x = \
            self.elem[0].x * other.elem[2].x + \
            self.elem[1].x * other.elem[2].y + \
            self.elem[2].x * other.elem[2].z

        # y
        r.elem[0].y = \
            self.elem[0].y * other.elem[0].x + \
            self.elem[1].y * other.elem[0].y + \
            self.elem[2].y * other.elem[0].z

        r.elem[1].y = \
            self.elem[0].y * other.elem[1].x + \
            self.elem[1].y * other.elem[1].y + \
            self.elem[2].y * other.elem[1].z

        r.elem[2].y = \
            self.elem[0].y * other.elem[2].x + \
            self.elem[1].y * other.elem[2].y + \
            self.elem[2].y * other.elem[2].z

        # z
        r.elem[0].z = \
            self.elem[0].z * other.elem[0].x + \
            self.elem[1].z * other.elem[0].y + \
            self.elem[2].z * other.elem[0].z

        r.elem[1].z = \
            self.elem[0].z * other.elem[1].x + \
            self.elem[1].z * other.elem[1].y + \
            self.elem[2].z * other.elem[1].z

        r.elem[2].z = \
            self.elem[0].z * other.elem[2].x + \
            self.elem[1].z * other.elem[2].y + \
            self.elem[2].z * other.elem[2].z

        return r

    def rotate(self, rad, vec3_axes):
        axes = Vec3(vec3_axes.x, vec3_axes.y, vec3_axes.z)
        axes.normalize()

        x = axes.x
        y = axes.y
        z = axes.z

        s = math.sin(rad)
        c = math.cos(rad)

        one_minus_c = 1.0 - c
        xy_one_minus_c = x * y * one_minus_c
        xz_one_minus_c = x * z * one_minus_c
        yz_one_minus_c = y * z * one_minus_c

        xs = x * s
        ys = y * s
        zs = z * s

        self.elem[0].x = c + x * x * one_minus_c
        self.elem[0].y = xy_one_minus_c + zs
        self.elem[0].z = xz_one_minus_c - ys

        self.elem[1].x = xy_one_minus_c - zs
        self.elem[1].y = c + y * y * one_minus_c
        self.elem[1].z = yz_one_minus_c + xs

        self.elem[2].x = xz_one_minus_c + ys
        self.elem[2].y = yz_one_minus_c - xs
        self.elem[2].z = c + z * z * one_minus_c

    def transform(self, vec3):
        r = Vec3(0.0, 0.0, 0.0)

        r.x = self.elem[0].x * vec3.x + self.elem[1].x * vec3.y + self.elem[2].x * vec3.z
        r.y = self.elem[0].y * vec3.x + self.elem[1].y * vec3.y + self.elem[2].y * vec3.z
        r.z = self.elem[0].z * vec3.x + self.elem[1].z * vec3.y + self.elem[2].z * vec3.z

        return r

    def transform_inplace(self, vec3):
        r = self.transform(vec3)
        vec3.x = r.x
        vec3.y = r.y
        vec3.z = r.z


# ------------------------------------------------------------------------------#
# Mat4
# ------------------------------------------------------------------------------#


class Mat4:
    def __init__(self):
        self.elem = [Vec4(1.0, 0.0, 0.0, 0.0),
                     Vec4(0.0, 1.0, 0.0, 0.0),
                     Vec4(0.0, 0.0, 1.0, 0.0),
                     Vec4(0.0, 0.0, 0.0, 1.0)]
        
    def identity(self):
        self.elem[0].set(1.0, 0.0, 0.0, 0.0)
        self.elem[1].set(0.0, 1.0, 0.0, 0.0)
        self.elem[2].set(0.0, 0.0, 1.0, 0.0)
        self.elem[3].set(0.0, 0.0, 0.0, 1.0)
        
    def zero(self):
        self.elem[0].zero()
        self.elem[1].zero()
        self.elem[2].zero()
        self.elem[3].zero()
        
    def __mul__(self, other):
        r = Mat4()  # create a new matrix to store the multiplication result

        # x
        r.elem[0].x = \
            self.elem[0].x * other.elem[0].x + \
            self.elem[1].x * other.elem[0].y + \
            self.elem[2].x * other.elem[0].z + \
            self.elem[3].x * other.elem[0].w
        
        r.elem[1].x = \
            self.elem[0].x * other.elem[1].x + \
            self.elem[1].x * other.elem[1].y + \
            self.elem[2].x * other.elem[1].z + \
            self.elem[3].x * other.elem[1].w
    
        r.elem[2].x = \
            self.elem[0].x * other.elem[2].x + \
            self.elem[1].x * other.elem[2].y + \
            self.elem[2].x * other.elem[2].z + \
            self.elem[3].x * other.elem[2].w
        
        r.elem[3].x = \
            self.elem[0].x * other.elem[3].x + \
            self.elem[1].x * other.elem[3].y + \
            self.elem[2].x * other.elem[3].z + \
            self.elem[3].x * other.elem[3].w

        # y
        r.elem[0].y = \
            self.elem[0].y * other.elem[0].x + \
            self.elem[1].y * other.elem[0].y + \
            self.elem[2].y * other.elem[0].z + \
            self.elem[3].y * other.elem[0].w

        r.elem[1].y = \
            self.elem[0].y * other.elem[1].x + \
            self.elem[1].y * other.elem[1].y + \
            self.elem[2].y * other.elem[1].z + \
            self.elem[3].y * other.elem[1].w

        r.elem[2].y = \
            self.elem[0].y * other.elem[2].x + \
            self.elem[1].y * other.elem[2].y + \
            self.elem[2].y * other.elem[2].z + \
            self.elem[3].y * other.elem[2].w

        r.elem[3].y = \
            self.elem[0].y * other.elem[3].x + \
            self.elem[1].y * other.elem[3].y + \
            self.elem[2].y * other.elem[3].z + \
            self.elem[3].y * other.elem[3].w
        
        # z
        r.elem[0].z = \
            self.elem[0].z * other.elem[0].x + \
            self.elem[1].z * other.elem[0].y + \
            self.elem[2].z * other.elem[0].z + \
            self.elem[3].z * other.elem[0].w

        r.elem[1].z = \
            self.elem[0].z * other.elem[1].x + \
            self.elem[1].z * other.elem[1].y + \
            self.elem[2].z * other.elem[1].z + \
            self.elem[3].z * other.elem[1].w

        r.elem[2].z = \
            self.elem[0].z * other.elem[2].x + \
            self.elem[1].z * other.elem[2].y + \
            self.elem[2].z * other.elem[2].z + \
            self.elem[3].z * other.elem[2].w

        r.elem[3].z = \
            self.elem[0].z * other.elem[3].x + \
            self.elem[1].z * other.elem[3].y + \
            self.elem[2].z * other.elem[3].z + \
            self.elem[3].z * other.elem[3].w
    
        # w
        r.elem[0].w = \
            self.elem[0].w * other.elem[0].x + \
            self.elem[1].w * other.elem[0].y + \
            self.elem[2].w * other.elem[0].z + \
            self.elem[3].w * other.elem[0].w

        r.elem[1].w = \
            self.elem[0].w * other.elem[1].x + \
            self.elem[1].w * other.elem[1].y + \
            self.elem[2].w * other.elem[1].z + \
            self.elem[3].w * other.elem[1].w

        r.elem[2].w = \
            self.elem[0].w * other.elem[2].x + \
            self.elem[1].w * other.elem[2].y + \
            self.elem[2].w * other.elem[2].z + \
            self.elem[3].w * other.elem[2].w

        r.elem[3].w = \
            self.elem[0].w * other.elem[3].x + \
            self.elem[1].w * other.elem[3].y + \
            self.elem[2].w * other.elem[3].z + \
            self.elem[3].w * other.elem[3].w
    
        return r
        
    def look_at(self, vec3_eye, vec3_center, vec3_up):
        forward = vec3_center - vec3_eye
        forward.normalize()
        
        up_ = Vec3(vec3_up.x, vec3_up.y, vec3_up.z)
        up_.normalize()
        
        side = Vec3.cross_product(forward, up_)
        
        self.elem[0].x = side.x
        self.elem[1].x = side.y
        self.elem[2].x = side.z
        self.elem[3].x = -Vec3.dot_product(side, vec3_eye)
        
        self.elem[0].y = up_.x
        self.elem[1].y = up_.y
        self.elem[2].y = up_.z
        self.elem[3].y = -Vec3.dot_product(up_, vec3_eye)
        
        self.elem[0].z = -forward.x
        self.elem[1].z = -forward.y
        self.elem[2].z = -forward.z
        self.elem[3].z = Vec3.dot_product(forward, vec3_eye)
        
        self.elem[0].w = self.elem[1].w = self.elem[2].w = 0.0
        self.elem[3].w = 1.0
    
    def perspective(self, fovy_rad, width_over_height, z_near, z_far):
        t = math.tan(fovy_rad * 0.5)

        tp = t * z_near
        rt = tp * width_over_height
        
        self.frustum(-rt, rt, -tp, tp, z_near, z_far)

    # make a perspective projection matrix
    def frustum(self, left, right, bottom, top, z_near, z_far):
        self.zero()
        
        r_sub_l = right - left
        r_add_l = right + left
        t_add_b = top + bottom
        t_sub_b = top - bottom
        n_mul_2 = z_near * 2.0
        f_add_n = z_far + z_near
        f_sub_n = z_far - z_near

        inv_f_sub_n = inv(f_sub_n)
        
        self.elem[0].x = n_mul_2 / r_sub_l
        self.elem[1].y = n_mul_2 / t_sub_b
        self.elem[2].x = r_add_l / r_sub_l
        self.elem[2].y = t_add_b / t_sub_b
        self.elem[2].z = -f_add_n * inv_f_sub_n
        self.elem[2].w = -1.0
        self.elem[3].z = -2.0 * z_near * z_far * inv_f_sub_n

    # make an orthographic projection matrix
    def ortho(self, left, right, bottom, top, z_near, z_far):
        self.zero()

        r_sub_l = right - left
        t_sub_b = top - bottom
        f_sub_n = z_far - z_near

        self.elem[0].x = 2.0 / r_sub_l
        self.elem[1].y = 2.0 / t_sub_b
        self.elem[2].z = -2.0 / f_sub_n
        self.elem[3].x = -(right + left) / r_sub_l
        self.elem[3].y = -(top + bottom) / t_sub_b
        self.elem[3].z = -(z_far + z_near) / f_sub_n
        self.elem[3].w = 1.0

    # make a rotation matrix: rotate point around an axes specified in vec3_axes by rad angle
    def rotate(self, rad, vec3_axes):
        axes = Vec3(vec3_axes.x, vec3_axes.y, vec3_axes.z)
        axes.normalize()
        
        x = axes.x
        y = axes.y
        z = axes.z
        
        s = math.sin(rad)
        c = math.cos(rad)

        one_minus_c = 1.0 - c
        xy_one_minus_c = x * y * one_minus_c
        xz_one_minus_c = x * z * one_minus_c
        yz_one_minus_c = y * z * one_minus_c
        
        xs = x * s
        ys = y * s
        zs = z * s
        
        self.elem[0].x = c + x * x * one_minus_c
        self.elem[0].y = xy_one_minus_c + zs
        self.elem[0].z = xz_one_minus_c - ys
        self.elem[0].w = 0.0

        self.elem[1].x = xy_one_minus_c - zs
        self.elem[1].y = c + y * y * one_minus_c
        self.elem[1].z = yz_one_minus_c + xs
        self.elem[1].w = 0.0
        
        self.elem[2].x = xz_one_minus_c + ys
        self.elem[2].y = yz_one_minus_c - xs
        self.elem[2].z = c + z * z * one_minus_c
        self.elem[2].w = 0.0
        
        self.elem[3].x = 0.0
        self.elem[3].y = 0.0
        self.elem[3].z = 0.0
        self.elem[3].w = 0.0
        
    def scale(self, sx, sy, sz):
        self.zero()
        self.elem[0].x = sx
        self.elem[1].y = sy
        self.elem[2].z = sz
        self.elem[3].w = 1.0
    
    def translate(self, dx, dy, dz):
        self.identity()
        self.elem[3].x = dx
        self.elem[3].y = dy
        self.elem[3].z = dz

    def transform(self, vec4):
        r = Vec4(0.0, 0.0, 0.0, 0.0)

        r.x = self.elem[0].x * vec4.x + self.elem[1].x * vec4.y + self.elem[2].x * vec4.z + self.elem[3].x * vec4.w
        r.y = self.elem[0].y * vec4.x + self.elem[1].y * vec4.y + self.elem[2].y * vec4.z + self.elem[3].y * vec4.w
        r.z = self.elem[0].z * vec4.x + self.elem[1].z * vec4.y + self.elem[2].z * vec4.z + self.elem[3].z * vec4.w
        r.w = self.elem[0].w * vec4.x + self.elem[1].w * vec4.y + self.elem[2].w * vec4.z + self.elem[3].w * vec4.w
    
        return r

    def transform_inplace(self, vec4):
        r = self.transform(vec4)
        vec4.x = r.x
        vec4.y = r.y
        vec4.z = r.z
        vec4.w = r.w

# ------------------------------------------------------------------------------#
# Line3D
# ------------------------------------------------------------------------------#


class Line3D:
    def __init__(self, vec3_pt1, vec3_pt2):
        self.pt1 = vec3_pt1
        self.pt2 = vec3_pt2

    
# ------------------------------------------------------------------------------#
# CanvasIntf
# ------------------------------------------------------------------------------#


class CanvasIntf(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def clear(self):
        pass

    @abstractmethod
    def draw_line(self, vec2_pt1, vec2_pt2):
        pass


# ------------------------------------------------------------------------------#
# ParallelJobSys
# ------------------------------------------------------------------------------#


class ParallelJobSys:
    class ParallelThread(Thread):
        def __init__(self, job_queue):
            Thread.__init__(self)
            self.__job_queue = job_queue

        # override
        def run(self):
            while True:
                job = self.__job_queue.get()
                if job is None:
                    self.__job_queue.task_done()
                    break
                else:
                    job.exec()
                    self.__job_queue.task_done()

    def __init__(self):
        self.__job_queue = Queue()
        self.__thread_pool = []

        for i in range(0, 4):
            trd = ParallelJobSys.ParallelThread(self.__job_queue)
            self.__thread_pool.append(trd)
            trd.start()

    def quit(self):
        trd_sz = len(self.__thread_pool)
        for i in range(0, trd_sz):
            self.push_job(None)

        for trd in self.__thread_pool:
            trd.join()

        self.__thread_pool.clear()

    def push_job(self, job):
        self.__job_queue.put(job)


# ------------------------------------------------------------------------------#
# globals
# ------------------------------------------------------------------------------#

g_font_tuple = ('SimSun', 10)

PROJ_MODE_PERSPECTIVE = "Perspective"
PROJ_MODE_ORTHOGRAPHIC = "Orthographic"
