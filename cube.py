import time
import math
import curses

def rotate_x(x, y, z, angle):
    """Rotate point (x, y, z) around the x-axis by angle."""
    cos_angle = math.cos(angle)
    sin_angle = math.sin(angle)
    new_y = y * cos_angle - z * sin_angle
    new_z = y * sin_angle + z * cos_angle
    return x, new_y, new_z

def rotate_y(x, y, z, angle):
    """Rotate point (x, y, z) around the y-axis by angle."""
    cos_angle = math.cos(angle)
    sin_angle = math.sin(angle)
    new_x = x * cos_angle + z * sin_angle
    new_z = -x * sin_angle + z * cos_angle
    return new_x, y, new_z

def rotate_z(x, y, z, angle):
    """Rotate point (x, y, z) around the z-axis by angle."""
    cos_angle = math.cos(angle)
    sin_angle = math.sin(angle)
    new_x = x * cos_angle - y * sin_angle
    new_y = x * sin_angle + y * cos_angle
    return new_x, new_y, z

def project(x, y, z):
    """Project 3D coordinates onto 2D plane."""
    factor = 20 / (z + 3)  # Adjust for perspective
    new_x = int(x * factor + 40)  # Translate to screen coordinates
    new_y = int(-y * factor + 12)  # Translate to screen coordinates
    return new_x, new_y

def print_cube(stdscr, vertices):
    """Print the cube on the screen."""
    # Define the cube's edges by connecting vertices
    edges = [(0, 1), (1, 2), (2, 3), (3, 0),
             (4, 5), (5, 6), (6, 7), (7, 4),
             (0, 4), (1, 5), (2, 6), (3, 7)]

    for edge in edges:
        start_vertex = vertices[edge[0]]
        end_vertex = vertices[edge[1]]
        start_x, start_y = project(*start_vertex)
        end_x, end_y = project(*end_vertex)
        try:
            draw_line(stdscr, start_x, start_y, end_x, end_y)
        except curses.error:
            pass

def draw_line(stdscr, x0, y0, x1, y1):
    """Draw a line on the screen using Bresenham's line algorithm."""
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy

    while x0 != x1 or y0 != y1:
        try:
            stdscr.addch(y0, x0, ord('#'))
        except curses.error:
            pass
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy

def main(stdscr):
    # Hide cursor
    curses.curs_set(0)

    # Define cube dimensions
    width = 2  # Width of the cube
    height = 2  # Height of the cube
    depth = 2  # Depth of the cube

    # Calculate half dimensions for convenience
    half_width = width / 2
    half_height = height / 2
    half_depth = depth / 2

    # Define initial cube vertices
    vertices = [
        (-half_width, -half_height, -half_depth),
        (half_width, -half_height, -half_depth),
        (half_width, half_height, -half_depth),
        (-half_width, half_height, -half_depth),
        (-half_width, -half_height, half_depth),
        (half_width, -half_height, half_depth),
        (half_width, half_height, half_depth),
        (-half_width, half_height, half_depth)
    ]

    # Main loop for rotating the cube
    angle_x = angle_y = angle_z = 0
    while True:
        stdscr.clear()
        rotated_vertices = []
        for vertex in vertices:
            # Rotate each vertex around the x, y, and z axes
            x, y, z = vertex
            x, y, z = rotate_x(x, y, z, angle_x)
            x, y, z = rotate_y(x, y, z, angle_y)
            x, y, z = rotate_z(x, y, z, angle_z)
            rotated_vertices.append((x, y, z))

        print_cube(stdscr, rotated_vertices)

        # Increment angles for rotation
        angle_x += 0.1
        angle_y += 0.05
        angle_z += 0.03

        stdscr.refresh()
        time.sleep(0.05)  # Adjust speed of rotation

if __name__ == "__main__":
    curses.wrapper(main)
