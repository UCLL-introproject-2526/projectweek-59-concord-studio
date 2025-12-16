
def main():
    pygame.init()
    screen_width, screen_height = 800, 600
    font = pygame.font.Font(None, 36)

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("No Lock, No Mercy")
    clock = pygame.time.Clock()

    # Background
    bg = pygame.image.load(r"C:\UCLL\Introduction_project\Group_project\projectweek-59-concord-studio\assets\background.png")

    bgBig = pygame.transform.scale(bg, (2272 * 2, 1888 * 2))