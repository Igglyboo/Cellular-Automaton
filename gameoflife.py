import pyglet
import numpy
from pyglet.window import key, mouse

window_width = 1200
window_height = 600

cell_size = 25
cells_high = window_height / cell_size
cells_wide = window_width / cell_size

grid = numpy.ones(dtype=int, shape=(cells_wide, cells_high))
working_grid = numpy.zeros(dtype=int, shape=(cells_wide, cells_high))

dead_color = [1.0, 1.0, 1.0, 1.0]
alive_color = [0.0, 0.0, 0.0, 1.0]

born = {3}
survives = {2, 3}

paused = False

window = pyglet.window.Window(window_width, window_height)
window.set_caption("Cellular Automaton")


@window.event
def on_draw():
    global alive_color
    window.clear()
    color_cells()
    draw_grid()
    alive_color = color.next()


@window.event
def on_key_press(symbol, modifiers):
    global paused
    global grid
    if symbol == key.ENTER:
        paused = not paused
    elif symbol == key.I and paused:
        grid.fill(0)
    elif symbol == key.O and paused:
        grid.fill(1)
    elif symbol == key.P and paused:
        randomize_grid()
    elif symbol == key.RIGHT and paused:
        update_grid()


@window.event
def on_mouse_press(x, y, button, modifiers):
    global grid
    if button == mouse.LEFT and paused:
        grid[x/cell_size][y/cell_size] = not grid[x/cell_size][y/cell_size]


def update(dt):
    if not paused:
        update_grid()


def draw_grid():
    pyglet.gl.glColor4f(dead_color[0], dead_color[1], dead_color[2], dead_color[3])
    for i in range(0, window_width, cell_size):
        pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2i', (i, 0, i, window_height)))
    for i in range(0, window_height, cell_size):
        pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2i', (0, i, window_width, i)))


def color_cells():
    pyglet.gl.glColor4f(alive_color[0], alive_color[1], alive_color[2], alive_color[3])
    for x in xrange(cells_wide):
        for y in xrange(cells_high):
            if grid[x][y]:
                x1 = x * cell_size
                y1 = y * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size
                pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2i', (x1, y1, x1, y2, x2, y2, x2, y1)))


def update_grid():
    global grid
    for x in xrange(cells_wide):
        for y in xrange(cells_high):
            n = get_neighbors(x, y)
            if not grid[x][y]:
                if n in born:
                    working_grid[x][y] = 1
                else:
                    working_grid[x][y] = 0
            else:
                if n in survives:
                    working_grid[x][y] = 1
                else:
                    working_grid[x][y] = 0
    grid = numpy.copy(working_grid)


def get_neighbors(x, y):
    n = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if not(i == 0 and j == 0):
                if 0 <= x + i < cells_wide and 0 <= y + j < cells_high:
                    if grid[x + i][y + j] == 1:
                        n += 1
    return n


def randomize_grid():
    global grid
    for x in xrange(cells_wide):
        for y in xrange(cells_high):
            grid[x][y] = numpy.random.randint(0, 2)


def color_generator():
    while True:
        r = 1.0
        g = 0.0
        b = 0.0
        increment = 50

        for i in xrange(increment):
            g += 1.0/increment
            yield [r, g, b, 1.0]
        for i in xrange(increment):
            r -= 1.0/increment
            yield [r, g, b, 1.0]
        for i in xrange(increment):
            b += 1.0/increment
            yield [r, g, b, 1.0]
        for i in xrange(increment):
            g -= 1.0/increment
            yield [r, g, b, 1.0]
        for i in xrange(increment):
            r += 1.0/increment
            yield [r, g, b, 1.0]
        for i in xrange(increment):
            b -= 1.0/increment
            yield [r, g, b, 1.0]


if __name__ == "__main__":
    randomize_grid()
    color = color_generator()
    pyglet.clock.schedule_interval(update, 1.0/15.0)
    pyglet.app.run()
else:
    exit()