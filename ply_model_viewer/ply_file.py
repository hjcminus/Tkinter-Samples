"""@ package docstring
load ply file from disk

"""


from enum import IntEnum
from common import Vec3, Line3D


# -----------------------------------------------------------------------------#
# PLY
# -----------------------------------------------------------------------------#

def load_ply_model(filename):

    class FileFormat(IntEnum):
        FMT_ASCII = 1
        FMT_BINARY_BIG = 2
        FMT_BINARY_LIT = 3

    class PropertyType(IntEnum):
        TYPE_FLOAT = 1
        TYPE_UINT8 = 2

    class PropertyName(IntEnum):
        NAME_X = 1
        NAME_Y = 2
        NAME_Z = 3
        NAME_NORMAL_X = 4
        NAME_NORMAL_Y = 5
        NAME_NORMAL_Z = 6
        NAME_CONFIDENCE = 7
        NAME_INTENSITY = 8
        NAME_RED = 9
        NAME_GREEN = 10
        NAME_BLUE = 11
        NAME_ALPHA = 12
        NAME_S = 13
        NAME_T = 14

    def check_head():
        if len(file_lines) < 1:
            raise Exception('empty file')

        first_line = file_lines[0]
        if first_line != 'ply':
            raise Exception('"{}" is not a ply file'.format(first_line))

    def load_format() -> FileFormat:
        for file_line in file_lines:
            if file_line == 'end_header':
                break
            elif file_line.startswith('format ascii'):
                return FileFormat.FMT_ASCII
            elif file_line.startswith('format binary_big_endian'):
                return FileFormat.FMT_BINARY_BIG
            elif file_line.startswith('format binary_little_endian'):
                return FileFormat.FMT_BINARY_LIT

        raise Exception('format section not found')

    def load_vertex_count() -> int:
        for file_line in file_lines:
            if file_line == 'end_header':
                break
            elif file_line.startswith('element vertex'):
                sl = file_line.split()
                if len(sl) >= 3:
                    return int(sl[2])

        raise Exception('element vertex section not found')

    def load_face_count() -> int:
        for file_line in file_lines:
            if file_line == 'end_header':
                break
            elif file_line.startswith('element face'):
                sl = file_line.split()
                if len(sl) >= 3:
                    return int(sl[2])

        raise Exception('element face section not found')

    def load_properties() -> list:
        properties = []

        x_found = False
        y_found = False
        z_found = False

        for file_line in file_lines:
            if file_line == 'end_header':
                break
            elif file_line.startswith('property list'):
                continue  # ignore
            elif file_line.startswith('property'):
                sl = file_line.split()
                if len(sl) >= 3:
                    type_str = sl[1]
                    if type_str == 'float' or type_str == 'float32':
                        tp = PropertyType.TYPE_FLOAT
                    elif type_str == 'uchar' or type_str == 'uint8':
                        tp = PropertyType.TYPE_UINT8
                    else:
                        raise Exception('unknown date type "{}"'.format(type_str))

                    name_str = sl[2]
                    if name_str == 'x':
                        name = PropertyName.NAME_X
                        x_found = True
                    elif name_str == 'y':
                        name = PropertyName.NAME_Y
                        y_found = True
                    elif name_str == 'z':
                        name = PropertyName.NAME_Z
                        z_found = True
                    elif name_str == 'nx':
                        name = PropertyName.NAME_NORMAL_X
                    elif name_str == 'ny':
                        name = PropertyName.NAME_NORMAL_Y
                    elif name_str == 'nz':
                        name = PropertyName.NAME_NORMAL_Z
                    elif name_str == 'confidence':
                        name = PropertyName.NAME_CONFIDENCE
                    elif name_str == 'intensity':
                        name = PropertyName.NAME_INTENSITY
                    elif name_str == 'red':
                        name = PropertyName.NAME_RED
                    elif name_str == 'green':
                        name = PropertyName.NAME_GREEN
                    elif name_str == 'blue':
                        name = PropertyName.NAME_BLUE
                    elif name_str == 'alpha':
                        name = PropertyName.NAME_ALPHA
                    elif name_str == 's':
                        name = PropertyName.NAME_S
                    elif name_str == 't':
                        name = PropertyName.NAME_T
                    else:
                        raise Exception('unknown property "{}"'.format(name_str))

                    properties.append((tp, name))
                else:
                    raise Exception('too many property fields "{}"'.format(file_line))

        if not x_found or not y_found or not z_found:
            raise Exception('x, y, z not all found')

        return properties

    def find_head_end_idx() -> int:
        for i, file_line in enumerate(file_lines):
            if file_line == 'end_header':
                return i
        raise Exception('head end section not found')

    def load_ascii(properties, vertex_start_idx, face_start_idx):

        def make_line_id(v_idx1, v_idx2):
            return f'{v_idx1}_{v_idx2}' if v_idx1 < v_idx2 else f'{v_idx2}_{v_idx1}'

        model_min = Vec3(99999999.0, 99999999.0, 99999999.0)
        model_max = Vec3(-99999999.0, -99999999.0, -99999999.0)
        model_lines = []

        sz = len(file_lines)
        vertex_stop_idx = vertex_start_idx + vertex_count
        if vertex_stop_idx > sz:
            raise Exception('vertex count overflow')

        face_stop_idx = face_start_idx + face_count
        if face_stop_idx > sz:
            raise Exception('face count overflow')

        vertices = []
        sz_of_properties = len(properties)
        for i in range(vertex_start_idx, vertex_stop_idx):
            file_line = file_lines[i]
            sl = file_line.split()
            if len(sl) != sz_of_properties:
                raise Exception('num properties should be {}'.format(sz_of_properties))

            pt = Vec3(0.0, 0.0, 0.0)

            for j, s in enumerate(sl):
                if properties[j][1] == PropertyName.NAME_X:
                    pt.x = float(s)
                elif properties[j][1] == PropertyName.NAME_Y:
                    pt.y = float(s)
                elif properties[j][1] == PropertyName.NAME_Z:
                    pt.z = float(s)

            if pt.x < model_min.x:
                model_min.x = pt.x

            if pt.x > model_max.x:
                model_max.x = pt.x

            if pt.y < model_min.y:
                model_min.y = pt.y

            if pt.y > model_max.y:
                model_max.y = pt.y

            if pt.z < model_min.z:
                model_min.z = pt.z

            if pt.z > model_max.z:
                model_max.z = pt.z

            vertices.append(pt)

        sz_of_vertices = len(vertices)

        # avoid add duplicate line
        added_lines = {}

        for i in range(face_start_idx, face_stop_idx):
            file_line = file_lines[i]
            sl = file_line.split()
            if len(sl) > 0:
                vertex_cnt = int(sl[0])
                if vertex_cnt == 3:

                    if len(sl) == 4:
                        v_indices = [int(sl[1]), int(sl[2]), int(sl[3])]
                        for v in v_indices:
                            if v < 0 or v >= sz_of_vertices:
                                raise Exception('vertex index overflow')

                        for j in range(0, 3):
                            v1 = v_indices[j]
                            v2 = v_indices[(j+1)%3]
                            line_id = make_line_id(v1, v2)
                            if added_lines.get(line_id) is None:
                                model_lines.append(Line3D(vertices[v1], vertices[v2]))
                                added_lines[line_id] = 0   # dummy

                    else:
                        raise Exception('vertex num of face mismatch')

                else:
                    raise Exception('face more than 3 vertices not supported yet')

        return model_lines, model_min, model_max

    # read file to memory
    f = open(filename, "r")
    file_lines = f.readlines()
    f.close()

    # strip \r\n
    for idx, it in enumerate(file_lines):
        it = it.replace('\n', '')
        it = it.replace('\r', '')
        file_lines[idx] = it

    # parse from memory
    check_head()
    format_ = load_format()
    vertex_count = load_vertex_count()
    face_count = load_face_count()
    properties_ = load_properties()
    end_header_idx = find_head_end_idx()

    if format_ == FileFormat.FMT_ASCII:
        return load_ascii(properties_, end_header_idx + 1, end_header_idx + 1 + vertex_count)
    else:
        raise Exception('binary format not supported yet')
