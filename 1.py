import pygame

class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[1] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 30

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        colors = [ 'blue','black', 'red']
        for i in range(self.height):
            for j in range(self.width):

                pygame.draw.rect(screen, 'white',
                                 ((self.left + j * self.cell_size, self.top + i * self.cell_size),
                                 (self.cell_size, self.cell_size)),1)
                pygame.draw.rect(screen, colors[self.board[i][j]],
                                ((self.left + j * self.cell_size + 1, self.top + i * self.cell_size + 1),
                                (self.cell_size - 2, self.cell_size - 2)))

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)

    def on_click(self, cell):
        i, j = cell
        self.board[i][j] = (self.board[i][j] + 1) % 3



    def get_cell(self, pos):
        x, y = pos
        j = (x - self.left) // self.cell_size
        i = (y - self.top) // self.cell_size
        if 0 <= i < self.height and 0 <= j < self.width:
            return i, j
        else:
            None


if __name__ == '__main__':
    pygame.init()
    size = 800, 600
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Инициализация')

    board = Board(5, 8)
    board.set_view(100,100,50)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.get_click(event.pos)
        screen.fill((0, 0, 0))
        board.render(screen)
        pygame.display.flip()

    pygame.quit()