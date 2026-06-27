from kivy.core.window import Window
from kivy.graphics import Color, Mesh
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.properties import ListProperty


class CardRegion(Widget):
    polygon = ListProperty([])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.polygon_bb = [(0, 0), (0, 0)]  # Top-left, bottom-right
        self.is_hovered = False

        Window.bind(mouse_pos = self.on_mouse_move)
        self.bind(
            polygon = self.draw_polygon,
            pos = self.draw_polygon,
            size = self.draw_polygon
        )

        with self.canvas.before:
            self.region_color = Color(1, 0, 0, 0.3)  # red with transparency
            self.mesh = Mesh(
                vertices= [],
                indices = [],
                mode = 'triangle_fan'
            )

        self.draw_polygon()

    def draw_polygon(self, *args):
        vertices = []
        indices = []

        if self.parent is not None:
            offset_x, offset_y = self.pos
            w, h = self.size

            if len(self.polygon) > 0:
                self.calculate_region_bb()
                for i, (px, py) in enumerate(self.polygon):
                    vertices += [offset_x + int(px * w), offset_y + int(py * h), 0, 0]
                    indices += [i]

                self.mesh.vertices = vertices
                self.mesh.indices = indices

    def on_mouse_move(self, window, mouse_pos):
        local_mouse_pos = self.to_widget(*mouse_pos)
        mouse_x, mouse_y = mouse_pos
        norm_x = mouse_x - self.x
        norm_y = mouse_y - self.y
        norm_x = norm_x / self.width
        norm_y = norm_y / self.height


        if 0 <= norm_x <= 1.0 and 0 <= norm_y <= 1.0:
            is_inside = self.point_within_region((norm_x, norm_y))

            if is_inside is True and self.is_hovered is False:
                self.is_hovered = True
                print(f"Mouse entered region!")
                self.region_color.rgba = (1, 0, 0, 0.6)
                # self.on_hover_enter()

            elif is_inside is False and self.is_hovered is True:
                self.is_hovered = False
                print(f"Mouse left region!")
                self.region_color.rgba = (1, 0, 0, 0.3)
                # self.on_hover_leave()

    def calculate_region_bb(self, *args):
        bb_top = max([point[1] for point in self.polygon])
        bb_bottom = min([point[1] for point in self.polygon])
        bb_left = min([point[0] for point in self.polygon])
        bb_right= max([point[0] for point in self.polygon])

        self.polygon_bb = [(bb_left, bb_top), (bb_right, bb_bottom)]

    def point_within_region(self, point):
        is_inside = False

        point_x, point_y = point
        # Bounding box check first to eliminate outliers
        if point_x < self.polygon_bb[0][0] or point_x > self.polygon_bb[1][0]:
            return False
        if point_y < self.polygon_bb[1][1] or point_y > self.polygon_bb[0][1]:
            return False

        # Check if within polygon
        # Raycasting algorithm: "If drawing a line from point to the right, how many polygon edges does it intersect?"
        polygon = self.polygon

        p1 = polygon[0]
        for i in range(len(polygon) + 1):
            p2 = polygon[i % len(polygon)]

            p1_x, p1_y = p1
            p2_x, p2_y = p2

            # Skip horizontal edges
            if p1_y != p2_y:
                # Check if point is within y bounds of polygon edge (p1, p2)
                if min(p1_y, p2_y) < point_y <= max(p1_y, p2_y):
                    # Check if intersection happens on the right of the given point
                    if point_x < max(p1_x, p2_x):
                        x_intersect = p1_x + (point_y - p1_y) * (p2_x - p1_x) / (p2_y - p1_y)
                        if point_x <= x_intersect:
                            is_inside = not is_inside  # Crossing an edge, flip the return value

            # Move points for next edge
            p1 = p2

        return is_inside








