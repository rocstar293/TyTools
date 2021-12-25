vertices = [
    (0.0, 0.0, 0.0), (1.0, 0.0, 0.0),
    (0.0, 0.0, 0.0), (0.0, 1.0, 0.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 1.0)
    ]

col = [
    (1.0, 0.0, 0.0, 1.0), (1.0, 0.0, 0.0, 1.0),
    (0.0, 1.0, 0.0, 1.0), (0.0, 1.0, 0.0, 1.0),
    (0.0, 0.0, 1.0, 1.0), (0.0, 0.0, 1.0, 1.0)
    ]

import gpu

shader = gpu.shader.from_builtin('3D_SMOOTH_COLOR')

from gpu_extras.batch import batch_for_shader

batch = batch_for_shader(shader, 'LINES', {"pos": vertices, "color": col})

def draw():
    shader.bind()
    batch.draw(shader)