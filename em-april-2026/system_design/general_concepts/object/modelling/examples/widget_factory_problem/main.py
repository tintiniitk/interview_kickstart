from dataclasses import dataclass
from typi

# 1. Geometry (Shapes)
class Shape(ABC):
    @abstractmethod
    def get_coordinates((self) -> List[Point]:
        pass

class Circle(Shape):
    def __init__(self, radius: float, center: Point):
        self.radius = radius
        self.center = center

    def get_coordinates(self) -> List[Point]:
        # Return discretized boundary points
        return calculate_circle_points(self.center, self.radius)


# 2. Style Properties (Value Objects / Flyweights)
class Color:
    RED = None  # Singleton
    BLUE = None # Singleton

    def __init__(self, r: int, g: int, b: int):
        self.r, self.g, self.b = r, g, b

Color.RED = Color(255, 0, 0)
Color.BLUE = Color(0, 0, 255)

class DrawType(Enum):
    SOLID = 1
    DASHED = 2
    DOTTED = 3

@dataclass(frozen=True)
class DrawProperties:
    color: Color
    draw_type: DrawType

# 3. Drawing Engine (Bridge / Strategy)
class Drawing(ABC):
    @abstractmethod
    def draw(self, shape: Shape, props: DrawProperties):
        pass

class CanvasDrawing(Drawing):
    def __init__(self, canvas: Canvas):
        self.canvas = canvas

    def draw(self, shape: Shape, props: DrawProperties):
        coords = shape.get_coordinates()
        # Apply stroke style (props.draw_type) and color (props.color) to canvas context
        self.canvas.set_pen(props.color, props.draw_type)
        self.canvas.draw_lines(coords)
