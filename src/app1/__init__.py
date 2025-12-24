import platform
import os
import sys
import numpy as np

DISPLAY_MODE = None
display_module = None

def _detect_display_mode():
    global DISPLAY_MODE, display_module
    if os.uname().nodename == 'raspberrypi':
        try:
            import pi0disp
            DISPLAY_MODE = 'PI0DISP'
            display_module = pi0disp.ST7789V # ドライバクラスを代入
        except ImportError:
            import cv2
            DISPLAY_MODE = 'OPENCV'
            display_module = cv2
    else:
        import cv2
        DISPLAY_MODE = 'OPENCV'
        display_module = cv2

# _detect_display_mode() # この行を削除

class Display:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        if DISPLAY_MODE == 'PI0DISP':
            self.display = display_module() # ドライバクラスのインスタンスを作成
            self.display.clear()
        else:
            display_module.namedWindow("app1", display_module.WINDOW_NORMAL)
            self.frame = None

    def clear(self, color=(0, 0, 0)): # color引数を追加、デフォルトは黒
        if DISPLAY_MODE == 'PI0DISP':
            self.display.clear(color) # pi0dispもcolor引数を受け取ると仮定
        else:
            # OpenCVの場合、指定した色でフレームを塗りつぶす
            self.frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
            self.frame[:, :, 0] = color[0] # Blue
            self.frame[:, :, 1] = color[1] # Green
            self.frame[:, :, 2] = color[2] # Red
            display_module.imshow("app1", self.frame)
            display_module.waitKey(1) # Refresh window

    def draw_rect(self, x, y, width, height, color):
        if DISPLAY_MODE == 'PI0DISP':
            self.display.draw_rect(x, y, width, height, color)
        else:
            # OpenCVの場合、フレームに矩形を描画
            # OpenCVはBGR形式なので、colorもBGRで渡す必要がある
            # ここではcolorがRGB形式であると仮定し、BGRに変換
            display_module.rectangle(self.frame, (x, y), (x + width, y + height), color[::-1], -1)
            display_module.imshow("app1", self.frame)
            display_module.waitKey(1)


    def __del__(self):
        if DISPLAY_MODE == 'PI0DISP':
            self.display.exit()
        else:
            display_module.destroyAllWindows()

def main() -> None:
    _detect_display_mode() # ここに移動
    assert display_module is not None # mypyのために追加
    
    # Constants for screen and object sizes
    SCREEN_WIDTH = 640
    SCREEN_HEIGHT = 480
    PADDLE_WIDTH = 80
    PADDLE_HEIGHT = 10
    BALL_RADIUS = 5
    BLOCK_WIDTH = 50
    BLOCK_HEIGHT = 20
    
    display = Display(SCREEN_WIDTH, SCREEN_HEIGHT)
    display.clear()
    
    # Draw Paddle (bottom center)
    paddle_x = (SCREEN_WIDTH - PADDLE_WIDTH) // 2
    paddle_y = SCREEN_HEIGHT - PADDLE_HEIGHT - 10
    display.draw_rect(paddle_x, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT, (255, 255, 255)) # White
    
    # Draw Ball (above paddle)
    ball_x = SCREEN_WIDTH // 2
    ball_y = paddle_y - BALL_RADIUS - 5
    display.draw_rect(ball_x - BALL_RADIUS, ball_y - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2, (255, 255, 255)) # White
    
    # Draw some Blocks (top area)
    block_rows = 3
    block_cols = 5
    for r in range(block_rows):
        for c in range(block_cols):
            block_x = 50 + c * (BLOCK_WIDTH + 10)
            block_y = 50 + r * (BLOCK_HEIGHT + 10)
            display.draw_rect(block_x, block_y, BLOCK_WIDTH, BLOCK_HEIGHT, (0, 255, 0)) # Green

    print("Hello from app1!")
    # Keep the window open for a short period on PC
    if DISPLAY_MODE == 'OPENCV':
        display_module.waitKey(2000)
