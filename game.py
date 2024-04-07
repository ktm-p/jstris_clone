import random
from board import Board
from tetromino import *
import pygame

class Game:
    def __init__(self) -> None:
        self.board = Board()
        self.blocks = [IPiece(), JPiece(), LPiece(), OPiece(), SPiece(), TPiece(), ZPiece()]

        self.current_block = self.get_block()
        self.next_blocks = [self.get_block() for i in range(5)]
        self.next_block = self.next_blocks[0]

        self.silhouette_col_offset = 0
        self.silhouette_rotation_state = 0
        self.silhouette = self.get_silhouette()

        self.held_block = None
        self.holding = False
        self.turn_holding = False
        self.game_over = False

    def get_block(self) -> Block:
        if len(self.blocks) == 0:
            self.blocks = [IPiece(), JPiece(), LPiece(), OPiece(), SPiece(), TPiece(), ZPiece()]

        block = random.choice(self.blocks)
        self.blocks.remove(block)

        return block

    def get_silhouette(self) -> Block:
        silhouette = self.silhouette_copy(self.current_block)
        silhouette.move(0, self.silhouette_col_offset)
        silhouette.move(self.current_block.row_state, 0)
        silhouette.set_rotation_state(self.silhouette_rotation_state)
        while True:
            silhouette.move(1, 0)
            if not (self.silhouette_inside(silhouette) and self.silhouette_fit(silhouette)):
                silhouette.move(-1, 0)
                break
            
        return silhouette
    
    # BASIC MOVEMENTS
    def move_right(self) -> None:
        self.current_block.move(0, 1)
        self.silhouette_col_offset += 1

        if not (self.block_inside() and self.block_fit()):
            self.current_block.move(0, -1)
            self.silhouette_col_offset -= 1

        self.silhouette = self.get_silhouette()

    def move_left(self) -> None:
        self.current_block.move(0, -1)
        self.silhouette_col_offset -= 1

        if not (self.block_inside() and self.block_fit()):
            self.current_block.move(0, 1)
            self.silhouette_col_offset += 1

        self.silhouette = self.get_silhouette()

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
    # TODO: IMPLEMENT KICK-BACKS FOR ROTATION
    def rotate_up(self) -> None:
        self.current_block.rotate_up()
        self.silhouette_rotation_state = (self.silhouette_rotation_state + 1) % 4

        cells = self.current_block.get_cell_position()
        for cell in cells:
            if not(self.board.is_inside(cell.row, cell.col)):
                self.kickback(cell.row, cell.col)
        
        if not self.block_fit():
            self.srs(False)

        self.silhouette = self.get_silhouette()
    
    def rotate_down(self) -> None:
        self.current_block.rotate_down()
        self.silhouette_rotation_state = (self.silhouette_rotation_state - 1) % 4

        cells = self.current_block.get_cell_position()
        for cell in cells:
            if not(self.board.is_inside(cell.row, cell.col)):
                self.kickback(cell.row, cell.col)

        if not self.block_fit():
            self.srs(True)

        self.silhouette = self.get_silhouette()

    def kickback(self, row: int, col: int) -> None:
        if (row < 0):
            self.current_block.move(1, 0)
        elif (row >= self.board.num_rows):
            self.current_block.move(-1, 0)
        elif (col >= self.board.num_cols):
            self.current_block.move(0, -1)
            self.silhouette_col_offset -= 1
        elif (col < 0):
            self.current_block.move(0, 1)
            self.silhouette_col_offset += 1
    
    # TODO: FIX EDGE CASE OF ROTATING ON EDGE OF BOARD...!!!
    def srs(self, down: bool) -> None:
        id = self.current_block.id
        rotation_state = self.current_block.rotation_state
        self.srs_helper(id, rotation_state, down)
    
    def srs_helper(self, id: int, rotation_state: int, down: bool) -> None:
        if id in [2, 3, 5, 6, 7]:
            if down:
                if rotation_state == 0:
                    self.fromRto0_fromRto2(down)
                
                if rotation_state == 1:
                    self.from2toR_from0toR(down)

                if rotation_state == 2:
                    self.fromLto2_fromLto0(down)

                if rotation_state == 3:
                    self.from0toL_from2toL(down)
            else:
                if rotation_state == 0:
                    self.fromLto2_fromLto0(down)
                
                if rotation_state == 1:
                    self.from2toR_from0toR(down)

                if rotation_state == 2:
                    self.fromRto0_fromRto2(down)

                if rotation_state == 3:
                    self.from0toL_from2toL(down)
                    
        elif id == 1:
            if down:
                if rotation_state == 0:
                    self.fromRto0_from2toL(down)
                
                if rotation_state == 1:
                    self.from2toR_fromLto0(down)

                if rotation_state == 2:
                    self.fromLto2_from0toR(down)

                if rotation_state == 3:
                    self.from0toL_fromRto2(down)
            else:
                if rotation_state == 0:
                    self.from2toR_fromLto0(down)  

                if rotation_state == 1:
                    self.fromLto2_from0toR(down)

                if rotation_state == 2:
                    self.from0toL_fromRto2(down)

                if rotation_state == 3:
                    self.fromRto0_from2toL(down)

    # Non-I rotations
    def fromRto0_fromRto2(self, down: bool) -> None:
        # Test 2
        self.srs_move_right()
        if self.block_inside() and self.block_fit():
            return
        
        # Test 3
        self.srs_move_down()
        if self.block_inside() and self.block_fit():
            return
        
        # Test 4
        self.srs_move_left()
        self.srs_move_up(3)
        if self.block_inside() and self.block_fit():
            return
        
        # Test 5
        self.srs_move_right()
        if self.block_inside() and self.block_fit():
            return
        
        self.srs_move_left()
        self.srs_move_down(2)
        if down:
            self.srs_rotate_up()
        else:
            self.srs_rotate_down()
        return
    
    def from2toR_from0toR(self, down: bool) -> None:
        # Test 2
        self.srs_move_left()
        if self.block_inside() and self.block_fit():
            return

        # Test 3
        self.srs_move_up()
        if self.block_inside() and self.block_fit():
            return
        
        # Test 4
        self.srs_move_right()
        self.srs_move_down(3)
        if self.block_inside() and self.block_fit():
            return

        # Test 5
        self.srs_move_left()
        if self.block_inside() and self.block_fit():
            return
        
        self.srs_move_right()
        self.srs_move_up(2)
        if down:
            self.srs_rotate_up()
        else:
            self.srs_rotate_down()
        return
    
    def fromLto2_fromLto0(self, down: bool) -> None:
        # Test 2
        self.srs_move_left()
        if self.block_inside() and self.block_fit():
            return
        
        # Test 3
        self.srs_move_down()
        if self.block_inside() and self.block_fit():
            return
        
        # Test 4
        self.srs_move_right()
        self.srs_move_up(3)
        if self.block_inside() and self.block_fit():
            return

        # Test 5
        self.srs_move_left()
        if self.block_inside() and self.block_fit():
            return

        self.srs_move_right()
        self.srs_move_down(2)
        if down:
            self.srs_rotate_up()
        else:
            self.srs_rotate_down()
        return
    
    def from0toL_from2toL(self, down: bool) -> None:
        # Test 2
        self.srs_move_right()
        if self.block_inside() and self.block_fit():
            return
        
        # Test 3
        self.srs_move_up()
        if self.block_inside() and self.block_fit():
            return
        
        # Test 4
        self.srs_move_left()
        self.srs_move_down(3)
        if self.block_inside() and self.block_fit():
            return
        
        # Test 5
        self.srs_move_right()
        if self.block_inside() and self.block_fit():
            return
        
        self.srs_move_left()
        self.srs_move_up(2)
        if down:
            self.srs_rotate_up()
        else:
            self.srs_rotate_down()
        return
    
    # I rotations
    def fromRto0_from2toL(self, down: bool) -> None:
        # Test 2
        self.srs_move_right(2)
        if self.block_inside() and self.block_fit():
            return
        
        # Test 3
        self.srs_move_left(3)
        if self.block_inside() and self.block_fit():
            return
        
        # Test 4
        self.srs_move_right(3)
        self.srs_move_up()
        if self.block_inside() and self.block_fit():
            return
        
        # Test 5
        self.srs_move_left(3)
        self.srs_move_down(3)
        if self.block_inside() and self.block_fit():
            return
        
        self.srs_move_right(1)
        self.srs_move_up(2)
        if down:
            self.srs_rotate_up()
        else:
            self.srs_rotate_down()
        return
    
    def from2toR_fromLto0(self, down: bool) -> None:
        # Test 2
        self.srs_move_right()
        if self.block_inside() and self.block_fit():
            return
        
        # Test 3
        self.srs_move_left(3)
        if self.block_inside() and self.block_fit():
            return
        
        # Test 4
        self.srs_move_right(3)
        self.srs_move_down(2)
        if self.block_inside() and self.block_fit():
            return
        
        # Test 5
        self.srs_move_left(3)
        self.srs_move_up(3)
        if self.block_inside() and self.block_fit():
            return
        
        if down:
            self.srs_rotate_up()
        else:
            self.srs_rotate_down()
        return

    def fromLto2_from0toR(self, down: bool) -> None:
        # Test 2
        self.srs_move_left(2)
        if self.block_inside() and self.block_fit():
            return
        
        # Test 3
        self.srs_move_right(3)
        if self.block_inside() and self.block_fit():
            return
        
        # Test 4
        self.srs_move_left(3)
        self.srs_move_down(1)
        if self.block_inside() and self.block_fit():
            return
        
        # Test 5
        self.srs_move_right(3)
        self.srs_move_up(3)
        if self.block_inside() and self.block_fit():
            return
        
        self.srs_move_left()
        self.srs_move_down(2)
        if down:
            self.srs_rotate_up()
        else:
            self.srs_rotate_down()
        return

    def from0toL_fromRto2(self, down: bool) -> None:
        # Test 2
        self.srs_move_left()
        if self.block_inside() and self.block_fit():
            return
        
        # Test 3
        self.srs_move_right(3)
        if self.block_inside() and self.block_fit():
            return
        
        # Test 4
        self.srs_move_left(3)
        self.srs_move_up(2)
        if self.block_inside() and self.block_fit():
            return
        
        # Test 5
        self.srs_move_right(3)
        self.srs_move_down(3)
        if self.block_inside() and self.block_fit():
            return
        
        self.srs_move_left(2)
        self.srs_move_up()
        if down:
            self.srs_rotate_up()
        else:
            self.srs_rotate_down()
        return
    
    def srs_move_up(self, steps: int = 1) -> None:
        self.current_block.move(-steps, 0)
    
    def srs_move_right(self, steps: int = 1):
        self.current_block.move(0, steps)
        self.silhouette_col_offset += steps

    def srs_move_left(self, steps: int = 1):
        self.current_block.move(0, -steps)
        self.silhouette_col_offset -= steps

    def srs_move_down(self, steps: int = 1):
        self.current_block.move(steps, 0)

    def srs_rotate_up(self):
        self.current_block.rotate_up()
        self.silhouette_rotation_state = (self.silhouette_rotation_state + 1) % 4
    
    def srs_rotate_down(self):
        self.current_block.rotate_down()
        self.silhouette_rotation_state = (self.silhouette_rotation_state - 1) % 4

    # PLACES BLOCK
    def place_block(self) -> None:
        cells = self.current_block.get_cell_position()
        for cell in cells:
            self.board.grid[cell.row][cell.col] = self.current_block.id
        
        self.current_block = self.next_block
        self.get_next_block()

        self.board.clear_rows()
        self.turn_holding = False

        self.silhouette_col_offset = 0
        self.silhouette_rotation_state = 0
        self.silhouette = self.get_silhouette()

        if not self.block_fit():
            self.game_over = True
    
    # HOLDS BLOCK
    def hold_block(self) -> None:
        if not self.turn_holding:
            if not self.holding:
                self.held_block = self.copy(self.current_block)
                self.get_next_block()

                self.silhouette_col_offset = 0
                self.silhouette_rotation_state = 0
                self.silhouette = self.get_silhouette()
                
                self.holding = True

            else:
                self.held_block, self.current_block = self.copy(self.current_block), self.copy(self.held_block)

                self.silhouette_col_offset = 0
                self.silhouette_rotation_state = 0
                self.silhouette = self.get_silhouette()
            
            self.turn_holding = True

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

    # UTILITY FUNCTIONS
    def copy(self, block: Block) -> Block:
        blocks = [None, IPiece(), JPiece(), LPiece(), OPiece(), SPiece(), TPiece(), ZPiece()]
        return blocks[block.id]
    
    def silhouette_copy(self, block: Block) -> Block:
        blocks = [None, ISilhouette(), JSilhouette(), LSilhouette(), OSilhouette(), SSilhouette(), TSilhouette(), ZSilhouette()]
        return blocks[block.id]
    
    def get_next_block(self) -> None:
        self.current_block = self.next_blocks.pop(0)
        self.next_blocks.append(self.get_block())
        self.next_block = self.next_blocks[0]

    # DRAW CELLS
    def draw(self, screen: pygame.display, col_offset: int, row_offset: int) -> None:
        if self.game_over:
            self.place_block()
            self.board.draw_game_over(screen, col_offset, row_offset)
        else:
            self.board.draw(screen, col_offset, row_offset)
            self.silhouette.draw(screen, col_offset, row_offset)
            self.current_block.draw(screen, col_offset, row_offset)
            self.draw_next(screen, col_offset, row_offset)
            self.draw_held(screen, 0, row_offset)
    
    def draw_next(self, screen: pygame.display, col_offset: int, row_offset: int) -> None:
        row_offset_multiplier = 0
        for block in self.next_blocks:
            if (block.id == 4):
                block.draw(screen, col_offset + 240 - block.cell_size, row_offset + 30 + (3 * block.cell_size * row_offset_multiplier))
            else:
                block.draw(screen, col_offset + 240, row_offset + 30 + (3 * block.cell_size * row_offset_multiplier))
            row_offset_multiplier += 1
    
    def draw_held(self, screen: pygame.display, col_offset: int, row_offset: int) -> None:
        if self.holding:
            if self.held_block.id == 1:
                self.held_block.draw(screen, -60, row_offset + 30)
            else:    
                self.held_block.draw(screen, -30, row_offset + 30)

    def reset(self) -> None:
        self.board.reset()
        self.blocks = [IPiece(), JPiece(), LPiece(), OPiece(), SPiece(), TPiece(), ZPiece()]
        self.silhouettes = [ISilhouette(), JSilhouette(), LSilhouette(), OSilhouette(), SSilhouette(), TSilhouette(), ZSilhouette()]
        self.current_block = self.get_block()
        self.next_blocks = [self.get_block() for i in range(5)]
        self.next_block = self.next_blocks[0]

        self.silhouette_col_offset = 0
        self.silhouette_rotation_state = 0
        self.silhouette = self.get_silhouette()

        self.game_over = False
        self.held_block = None
        self.holding = False