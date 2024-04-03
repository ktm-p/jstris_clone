import random
from board import Board
from tetromino import *
import pygame

class Game:
    def __init__(self) -> None:
        self.board = Board()
        self.blocks = [IPiece(), JPiece(), LPiece(), OPiece(), SPiece(), TPiece(), ZPiece()]
        self.silhouettes = [ISilhouette(), JSilhouette(), LSilhouette(), OSilhouette(), SSilhouette(), TSilhouette(), ZSilhouette()]
        self.current_block = self.get_block()
        self.next_block = self.get_block()
        self.silhouette = self.get_silhouette()
        self.game_over = False

    def get_block(self) -> Block:
        if len(self.blocks) == 0:
            self.blocks = [IPiece(), JPiece(), LPiece(), OPiece(), SPiece(), TPiece(), ZPiece()]

        block = random.choice(self.blocks)
        self.blocks.remove(block)

        return block

    def get_silhouette(self) -> Block:
        id = self.current_block.id
        silhouette = self.silhouettes[id - 1]
        while True:
            silhouette.move(1, 0)
            if not (self.silhouette_inside(silhouette) and self.silhouette_fit(silhouette)):
                silhouette.move(-1, 0)
                break
            
        return silhouette
    
    # BASIC MOVEMENTS
    def move_right(self) -> None:
        self.current_block.move(0, 1)
        if not (self.block_inside() and self.block_fit()):
            self.current_block.move(0, -1)

    def move_left(self) -> None:
        self.current_block.move(0, -1)
        if not (self.block_inside() and self.block_fit()):
            self.current_block.move(0, 1)

    def move_down(self) -> None:
        self.current_block.move(1, 0)
        if not (self.block_inside() and self.block_fit()):
            self.current_block.move(-1, 0)
            self.place_block()

    def hard_drop(self) -> None:
        while True:
            self.current_block.move(1, 0)
            if not (self.block_inside() and self.block_fit()):
                self.current_block.move(-1, 0)
                self.place_block()
                break
    
    # ROTATIONS
    def rotate_up(self) -> None:
        self.current_block.rotate_up()
        cells = self.current_block.get_cell_position()
        for cell in cells:
            if not(self.board.is_inside(cell.row, cell.col)):
                self.kickback(cell.row, cell.col)
    
    def rotate_down(self) -> None:
        self.current_block.rotate_down()
        cells = self.current_block.get_cell_position()
        for cell in cells:
            if not(self.board.is_inside(cell.row, cell.col)):
                self.kickback(cell.row, cell.col)

    def kickback(self, row: int, col: int) -> None:
        if (row < 0):
            self.current_block.move(1, 0)
        elif (row >= self.board.num_rows):
            self.current_block.move(-1, 0)
        elif (col >= self.board.num_cols):
            self.current_block.move(0, -1)
        elif (col < 0):
            self.current_block.move(0, 1)
        
    # PLACES BLOCK
    def place_block(self) -> None:
        cells = self.current_block.get_cell_position()
        for cell in cells:
            self.board.grid[cell.row][cell.col] = self.current_block.id
        
        self.current_block = self.next_block
        self.silhouette = self.get_silhouette()
        self.next_block = self.get_block()

        self.board.clear_rows()

        if not self.block_fit():
            self.game_over = True

    # COLLISION CHECKS
    def block_inside(self) -> bool:
        cells = self.current_block.get_cell_position()
        for cell in cells:
            if not (self.board.is_inside(cell.row, cell.col)):
                return False
        return True
    
    def block_fit(self) -> bool:
        cells = self.current_block.get_cell_position()
        for cell in cells:
            if not self.board.is_empty(cell.row, cell.col):
                return False
        return True
    
    def silhouette_inside(self, silhouette: Block) -> bool:
        cells = silhouette.get_cell_position()
        for cell in cells:
            if not (self.board.is_inside(cell.row, cell.col)):
                return False
        return True
    
    def silhouette_fit(self, silhouette: Block) -> bool:
        cells = silhouette.get_cell_position()
        for cell in cells:
            if not self.board.is_empty(cell.row, cell.col):
                return False
        return True
    
    def draw(self, screen: pygame.display) -> None:
        self.board.draw(screen)
        # self.silhouette.draw(screen) TODO: Figure out how to implement silhouettes.
        self.current_block.draw(screen)
    
    def reset(self) -> None:
        self.board.reset()
        self.blocks = [IPiece(), JPiece(), LPiece(), OPiece(), SPiece(), TPiece(), ZPiece()]
        self.silhouettes = [ISilhouette(), JSilhouette(), LSilhouette(), OSilhouette(), SSilhouette(), TSilhouette(), ZSilhouette()]
        self.current_block = self.get_block()
        self.next_block = self.get_block()
        self.silhouette = self.get_silhouette()
        self.game_over = False