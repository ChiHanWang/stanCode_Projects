"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman, 
and Jerry Liao.

This program plays a game called
"break out" in which players
moving the paddle to make the ball bounce
and break all bricks!
"""
# coder端

from campy.graphics.gwindow import GWindow
from campy.graphics.gobjects import GOval, GRect, GLabel
from campy.gui.events.mouse import onmouseclicked, onmousemoved
import random

BRICK_SPACING = 5      # Space between bricks (in pixels). This space is used for horizontal and vertical spacing
BRICK_WIDTH = 40       # Width of a brick (in pixels)
BRICK_HEIGHT = 15      # Height of a brick (in pixels)
BRICK_ROWS = 10        # Number of rows of bricks
BRICK_COLS = 10        # Number of columns of bricks
BRICK_OFFSET = 50      # Vertical offset of the topmost brick from the window top (in pixels)
BALL_RADIUS = 10       # Radius of the ball (in pixels)
PADDLE_WIDTH = 75      # Width of the paddle (in pixels)
PADDLE_HEIGHT = 15     # Height of the paddle (in pixels)
PADDLE_OFFSET = 50     # Vertical offset of the paddle from the window bottom (in pixels)
INITIAL_Y_SPEED = 7    # Initial vertical speed for the ball
MAX_X_SPEED = 5        # Maximum initial horizontal speed for the ball
BRICK_COLOR_TYPE_NUM = 5  # Number of different colors' type


class BreakoutGraphics:

    def __init__(self, ball_radius=BALL_RADIUS, paddle_width=PADDLE_WIDTH, paddle_height=PADDLE_HEIGHT,
                 paddle_offset=PADDLE_OFFSET, brick_rows=BRICK_ROWS, brick_cols=BRICK_COLS, brick_width=BRICK_WIDTH,
                 brick_height=BRICK_HEIGHT, brick_offset=BRICK_OFFSET, brick_spacing=BRICK_SPACING, title='Breakout'):

        # Create a graphical window, with some extra space
        window_width = brick_cols * (brick_width + brick_spacing) - brick_spacing
        window_height = brick_offset + 3 * (brick_rows * (brick_height + brick_spacing) - brick_spacing)
        self.window = GWindow(width=window_width, height=window_height, title=title)

        # Create a paddle
        self.paddle = GRect(paddle_width, paddle_height)
        self.paddle.filled = True
        self.paddle.fill_color = 'black'
        self.paddle.color = 'black'
        self.window.add(self.paddle, x=(self.window.width-paddle_width)/2,
                        y=self.window.height-paddle_offset-paddle_height)

        # Center a filled ball in the graphical window
        self.ball = GOval(ball_radius*2, ball_radius*2)
        self.b_r = ball_radius
        self.ball.filled = True
        self.ball.fill_color = 'black'
        self.ball.color = 'black'
        self.window.add(self.ball, x=self.window.width / 2 - self.b_r,
                        y=self.window.height / 2 - self.b_r)

        # Draw bricks，create list_b[] and list_color[]
        self.bs = BRICK_SPACING
        self.b_n = brick_rows * brick_cols       # Number of bricks in the window
        mod = brick_rows % BRICK_COLOR_TYPE_NUM  # 有幾種顏色的磚塊要比別人多一列, 並且由最後一列往上遞增
        q = brick_rows // BRICK_COLOR_TYPE_NUM   # 每一種顏色最少要有q列
        list_b = []                              # 空list用來裝q

        for i in range(BRICK_COLOR_TYPE_NUM):
            list_b.append(q)

        a = 4                                    # 當作index使用, 多餘的列數會由最後一列往上平均遞增
        while (mod > 0):                         # 跑完while (mod>0)後, list_b就是每一種顏色要有幾列
            mod -= 1
            list_b[a] += 1
            a -= 1                               # index of next: 取前一個元素，index-1

        list_color = []                          # 存放呈現在window上每一列的顏色
        color_type = ['red', 'orange', 'yellow', 'green', 'blue']

        a = 0                                    # 當作index使用, 用來取list_b的值跟color_type的顏色
        while brick_rows != len(list_color):     # list_color裡面的數量必須等於磚塊的列數才行
            if list_b[a] != 0:                   # 根據list_b的值建構從第一列到最後一列的顏色list
                list_color.append(color_type[a])
                list_b[a] -= 1
                if list_b[a] == 0:
                    a += 1
            else:                                # 當brick_rows小於BRICK_COLOR_TYPE_NUM, list_b中的element會有0
                a += 1                           # 遇到0就跳到下一個element去檢查

        for i in range(brick_rows):
            for j in range(brick_cols):
                self.brick = GRect(brick_width, brick_height)
                self.brick.filled = True
                self.brick.fill_color = list_color[i]
                self.brick.color = list_color[i]  # 邊框顏色
                self.window.add(self.brick, x=(brick_width + brick_spacing) * j,
                                y=(brick_offset + (brick_height + brick_spacing) * i))

        # Default initial velocity for the ball
        self.ball.__dx = 0
        self.ball.__dy = 0

        # Initialize our mouse listeners
        onmousemoved(self.moving)
        onmouseclicked(self.click)
        self.isclicked = False

    def get_dx(self):
        return self.ball.__dx

    # Animation for the ball
    def click(self, _):
        if not self.isclicked:
            self.ball.__dx = random.randint(1, MAX_X_SPEED)
            if (random.random() > 0.5):
                self.ball.__dx = -self.ball.__dx
            if self.ball.y + self.ball.height <= self.window.height:
                self.ball.__dy = INITIAL_Y_SPEED
        self.isclicked = True

    def get_dy(self):
        return self.ball.__dy

    # Animation for the paddle
    # 游標會在箭頭正中間
    def moving(self, mouse):
        if self.paddle.width/2 < mouse.x < self.window.width - self.paddle.width/2:
            self.paddle.x = mouse.x - self.paddle.width/2

    def reset_position(self):
        """
        back to the original position
        """
        self.ball.x = self.window.width / 2 - self.b_r
        self.ball.y = self.window.height / 2 - self.b_r
        self.ball.__dx = 0
        self.ball.__dy = 0
        self.isclicked = False

    # 可更改球的y速度
    def set_vy(self, num):
        self.ball.__dy *= num
        return self.ball.__dy