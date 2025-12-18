import pygame
from hitbox import Hitbox
import heapq
from pygame.math import Vector2

class Police(pygame.sprite.Sprite):
    def __init__(self, x, y, hitbox_map, speed=3, spawn_pos = None):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 255, 0))
        self.image.set_alpha(190)
        self.rect = self.image.get_rect(topleft=(x, y))

        self._pos = Vector2(self.rect.center)
        self.speed = speed

        self.image_normal = pygame.image.load("../assets/images/cop_standing.png").convert_alpha()
        self.image_normal = pygame.transform.scale(self.image_normal, (76, 76))

        self.running_images = [
            pygame.transform.scale(pygame.image.load("../assets/images/cop_run_1.png").convert_alpha(), (76, 76)),
            pygame.transform.scale(pygame.image.load("../assets/images/cop_running_2.png").convert_alpha(), (76, 76))
        ]

        self.idle_image = self.image_normal
        self.current_frame = 0
        self.animation_interval_ms = 450 #ms
        self.last_animation_time = pygame.time.get_ticks()

        self.idle_image = self.image_normal
        self.current_frame = 0
        self.animation_speed = 5  # frames per image


        self.image = self.image_normal
        #self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed
        if spawn_pos:
            self.spawn_pos = spawn_pos
        else:
            self.spawn_pos = (x, y)

        self.node_size = Hitbox.TILE_SIZE * Hitbox.SCALE_FACTOR
        map_objects = hitbox_map
        self.blocked = set()

        try:
            map_image = pygame.image.load('../assets/images/hitbox_map.png').convert()
            map_w, map_h = map_image.get_size()
            self.cols = map_w // Hitbox.TILE_SIZE
            self.rows = map_h // Hitbox.TILE_SIZE
        except Exception:
            self.cols = 100
            self.rows = 100

        for obj in map_objects:
            cx = obj['rect'].x // self.node_size
            cy = obj['rect'].y // self.node_size
            self.blocked.add((cx, cy))

        self.path = []
        self.path_index = 0
        self.recalc_every = 20
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
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def _astar(self, start, goal):
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

    def _rebuild_path(self, target_rect, go_to_spawn=False):
        start = self._grid_pos(self.rect.center)

        if go_to_spawn:
            goal = self._grid_pos((self.spawn_pos[0] + 25, self.spawn_pos[1] + 25))
        else:
            goal = self._grid_pos(target_rect.center)

        gx = max(0, min(self.cols - 1, goal[0]))
        gy = max(0, min(self.rows - 1, goal[1]))
        goal = (gx, gy)

        if start == goal:
            self.path = []
            self.path_index = 0
            return

        if goal in self.blocked:
            new_goal = self._find_nearest_unblocked(goal, max_radius=20)
            if new_goal:
                goal = new_goal
            else:
                self.path = []
                self.path_index = 0
                return

        raw_path = self._astar(start, goal)
        if raw_path:
            self.path = [self._pixel_center(n) for n in raw_path]
            self.path_index = 0
        else:
            self.path = []
            self.path_index = 0

    def update(self, target_rect, go_to_spawn=False):
        self._frame_counter += 1

        if (self._frame_counter % self.recalc_every) == 0 or not self.path:
            self._rebuild_path(target_rect, go_to_spawn=go_to_spawn)

        if self.path:
            if self.path_index < len(self.path):
                waypoint = Vector2(self.path[self.path_index])

                delta = waypoint - self._pos
                dist = delta.length()

                threshold = float(max(self.reached_target_threshold, self.speed))
                if dist <= threshold:
                    self._pos = Vector2(waypoint)
                    self.path_index += 1
                else:

                    movement = delta.normalize() * self.speed
                    self._pos += movement

                self.rect.center = (int(round(self._pos.x)), int(round(self._pos.y)))
            else:
                self.path = []
                self.path_index = 0
        else:
            epsilon = 5
            target_center = Vector2(target_rect.center)
            delta = target_center - self._pos
            if delta.length() > epsilon:
                move = delta.normalize() * self.speed

                if delta.length() <= self.speed:
                    self._pos = Vector2(target_center)
                else:
                    self._pos += move
                self.rect.center = (int(round(self._pos.x)), int(round(self._pos.y)))

        now = pygame.time.get_ticks()
        if self.path or (Vector2(target_rect.center) - self._pos).length() > 0:
            # Cop is moving
            if now - self.last_animation_time >= self.animation_interval_ms:
                self.current_frame = (self.current_frame + 1) % len(self.running_images)
                self.last_animation_time = now
            self.image = self.running_images[self.current_frame]
        else:
            # Cop is idle
            self.image = self.idle_image

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def get_position(self):
        return self.rect.topleft

    def set_position(self, position):
        self.rect.topleft = position
        self._pos = Vector2(self.rect.center)

    def set_speed(self, speed):
        self.speed = speed
