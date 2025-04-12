#===== imports =====#
from .vector_text import Texter

import pyglet
from pyglet import gl

import ctypes

#===== consts =====#
vert_shader_src = b'''\
uniform vec2 uOrigin;
uniform vec2 uZoom;

attribute vec2 aPosition;
attribute vec4 aColor;

varying vec4 vColor;

void main() {
    gl_Position = vec4(
        (aPosition.x - uOrigin.x) * uZoom.x,
        (aPosition.y - uOrigin.y) * uZoom.y,
        0.0,
        1.0
    );
    vColor = aColor;
}
'''

frag_shader_src = b'''\
varying vec4 vColor;

void main() {
    gl_FragColor = vColor;
}
'''

#===== helpers =====#
def compile_shader(type_, src):
    shader = gl.glCreateShader(type_)
    gl.glShaderSource(
        shader,
        1,
        ctypes.cast(
            ctypes.pointer(ctypes.pointer(ctypes.create_string_buffer(src))),
            ctypes.POINTER(ctypes.POINTER(ctypes.c_char)),
        ),
        ctypes.byref(ctypes.c_int(len(src) + 1)),
    )
    gl.glCompileShader(shader)
    status = ctypes.c_int(0)
    gl.glGetShaderiv(shader, gl.GL_COMPILE_STATUS, ctypes.byref(status))
    if not status.value:
        log = ctypes.create_string_buffer(4096)
        gl.glGetShaderInfoLog(shader, len(log), None, log)
        raise Exception('Error compiling shader: ' + log.value.decode('utf8'))
    return shader

#===== file-scope =====#
class F:
    program = None
    program_is_default = True
    locations = {}
    window = None
    origin = [0, 0]
    zoom = [1, 1]

#===== interfaces =====#
class Buffer:
    def __init__(self):
        self.data = []
        self.draws = []
        self.buffer = gl.GLuint()
        gl.glGenBuffers(1, self.buffer)

    def __len__(self):
        return len(self.data) // 6

    def add(self, x, y, r, g, b, a):
        self.data.extend([x, y, r, g, b, a])

    def add_vertices(self, vertices):
        for v in self.vertices:
            self.add(v)

    def add_data(self, data):
        self.data.extend(data)

    def recolor(self, i, n, r, g, b, a):
        for _ in range(n):
            self.data[6*i+2:6*i+6] = [r, g, b, a]
            i += 1
        return i

    def clear(self):
        self.data = []

    def prep(self, usage):
        if type(self.data) == list:
            self.data = (gl.GLfloat * len(self.data))(*self.data)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.buffer)
        gl.glBufferData(
            gl.GL_ARRAY_BUFFER,
            len(self.data)*4,
            self.data,
            getattr(gl, f'GL_{usage.upper()}_DRAW'),
        )

    def draw(self, attributes=None):
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.buffer)
        if attributes == None:
            attributes = self._attributes()
        stride = sum(components for _, components in attributes)
        offset = 0
        for attribute in attributes:
            attribute, components = attribute
            gl.glVertexAttribPointer(F.locations[attribute], components, gl.GL_FLOAT, gl.GL_FALSE, stride * 4, offset * 4)
            offset += components
        for mode, first, count in self.draws:
            gl.glDrawArrays(getattr(gl, f'GL_{mode.upper()}'), first, count)

    def _attributes(self):
        return [
            ('aPosition', 2),
            ('aColor', 4),
        ]

class Buffer3d(Buffer):
    def __len__(self):
        return len(self.data) // 7

    def add(self, x, y, z, r, g, b, a):
        self.data.extend([x, y, z, r, g, b, a])

    def add_data_2d_with_z(self, data, z):
        for i in range(0, len(data), 6):
            x, y, r, g, b, a = data[i:i+6]
            self.add(x, y, z, r, g, b, a)

    def _attributes(self):
        return [
            ('aPosition', 3),
            ('aColor', 4),
        ]

def init(
    w,
    h,
    title,
    *,
    program=None,
):
    if program == None:
        global vert_shader_src
        global frag_shader_src
        uniforms = ['uOrigin', 'uZoom']
        attributes = ['aPosition', 'aColor']
        F.program_is_default = True
    else:
        vert_shader_src, frag_shader_src, uniforms, attributes = program
        F.program_is_default = False
    # window
    F.window = pyglet.window.Window(
        width=w,
        height=h,
        caption=title,
        resizable=True,
        vsync=True,
    )
    # shader
    F.program = gl.glCreateProgram()
    gl.glAttachShader(F.program, compile_shader(gl.GL_VERTEX_SHADER, vert_shader_src))
    gl.glAttachShader(F.program, compile_shader(gl.GL_FRAGMENT_SHADER, frag_shader_src))
    gl.glLinkProgram(F.program)
    # uniforms
    for uniform in uniforms:
        F.locations[uniform] = gl.glGetUniformLocation(F.program, uniform.encode())
    # attributes
    for attribute in attributes:
        F.locations[attribute] = gl.glGetAttribLocation(F.program, attribute.encode())
    for attribute in attributes:
        gl.glEnableVertexAttribArray(F.locations[attribute])

def view_set(x, y, w, h):
    F.origin = [x + w/2, y + h/2]
    F.zoom = [2/w, 2/h]

def width():
    return F.window.width

def height():
    return F.window.height

def capture():
    pyglet.image.get_buffer_manager().get_color_buffer().save('plot.png')

def clear():
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)

def set_callbacks(
    mouse_press_left=None,
    mouse_press_right=None,
    mouse_release_left=None,
    mouse_release_right=None,
    mouse_drag_left=None,
    mouse_drag_right=None,
    mouse_scroll=None,
    key_press=None,
    key_release=None,
    draw=None,
    resize=None,
):
    @F.window.event
    def on_mouse_press(x, y, button, modifiers):
        if button == pyglet.window.mouse.LEFT and mouse_press_left:
            mouse_press_left(x, y)
        if button == pyglet.window.mouse.RIGHT and mouse_press_right:
            mouse_press_right(x, y)

    @F.window.event
    def on_mouse_release(x, y, button, modifiers):
        if button == pyglet.window.mouse.LEFT and mouse_release_left:
            mouse_release_left(x, y)
        if button == pyglet.window.mouse.RIGHT and mouse_release_right:
            mouse_release_right(x, y)

    @F.window.event
    def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
        if buttons & pyglet.window.mouse.LEFT and mouse_drag_left:
            mouse_drag_left(x, y, dx, dy)
        if buttons & pyglet.window.mouse.RIGHT and mouse_drag_right:
            mouse_drag_right(x, y, dx, dy)

    @F.window.event
    def on_mouse_scroll(x, y, scroll_x, scroll_y):
        if mouse_scroll:
            mouse_scroll(x, y, scroll_y)

    @F.window.event
    def on_key_press(symbol, modifiers):
        if key_press:
            if 32 <= symbol < 127:
                key = chr(symbol)
            else:
                key = {
                    pyglet.window.key.LEFT  : 'Left',
                    pyglet.window.key.RIGHT : 'Right',
                    pyglet.window.key.UP    : 'Up',
                    pyglet.window.key.DOWN  : 'Down',
                    pyglet.window.key.SPACE : 'Space',
                    pyglet.window.key.RETURN: 'Return',
                    pyglet.window.key.LSHIFT: 'LShift',
                    pyglet.window.key.RSHIFT: 'RShift',
                    pyglet.window.key.LCTRL : 'LCtrl',
                    pyglet.window.key.RCTRL : 'RCtrl',
                }.get(symbol)
            if key: key_press(key)

    @F.window.event
    def on_key_release(symbol, modifiers):
        if key_release:
            if 32 <= symbol < 127:
                key = chr(symbol)
            else:
                key = {
                    pyglet.window.key.LEFT  : 'Left',
                    pyglet.window.key.RIGHT : 'Right',
                    pyglet.window.key.UP    : 'Up',
                    pyglet.window.key.DOWN  : 'Down',
                    pyglet.window.key.SPACE : 'Space',
                    pyglet.window.key.RETURN: 'Return',
                    pyglet.window.key.LSHIFT: 'LShift',
                    pyglet.window.key.RSHIFT: 'RShift',
                    pyglet.window.key.LCTRL : 'LCtrl',
                    pyglet.window.key.RCTRL : 'RCtrl',
                }.get(symbol)
            if key: key_release(key)

    @F.window.event
    def on_draw():
        gl.glUseProgram(F.program)
        if F.program_is_default:
            gl.glUniform2f(F.locations['uOrigin'], *F.origin)
            gl.glUniform2f(F.locations['uZoom'  ], *F.zoom)
        if draw:
            draw()

    @F.window.event
    def on_resize(width, height):
        if resize:
            resize(width, height)

def run(update=None):
    gl.glEnable(gl.GL_BLEND);
    gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA);
    if update:
        pyglet.clock.schedule_interval(update, 1/60)
    pyglet.app.run()
    if update:
        pyglet.clock.unschedule(update)
