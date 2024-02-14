import tkinter
import random
import pygame
import time

pygame.mixer.init()
pygame.mixer.music.load("passepied.mp3")
pygame.mixer.music.play(-1)

se = pygame.mixer.Sound('huri.mp3')
se.set_volume(0.2)  # 0.0から1.0までの範囲で設定（1.0がデフォルトの音量）



index = 0
timer = 0
score = 0
hisc = 1000
difficulty = 0
tsugi = 0

cursor_x = 0
cursor_y = 0
mouse_x = 0
mouse_y = 0
mouse_c = 0

def on_closing():
    pygame.mixer.music.stop()  # BGMを停止
    root.destroy()  # ウィンドウを閉じる

def close_window():
    window.destroy()
    window.quit()

def mouse_move(e):
    global mouse_x, mouse_y
    mouse_x = e.x
    mouse_y = e.y

def mouse_press(e):
    global mouse_c
    mouse_c = 1

neko = []
check = []
for i in range(10):
    neko.append([0, 0, 0, 0, 0, 0, 0, 0])
    check.append([0, 0, 0, 0, 0, 0, 0, 0])

def draw_neko():
    cvs.delete("NEKO")
    for y in range(10):
        for x in range(8):
            if neko[y][x] > 0:
                cvs.create_image(x * 72 + 60, y * 72 + 60, image=img_neko[neko[y][x]], tag="NEKO")

def check_neko():
    for y in range(10):
        for x in range(8):
            check[y][x] = neko[y][x]
            

    for y in range(1, 9):
        for x in range(8):
            if check[y][x] > 0:
                if check[y - 1][x] == check[y][x] and check[y + 1][x] == check[y][x]:
                    neko[y - 1][x] = 7
                    neko[y][x] = 7
                    neko[y + 1][x] = 7
                    se.set_volume(0.2)
                    se.play()


    for y in range(10):
        for x in range(1, 7):
            if check[y][x] > 0:
                if check[y][x - 1] == check[y][x] and check[y][x + 1] == check[y][x]:
                    neko[y][x - 1] = 7
                    neko[y][x] = 7
                    neko[y][x + 1] = 7
                    se.set_volume(0.2)
                    se.play()


    for y in range(1, 9):
        for x in range(1, 7):
            if check[y][x] > 0:
                if check[y - 1][x - 1] == check[y][x] and check[y + 1][x + 1] == check[y][x]:
                    neko[y - 1][x - 1] = 7
                    neko[y][x] = 7
                    neko[y + 1][x + 1] = 7
                if check[y + 1][x - 1] == check[y][x] and check[y - 1][x + 1] == check[y][x]:
                    neko[y + 1][x - 1] = 7
                    neko[y][x] = 7
                    neko[y - 1][x + 1] = 7
                    se.set_volume(0.2)
                    se.play()

def sweep_neko():
    num = 0
    for y in range(10):
        for x in range(8):
            if neko[y][x] == 7:
                neko[y][x] = 0
                num = num + 1
    return num

def drop_neko():
    flg = False
    for y in range(8, -1, -1):
        for x in range(8):
            if neko[y][x] != 0 and neko[y + 1][x] == 0:
                neko[y + 1][x] = neko[y][x]
                neko[y][x] = 0
                flg = True
    return flg

def over_neko():
    for x in range(8):
        if neko[0][x] > 0:
            return True
    return False

def set_neko():
    for x in range(8):
        neko[0][x] = random.randint(0, difficulty)

def draw_txt(txt, x, y, siz, col, tg):
    # siz の値を適切な大きさに変更してください
    fnt = ("Yu Gothic", 26, "bold")
    cvs.create_text(x + 2, y + 2, text=txt, fill="black", font=fnt, tag=tg)
    cvs.create_text(x, y, text=txt, fill=col, font=fnt, tag=tg)


def game_main():
    global index, timer, score, hisc, difficulty, tsugi
    global cursor_x, cursor_y, mouse_c

    # difficulty を初期化
    if 'difficulty' not in globals():
        difficulty = 0

    if index == 0:  # タイトルロゴ
        draw_txt("　", 312, 240, 100, "white", "TITLE")
        cvs.create_rectangle(168, 384, 456, 456, fill="#999999", width=0, tag="TITLE")
        draw_txt("Easy", 312, 420, 40, "white", "TITLE")
        cvs.create_rectangle(168, 528, 456, 600, fill="#666666", width=0, tag="TITLE")
        draw_txt("Normal", 312, 564, 40, "white", "TITLE")
        cvs.create_rectangle(168, 672, 456, 744, fill="#333333", width=0, tag="TITLE")
        draw_txt("Hard", 312, 708, 40, "white", "TITLE")
        index = 1
        mouse_c = 0
    elif index == 1:  # タイトル画面　スタートまち
        difficulty = 0
        if mouse_c == 1:
            if 168 < mouse_x and mouse_x < 456 and 384 < mouse_y and mouse_y < 456:
                difficulty = 4
            if 168 < mouse_x and mouse_x < 456 and 528 < mouse_y and mouse_y < 600:
                difficulty = 8
            if 168 < mouse_x and mouse_x < 456 and 672 < mouse_y and mouse_y < 744:
                difficulty = 12
        if difficulty > 0:
            for y in range(10):
                for x in range(8):
                    neko[y][x] = 0
            mouse_c = 0
            score = 0
            tsugi = 0
            cursor_x = 0
            cursor_y = 0
            set_neko()
            draw_neko()
            cvs.delete("TITLE")
            index = 2

    elif index == 2:  # 落下
        if drop_neko() == False:
            index = 3
        draw_neko()
    elif index == 3:  # 揃ったか
        check_neko()
        draw_neko()
        index = 4
    elif index == 4:  # 揃ったものがあれば消す
        sc = sweep_neko()
        score = score + sc * difficulty * 2
        if score > hisc:
            hisc = score
        if sc > 0:
            index = 2
        else:
            if over_neko() == False:
                tsugi = random.randint(1, difficulty)
                index = 5
            else:
                index = 6
                timer = 0
        draw_neko()
    elif index == 5:  # マウス入力を待つ
        if 24 <= mouse_x and mouse_x < 24 + 72 * 8 and 24 <= mouse_y and mouse_y < 24 + 72 * 10:
            cursor_x = int((mouse_x - 24) / 72)
            cursor_y = int((mouse_y - 24) / 72)
            if mouse_c == 1:
                mouse_c = 0
                set_neko()
                neko[cursor_y][cursor_x] = tsugi
                tsugi = 0
                index = 2
        cvs.delete("CURSOR")
        cvs.create_image(cursor_x * 72 + 60, cursor_y * 72 + 60, image=cursor, tag="CURSOR")
        draw_neko()
    elif index == 6:  # ゲームオーバー
        timer += 1
        if timer == 1:
            draw_txt("GAME OVER", 312, 348, 60, "#B1221A", "OVER")
    
        if timer == 50:
            cvs.delete("OVER")
        
        # スコアに応じて画像表示およびindexの更新

                
            index = 0
    cvs.delete("INFO")
    draw_txt("SCORE" + str(score), 160, 60, 32, "#5D8165", "INFO")
    draw_txt("HISC" + str(hisc), 450, 60, 32, "#F1E266", "INFO")   

    if tsugi > 0:
        cvs.create_image(752, 128, image=img_neko[tsugi], tag="INFO")

    root.after(100, game_main)


root = tkinter.Tk()
root.title("パズル《KRNG NOODLE》")
root.resizable(False, False)
root.bind("<Motion>", mouse_move)
root.bind("<ButtonPress>", mouse_press)
# ウィンドウが閉じられたときに呼び出される関数を設定
root.protocol("WM_DELETE_WINDOW", on_closing)
cvs = tkinter.Canvas(root, width=912, height=768)
cvs.pack()

bg = tkinter.PhotoImage(file="pz_bg.png")
cursor = tkinter.PhotoImage(file="cursor.png")
img_neko = [
    None,
    tkinter.PhotoImage(file="uf_01.png"),
    tkinter.PhotoImage(file="sco_01.png"),
    tkinter.PhotoImage(file="mila_01.png"),
    tkinter.PhotoImage(file="sas_01.png"),
    tkinter.PhotoImage(file="jr_01.png"),
    tkinter.PhotoImage(file="yagi_02.png"),
    tkinter.PhotoImage(file="aruria_01.png"),
    tkinter.PhotoImage(file="yuki_01.png"),
    tkinter.PhotoImage(file="org_01.png"),
    tkinter.PhotoImage(file="h_01.png"),
    tkinter.PhotoImage(file="par_01.png"),
    tkinter.PhotoImage(file="oo_01.png"),
]

cvs.create_image(456, 384, image=bg)
game_main()
root.mainloop()

