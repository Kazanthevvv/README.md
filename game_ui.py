"""
Модуль графического интерфейса шашек
"""
import pygame
import sys
from game_logic import CheckersGame

class CheckersUI:
    def __init__(self):
        self.game = CheckersGame()
        self.cell_size = 80
        self.board_size = 8 * self.cell_size
        self.selected_piece = None
        self.valid_moves = []
        
        # Инициализация Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.board_size, self.board_size))
        pygame.display.set_caption("Шашки")
        
        # Цвета
        self.colors = {
            'light': (240, 217, 181),
            'dark': (181, 136, 99),
            'highlight': (106, 190, 48),
            'move_highlight': (70, 130, 180),
            'white': (255, 255, 255),
            'black': (60, 60, 60),
            'white_king': (200, 200, 255),
            'black_king': (100, 100, 150)
        }
        
        # Шрифт
        self.font = pygame.font.SysFont('Arial', 24)
    
    def draw_board(self):
        """Отрисовка игровой доски"""
        for row in range(8):
            for col in range(8):
                color = self.colors['light'] if (row + col) % 2 == 0 else
