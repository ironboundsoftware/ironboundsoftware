#!/usr/bin/env python
#
# pyglet_pong.py
# Sep 9, 2007
# Nick Loadholtes nick@ironboundsoftware.com
#
# A little game of pong made with pyglet, based off of the examples. Nothing
# real fancy, just a proof of concept.
#

import os
from pyglet import window
from pyglet import image
from pyglet import font
from random import randint

win = window.Window(600, 600)
img = image.load('red_paddle.png')
ball_img = image.load('ball.png')
ft = font.load('Arial', 36)

paddle_x = 0
paddle_y = 0
ball_x = 300
ball_y = 300
ball_vx = -5
ball_vy = -5
width = 600
height = 600
score_player = 0
score_comp = 0

def moveMouse(x,y,dx,dy, buttons=None, modifiers=None):
	global paddle_y
	paddle_y = y

win.on_mouse_motion = moveMouse
win.on_mouse_drag = moveMouse
win.set_mouse_visible(False)

def moveBall():
	global ball_x, ball_y, ball_vx, ball_vy, width, height, paddle_x, paddle_y, score_player, score_comp
	ball_x += ball_vx
	ball_y += ball_vy

	if ball_x > width:
		ball_vx *= -1
		ball_x += ball_vx *2
		return
	if ball_x+10 in range(paddle_x, paddle_x+10) and ball_y+10 in range(paddle_y, paddle_y+40):
		ball_vx *= -1
		ball_vy *= -1
		ball_x += ball_vx *(1 + randint(2,5))
		ball_y += ball_vy *(1 + randint(2,5))
		return
	if ball_x+10 <= 0:
		print "Score!"
		score_comp += 1
		ball_x = randint(width/2, width)
		ball_y = randint(height/2, height)
		return
	if ball_y >= height or  ball_y <= 0:
		ball_vy *= -1
		ball_y += ball_vy *2
	
def printScore(you, me):
	global ft, height
	s =  'Player: '+str(you)+'        Computer:'+str(me)
	text = font.Text(ft,s, 0, height-40)
	text.draw()

#
# Event loop
while not win.has_exit:
	win.dispatch_events()
	moveBall()
	win.clear()
	printScore(score_player, score_comp)
	img.blit(paddle_x, paddle_y)
	ball_img.blit(ball_x, ball_y)
	win.flip()
