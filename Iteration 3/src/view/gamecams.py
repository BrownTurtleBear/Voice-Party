import pygame
from view.cameras import Camera


class RocketCamera(Camera):
    def __init__(self):
        super().__init__("rocket", "stars")

        # Splitting the sprite sheet into large and small stars
        sheet_width, sheet_height = self.background_surf.get_size()
        half_height = sheet_height // 2

        self.large_stars_surf = self.background_surf.subsurface(pygame.Rect(0, 0, sheet_width, half_height))
        self.small_stars_surf = self.background_surf.subsurface(pygame.Rect(0, half_height, sheet_width, half_height))

        # Flip the large stars horizontally
        self.large_stars_surf_flipped = pygame.transform.flip(self.large_stars_surf, True, False)

    def draw_background(self):
        # Get background dimensions
        large_width = self.large_stars_surf.get_width()
        large_height = self.large_stars_surf.get_height()
        small_height = self.small_stars_surf.get_height()

        # Determine how many tiles are needed to fill the screen
        num_tiles_x = self.display_surface.get_width() // large_width + 2
        num_tiles_y = self.display_surface.get_height() // large_height + 2

        # Calculate initial offset positions for the background tiles
        start_x = -self.offset.x % large_width - large_width
        start_y = -self.offset.y % large_height - large_height

        for i in range(num_tiles_x):
            for j in range(num_tiles_y):
                large_star_offset = (start_x + i * large_width, start_y + j * large_height)
                small_star_offset = (start_x + i * large_width, start_y + j * large_height + large_height)

                # Blit the large stars and flipped large stars with a 1-pixel overlap
                self.display_surface.blit(self.large_stars_surf, large_star_offset)
                self.display_surface.blit(self.large_stars_surf_flipped, (large_star_offset[0] + large_width - 1, large_star_offset[1]))

                # Blit the small stars
                self.display_surface.blit(self.small_stars_surf, small_star_offset)