"""
Snake Game
Made with PyGame
"""

import pygame, sys, time, random
import pygame_gui

# 난이도 설정
# Easy      ->  10
# Medium    ->  25
# Hard      ->  40
# Harder    ->  60
# Impossible->  120
difficulty = 25

# 배경 이미지 불러오고 창 크기 설정
background_img = pygame.image.load('background.png')
orig_w, orig_h = background_img.get_width(), background_img.get_height()
frame_size_y = 700
frame_size_x = int(orig_w * (frame_size_y / orig_h))
# 배경 이미지 사이즈가 10단위가 아니라서 10의 배수로 내림
frame_size_x -= frame_size_x % 10
frame_size_y -= frame_size_y % 10
background_img = pygame.transform.smoothscale(background_img, (frame_size_x, frame_size_y))

# 오류 체크
check_errors = pygame.init()
# pygame.init() 예시 출력 -> (6, 0)
# 튜플의 두 번째 숫자가 에러 개수
if check_errors[1] > 0:
    print(f'[!] 초기화 중 {check_errors[1]}개의 에러가 발생하여 종료합니다...')
    sys.exit(-1)
else:
    print('[+] 게임이 성공적으로 초기화되었습니다')

# 게임 창 초기화
pygame.display.set_caption('Snake Game')
game_window = pygame.display.set_mode((frame_size_x, frame_size_y))

# pygame_gui 초기화 (도트 스타일 버튼을 위한 theme.json 필요)
# https://pygame-gui.readthedocs.io/en/latest/index.html 참고
manager = pygame_gui.UIManager((frame_size_x, frame_size_y), 'theme.json')

# 색상 (R, G, B)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)
pink = pygame.Color(255, 192, 203)

# FPS 컨트롤러
fps_controller = pygame.time.Clock()

# 게임 상태
GAME_STATE_MENU = 0    # 시작 화면
GAME_STATE_PLAYING = 1 # 게임 중
GAME_STATE_PAUSED = 2  # 일시정지
GAME_STATE_COUNTDOWN = 3  # 카운트다운
GAME_STATE_GAME_OVER = 4  # 게임 오버
current_state = GAME_STATE_MENU

# 시작 버튼 생성
start_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((frame_size_x//2 - frame_size_x//8, frame_size_y//2), (frame_size_x//4, frame_size_y//12)),
    text='Start Game',
    manager=manager
)

# 일시정지 화면 버튼 생성
resume_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((frame_size_x//2 - frame_size_x//8, frame_size_y//2 + frame_size_y//8), (frame_size_x//4, frame_size_y//12)),
    text='Resume',
    manager=manager
)
resume_button.hide()  # 처음에는 숨김

# 재시작 버튼 생성
restart_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((frame_size_x//2 - frame_size_x//8, frame_size_y//2 + frame_size_y//8), (frame_size_x//4, frame_size_y//12)),
    text='Restart',
    manager=manager
)
restart_button.hide()  # 처음에는 숨김

# 게임 변수
snake_pos = [100, 50]  # 뱀 머리 위치
snake_body = [[100, 50], [90, 50], [80, 50]]  # 뱀 몸통
food_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]  # 먹이 위치
food_spawn = True
direction = 'RIGHT'  # 초기 방향
change_to = direction
score = 0

# 카운트다운 변수
countdown_time = 0
countdown_number = 3

# 게임 변수 리셋 함수
def reset_game():
    global snake_pos, snake_body, food_pos, food_spawn, direction, change_to, score
    snake_pos = [100, 50]
    snake_body = [[100, 50], [90, 50], [80, 50]]
    food_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
    food_spawn = True
    direction = 'RIGHT'
    change_to = direction
    score = 0

# 게임 오버 처리 함수
def game_over():
    global current_state
    current_state = GAME_STATE_GAME_OVER
    start_button.hide()
    resume_button.hide()
    restart_button.show()

# 점수 표시 함수
def show_score(choice, color, font, size):
    score_font = pygame.font.Font('TR.ttf', int(size * 1.2 * frame_size_x / 720))
    score_surface = score_font.render('Score : ' + str(score), True, (0, 0, 0))
    score_rect = score_surface.get_rect()
    if choice == 1:
        score_rect.midtop = (frame_size_x/10, frame_size_y/48)  # 조금 더 위로
    else:
        score_rect.midtop = (frame_size_x/2, frame_size_y/1.25)
    game_window.blit(score_surface, score_rect)

# 시작 화면 그리기 함수
def draw_menu():
    game_window.blit(background_img, (0, 0))
    # 게임 로고
    font = pygame.font.Font('TR.ttf', int(frame_size_x/8))
    logo_surface = font.render('SNAKE GAME', True, green)
    logo_rect = logo_surface.get_rect()
    logo_rect.midtop = (frame_size_x/2, frame_size_y/4)
    game_window.blit(logo_surface, logo_rect)
    start_button.show()
    resume_button.hide()
    restart_button.hide()
    manager.draw_ui(game_window)
    pygame.display.update()

# 일시정지 화면 그리기 함수
def draw_pause_screen():
    game_window.blit(background_img, (0, 0))
    font = pygame.font.Font('TR.ttf', int(frame_size_x/8))
    pause_surface = font.render('PAUSED', True, white)
    pause_rect = pause_surface.get_rect()
    pause_rect.midtop = (frame_size_x/2, frame_size_y/4)
    game_window.blit(pause_surface, pause_rect)
    start_button.hide()
    resume_button.show()
    restart_button.hide()
    manager.draw_ui(game_window)
    pygame.display.update()

# 게임 오버 화면 그리기 함수
def draw_game_over():
    game_window.blit(background_img, (0, 0))
    font = pygame.font.Font('TR.ttf', int(frame_size_x/8))
    game_over_surface = font.render('GAME OVER', True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (frame_size_x/2, frame_size_y/4)
    game_window.blit(game_over_surface, game_over_rect)
    show_score(0, white, 'TR.ttf', 40)
    manager.draw_ui(game_window)
    pygame.display.update()

# 카운트다운 화면 그리기 함수
def draw_countdown():
    game_window.blit(background_img, (0, 0))
    font = pygame.font.Font('TR.ttf', int(frame_size_x/6))
    if countdown_number > 0:
        count_surface = font.render(str(countdown_number), True, white)
    else:
        count_surface = font.render('GO!', True, green)
    count_rect = count_surface.get_rect()
    count_rect.midtop = (frame_size_x/2, frame_size_y/3)
    game_window.blit(count_surface, count_rect)
    pygame.display.update()

# 메인 게임 루프
while True:
    time_delta = fps_controller.tick(60)/1000.0
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if current_state == GAME_STATE_MENU:
            manager.process_events(event)
            
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == start_button:
                    current_state = GAME_STATE_COUNTDOWN
                    countdown_time = time.time()
                    countdown_number = 3
                    reset_game()
                    
        elif current_state == GAME_STATE_PAUSED:
            manager.process_events(event)
            
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == resume_button:
                    current_state = GAME_STATE_COUNTDOWN
                    countdown_time = time.time()
                    countdown_number = 3
                    
        elif current_state == GAME_STATE_GAME_OVER:
            manager.process_events(event)
            
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == restart_button:
                    current_state = GAME_STATE_COUNTDOWN
                    countdown_time = time.time()
                    countdown_number = 3
                    reset_game()
                    
        elif current_state == GAME_STATE_PLAYING:
            # 게임 조작
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == ord('w'):
                    change_to = 'UP'
                if event.key == pygame.K_DOWN or event.key == ord('s'):
                    change_to = 'DOWN'
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    change_to = 'LEFT'
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    change_to = 'RIGHT'
                if event.key == pygame.K_ESCAPE:
                    current_state = GAME_STATE_PAUSED

    if current_state == GAME_STATE_MENU:
        manager.update(time_delta)
        draw_menu()
    elif current_state == GAME_STATE_PAUSED:
        manager.update(time_delta)
        draw_pause_screen()
    elif current_state == GAME_STATE_GAME_OVER:
        manager.update(time_delta)
        draw_game_over()
    elif current_state == GAME_STATE_COUNTDOWN:
        current_time = time.time()
        if current_time - countdown_time >= 1:
            countdown_time = current_time
            countdown_number -= 1
            if countdown_number < 0:
                current_state = GAME_STATE_PLAYING
        draw_countdown()
    elif current_state == GAME_STATE_PLAYING:
        # 반대 방향으로 이동 방지
        if change_to == 'UP' and direction != 'DOWN':
            direction = 'UP'
        if change_to == 'DOWN' and direction != 'UP':
            direction = 'DOWN'
        if change_to == 'LEFT' and direction != 'RIGHT':
            direction = 'LEFT'
        if change_to == 'RIGHT' and direction != 'LEFT':
            direction = 'RIGHT'

        # 뱀 이동
        if direction == 'UP':
            snake_pos[1] -= 10
        if direction == 'DOWN':
            snake_pos[1] += 10
        if direction == 'LEFT':
            snake_pos[0] -= 10
        if direction == 'RIGHT':
            snake_pos[0] += 10

        # 뱀 몸통 증가
        snake_body.insert(0, list(snake_pos))
        if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
            score += 1
            food_spawn = False
        else:
            snake_body.pop()

        # 먹이 생성
        if not food_spawn:
            food_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
        food_spawn = True

        # 그래픽 그리기
        game_window.blit(background_img, (0, 0))
        body_colors = [green, pygame.Color(181, 230, 29)]  # 초록, 연한초록
        for i, pos in enumerate(snake_body):
            color = body_colors[i % 2]
            if i == 0:
                pygame.draw.rect(game_window, color, pygame.Rect(pos[0], pos[1], 10, 10))
                # 머리 방향에 Y자 혀와 눈 그리기
                cx, cy = pos[0]+5, pos[1]+5
                tongue_color = (220, 40, 40)
                if direction == 'UP':
                    tip = (cx, pos[1]-8)
                    left = (cx-3, pos[1]-13)
                    right = (cx+3, pos[1]-13)
                    pygame.draw.line(game_window, tongue_color, (cx, pos[1]), tip, 2)
                    pygame.draw.line(game_window, tongue_color, tip, left, 2)
                    pygame.draw.line(game_window, tongue_color, tip, right, 2)
                    pygame.draw.circle(game_window, (0,0,0), (cx-2, pos[1]+2), 1)
                    pygame.draw.circle(game_window, (0,0,0), (cx+2, pos[1]+2), 1)
                elif direction == 'DOWN':
                    tip = (cx, pos[1]+18)
                    left = (cx-3, pos[1]+23)
                    right = (cx+3, pos[1]+23)
                    pygame.draw.line(game_window, tongue_color, (cx, pos[1]+10), tip, 2)
                    pygame.draw.line(game_window, tongue_color, tip, left, 2)
                    pygame.draw.line(game_window, tongue_color, tip, right, 2)
                    pygame.draw.circle(game_window, (0,0,0), (cx-2, pos[1]+8), 1)
                    pygame.draw.circle(game_window, (0,0,0), (cx+2, pos[1]+8), 1)
                elif direction == 'LEFT':
                    tip = (pos[0]-8, cy)
                    left = (pos[0]-13, cy-3)
                    right = (pos[0]-13, cy+3)
                    pygame.draw.line(game_window, tongue_color, (pos[0], cy), tip, 2)
                    pygame.draw.line(game_window, tongue_color, tip, left, 2)
                    pygame.draw.line(game_window, tongue_color, tip, right, 2)
                    pygame.draw.circle(game_window, (0,0,0), (pos[0]+2, cy-2), 1)
                    pygame.draw.circle(game_window, (0,0,0), (pos[0]+2, cy+2), 1)
                elif direction == 'RIGHT':
                    tip = (pos[0]+18, cy)
                    left = (pos[0]+23, cy-3)
                    right = (pos[0]+23, cy+3)
                    pygame.draw.line(game_window, tongue_color, (pos[0]+10, cy), tip, 2)
                    pygame.draw.line(game_window, tongue_color, tip, left, 2)
                    pygame.draw.line(game_window, tongue_color, tip, right, 2)
                    pygame.draw.circle(game_window, (0,0,0), (pos[0]+8, cy-2), 1)
                    pygame.draw.circle(game_window, (0,0,0), (pos[0]+8, cy+2), 1)
            else:
                pygame.draw.rect(game_window, color, pygame.Rect(pos[0], pos[1], 10, 10))
        pygame.draw.rect(game_window, white, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

        # 게임 오버 조건
        # 창 범위 벗어나면 게임 오버
        if snake_pos[0] < 0 or snake_pos[0] >= frame_size_x:
            game_over()
        if snake_pos[1] < 0 or snake_pos[1] >= frame_size_y:
            game_over()
        # 몸통과 충돌하면 게임 오버
        for block in snake_body[1:]:
            if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
                game_over()

        show_score(1, white, 'TR.ttf', 20)
        pygame.display.update()
        fps_controller.tick(difficulty)
