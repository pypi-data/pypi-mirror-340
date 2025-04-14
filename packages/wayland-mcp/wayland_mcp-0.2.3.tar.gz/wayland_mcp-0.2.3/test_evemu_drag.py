from wayland_mcp.mouse_utils import MouseController

if __name__ == "__main__":
    mouse = MouseController()
    mouse.drag(350, 150, 1350, 150)