"""@ package docstring
Renderer

convert 3d line segments into 2d screen space counterpart
"""

import math

import common
from common import CanvasIntf, Vec2, Vec3, Vec4, Mat4, ParallelJobSys
from threading import Lock
import time


# -----------------------------------------------------------------------------#
# Renderer
# -----------------------------------------------------------------------------#


class Renderer:

    class RunGeometryPipeline:

        def __init__(self, renderer, clip_planes, mat, viewport_w, viewport_h,
                     lines_3d, start_idx, stop_idx, canvas_lines_pool):
            self.__renderer = renderer
            self.__mat = mat
            self.__viewport_h = viewport_h
            self.__half_viewport_w = viewport_w * 0.5
            self.__half_viewport_h = viewport_h * 0.5
            self.__lines_3d = lines_3d
            self.__start_idx = start_idx
            self.__stop_idx = stop_idx
            self.__canvas_lines_pool = canvas_lines_pool
            self.__clip_planes = clip_planes

        def convert_to_screen_space(self, v4):
            # do perspective division
            x = v4.x / v4.w
            y = v4.y / v4.w

            # convert to screen space
            x_ = x * self.__half_viewport_w + self.__half_viewport_w
            y_ = y * self.__half_viewport_h + self.__half_viewport_h

            v2 = Vec2(x_, self.__viewport_h - y_)  # flip y

            return v2

        def exec(self):

            def clip_line_segment(clip_pt1, clip_pt2) -> list:

                def clip_point_inside_clip_plane(pt) -> bool:
                    return (clip_plane.x * pt.x +
                            clip_plane.y * pt.y +
                            clip_plane.z * pt.z +
                            clip_plane.w * pt.w) >= 0.0

                def calc_intersect(pt1, pt2):
                    dist_pt1 = clip_plane.x * pt1.x + clip_plane.y * pt1.y + clip_plane.z * pt1.z + clip_plane.w * pt1.w
                    dist_pt2 = clip_plane.x * pt2.x + clip_plane.y * pt2.y + clip_plane.z * pt2.z + clip_plane.w * pt2.w

                    f = -dist_pt1 / (dist_pt2 - dist_pt1)
                    delta = pt2 - pt1
                    return pt1 + delta * f

                local_clip_result = [clip_pt1, clip_pt2]

                for clip_plane in self.__clip_planes:   # clip to each plane
                    if len(local_clip_result) != 2:
                        return local_clip_result   # clipped away

                    clip_pt1 = local_clip_result[0]
                    clip_pt2 = local_clip_result[1]
                    local_clip_result.clear()

                    if clip_point_inside_clip_plane(clip_pt1):
                        if not clip_point_inside_clip_plane(clip_pt2):
                            inter_pt = calc_intersect(clip_pt1, clip_pt2)
                            local_clip_result.append(clip_pt1)
                            local_clip_result.append(inter_pt)
                        else:
                            local_clip_result.append(clip_pt1)
                            local_clip_result.append(clip_pt2)
                    elif clip_point_inside_clip_plane(clip_pt2):
                        inter_pt = calc_intersect(clip_pt1, clip_pt2)
                        local_clip_result.append(inter_pt)
                        local_clip_result.append(clip_pt2)

                return local_clip_result

            for i in range(self.__start_idx, self.__stop_idx):
                line3d = self.__lines_3d[i]

                # clip avoid w <= 0.0    if w < 0.0 will course object flipping

                # clip in homogeneous clip space

                # point inside the clip volume
                # -clip.w <= clip.x <= clip.w
                # -clip.w <= clip.y <= clip.w
                # -clip.w <= clip.z <= clip.w

                vec4_pt1 = Vec4(line3d.pt1.x, line3d.pt1.y, line3d.pt1.z, 1.0)
                vec4_prj_pt1 = self.__mat.transform(vec4_pt1)

                vec4_pt2 = Vec4(line3d.pt2.x, line3d.pt2.y, line3d.pt2.z, 1.0)
                vec4_prj_pt2 = self.__mat.transform(vec4_pt2)

                clip_result = clip_line_segment(vec4_prj_pt1, vec4_prj_pt2)
                if len(clip_result) == 2:
                    # entirely or partially inside the clip volume
                    pt1_2d = self.convert_to_screen_space(clip_result[0])
                    pt2_2d = self.convert_to_screen_space(clip_result[1])
                    self.__canvas_lines_pool.append((pt1_2d, pt2_2d))

            self.__renderer.inc_finished_tasks()

    def __init__(self, canvas_intf: CanvasIntf):
        self.__parallel_job_sys = ParallelJobSys()
        self.__canvas_intf = canvas_intf
        self.__lock = Lock()
        self.__finished_tasks = 0

        self.__projection_matrix = Mat4()
        self.__view_matrix = Mat4()

        self.__proj_mode = common.PROJ_MODE_PERSPECTIVE

        # left-handed
        self.__clip_planes = [
            # keep w == 1.0, in function 'clip_point_inside_clip_plane', D = line.w * p.w
            Vec4(0.0, 0.0, 1.0, 1.0),  # near
            Vec4(0.0, 0.0, -1.0, 1.0),  # far
            Vec4(1.0, 0.0, 0.0, 1.0),  # left
            Vec4(-1.0, 0.0, 0.0, 1.0),  # right
            Vec4(0.0, -1.0, 0.0, 1.0),  # top
            Vec4(0.0, 1.0, 0.0, 1.0)  # bottom
        ]

    def quit(self):
        self.__parallel_job_sys.quit()

    def set_proj_mode(self, proj_mode):
        self.__proj_mode = proj_mode

    def inc_finished_tasks(self):
        self.__lock.acquire()
        self.__finished_tasks += 1
        self.__lock.release()

    def __get_finished_tasks(self):
        self.__lock.acquire()
        r = self.__finished_tasks
        self.__lock.release()
        return r

    # lines: defined in 3D space
    def draw(self, eye: Vec3, center: Vec3, up: Vec3, fovy, viewport_w, viewport_h, z_near, z_far, lines):
        if not self.__canvas_intf:
            return

        self.__view_matrix.look_at(eye, center, up)

        if self.__proj_mode == common.PROJ_MODE_PERSPECTIVE:
            self.__projection_matrix.perspective(math.radians(fovy), viewport_w / viewport_h, z_near, z_far)
        else:
            delta = eye - center
            dist = delta.length()
            t = math.tan(math.radians(fovy) * 0.5)
            aspect = viewport_w / viewport_h
            tp = t * dist
            rt = tp * aspect
            self.__projection_matrix.ortho(-rt, rt, -tp, tp, z_near, z_far)

        # setup parameters
        mvp = self.__projection_matrix * self.__view_matrix

        # emit tasks
        line2d_pools1 = []
        line2d_pools2 = []
        line2d_pools3 = []
        line2d_pools4 = []
        line2d_pools_list = [line2d_pools1, line2d_pools2, line2d_pools3, line2d_pools4]

        sz_of_lines = len(lines)
        d = sz_of_lines // 4
        job_count_list = [d, d, d, d + sz_of_lines % 4]

        self.__finished_tasks = 0
        post_job_count = 0
        start_idx = 0
        for i in range(0, 4):
            cur_job_line_cnt = job_count_list[i]
            if cur_job_line_cnt > 0:
                job = Renderer.RunGeometryPipeline(self, self.__clip_planes, mvp, viewport_w, viewport_h,
                                                   lines, start_idx, start_idx + cur_job_line_cnt,
                                                   line2d_pools_list[i])
                start_idx += cur_job_line_cnt
                self.__parallel_job_sys.push_job(job)
                post_job_count += 1

        # wait tasks finish
        while self.__get_finished_tasks() < post_job_count:
            time.sleep(0.001)

        # present
        self.__canvas_intf.clear()
        for i in range(0, 4):
            for line2d in line2d_pools_list[i]:
                self.__canvas_intf.draw_line(line2d[0], line2d[1])
