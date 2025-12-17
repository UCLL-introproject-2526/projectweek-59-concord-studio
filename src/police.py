import pygame
from hitbox import Hitbox
import heapq

class Police(pygame.sprite.Sprite):
    def __init__(self, x, y, speed=3):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 255, 0))
        self.image.set_alpha(190)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed

        # Pathfinding setup
        self.node_size = Hitbox.TILE_SIZE * Hitbox.SCALE_FACTOR
        # load hitbox objects and build blocked set as grid coordinates
        map_objects = Hitbox.load_map_objects('../assets/hitbox_map.png')
        self.blocked = set()
        # determine grid size from the hitbox image
        try:
            map_image = pygame.image.load('../assets/hitbox_map.png').convert()
            map_w, map_h = map_image.get_size()
            self.cols = map_w // Hitbox.TILE_SIZE
            self.rows = map_h // Hitbox.TILE_SIZE
        except Exception:
            # fallback to something reasonable
            self.cols = 100
            self.rows = 100

        for obj in map_objects:
            cx = obj['rect'].x // self.node_size
            cy = obj['rect'].y // self.node_size
            self.blocked.add((cx, cy))

        self.path = []  # list of pixel centers to follow
        self.path_index = 0
        self.recalc_every = 20  # frames between forced recalcs
        self._frame_counter = 0
        self.reached_target_threshold = 8

    def _grid_pos(self, pixel_pos):
        px, py = pixel_pos
        return (px // self.node_size, py // self.node_size)

    def _pixel_center(self, grid_pos):
        gx, gy = grid_pos
        cx = gx * self.node_size + self.node_size // 2
        cy = gy * self.node_size + self.node_size // 2
        return (cx, cy)

    def _neighbors(self, node):
        x, y = node
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.cols and 0 <= ny < self.rows and (nx, ny) not in self.blocked:
                yield (nx, ny)

    def _heuristic(self, a, b):
        # Manhattan distance
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def _astar(self, start, goal):
        # start/goal are grid positions (gx, gy)
        if start == goal:
            return [start]
        open_set = []
        heapq.heappush(open_set, (0, start))
        came_from = {}
        gscore = {start: 0}
        fscore = {start: self._heuristic(start, goal)}

        while open_set:
            _, current = heapq.heappop(open_set)
            if current == goal:
                # reconstruct path
                path = [current]
                while current in came_from:
                    current = came_from[current]
                    path.append(current)
                path.reverse()
                return path

            for neighbor in self._neighbors(current):
                tentative_g = gscore[current] + 1
                if tentative_g < gscore.get(neighbor, float('inf')):
                    came_from[neighbor] = current
                    gscore[neighbor] = tentative_g
                    f = tentative_g + self._heuristic(neighbor, goal)
                    if f < fscore.get(neighbor, float('inf')):
                        fscore[neighbor] = f
                    heapq.heappush(open_set, (f, neighbor))

        return None  # no path

    def _find_nearest_unblocked(self, pos, max_radius=10):
        """If pos is blocked, search outward (BFS) up to max_radius tiles for a free cell."""
        if pos not in self.blocked:
            return pos
        from collections import deque
        q = deque([pos])
        visited = {pos}
        radius = 0
        while q and radius <= max_radius:
            for _ in range(len(q)):
                cur = q.popleft()
                if cur not in self.blocked:
                    return cur
                x, y = cur
                for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
                    nx, ny = x+dx, y+dy
                    if 0 <= nx < self.cols and 0 <= ny < self.rows and (nx, ny) not in visited:
                        visited.add((nx, ny))
                        q.append((nx, ny))
            radius += 1
        return None

    def _rebuild_path(self, target_rect):
        start = self._grid_pos(self.rect.center)
        goal = self._grid_pos(target_rect.center)
        # clamp goal inside grid
        gx = max(0, min(self.cols - 1, goal[0]))
        gy = max(0, min(self.rows - 1, goal[1]))
        goal = (gx, gy)

        if start == goal:
            self.path = []
            self.path_index = 0
            return

        # if goal cell is blocked, try to find nearest free cell
        if goal in self.blocked:
            new_goal = self._find_nearest_unblocked(goal, max_radius=20)
            if new_goal:
                goal = new_goal
            else:
                # can't reach a nearby free cell
                self.path = []
                self.path_index = 0
                return

        raw_path = self._astar(start, goal)
        if raw_path:
            # convert to pixel centers
            self.path = [self._pixel_center(n) for n in raw_path]
            self.path_index = 0
        else:
            self.path = []
            self.path_index = 0

    def update(self, target_rect):
        """
        Move toward the target using a generated path. This keeps the same signature
        so `main.py` doesn't need changes.
        """
        self._frame_counter += 1
        # Rebuild path periodically or if path empty or target grid changed
        if (self._frame_counter % self.recalc_every) == 0 or not self.path:
            self._rebuild_path(target_rect)

        # If we have a path, follow it
        if self.path:
            # advance path_index if close to current waypoint
            if self.path_index < len(self.path):
                waypoint = self.path[self.path_index]
                dx = waypoint[0] - self.rect.centerx
                dy = waypoint[1] - self.rect.centery
                dist_sq = dx * dx + dy * dy
                if dist_sq <= (self.reached_target_threshold ** 2):
                    self.path_index += 1
                else:
                    # move towards waypoint proportional to speed
                    dist = max(1, (dist_sq ** 0.5))
                    vx = (dx / dist) * self.speed
                    vy = (dy / dist) * self.speed
                    # apply movement
                    self.rect.x += int(round(vx))
                    self.rect.y += int(round(vy))
            else:
                # reached end of path
                self.path = []
                self.path_index = 0
        else:
            # fallback: direct movement (old behavior)
            epsilon = 5
            if abs(self.rect.x - target_rect.x) > epsilon:
                if self.rect.x < target_rect.x:
                    self.rect.x += self.speed
                elif self.rect.x > target_rect.x:
                    self.rect.x -= self.speed
            if abs(self.rect.y - target_rect.y) > epsilon:
                if self.rect.y < target_rect.y:
                    self.rect.y += self.speed
                elif self.rect.y > target_rect.y:
                    self.rect.y -= self.speed

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def get_position(self):
        return self.rect.topleft

    def set_position(self, position):
        self.rect.topleft = position

