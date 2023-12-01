from pygame import Surface
from pygame.event import Event
from elements import BaseElement
from typing import List, Optional
from pygame.rect import Rect

class Screen:
    def __init__(self) -> None:
        self.elements: List[BaseElement] = []
        self.active_element: Optional[int] = None

    def add_element(self, el: BaseElement) -> None:
        self.elements.append(el)

    def draw(self, screen: Surface) -> None:
        for element in self.elements:
            is_active = element is self.active_element
            element.draw(screen, is_active)
    def handle_mouse_click(self, event: Event):
        for element in self.elements:
            el_rect = Rect(element.pos, element.size)
            if el_rect.collidepoint(event.pos):
                self.active_element = element
                element.handle_mouse_click(event)
    def handle_keyboard(self, event: Event):
        if self.active_element is not None:
            self.active_element.handle_keyboard(event)


