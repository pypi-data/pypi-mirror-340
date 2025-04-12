class Color:
    def __init__(self, r, g, b, a=1.0):
        self.r = r
        self.g = g
        self.b = b
        self.a = a

    def mix(self, other, amount):
        return Color(
            int((1-amount) * self.r + amount * other.r),
            int((1-amount) * self.g + amount * other.g),
            int((1-amount) * self.b + amount * other.b),
        )

Color.w = Color(255, 255, 255)
Color.r = Color(255,   0,   0)
Color.g = Color(  0, 255,   0)
Color.b = Color(  0,   0, 255)
Color.y = Color(255, 255,   0)
Color.c = Color(  0, 255, 255)
Color.m = Color(255,   0, 255)
Color.o = Color(255, 128,   0)

Color.all = [
    Color.w,
    Color.r,
    Color.g,
    Color.b,
    Color.y,
    Color.c,
    Color.m,
    Color.o,
    Color(128, 128, 128),
    Color(128,   0,   0),
    Color(  0, 128,   0),
    Color(  0,   0, 128),
    Color(128, 128,   0),
    Color(  0, 128, 128),
    Color(128,   0, 128),
    Color(128,  64,   0),
]

class Colors:
    def __init__(self, colors):
        if type(colors) == str:
            colors = [getattr(Color, i) for i in colors]
        self.colors = colors

    def __call__(self, x, y, i, series):
        color = self.colors[series % len(self.colors)]
        return {
            'x': x, 'y': y,
            'r': color.r, 'g': color.g, 'b': color.b, 'a': color.a,
        }

class Default(Colors):
    def __init__(self):
        Colors.__init__(self, Color.all)

class Grid:
    def __init__(self, cell_w, cell_h, grid_w):
        self.cell_w = cell_w
        self.cell_h = cell_h
        self.grid_w = grid_w

    def __call__(self, x, y, i, series):
        dx = self.cell_w * (series % self.grid_w)
        dy = -self.cell_h * (series // self.grid_w)
        return {'x': x + dx, 'y': y + dy}

class Gradient:
    def __init__(self, steps, colors=[Color.r, Color.c]):
        self.steps = steps
        self.colors = colors

    def __call__(self, x, y, i, series):
        c = series / self.steps
        c_i = int(c)
        color = self.colors[c_i].mix(self.colors[c_i+1], c-c_i)
        return {
            'x': x, 'y': y,
            'r': color.r, 'g': color.g, 'b': color.b,
        }

class Compound:
    def __init__(self, significant, *others):
        'Each element of `others` should be a tuple `(transform, n)` where `n`'
        ' specifies how many series to take before incrementing the series in '
        'the next most significant transform.'
        self.significant = significant
        self.others = others

    def __call__(self, x, y, i, series):
        result = {'x': x, 'y': y}
        for trans, mod in reversed(self.others):
            result.update(trans(result['x'], result['y'], i, series % mod))
            series //= mod
        result.update(self.significant(result['x'], result['y'], i, series))
        return result

    def series_insignificant(self, series):
        if len(self.others) == 0:
            return series
        return series % self.others[-1][1]
