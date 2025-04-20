import pgzrun
from pygame import Rect

WIDTH, HEIGHT = 800, 400

# Game state
is_sound_muted = False
game_started = False
is_menu = True
is_facing_right =  True

# Texts
start_text, sound_text, exit_text = "Start Adventure", "SOUND: MUTED", "EXIT"

# Buttons
title_button = Rect(WIDTH // 2 - 150, HEIGHT // 3 - 30, 300, 60)
sound_button = Rect(WIDTH // 2 - 100, HEIGHT // 2 + 70, 200, 60)
exit_button = Rect(WIDTH // 2 - 100, HEIGHT // 2 + 140, 200, 60)

# Player and objects
hero = Actor("hero_right", pos=(-100, -100))
plate = Actor("plate", pos=(-200, -100))

# Platforms
platforms = [
    Actor("platform", pos=(30, 390)),
    Actor("platform", pos=(100, 390)),
    Actor("platform", pos=(130, 390)),
    Actor("platform", pos=(345, 330)),
    Actor("platform", pos=(420, 330)),
    Actor("platform", pos=(480, 330)),
    Actor("platform", pos=(90, 150)),
    Actor("platform", pos=(70, 150)),
    Actor("platform", pos=(30, 150)),
]


# Zombie
zombie = Actor("zombie_idle_0", pos=(500, 240))
zombie_anim_index, zombie_anim_timer, zombie_anim_interval = 0, 0, 0.4

# Physics
gravity, vertical_speed, horizontal_speed, jump_impulse = 1, 0, 4, -15
on_ground = False

# Sounds
walk_sound = sounds.load("walking.ogg")
jump_sound = sounds.load("jump.ogg")
ambient_sound = sounds.load("ambient.ogg")

# Volume settings
walk_sound.set_volume(0.1)
jump_sound.set_volume(5.0)
ambient_sound.set_volume(0.5)
ambient_sound.play()

# Draw function
def draw():
    screen.clear()
    screen.blit("world", (0, 0))

    if not game_started:
        screen.draw.text(start_text, center=title_button.center, fontsize=50, color="black")
        screen.draw.text(sound_text, center=sound_button.center, fontsize=40, color="blue")
        screen.draw.text(exit_text, center=exit_button.center, fontsize=40, color="red")
    else:
        hero.draw()
        plate.draw()
        for platform in platforms:
            platform.draw()
        zombie.draw()

# Update function
def update():
    global vertical_speed, on_ground, zombie_anim_timer, zombie_anim_index, is_facing_right

    if game_started:
        if keyboard.left or keyboard.a:
            hero.x -= horizontal_speed
            if is_facing_right:
                hero.image = "hero_left"
                is_facing_right = False
            if not is_sound_muted:
                walk_sound.play()

        if keyboard.right or keyboard.d:
            hero.x += horizontal_speed
            if not is_facing_right:
                hero.image = "hero_right"
                is_facing_right = True
            if not is_sound_muted:
                walk_sound.play()

        hero.x = max(hero.width // 2, min(WIDTH - hero.width // 2, hero.x))

        # Gravity
        if not on_ground:
            vertical_speed += gravity
            hero.y += vertical_speed

        # Jumping
        if keyboard.space and on_ground:
            vertical_speed = jump_impulse
            on_ground = False
            if not is_sound_muted:
                jump_sound.play()

        on_ground = False
        for platform in platforms:
            if hero.colliderect(platform) and vertical_speed >= 0:
                hero.y = platform.top - hero.height // 2
                vertical_speed = 0
                on_ground = True
                break

            if hero.colliderect(platform) and vertical_speed < 0:
                hero.y = platform.bottom + hero.height // 2
                vertical_speed = 0

        if hero.colliderect(plate):
            restart_game()

        if hero.y > HEIGHT + 100:
            respawn()

        # Zombie animation
        zombie_anim_timer += 1 / 60
        if zombie_anim_timer >= zombie_anim_interval:
            zombie_anim_timer = 0
            zombie_anim_index = (zombie_anim_index + 1) % 2
            zombie.image = f"zombie_idle_{zombie_anim_index}"

        # Collision with zombie
        if hero.colliderect(zombie):
            hero.pos = (-100, -100)
            clock.schedule_unique(restart_game, 2.0)

# Restart
def restart_game():
    global game_started, is_menu
    game_started, is_menu = False, True
    hero.pos = (-100, -100)

# Respawn player
def respawn():
    global is_menu
    is_menu = False
    hero.pos = (100, 390)
    plate.pos = (40, 70)

# Close
def close_game():
    raise SystemExit

# Click 
def on_mouse_down(pos):
    global is_sound_muted, sound_text, game_started

    if not is_menu:
        return

    if sound_button.collidepoint(pos):
        is_sound_muted = not is_sound_muted
        sound_text = "SOUND: MUTED" if is_sound_muted else "SOUND: UNMUTED"
        if is_sound_muted:
            ambient_sound.stop()
        else:
            ambient_sound.play(loops=-1, fade_ms=1000)

    if title_button.collidepoint(pos):
        game_started = True
        respawn()

    if exit_button.collidepoint(pos):
        close_game()

pgzrun.go()
