import pgzero
import random
from pgzero.actor import Actor

HEIGHT = 655
WIDTH = 800

game_state = "menu"
score = 0

class Player():
    def __init__(self):
        self.actor = Actor('alien')
        self.animations_moving = ['p3_walk01', 'p3_walk02', 'p3_walk03', 'p3_walk04',
                        'p3_walk05', 'p3_walk06', 'p3_walk07', 'p3_walk08',
                        'p3_walk09', 'p3_walk10', 'p3_walk11']
        self.animations_idle = ['alien', 'alienbeige', 'alienblue', 'aliengreen', 'alienpink', 'alienyellow']
        self.is_moving = False
        self.actor.x = 200
        self.actor.y = 480
        self.on_ground = True
        self.vel_y = 0
        self.gravity = 0.8
        self.jump_strength = -18
        self.ground_y = 480
        self.walk_index = 0
        self.anim_timer = 0

    def draw(self):
        self.actor.draw()
      
    def update(self):
        self.is_moving = False
        if keyboard.left:
            self.actor.x -= 5
            self.is_moving = True
        if keyboard.right:
            self.actor.x += 5
            self.is_moving = True

        self.actor.y += self.vel_y
        self.vel_y += self.gravity
        if self.actor.y >= self.ground_y:
            self.actor.y = self.ground_y
            self.vel_y = 0
            self.on_ground = True

        if keyboard.up and self.on_ground:
            self.vel_y = self.jump_strength
            self.on_ground = False

        # Ekran dışına çıkmasın
        if self.actor.x < 50:
            self.actor.x = 50
        if self.actor.x > WIDTH - 50:
            self.actor.x = WIDTH - 50

        self.animation()

    def animation(self):
        self.anim_timer += 1
        if self.anim_timer > 5:
            self.anim_timer = 0
            if not self.on_ground:
                self.actor.image = 'p3_jump'
            elif self.is_moving:
                self.walk_index = (self.walk_index + 1) % len(self.animations_moving)
                self.actor.image = self.animations_moving[self.walk_index]
            else:
                self.actor.image = random.choice(self.animations_idle)


class Enemy():
    def __init__(self, sprite_name, animations, speed):
        self.actor = Actor(sprite_name)
        self.animations = animations
        self.speed = speed
        self.anim_index = 0
        self.anim_timer = 0

    def collide_player(self, player):
       if self.actor.colliderect(player.actor):
            print("Collision detected!")
            return True
       return False
  
    def update(self):
        self.actor.x -= self.speed
        if self.actor.x < 0:
            self.actor.x = WIDTH + random.randint(30, 200)
            if 'fly' in self.animations[0].lower():
                self.actor.y = random.randint(100, HEIGHT - 120)

        self.anim_timer += 1
        if self.anim_timer > 4:
            self.anim_timer = 0
            self.anim_index = (self.anim_index + 1) % len(self.animations)
            self.actor.image = self.animations[self.anim_index]

    def draw(self):
        self.actor.draw()


class Bird(Enemy):
    def __init__(self):
        super().__init__("fly1", ['fly1', 'fly2'], 5)
        self.actor.y = random.randint(100, HEIGHT - 100)


class Slim(Enemy):
    def __init__(self):
        super().__init__("slim1", ['slim1', 'slim2'], 1)   
        self.actor.y = 510


def start_game():
    global game_state, score, player, enemies
    game_state = "playing"
    score = 0
    player = Player()
    enemies = [Bird(), Slim()]


def reset_to_menu():
    global game_state
    game_state = "menu"


player = Player()
enemies = [Bird(), Slim()]
background = Actor('background_1')


def draw():
    if game_state == "playing":
        screen.clear()
        background.draw()
        player.draw()
        for enemy in enemies:
            enemy.draw()
        screen.draw.text(f"Score: {score}", (20, 20), color="white", fontsize=36, shadow=(1,1))
    else:
        screen.fill((15, 15, 35))
        
        if game_state == "menu":
            screen.draw.text("RUNNER", centerx=WIDTH//2, centery=180, color="yellow", fontsize=72, shadow=(3,3))
            screen.draw.text("Press SPACE to Start", centerx=WIDTH//2, centery=320, color="white", fontsize=36)
            screen.draw.text("Arrow Keys to move  |  UP to Jump", centerx=WIDTH//2, centery=400, color="lightblue", fontsize=24)
            screen.draw.text("Survive as long as you can!", centerx=WIDTH//2, centery=460, color="lime", fontsize=22)
        
        elif game_state == "game_over":
            screen.draw.text("GAME OVER", centerx=WIDTH//2, centery=200, color="red", fontsize=68, shadow=(2,2))
            screen.draw.text(f"Your Score: {score}", centerx=WIDTH//2, centery=300, color="white", fontsize=40)
            screen.draw.text("Press R or SPACE to Restart", centerx=WIDTH//2, centery=400, color="yellow", fontsize=28)
            screen.draw.text("Press M to return to Menu", centerx=WIDTH//2, centery=450, color="lightgray", fontsize=22)
        
        elif game_state == "win":
            screen.draw.text("YOU WIN!", centerx=WIDTH//2, centery=200, color="lime", fontsize=72, shadow=(2,2))
            screen.draw.text("Amazing! You survived long enough!", centerx=WIDTH//2, centery=290, color="white", fontsize=32)
            screen.draw.text(f"Final Score: {score}", centerx=WIDTH//2, centery=350, color="yellow", fontsize=36)
            screen.draw.text("Press SPACE to Play Again", centerx=WIDTH//2, centery=430, color="white", fontsize=28)
            screen.draw.text("Press M for Main Menu", centerx=WIDTH//2, centery=480, color="lightgray", fontsize=22)


def update():
    global game_state, score

    if game_state == "playing":
        player.update()
        for e in enemies:
            e.update()
            if e.collide_player(player):
                sounds.eep.play()
                game_state = "game_over"
                return   
        score += 1

        if score >= 2000:
            game_state = "win"

    elif game_state == "menu":
        if keyboard.space:
            start_game()

    elif game_state == "game_over":
        if keyboard.r or keyboard.space:
            start_game()
        if keyboard.m:
            reset_to_menu()

    elif game_state == "win":
        if keyboard.space:
            start_game()
        if keyboard.m:
            reset_to_menu()
