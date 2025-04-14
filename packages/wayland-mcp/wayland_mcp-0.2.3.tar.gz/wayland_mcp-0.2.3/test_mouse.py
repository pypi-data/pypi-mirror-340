import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from wayland_mcp.mouse_utils import MouseController

def test_mouse():
    mouse = MouseController()
    print("Testing drag from (350, 150) to (1350, 150)")
    mouse.mousemove(350, 150)
    print("Starting drag...")
    mouse.drag(350, 150, 1350, 150)
    print("Drag test completed - please verify")

if __name__ == "__main__":
    test_mouse()