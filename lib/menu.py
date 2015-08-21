'''
@author: avalanchy (at) google mail dot com
@translation by MarcusDrake, 2015-08-21
@version: 0.1; python 2.7; pygame 1.9.2pre; SDL 1.2.14; MS Windows XP SP3
@date: 2012-04-08
@license: This document is under GNU GPL v3

README on the bottom of document.

@font: from http://www.dafont.com/coders-crux.font
      more abuot license you can find in data/coders-crux/license.txt
'''

import pygame
from pygame.locals import *

if not pygame.display.get_init():
    pygame.display.init()

if not pygame.font.get_init():
    pygame.font.init()


class Menu:
    list = []
    field = []
    font_size = 32
    font_path = 'lib/data/coders_crux.ttf'
    font = pygame.font.Font
    dest_surface = pygame.Surface
    number_of_fields = 0
    bg_color = (51,51,51)
    text_color =  (255, 255, 153)
    selection_color = (153,102,255)
    menu_selection = 0
    menu_position = (0,0)
    menu_width = 0
    menu_height = 0

    class Menu:
        text = ''
        Menu = pygame.Surface
        field_rectangle = pygame.Rect
        selection_rectangle = pygame.Rect

    def move_menu(self, top, left):
        self.menu_position = (top,left)

    def set_colors(self, text, selection, background):
        self.bg_color = background
        self.text_color =  text
        self.selection_color = selection

    def set_fontsize(self, font_size):
        self.font_size = font_size

    def set_font(self, path):
        self.font_path = path

    def get_position(self):
        return self.menu_selection

    def init(self, list, dest_surface):
        self.list = list
        self.dest_surface = dest_surface
        self.number_of_fields = len(self.list)
        self.create_menu()

    def draw(self, przesun=0):
        if przesun:
            self.menu_selection += przesun
            if self.menu_selection == -1:
                self.menu_selection = self.number_of_fields - 1
            self.menu_selection %= self.number_of_fields
        menu = pygame.Surface((self.menu_width, self.menu_height))
        menu.fill(self.bg_color)
        selection_rectangle = self.field[self.menu_selection].selection_rectangle
        pygame.draw.rect(menu,self.selection_color,selection_rectangle)

        for i in xrange(self.number_of_fields):
            menu.blit(self.field[i].Menu,self.field[i].field_rectangle)
        self.dest_surface.blit(menu,self.menu_position)
        return self.menu_selection

    def create_menu(self):
        przesuniecie = 0
        self.menu_height = 0
        self.font = pygame.font.Font(self.font_path, self.font_size)
        for i in xrange(self.number_of_fields):
            self.field.append(self.Menu())
            self.field[i].text = self.list[i]
            self.field[i].Menu = self.font.render(self.field[i].text, 1, self.text_color)

            self.field[i].field_rectangle = self.field[i].Menu.get_rect()
            przesuniecie = int(self.font_size * 0.2)

            height = self.field[i].field_rectangle.height
            self.field[i].field_rectangle.left = przesuniecie
            self.field[i].field_rectangle.top = przesuniecie+(przesuniecie*2+height)*i

            width = self.field[i].field_rectangle.width+przesuniecie*2
            height = self.field[i].field_rectangle.height+przesuniecie*2
            left = self.field[i].field_rectangle.left-przesuniecie
            top = self.field[i].field_rectangle.top-przesuniecie

            self.field[i].selection_rectangle = (left,top ,width, height)
            if width > self.menu_width:
                    self.menu_width = width
            self.menu_height += height
        x = self.dest_surface.get_rect().centerx - self.menu_width / 2
        y = self.dest_surface.get_rect().centery - self.menu_height / 2
        mx, my = self.menu_position
        self.menu_position = (x+mx, y+my)
