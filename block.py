import pygame
from colors import Colors
from position import Position

class Block:
    def __init__(self, id: int) -> None:
        self.id = id
        self.cells = {}
        self.cell_size = 30
        self.rotation_state = 0
        self.colors = Colors.get_colors()

        self.row_offset = 0
        self.row_state = 0
        self.col_offset = 0
    
    # BASIC MOVEMENT
    def move(self, rows: int, cols: int) -> None:
        self.row_offset += rows
        self.row_state += rows
        self.col_offset += cols
    
    # ROTATIONS
    def rotate_up(self) -> None:
        self.rotation_state = (self.rotation_state + 1) % len(self.cells)

    def rotate_down(self) -> None:
        self.rotation_state = (self.rotation_state - 1) % len(self.cells)

    def set_row_state(self, row_state: int) -> None:
        self.row_state = row_state

    def set_rotation_state(self, rotation_state: int) -> None:
        self.rotation_state = rotation_state

    # GETS ALL CELLS
    def get_cell_position(self) -> list[Position]:
        cells = self.cells[self.rotation_state]
        moved_cells = []
        for position in cells:
            position = Position(position.row + self.row_offset, position.col + self.col_offset)
            moved_cells.append(position)
        
        return moved_cells

    # DRAWS BLOCK
    def draw(self, screen: pygame.display, col_offset: int, row_offset: int) -> None:
        cells = self.get_cell_position()
        for cell in cells:
            cell_rect = pygame.Rect(cell.col * self.cell_size + col_offset, cell.row * self.cell_size + row_offset, self.cell_size, self.cell_size)
            pygame.draw.rect(screen, self.colors[self.id], cell_rect)