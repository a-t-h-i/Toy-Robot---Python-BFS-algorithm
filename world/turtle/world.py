from random import randint, random
import turtle

pen = turtle.Turtle()
my_ninja = turtle.Turtle()

pen.pencolor('red')
pen.speed(1000)
pen.setheading(90)
pen.penup()

real_ninja = turtle

def draw_world():
    my_ninja.ht()
    my_ninja.penup()
    my_ninja.goto(-100,200)
    my_ninja.pendown()
    my_ninja.goto(100,200)
    my_ninja.goto(100,-200)
    my_ninja.goto(-100,-200)
    my_ninja.goto(-100, 200)
    
    
draw_world()

def place_obstacle(position):
    real_ninja.tracer(0,0)
    real_ninja.ht()
    real_ninja.pencolor('red')
    real_ninja.pensize(1)
    real_ninja.speed(1000)
    real_ninja.penup()
    real_ninja.goto(position)
    real_ninja.fillcolor('red')
    real_ninja.pendown()
    real_ninja.begin_fill()
    real_ninja.forward(4)
    real_ninja.right(90)
    real_ninja.forward(4)
    real_ninja.right(90)
    real_ninja.forward(4)
    real_ninja.right(90)
    real_ninja.forward(4)
    real_ninja.right(90)
    real_ninja.end_fill()
    real_ninja.penup()
    real_ninja.tracer(1,1)