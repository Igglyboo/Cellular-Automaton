import pyglet
import numpy
from itertools import cycle
from pyglet.window import key, mouse

window_width = 700
window_height = 700

cell_size = 10
cells_high = window_height / cell_size
cells_wide = window_width / cell_size

grid = numpy.zeros(dtype=int, shape=(cells_wide, cells_high))
working_grid = numpy.zeros(dtype=int, shape=(cells_wide, cells_high))

born = {3}
survives = {2, 3}

paused = False

window = pyglet.window.Window(window_width, window_height)
window.set_caption("Cellular Automaton")


@window.event
def on_draw():
    window.clear()
    color_cells()
    draw_grid()


@window.event
def on_key_press(symbol, modifiers):
    global paused
    if symbol == key.ENTER:
        paused = not paused
    elif paused:
        if symbol == key.I:
            grid.fill(0)
        elif symbol == key.O:
            grid.fill(1)
        elif symbol == key.P:
            randomize_grid()
        elif symbol == key.RIGHT:
            update_grid()


@window.event
def on_mouse_press(x, y, button, modifiers):
    if paused:
        if button == mouse.LEFT:
            grid[x/cell_size][y/cell_size] = 1
        elif button == mouse.RIGHT:
            grid[x/cell_size][y/cell_size] = 0
            

@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    if paused:
        if 0 <= x / cell_size < cells_wide and 0 <= y / cell_size < cells_high:
            if buttons == mouse.LEFT:
                grid[x/cell_size][y/cell_size] = 1
            elif buttons == mouse.RIGHT:
                grid[x/cell_size][y/cell_size] = 0


def update(dt):
    if not paused:
        update_grid()


def draw_grid():
    pyglet.gl.glColor4f(1.0, 1.0, 1.0, 1.0)
    for i in range(0, window_width, cell_size):
        pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2i', (i, 0, i, window_height)))
    for i in range(0, window_height, cell_size):
        pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2i', (0, i, window_width, i)))


def color_cells():
    alive_color = color_iterator.next()
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
            if i or j:
                if 0 <= x + i < cells_wide and 0 <= y + j < cells_high:
                    n += grid[x + i][y + j]
    return n


def randomize_grid():
    for x in xrange(cells_wide):
        for y in xrange(cells_high):
            grid[x][y] = numpy.random.randint(0, 2)


def color_generator():
    color = [1.0, 0, 0]
    iterations = 50
    increment = 1.0 / iterations
    fill = True

    for i in cycle((1, 0, 2)):
        for n in xrange(iterations):
            if fill:
                color[i] += increment
            else:
                color[i] -= increment
            color.append(1.0);
            yield color
        fill = not fill


if __name__ == "__main__":
    randomize_grid()
    color_iterator = color_generator()
    pyglet.clock.schedule_interval(update, 1.0/15.0)
    pyglet.app.run()
else:
    exit()