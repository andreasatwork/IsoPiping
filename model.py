import math

class Vector3:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def to_tuple(self):
        return (self.x, self.y, self.z)

    def __add__(self, other):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scalar):
        return Vector3(self.x * scalar, self.y * scalar, self.z * scalar)

    def __neg__(self):
        return Vector3(-self.x, -self.y, -self.z)

    def normalize(self):
        mag = math.sqrt(self.x**2 + self.y**2 + self.z**2)
        if mag == 0: return Vector3(0,0,0)
        return Vector3(self.x/mag, self.y/mag, self.z/mag)

class Flange:
    def __init__(self, pos, direction):
        self.pos = pos # Vector3 (face center)
        self.dir = direction.normalize() # Vector3 (pointing towards the other flange of the flange pair)

class Pipe:
    def __init__(self, connected_flange, length):
        self.start_flange = Flange(connected_flange.pos, -connected_flange.dir) 
        self.length = length
        # Calculate end flange
        # flange[1] = flange[0].pos - flange[0].dir * length (incorrect in prompt? wait)
        # "flange[1] = flange[0].pos - flange[0].dir * length and flange[1].dir = -flange[0].dir"
        # If the start flange dir points OUTWARDS (away from the pipe), then the pipe grows in -dir.
        end_pos = connected_flange.pos + (connected_flange.dir * length)
        self.end_flange = Flange(end_pos, connected_flange.dir)

    def get_lines(self):
        return [(self.start_flange.pos.to_tuple(), self.end_flange.pos.to_tuple())]

class Elbow90:
    def __init__(self, connected_flange, target_dir):
        self.start_flange = Flange(connected_flange.pos, -connected_flange.dir)
        self.radius = 100 # Default 100mm
        
        # start_flange.dir is pointing OUTWARDS from the elbow.
        # So the elbow starts at start_flange.pos and goes into -start_flange.dir.
        # The target_dir is the OUTWARDS direction of the end flange.
        # So the elbow turns from -start_flange.dir to -target_dir.
        
        in_dir = -start_flange.dir
        out_target_dir = -target_dir
        
        # Center of the arc
        self.center = start_flange.pos + (out_target_dir * self.radius)
        self.end_pos = self.center + (start_flange.dir * self.radius)
        self.end_flange = Flange(self.end_pos, target_dir.normalize())

    def get_lines(self):
        # Approximate arc with segments
        lines = []
        segments = 16
        v_start = self.start_flange.pos - self.center
        v_end = self.end_pos - self.center
        
        for i in range(segments):
            t1 = i / segments
            t2 = (i + 1) / segments
            
            # Simple spherical interpolation (since it's a 90 deg turn on axis)
            p1 = self.center + (v_start * math.cos(t1 * math.pi/2) + v_end * math.sin(t1 * math.pi/2))
            p2 = self.center + (v_start * math.cos(t2 * math.pi/2) + v_end * math.sin(t2 * math.pi/2))
            lines.append((p1.to_tuple(), p2.to_tuple()))
        return lines

class PipingSystem:
    def __init__(self):
        self.elements = []
        self.current_flange = Flange(Vector3(0,0,0), Vector3(1,0,0)) # Initial: origin, pointing +X

    def add_pipe(self, length):
        p = Pipe(self.current_flange, length)
        self.elements.append(p)
        self.current_flange = p.end_flange
        return p

    def add_elbow(self, target_dir):
        e = Elbow90(self.current_flange, target_dir)
        self.elements.append(e)
        self.current_flange = e.end_flange
        return e
