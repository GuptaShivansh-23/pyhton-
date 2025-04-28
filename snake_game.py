import turtle
import time
import random

# Snake class definition
class Snake:
    def __init__(self):
        self.segments = []
        self.create_snake()
        self.head = self.segments[0]

    def create_snake(self):
        self.add_segment((0, 0), "green")
        for i in range(2):
            self.add_segment((-(i + 1) * 20, 0))

    def add_segment(self, position, color="grey"):
        segment = turtle.Turtle("square")
        segment.color(color)
        segment.penup()
        segment.goto(position)
        self.segments.append(segment)

    def extend(self):
        self.add_segment(self.segments[-1].position())

    def move(self):
        for seg_num in range(len(self.segments) - 1, 0, -1):
            x = self.segments[seg_num - 1].xcor()
            y = self.segments[seg_num - 1].ycor()
            self.segments[seg_num].goto(x, y)
        self.segments[0].forward(20)

    def up(self):
        if self.head.heading() != 270:
            self.head.setheading(90)

    def down(self):
        if self.head.heading() != 90:
            self.head.setheading(270)

    def left(self):
        if self.head.heading() != 0:
            self.head.setheading(180)

    def right(self):
        if self.head.heading() != 180:
            self.head.setheading(0)

    def reset(self):
        for segment in self.segments:
            segment.goto(1000, 1000)  # Move old segments off-screen
        self.segments.clear()
        self.create_snake()
        self.head = self.segments[0]

# Food class definition
class Food(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.penup()
        self.shapesize(stretch_len=0.5, stretch_wid=0.5)
        self.color("blue")
        self.speed("fastest")
        self.refresh()

    def refresh(self):
        random_x = random.randint(-280, 280)
        random_y = random.randint(-280, 280)
        self.goto(random_x, random_y)

# Set up the game window
screen = turtle.Screen()
screen.bgcolor("black")
screen.title("Snake Game")
screen.setup(width=600, height=600)
screen.tracer(0)

# Create the snake, food, and scoreboard
snake = Snake()
food = Food()

# Score
score = 0
high_score = 0
delay = 0.1

score_display = turtle.Turtle()
score_display.color("white")
score_display.penup()
score_display.hideturtle()
score_display.goto(0, 260)
score_display.write(f"Score: {score} High Score: {high_score}", align="center", font=("Arial", 24, "normal"))

# Functions
def update_score():
    score_display.clear()
    score_display.write(f"Score: {score} High Score: {high_score}", align="center", font=("Arial", 24, "normal"))

def game_over():
    global score, delay
    score_display.goto(0, 0)
    score_display.color("red")
    score_display.write("GAME OVER", align="center", font=("Arial", 36, "bold"))
    time.sleep(2)
    score_display.goto(0, 260)
    score_display.color("white")
    if score > high_score:
        update_high_score()
    reset_game()

def update_high_score():
    global high_score
    high_score = score

def reset_game():
    global score, delay, running
    score = 0
    delay = 0.1
    snake.reset()
    update_score()
    running = False  # Stop the current loop

# Control handlers
def up():
    snake.up()

def down():
    snake.down()

def left():
    snake.left()

def right():
    snake.right()

def restart():
    global running
    running = True

# Key bindings
screen.listen()
screen.onkey(up, "Up")
screen.onkey(down, "Down")
screen.onkey(left, "Left")
screen.onkey(right, "Right")
screen.onkey(restart, "r")

# Main Game Loop
running = True

while True:
    if running:
        screen.update()
        time.sleep(delay)

        snake.move()

        # Detect collision with food
        if snake.head.distance(food) < 15:
            food.refresh()
            snake.extend()
            score += 10
            update_score()
            if delay > 0.05:
                delay -= 0.005

        # Detect collision with wall
        if (snake.head.xcor() > 290 or snake.head.xcor() < -290 or 
            snake.head.ycor() > 290 or snake.head.ycor() < -290):
            game_over()

        # Detect collision with tail
        for segment in snake.segments[1:]:
            if snake.head.distance(segment) < 10:
                game_over()

    else:
        screen.update()

# Keep the window open
screen.mainloop()
p