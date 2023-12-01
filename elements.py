from pygame import Vector2, Surface
from pygame.font import Font
from pygame.draw import rect
from pygame.rect import Rect
from pygame.event import Event
from string import printable
import pygame
from storage import local_storage
from typing import Callable


class BaseElement:
    def __init__(self, pos: Vector2, size: Vector2) -> None:
        self.pos = pos
        self.size = size

    def draw(self, screen: Surface, is_active: bool = False):
        raise NotImplementedError
    
    def handle_mouse_click(self, event: Event):
        print("aaaaa")
    def handle_keyboard(self, event: Event):
        print(id(self), event.unicode)


class TextInput(BaseElement):
    def __init__(self, pos: Vector2, size: Vector2, label: str, storage_key: str) -> None:
        super().__init__(pos, size)
        self.storage_key = storage_key
        local_storage[self.storage_key] = ""
        self.label = label
        

        label_font = Font("ChakraPetch-Regular.ttf", 10)
        self.label_surface = label_font.render(self.label, True, (150,150,150), (255,255,255))

        self.txt_font = Font("ChakraPetch-Regular.ttf", 25)

    def handle_mouse_click(self, event: Event):
        print(f"input {id(self)} is active")
    
    def handle_keyboard(self, event: Event):

        if event.key == pygame.K_BACKSPACE:
            local_storage[self.storage_key] = local_storage[self.storage_key][0:-1]
            return

        if event.key == pygame.K_RETURN:
            local_storage.send_message()
            return
        if event.unicode in printable:
            local_storage[self.storage_key] += event.unicode


    def draw(self, screen: Surface, is_active: bool = False) -> None:
        outline = Rect(self.pos, self.size)
        rect(screen, (150,150,150), outline, 2, 5)
        screen.blit(self.label_surface, self.pos + Vector2(12,-self.label_surface.get_height()/2))

        input_value = local_storage[self.storage_key]
        if is_active:
            input_value+= "|"

        txt_surface = self.txt_font.render(input_value, True, (50,50,50))
        screen.blit(txt_surface, self.pos+ Vector2(10,self.size.y/2-txt_surface.get_height()/2))

class Button(BaseElement):
    def __init__(self, pos: Vector2, size: Vector2, txt: str, click_callback: Callable) -> None:
        super().__init__(pos, size)
        font = Font("ChakraPetch-Regular.ttf", 25)
        self.txt_image = font.render(txt, True, (0,0,0))

        self.clicked = click_callback


    def handle_mouse_click(self, event: Event):
        self.clicked()
        
    def draw(self, screen: Surface , is_active: bool = False):
        outline = Rect(self.pos, self.size)
        rect(screen, (150,150,150), outline, 1, 5)
        txt_x, txt_y = self.txt_image.get_size()
        screen.blit(self.txt_image, self.pos+ Vector2(self.size.x / 2 - txt_x/2, self.size.y / 2 - txt_y/2))

class ScreenTitle(BaseElement):
    def __init__(self, pos: Vector2, txt: str) -> None:
        
        self.txt = txt
        font = Font("ChakraPetch-Regular.ttf", 48)
        self.txt_surface = font.render(self.txt, True, (0,0,0))
        self.delta = Vector2(self.txt_surface.get_width()/2,0)

        super().__init__(pos, Vector2(self.txt_surface.get_size()))

    def handle_mouse_click(self, event: Event):
        return

    def draw(self, screen: Surface, is_active: bool = False):
        screen.blit(self.txt_surface, self.pos-self.delta)

class MessagesList(BaseElement):
    def __init__(self, pos: Vector2, size: Vector2) -> None:
        super().__init__(pos, size)
        self.author_font = Font("ChakraPetch-Regular.ttf", 12)
        self.message_font = Font("ChakraPetch-Regular.ttf", 11)
        self.date_font = Font("ChakraPetch-Regular.ttf", 10)

    def draw(self, screen:Surface, is_active:bool = False):
        lowest_y = self.pos.y + self.size.y
        messages = local_storage["messages"]
        if len(messages) == 0:
            return
        for author, text, date in reversed(messages):
            author_img = self.author_font.render(author, True, (227, 0, 120))
            txt_img = self.message_font.render(text, True, (0,0,0))
            date_img = self.date_font.render(date, True, (80,80,80))

            msg_height = author_img.get_height() + txt_img.get_height() + 10

            msg_surface = Surface((self.size.x, msg_height))
            msg_surface.fill((255,255,255))
            msg_surface.blit(author_img, (0,0))
            msg_surface.blit(txt_img, (0, author_img.get_height() + 10))
            msg_surface.blit(date_img, (self.size.x - date_img.get_width(), 0))

            screen.blit(msg_surface, (self.pos.x,lowest_y - msg_surface.get_height() ))

            lowest_y -= msg_surface.get_height() + 10