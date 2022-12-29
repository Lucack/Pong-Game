import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty,StringProperty
from kivy.vector import Vector
from kivy.clock import Clock
import random
import time
from kivy import platform,Config
if platform != 'android':
    Config.set('graphics', 'resizable', False)

class Paddle(Widget):

    score = NumericProperty(0)

class Ball(Widget):
    
    start = ['-7dp','7dp']
    velocity_x = NumericProperty(random.choice(start))
    velocity_y = NumericProperty(random.choice(start))
    velocity = ReferenceListProperty(velocity_x,velocity_y)
        
    def move(self):
        self.pos = Vector(self.velocity) + self.pos

class Game(Widget):
    
    ball = ObjectProperty(Ball())
    player1 = ObjectProperty(Paddle())
    player2 = ObjectProperty(Paddle())
    text = StringProperty()
    start = ['-7dp','7dp']
    vx = random.choice(start)
    vy=random.choice(start)
    global vel
    vel = [vx,vy]
    global restart
    restart = False

    def serve_ball(self):
    
        start = ['-7dp','7dp']
        vx = random.choice(start)
        vy=random.choice(start)
        global vel
        vel = [vx,vy]
        self.ball.center = self.center
        self.ball.velocity = vel
        restart = True        
        

    def update(self,event):
        self.ball.move()

        if (self.ball.y < self.y) or (self.ball.top > self.top):
            self.ball.velocity_y *= -1
        
            # ball and player 1
        if ((self.ball.center_x-(self.ball.width/2) < (self.player1.center_x+(self.player1.width/2))) and (self.ball.center_x-(self.ball.width/2) > self.player1.center_x+(self.player1.width/4)))  and ((self.ball.center_y-self.ball.height/2 < self.player1.center_y+self.player1.height/2 and self.ball.center_y+self.ball.height/2 > self.player1.center_y-self.player1.height/2)):
            self.ball.velocity_x *= -1
            if (self.ball.velocity_y < 0 and self.ball.velocity_x < 0 and self.ball.center_y > self.player1.center_y) and (self.ball.center_y-(self.ball.height/2) < self.player1.center_y + self.player1.height/2):
                self.ball.velocity_y *= -1
            if (self.ball.velocity_y > 0 and self.ball.velocity_x < 0 and self.ball.center_y < self.player1.center_y) and (self.ball.center_y+(self.ball.height/2) > self.player1.center_y - self.player1.height/2):
                self.ball.velocity_y *= -1
        

        if (self.ball.velocity_y < 0 and self.ball.velocity_x < 0 and self.ball.center_y > self.player1.center_y and self.ball.center_x-self.ball.width/2 < self.player1.center_x+self.player1.width/2) and (self.ball.center_y-(self.ball.height/2) < self.player1.center_y + self.player1.height/2):
            self.ball.velocity_y *= -1
        if (self.ball.velocity_y > 0 and self.ball.velocity_x < 0 and self.ball.center_y < self.player1.center_y and self.ball.center_x-self.ball.width/2 < self.player1.center_x+self.player1.width/2) and (self.ball.center_y+(self.ball.height/2) > self.player1.center_y - self.player1.height/2):
            self.ball.velocity_y *= -1
        
            # self.ball.velocity_x *= -1

            # ball and player 2
        if ((self.ball.center_x+(self.ball.width/2) > (self.player2.center_x-(self.player2.width/2))) and (self.ball.center_x+(self.ball.width/2) < self.player2.center_x-(self.player2.width/4))) and (self.ball.center_y-self.ball.height/2 < self.player2.center_y+self.player2.height/2 and self.ball.center_y+self.ball.height/2 > self.player2.center_y-self.player2.height/2):
            self.ball.velocity_x *= -1
            if (self.ball.velocity_y < 0 and self.ball.velocity_x > 0 and self.ball.center_y > self.player2.center_y) and (self.ball.center_y-(self.ball.height/2) < self.player2.center_y + self.player2.height/2):
                self.ball.velocity_y *= -1
            if (self.ball.velocity_y > 0 and self.ball.velocity_x > 0 and self.ball.center_y < self.player2.center_y) and (self.ball.center_y+(self.ball.height/2) > self.player2.center_y - self.player2.height/2):
                self.ball.velocity_y *= -1
        
        if (self.ball.velocity_y < 0 and self.ball.velocity_x > 0 and self.ball.center_y > self.player2.center_y and self.ball.center_x+(self.ball.width/2) > self.player2.center_x-(self.player2.width/2)) and (self.ball.center_y-(self.ball.height/2) < self.player2.center_y + self.player2.height/2):
            self.ball.velocity_y *= -1
        if (self.ball.velocity_y > 0 and self.ball.velocity_x > 0 and self.ball.center_y < self.player2.center_y and self.ball.center_x+(self.ball.width/2) > self.player2.center_x-(self.player2.width/2)) and (self.ball.center_y+(self.ball.height/2) > self.player2.center_y - self.player2.height/2):
            self.ball.velocity_y *= -1

        if self.ball.x < self.x:
            self.player2.score += 1
            counter()
            self.serve_ball()
            
        if self.ball.right > self.width:
            self.player1.score += 1
            counter()
            self.serve_ball()
    
    def on_touch_move(self, touch):
        if touch.x < self.width/3:
            self.player1.center_y = touch.y
        if touch.x > self.width - self.width/3:
            self.player2.center_y = touch.y

def counter():
    t0 = time.time()
    t = time.time()
    global count
    count = int(t-t0)
    times = [0,1]
    c=-1
    while count <= 1:
        t = time.time()
        count = int(t-t0)
        if count in times:
            if count !=c:
                #print(count)
                c=count

class MainApp(App):

    def build(self):
        game = Game()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0/60.0)
        return game

MainApp().run()
# buildozer android debug deploy run