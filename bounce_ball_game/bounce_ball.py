import tkinter as tk
import time
import random

class Ball:
    def __init__(self, canvas, paddle, color):
        self.canvas = canvas
        self.paddle = paddle
        self.color = color
        self.id = None # Will be created later
        self.x = 0
        self.y = 0
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()

    def create_visual(self):
        self.id = self.canvas.create_oval(10, 10, 25, 25, fill=self.color)
        self.canvas.move(self.id, 245, 100)
        starts = [-3, -2, -1, 1, 2, 3]
        random.shuffle(starts)
        self.x = starts[0]
        self.y = -3

    def hit_paddle(self, pos):
        paddle_pos = self.canvas.coords(self.paddle.id)
        if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
            if pos[3] >= paddle_pos[1] and pos[3] <= paddle_pos[3]:
                return True
        return False

    def draw(self):
        self.canvas.move(self.id, self.x, self.y)
        pos = self.canvas.coords(self.id)
        if pos[1] <= 0:
            self.y = 3
        if pos[3] >= self.canvas_height:
            return True  # Ball hit bottom
        if pos[0] <= 0:
            self.x = 3
        if pos[2] >= self.canvas_width:
            self.x = -3
        if self.hit_paddle(pos) == True:
            self.y = -3
        return False # Ball did not hit bottom

class Paddle:
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.color = color
        self.original_width = 100
        self.current_width = self.original_width
        self.original_speed = 2
        self.current_speed = self.original_speed
        self.id = None # Will be created later

        self.canvas_width = self.canvas.winfo_width()
        
        self.moving_left = False
        self.moving_right = False

        self.canvas.bind_all('<KeyPress-Left>', self.start_move_left)
        self.canvas.bind_all('<KeyRelease-Left>', self.stop_move_left)
        self.canvas.bind_all('<KeyPress-Right>', self.start_move_right)
        self.canvas.bind_all('<KeyRelease-Right>', self.stop_move_right)

    def create_visual(self):
        self.id = self.canvas.create_rectangle(0, 0, self.current_width, 10, fill=self.color)
        self.canvas.move(self.id, 200, 300)

    def draw(self):
        dx = 0
        if self.moving_left:
            dx = -self.current_speed
        elif self.moving_right:
            dx = self.current_speed

        self.canvas.move(self.id, dx, 0)
        pos = self.canvas.coords(self.id)
        
        # Boundary checks
        if pos[0] < 0:
            self.canvas.coords(self.id, 0, pos[1], self.current_width, pos[3])
        elif pos[2] > self.canvas_width:
            self.canvas.coords(self.id, self.canvas_width - self.current_width, pos[1], self.canvas_width, pos[3])

    def start_move_left(self, evt):
        self.moving_left = True

    def stop_move_left(self, evt):
        self.moving_left = False

    def start_move_right(self, evt):
        self.moving_right = True

    def stop_move_right(self, evt):
        self.moving_right = False

    def change_width(self, factor):
        current_pos = self.canvas.coords(self.id)
        center_x = (current_pos[0] + current_pos[2]) / 2
        new_width = self.current_width * factor
        
        min_width = 50
        max_width = 200
        new_width = max(min_width, min(max_width, new_width))

        self.current_width = new_width
        
        new_x1 = center_x - (new_width / 2)
        new_x2 = center_x + (new_width / 2)

        self.canvas.coords(self.id, new_x1, current_pos[1], new_x2, current_pos[3])

    def change_speed(self, factor):
        self.current_speed *= factor
        min_speed = 1
        max_speed = 5
        self.current_speed = max(min_speed, min(max_speed, self.current_speed))

class Item:
    def __init__(self, canvas, item_type, color):
        self.canvas = canvas
        self.item_type = item_type
        self.color = color
        self.speed = 1 
        self.id = None
        self.create_item()

    def create_item(self):
        x_start = random.randint(50, self.canvas.winfo_width() - 50)
        self.id = self.canvas.create_rectangle(x_start, 0, x_start + 20, 20, fill=self.color)

    def draw(self):
        self.canvas.move(self.id, 0, self.speed)
        pos = self.canvas.coords(self.id)
        if pos[3] >= self.canvas.winfo_height(): 
            self.canvas.delete(self.id)
            return True 
        return False

    def check_collision(self, paddle_id):
        item_pos = self.canvas.coords(self.id)
        paddle_pos = self.canvas.coords(paddle_id)

        if item_pos and paddle_pos: 
            if (item_pos[2] >= paddle_pos[0] and 
                item_pos[0] <= paddle_pos[2] and 
                item_pos[3] >= paddle_pos[1] and 
                item_pos[1] <= paddle_pos[3]):   
                return True
        return False

class Game:
    def __init__(self):
        self.tk = tk.Tk()
        self.tk.title("Bounce Ball Game")
        self.tk.resizable(0, 0)
        self.tk.wm_attributes("-topmost", 1)
        self.canvas = tk.Canvas(self.tk, width=500, height=400, bd=0, highlightthickness=0)
        self.canvas.pack()
        self.tk.update()

        self.paddle = Paddle(self.canvas, 'blue')
        self.balls = []
        self.game_over_text_id = None
        self.play_again_text_id = None
        self.yes_button_id = None
        self.no_button_id = None
        self.yes_text_id = None
        self.no_text_id = None

        self.items = []
        self.item_drop_counter = 0
        self.item_drop_frequency = 100 
        self.game_running = False # Game starts as not running

        self.item_types = {
            "wider_paddle": {"color": "green", "effect": "width", "factor": 1.2},
            "smaller_paddle": {"color": "orange", "effect": "width", "factor": 0.8},
            "faster_paddle": {"color": "purple", "effect": "speed", "factor": 1.5},
            "slower_paddle": {"color": "brown", "effect": "speed", "factor": 0.7},
            "add_ball": {"color": "cyan", "effect": "add_ball"}
        }

    def show_start_screen(self):
        self.canvas.delete("all") # Clear previous elements
        self.canvas.create_text(250, 150, text="Bounce Ball Game", font=('Helvetica', 30), fill='blue')

        # Start Game button
        self.start_button_id = self.canvas.create_rectangle(175, 220, 325, 260, fill="green", outline="")
        self.start_text_id = self.canvas.create_text(250, 240, text="Start Game", fill="white", font=('Helvetica', 15))
        self.canvas.tag_bind(self.start_button_id, '<Button-1>', self.on_start_game_click)
        self.canvas.tag_bind(self.start_text_id, '<Button-1>', self.on_start_game_click)

        # Exit button
        self.exit_button_id = self.canvas.create_rectangle(175, 270, 325, 310, fill="red", outline="")
        self.exit_text_id = self.canvas.create_text(250, 290, text="Exit", fill="white", font=('Helvetica', 15))
        self.canvas.tag_bind(self.exit_button_id, '<Button-1>', self.on_exit_click)
        self.canvas.tag_bind(self.exit_text_id, '<Button-1>', self.on_exit_click)

        self.tk.mainloop()

    def on_start_game_click(self, event):
        self.canvas.delete("all") # Clear all start screen elements
        self.game_running = True
        
        self.paddle.create_visual()
        
        new_ball = Ball(self.canvas, self.paddle, 'red')
        new_ball.create_visual()
        self.balls.append(new_ball)

        self.game_loop()

    def on_exit_click(self, event):
        self.tk.destroy()

    def reset_game(self):
        if self.game_over_text_id:
            self.canvas.delete(self.game_over_text_id)
            self.canvas.delete(self.play_again_text_id)
            self.canvas.delete(self.yes_button_id)
            self.canvas.delete(self.no_button_id)
            self.canvas.delete(self.yes_text_id)
            self.canvas.delete(self.no_text_id)
            self.game_over_text_id = None
            self.play_again_text_id = None
            self.yes_button_id = None
            self.no_button_id = None
            self.yes_text_id = None
            self.no_text_id = None

        for ball in self.balls:
            self.canvas.delete(ball.id)
        self.balls = []
        
        self.canvas.delete(self.paddle.id) # Delete old paddle visual
        self.paddle = Paddle(self.canvas, 'blue') # Recreate paddle object
        self.paddle.create_visual() # Create new paddle visual

        new_ball = Ball(self.canvas, self.paddle, 'red')
        new_ball.create_visual()
        self.balls.append(new_ball)

        for item in self.items:
            self.canvas.delete(item.id)
        self.items = []
        self.item_drop_counter = 0
        
        self.paddle.current_width = self.paddle.original_width
        self.paddle.current_speed = self.paddle.original_speed
        self.paddle.x = 0
        
        self.game_running = True
        self.game_loop()

    def game_over(self):
        self.game_running = False
        self.game_over_text_id = self.canvas.create_text(250, 150, text="GAME OVER", font=('Helvetica', 30), fill='red')
        self.play_again_text_id = self.canvas.create_text(250, 200, text="Play again?", font=('Helvetica', 15), fill='black')

        # Yes button
        self.yes_button_id = self.canvas.create_rectangle(200, 230, 240, 260, fill="green", outline="")
        self.yes_text_id = self.canvas.create_text(220, 245, text="Yes", fill="white")
        self.canvas.tag_bind(self.yes_button_id, '<Button-1>', self.on_yes_click)
        self.canvas.tag_bind(self.yes_text_id, '<Button-1>', self.on_yes_click)

        # No button
        self.no_button_id = self.canvas.create_rectangle(260, 230, 300, 260, fill="red", outline="")
        self.no_text_id = self.canvas.create_text(280, 245, text="No", fill="white")
        self.canvas.tag_bind(self.no_button_id, '<Button-1>', self.on_no_click)
        self.canvas.tag_bind(self.no_text_id, '<Button-1>', self.on_no_click)

    def on_yes_click(self, event):
        self.reset_game()

    def on_no_click(self, event):
        self.tk.destroy()

    def apply_item_effect(self, item):
        item_info = self.item_types[item.item_type]
        effect_type = item_info["effect"]

        if effect_type == "width":
            self.paddle.change_width(item_info["factor"])
        elif effect_type == "speed":
            self.paddle.change_speed(item_info["factor"])
        elif effect_type == "add_ball":
            new_ball = Ball(self.canvas, self.paddle, 'red')
            new_ball.create_visual()
            self.balls.append(new_ball)

    def game_loop(self):
        if self.game_running:
            balls_to_remove = []
            for ball in self.balls:
                if ball.draw(): # If ball hits bottom
                    self.canvas.delete(ball.id)
                    balls_to_remove.append(ball)
            
            for ball in balls_to_remove:
                self.balls.remove(ball)

            if not self.balls: # If all balls are gone, it's game over
                self.game_over()
                return # Stop the loop here

            self.paddle.draw()

            self.item_drop_counter += 1
            if self.item_drop_counter >= self.item_drop_frequency:
                self.item_drop_counter = 0
                item_name = random.choice(list(self.item_types.keys()))
                item_info = self.item_types[item_name]
                new_item = Item(self.canvas, item_name, item_info["color"])
                self.items.append(new_item)

            items_to_remove = []
            for item in self.items:
                if item.draw(): 
                    items_to_remove.append(item)
                elif item.check_collision(self.paddle.id):
                    self.apply_item_effect(item)
                    self.canvas.delete(item.id)
                    items_to_remove.append(item)

            for item in items_to_remove:
                if item in self.items: 
                    self.items.remove(item)

            self.tk.update_idletasks()
            self.tk.update()
        
        self.tk.after(10, self.game_loop) # Call game_loop again after 10ms

    def start(self):
        self.show_start_screen()

if __name__ == '__main__':
    game = Game()
    game.start()