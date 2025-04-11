import pygame
import math
import numpy as np
from brain import NeuralNetwork

class Car:
    def __init__(self, x, y, brain=None):
        self.x = x
        self.y = y
        self.angle = 0
        self.speed = 0
        self.max_speed = 4
        self.acceleration = 0.2
        self.rotation_speed = 5
        self.length = 20
        self.width = 10
        self.is_alive = True

        # Sensors
        self.num_sensors = 5
        self.sensor_length = 100
        self.sensors = []
        self.sensor_data = [1] * self.num_sensors

        # AI Brain
        self.brain = brain if brain else NeuralNetwork(self.num_sensors, 10, 2)

    def update(self, screen, track_mask):
        if not self.is_alive:
            return

        self.cast_sensors(track_mask)
        output = self.brain.forward(self.sensor_data)

        if output[0] > 0.5:
            self.angle -= self.rotation_speed
        if output[1] > 0.5:
            self.speed += self.acceleration
        else:
            self.speed *= 0.95

        self.speed = max(min(self.speed, self.max_speed), -self.max_speed)
        self.x += math.cos(math.radians(self.angle)) * self.speed
        self.y += math.sin(math.radians(self.angle)) * self.speed

        if self.check_collision(track_mask):
            self.is_alive = False

        self.draw(screen)

    def draw(self, screen):
        # Draw car
        rect = pygame.Rect(0, 0, self.length, self.width)
        rect.center = (self.x, self.y)
        rotated_image = pygame.transform.rotate(pygame.Surface((self.length, self.width)), -self.angle)
        rotated_image.fill((0, 255, 0) if self.is_alive else (255, 0, 0))
        rotated_rect = rotated_image.get_rect(center=(self.x, self.y))
        screen.blit(rotated_image, rotated_rect)

        # Draw sensors
        for sx, sy in self.sensors:
            pygame.draw.line(screen, (255, 255, 0), (self.x, self.y), (sx, sy), 1)
            pygame.draw.circle(screen, (255, 0, 0), (int(sx), int(sy)), 3)

    def cast_sensors(self, track_mask):
        self.sensors = []
        self.sensor_data = []

        track_width, track_height = track_mask.get_size()

        for i in range(self.num_sensors):
            angle_offset = (i - self.num_sensors // 2) * 30  # Spread out rays
            angle = math.radians(self.angle + angle_offset)

            for dist in range(self.sensor_length):
                sx = int(self.x + math.cos(angle) * dist)
                sy = int(self.y + math.sin(angle) * dist)

                if 0 <= sx < track_width and 0 <= sy < track_height:
                    if track_mask.get_at((sx, sy)) == 1:  # mask value: 1 = obstacle
                        break
                else:
                    break

            self.sensors.append((sx, sy))
            self.sensor_data.append(dist / self.sensor_length)


    def check_collision(self, track_mask):
        try:
            return track_mask.get_at((int(self.x), int(self.y))) == 1
        except:
            return True
