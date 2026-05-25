import tkinter as tk
import random

class ShieldGame:
   def_init_(self,root)
self.root=root
self.root.title("シールド＆パドルゲーム")
self.root.geometry("600×700")
self.root.resizable(False, False)

      # ゲーム状態
self.score=0
self.high_score=0
self.game_over=False

      #  速度設定
self.ball_dx=5
self.ball_dy=-5

      # --- 画面上部：スコア表示エリア ---
self.top_frame=tk.Frame(root, bg="black", height=100)
self.top_frame.pack(fill=tk.X)
self.top_frame.pack_propagate(False)
    
self.score_label=tk.Label(
self.top_frame,
           text =f"SCORE: {self.score} /  BEST: {self.high_score}",
           font=("Arial", 24, "bold"),
           fg=" lime",
           bg="black"
      )
self.score_label.pack(expand=True)
      
       # --- 画面中部～下部 : ゲーム画面 (キャンパス)　---
self.canvas= tk.Canvas(root, bg="#111122", width=600,height=600, highlightthickness=0)
self.canvas.pack()
    
       # 各オブジェクトの作成
self.ball=self.canvas.create_oval(290,290,310,310,fill="yellow") #ボール
self.paddle=self.canvas.create_rectangle(250,560,350,575, fill="cyan") # パドル
self.shield=self.canvas.create_rectangle(250, 300, 350, 315, fill="red") # 邪魔シールド
# シールドの移動速度
self.shield_dx = 3

        # 操作バインド（マウスの動きでパドルを操作）
self.canvas.bind("<Motion>", self.move_paddle)
        
        # クリックで再スタート
self.canvas.bind("<Button-1>", self.restart_game)

        # ゲームループ開始self.update()

def move_paddle(self, event):
        """マウスの位置に合わせてパドルを動かす（画面内に収める）"""
        if self.game_over:
            return
        x = event.x
        if x < 50: x = 50
        if x > 550: x = 550
        self.canvas.coords(self.paddle, x - 50, 560, x + 50, 575)

def update(self):
        """ゲームのメインループ（座標更新と衝突判定）"""
        if self.game_over:
            return

        # 1. ボールの移動
        self.canvas.move(self.ball, self.ball_dx, self.ball_dy)
        ball_pos = self.canvas.coords(self.ball)

        # 2. 壁との衝突判定（左右・天井）
        if ball_pos[0] <= 0 or ball_pos[2] >= 600:
            self.ball_dx *= -1
        if ball_pos[1] <= 0:
            self.ball_dy *= -1

        # 3. ゲームオーバー判定（床に落ちた場合）
        if ball_pos[3] >= 600:
            self.end_game()
            return

        # 4. プレイヤーパドルとの衝突判定
        paddle_pos = self.canvas.coords(self.paddle)
        if (ball_pos[3] >= paddle_pos[1] and ball_pos[1] <= paddle_pos[3] and
            ball_pos[2] >= paddle_pos[0] and ball_pos[0] <= paddle_pos[2]):
            if self.ball_dy > 0: # 下降中のみ跳ね返る
                self.ball_dy *= -1
                self.score += 10
                self.score_label.config(text=f"SCORE: {self.score}  /  BEST: {self.high_score}")
                # スコアに応じて少し加速
                self.ball_dx += 0.5 if self.ball_dx > 0 else -0.5
                self.ball_dy -= 0.5

        # 5. 邪魔シールドの移動と衝突判定
        self.canvas.move(self.shield, self.shield_dx, 0)
        shield_pos = self.canvas.coords(self.shield)
        
        # シールドの左右跳ね返り
        if shield_pos[0] <= 0 or shield_pos[2] >= 600:
            self.shield_dx *= -1

        # ボールがシールド（赤）に当たったらパドル同様に跳ね返る（プレイヤーを邪魔する）
        if (ball_pos[3] >= shield_pos[1] and ball_pos[1] <= shield_pos[3] and
            ball_pos[2] >= shield_pos[0] and ball_pos[0] <= shield_pos[2]):
            self.ball_dy *= -1
            # 貫通を防ぐために位置を微調整
            if self.ball_dy > 0:
                self.canvas.move(self.ball, 0, 5)
            else:
                self.canvas.move(self.ball, 0, -5)

        # 16ミリ秒（約60FPS）ごとに再帰呼び出し
        self.root.after(16, self.update)

def end_game(self):
        """ゲームオーバー処理"""
        self.game_over = True
        if self.score > self.high_score:
            self.high_score = self.score
        
        self.score_label.config(text=f"GAME OVER (SCORE: {self.score}) / BEST: {self.high_score}")
        self.canvas.create_text(300, 200, text="GAME OVER", fill="red", font=("Arial", 36, "bold"), tags="gameover_text")
        self.canvas.create_text(300, 260, text="クリックして再挑戦", fill="white", font=("Arial", 16), tags="gameover_text")

def restart_game(self, event):
        """ゲームのリセットと再スタート"""
        if not self.game_over:
            return
        
        self.canvas.delete("gameover_text")
        self.score = 0
        self.score_label.config(text=f"SCORE: {self.score}  /  BEST: {self.high_score}")
        
        # 位置の初期化
        self.canvas.coords(self.ball, 290, 290, 310, 310)
        self.ball_dx = random.choice([-5, 5])
        self.ball_dy = -5
        
        self.game_over = False
        self.update()

if __name__ == "__main__":
    root = tk.Tk()
    game = ShieldGame(root)
    root.mainloop()