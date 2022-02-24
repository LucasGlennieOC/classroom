import os
import pygame
 
class TypeWriterText:
    def __init__(self, text, font, color, interval):
        self.text = text
        self.font = font
        self.color = color
        self.image = None
        self.interval = interval
        self.do_offset()
 
    def do_offset(self, byletter=' '):
        self.offset = 0
        for i in self.text:
            if i != byletter:
                break
            self.offset += 1
 
    def create_image(self):
        self.image = self.font.render(self.text, 1, self.color)
        self.rect = self.image.get_rect()
 
    def update_image(self):
        self.image = self.font.render(self.text, 1, self.color)
 
    def text_width(self):
        return self.font.size(self.text)[0]
 
class TypeWriter:
    messages = {}
 
    def __init__(self, rect, display_lines):
        self.rect = rect
        self.clip_rect = None
        self.next_tick = None
        self.display_lines = display_lines
        self.text = []
        self.line = 0
        self.letter = 0
        self.sub_line = 0
        self.max_lines = 0
        self.max_letters = 0
        self.max_sub_lines = 0
        self.finish = True
 
    def current_data(self):
        return self.text[self.line][self.sub_line]
 
    def clear(self, down_to = 0):
        self.next_tick = None
        self.text = self.text[:down_to]
        self.finish = True
        if down_to == 0:
            self.line = 0
            self.letter = 0
            self.sub_line = 0
            self.max_lines = 0
            self.max_letters = 0
            self.max_sub_lines = 0
        else:
            self.line = down_to
            self.sub_line = 0
            self.letter = 0
 
    def change_text_color(self, color, to_color):
        for item in self.text:
            for it in item:
                if it.color == color:
                    it.color = to_color
                    if it.image != None:
                        it.update_image()
 
    def update_text_info(self):
        self.max_lines = len(self.text)
        self.max_letters = len(self.current_data().text)
        self.max_sub_lines = len(self.text[self.line])
 
    def do_message(self, key, font, color):
        for text, interval, text_type in TypeWriter.messages[key]:
            if text_type == 'line':
                self.add_text_line(text, font, color, interval)
            else:
                self.add_text(text, font, color, interval)
 
    def add_text_line(self, text, font, color, interval):
        if font.size(text)[0] < self.rect.w:
            self.text.append([TypeWriterText(text, font, color, interval)])
        else:
            words = text.split(' ')
            line = words[0]
            for word in words[1:]:
                if font.size(line + ' ' + word)[0] < self.rect.w:
                    line += ' ' + word
                else:
                    self.text.append([TypeWriterText(line, font, color, interval)])
                    line = word
 
            self.text.append([TypeWriterText(line, font, color, interval)])
        self.finish = False
        self.update_text_info()
 
    # TODO wordwarp
    def add_text(self, text, font, color, interval):
        if len(self.text) == 0:
            self.text.append([TypeWriterText(text, font, color, interval)])
        else:
            self.text[-1].append(TypeWriterText(text, font, color, interval))
        self.finish = False
        self.update_text_info()
 
    def push_text_line(self, text, font, color):
        self.text.append([TypeWriterText(text, font, color, 1)])
        self.line += 1
        self.check_lines()
 
    def check_lines(self):
        if self.line > self.display_lines:
            self.text = self.text[1:]
            self.line -= 1
            if self.line < len(self.text):
                self.update_text_info()
 
    def update_rect(self):
        if self.letter == 0:
            self.clip_rect = None
        else:
            data = self.text[self.line][self.sub_line]
            size = data.font.size(data.text[:self.letter])
            self.clip_rect = pygame.Rect(0, 0, *size)
 
    def next_letter(self):
        self.letter += 1
        if self.letter >= self.max_letters:
            self.letter = 0
            self.sub_line += 1
            if self.sub_line >= self.max_sub_lines:
                self.sub_line = 0
                self.line += 1
                if self.line >= self.max_lines:
                    self.finish = True
                else:
                    self.letter = self.current_data().offset
                    self.max_letters = len(self.current_data().text)
                    self.max_sub_lines = len(self.text[self.line])
            else:
                self.max_letters = len(self.current_data().text)
        self.update_rect()
 
    def elaspe(self, ticks):
        if not self.finish:
            if self.next_tick == None:
                self.next_tick = ticks + self.current_data().interval
            else:
                if ticks > self.next_tick:
                    self.next_tick = ticks + self.current_data().interval
                    self.next_letter()
 
    def line_height(self, line):
        height = 0
        for i in self.text[line]:
            height = max(height, i.font.get_ascent() + i.font.get_descent() +
                         int(i.font.get_linesize() / 2))
        return height
 
    def blit(self, surface):
        self.check_lines()
        x, y = self.rect.topleft
        for i in range(self.line):
            for text in self.text[i]:
                if text.image == None:
                    text.create_image()
                rect = text.rect
                rect.topleft = (x, y)
                surface.blit(text.image, rect)
                x += text.text_width()
            x = self.rect.x
            y += self.line_height(i)
 
        for j in range(self.sub_line):
            rect = self.text[self.line][j].rect
            rect.topleft = (x, y)
            surface.blit(self.text[self.line][j].image, rect)
            x += self.text[self.line][j].text_width()
 
        if self.rect and self.finish is False:
            if self.current_data().image == None:
                self.current_data().create_image()
 
            if self.clip_rect:
                surface.blit(self.current_data().image, (x,y), self.clip_rect)
 
class Screen:
    event = None
    blit = None
    width = None
    height = None
    rect = None
 
    @classmethod
    def set_state(cls, blit=None, event=None):
        cls.event = event
        cls.blit = blit
 
    def __init__(self, caption, size):
        pygame.init()
        pygame.display.set_caption(caption)
        self.screen = pygame.display.set_mode(size)
        self.clock = pygame.time.Clock()
        self.running = False
 
        Screen.width, Screen.height = size
        Screen.rect = pygame.Rect(0,0,*size)
 
    def get_size(self):
        return Screen.WIDTH, Screen.HEIGHT
 
    def get_rect(self):
        return pygame.Rect(0,0,Screen.WIDTH,Screen.HEIGHT)
 
    def loop(self, fps):
        self.running = True
        while self.running:
            if Screen.event:
                Screen.event(event)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                elif event.type == pygame.QUIT:
                    self.running = False
 
            if Screen.blit:
                Screen.blit(self.screen)
            pygame.display.flip()
            self.clock.tick(fps)
 
        pygame.quit()
 
class Scene:
    def __init__(self):
        Screen.set_state(self.blit)
        self.writer = TypeWriter(pygame.Rect(50,50,700,500), 20)
        font = pygame.font.Font(None, 24)
        speed = 120
        color = pygame.Color('steelblue')
        long_line = 'A pygame typewriter class. Typewriter will wrap really '
        long_line += 'long lines of text. So doing really long text is fine. '
        long_line += 'So there no such thing as to long of a line.'
        self.writer.add_text_line(long_line, font, color, speed)
        self.writer.add_text_line("But it won't wrap it into the next line.", font, color, speed)
        self.writer.add_text_line('You can have really fast lines.', font, color, 15)
        self.writer.add_text_line('You can have ', font, color, speed)
        self.writer.add_text('different ', font, pygame.Color('orangered'), speed)
        self.writer.add_text('col', font, pygame.Color('forestgreen'), speed)
        self.writer.add_text('or ', font, pygame.Color('lawngreen'), speed)
        self.writer.add_text('words.', font, pygame.Color('dodgerblue'), speed)
        self.writer.add_text_line('    Typewriter ignore spaces when in front of line.', font, color, speed)
        self.writer.add_text_line('What can I do to improve this ?', font, color, speed)
 
    def blit(self, surface):
        surface.fill((0,0,30))
        ticks = pygame.time.get_ticks()
        self.writer.elaspe(ticks)
        self.writer.blit(surface)
 
if __name__ == '__main__':
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    screen = Screen('TypeWriter', (800, 600))
    Scene()
    screen.loop(60)
