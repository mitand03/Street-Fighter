import pygame

class Sphere :
    _image_cache = {}  # shared across instances so each sprite/flip combo is only loaded from disk once

    def __init__(self, pos, speed, type, lifetime=2000):
        self.BASE='graphics/ninja/png/'
        self.pos = list(pos)  # Initial position
        self.speed = speed    # Speed of the bullet
        self.type=type
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = lifetime
        self.velocity=[0,0]

    def update(self):
        # Update position based on velocity
        self.velocity[0] = self.speed if self.type == 'knife' else -self.speed
        self.pos[0] += self.velocity[0]

    def render(self, surface, pos, image):
        flipped = self.speed == -30
        cache_key = (image, self.type, flipped)
        cached_image = Sphere._image_cache.get(cache_key)
        if cached_image is None:
            cached_image = pygame.image.load(self.BASE + image)
            zoom = 0.5 if self.type == 'knife' else 2
            cached_image = pygame.transform.rotozoom(cached_image, 1, zoom)
            if flipped:
                cached_image = pygame.transform.flip(cached_image, True, False)
            Sphere._image_cache[cache_key] = cached_image

        image_rect=cached_image.get_rect(center=pos)
        surface.blit(cached_image,image_rect)

    def is_expired(self):
        current_time = pygame.time.get_ticks()
        return (current_time - self.spawn_time) > self.lifetime