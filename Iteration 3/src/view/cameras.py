import pygame


class Camera(pygame.sprite.Group):
    def __init__(self, game, background):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

        # Camera Offset
        self.offset = pygame.math.Vector2()
        self.half_w = self.display_surface.get_size()[0] // 2
        self.half_h = self.display_surface.get_size()[1] // 2

        # Box Setup
        self.camera_boarders = {'left': 200, 'right': 200, 'top': 100, 'bottom': 100}
        l = self.camera_boarders["left"]
        t = self.camera_boarders["top"]
        w = self.display_surface.get_size()[0] - (self.camera_boarders["right"] + self.camera_boarders["left"])
        h = self.display_surface.get_size()[1] - (self.camera_boarders["top"] + self.camera_boarders["bottom"])
        self.camera_rect = pygame.Rect(l, t, w, h)

        # Background Setup
        self.background_surf = pygame.image.load(f"assets/{game}/images/{background}.png").convert_alpha()
        self.BLACK = "#00020b"

    def center_target_camera(self, target):
        self.offset.x = target.rect.centerx - self.half_w
        self.offset.y = target.rect.centery - self.half_h

    def box_target_camera(self, target):
        if target.rect.left < self.camera_rect.left:
            self.camera_rect.left = target.rect.left
        if target.rect.right > self.camera_rect.right:
            self.camera_rect.right = target.rect.right
        if target.rect.top < self.camera_rect.top:
            self.camera_rect.top = target.rect.top
        if target.rect.bottom > self.camera_rect.bottom:
            self.camera_rect.bottom = target.rect.bottom

        self.offset.x = self.camera_rect.left - self.camera_boarders["left"]
        self.offset.y = self.camera_rect.top - self.camera_boarders["top"]

    def custom_draw(self, player):
        self.box_target_camera(player)
        self.display_surface.fill(self.BLACK)
        self.draw_background()
        self.draw_sprites()

    def draw_background(self):
        # Default background draw method; can be overridden
        background_offset = self.background_surf.get_rect(topleft=(-self.offset.x, -self.offset.y))
        self.display_surface.blit(self.background_surf, background_offset)

    def draw_sprites(self):
        for sprite in self.sprites():
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

