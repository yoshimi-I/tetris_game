# テトリス作成(python)
## 作成日
- 2021年11月11日
## 作成目的
- 彼女と別れた -> なんかぶち壊したくなった　-> そうだテトリス作ろう!
## デモ動画
- ![デモ動画](https://media.giphy.com/media/J4gIasug6E5xR0mJfG/giphy.gif)
## 作成手順
1. テトリスを画面に表示する準備
2. テトリスに登場するブロックを作成する関数を作成
3. テトリスが動くフィールをを作成する関数の作成
4. キーボードを打ち込むことで、テトリスの座標を変化させブロックを動かす関数を作成(上下左右)
5. ブロックが回転する関数を作成
6. 今のままでは移動させたブロックがフィールドの外まで動けてしまうので、その問題を解決するプログラムを作成(テトリスのブロックの動け場所を制限)
7. ブロックが時間で落ちていく関数を作成
8. 一列揃ったらブロックが消える関数を作成
9. 全ての処理が終わったら次のブロックが落ちてくる関数を作成
10. 以上で作った関数を繋ぎ合わせて無限ループする関数を作成

## ソースコード解説
```
import tkinter as tk
import random as rd


win = tk.Tk()
can = tk.Canvas(height = 630,width = 360)
can.pack()
win.mainloop()
```
- テトリスを画面に表示する準備
    1. tkinterというpythonでGUIを提供してくれるライブラリをインポートした後、tkという名前に代入
        - 今回はtkinterというpythonでGUIを提供してくれるライブラリとramdom
        という範囲を指定することで乱数を提供してくれるライブラリをインポート。
        - tkinterにはtkという名前を、randomライブラリにはrdと名前をつけて使いやすくした。
    2. tkinterの持っているウィンドウを表示するという機能を用いて、Tk関数でウィンドウを表示
    3. canという変数に名前をつけてテトリスをかくキャンバスを表示(大きさも指定)
    4. can.pack()を用いてキャンバスをウィンドウに配置
    5. win.mainloop()で以上の処理を開始する
        - 以上の処理は意味を理解するというよりキャンバスに何か記載していく前の呪文のようなものだと考える方がわかりやすい気がした。

```
size = 30
pos_y = 3
pos_x = 5
n = rd.randint(0, 3)
tetro1 = [0,0,-1,0,1,0,0,1]
tetro2 = [0,0,-1,0,-1,-1,1,0]
tetro3 = [0,0,-1,0,1,0,2,0]
tetro4 = [0,0,-1,0,0,1,1,1]
rot_list = [0,0]
tetoro_list = [tetro1,tetro2,tetro3,tetro4]
tetoro_color = ["orange","blue","yellow","green","black","white"]

def drawTetoris():
    for i in range(4):
        x = (tetoro_list[n][i*2]+pos_x)*size
        y = (tetoro_list[n][i*2+1]+pos_y)*size
        can.create_rectangle(x,y,x+size,y+size,fill=tetoro_color[n])
```
- テトリスに登場するブロックを作成する関数を作成
    - テトリスの種類は4種類とした。
    1. 左上を(0,0),右がx軸,下がy軸であることを考慮してテトリスのブロックの座標を記載していく
        - テトリスのブロックは4個の正方形で作られており、1個あたり(x,y)と2個の値が必要であるので4×２で合計8個の値が必要である。詳しくは後ほど解説
        - この時、最初の2つの(x,y)座標を回転の中心になるブロックとしている(今回はずべて(0,0)の座標を取る)
    2. 1.で作ったテトリスのブロックをtetoro_listという名前の配列に代入
        - このような処理をしておくことでテトリスのブロックを数字で出力することができる。(例　テトリスのn番目であればtetoro_list[n]で出力できる。)
    3. 1.で作ったテトリスのブロックの色を指定する配列を作成
        - nの値によってどのブロックとどの色が紐づくかを指定。
    4. create_rectangle関数を用いてテトリスの正方形を1つずつ描いていく。
        - 左上と右下の(x,y)座標を指定するとそれに伴った長方形または正方形を記載してくれる関数である。
        - 左上の(x,y)座標が決まれば右下の座標は(x+正方形の1辺の長さ,y+正方形の正方形の1辺の長さ)で決まるため1.で作った左上の座標をfor文を使ってループ。(そのため配列の中には正方形１つにつき１つの（x,y）座標でいい)


```
field = []
for y in range(21):
    field_y = []
    for x in range(12):
        if x == 0 or x == 11 or y == 20:
            field_y.append(5)
        else:
            field_y.append(4)
    field.append(field_y)

def drawField():
    for y in range(21):
        for x in range(12):
            can.create_rectangle(x*size,y*size,(x*size)+size,(y*size)+size,fill = tetoro_color[field[y][x]])
```
- テトリスが動くフィールドを作成する関数の作成
    1. まずは壁とフィールドとで色を分けるために4と5を羅列する配列を作成する。
        1. ブロック以外のフィールドは周りの柵の色を白、ブロックが動ける範囲を黒とした。
            - tetoro_color[4] = 白,tetoro_color[5] = 黒であることを使う。
        3. y座標(縦の高さ)を固定しながらx座標(横の長さ)に沿って4,5の数を配列に格納していき、全て終わったらfieldという配列に追加していく。
```
          [[5, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5], 
            [5, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5], 
            [5, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5], 
            [5, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5], 
            [5, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5], 
            [5, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5], 
            [5, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5], 
            [5, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5], 
            [5, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5], 
            [5, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5], 
            [5, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5], 
            [5, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5], 
            [5, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5], 
            [5, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5], 
            [5, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5], 
            [5, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5], 
            [5, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5], 
            [5, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5], 
            [5, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5], 
            [5, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5], 
            [5, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5], 
            [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]]
```
- 以上のような配列がfield配列である。
2. 1で作った0と１の配列を用いて白と黒の正方形をキャンバスに埋め込んでいく
    1. drawField関数を作成し、1で作った配列の数字に基づく色の正方形を追加
        - 4であったら白、5であったら黒にする
        - fill = tetoro_color[field[y][x]]で指定しているため[field[y][x]]が色を指定している。yで縦をxで横を指定しているため、
```
win.bind("<Any-KeyPress>",keyPress)

def keyPress(event):
    global pos_x,pos_y
    test_x = pos_x
    test_y = pos_y
    test_list = tetoro_list[n]
    if event.keysym == "Right":
        test_x += 1
    elif event.keysym == "Left":
        test_x -= 1
    elif event.keysym == "Down":
        test_y += 1
    elif event.keysym == "Up":
        test_list = blockRot(tetoro_list[n])
    if checkTest(test_x,test_y):
        pos_x = test_x
        pos_y  = test_y
    if checkRot(test_list):
        tetoro_list[n] = test_list
```
- キーボードを打ち込むことで、テトリスの座標を変化させブロックを動かす関数を作成(上下左右)
    1. bind関数を用いることで指定したキーボードが打ち込まれたら,keyPress関数を呼び出す(コールバック)できるようにした。
    2. keyPress関数(コールバック関数)には引数としてeventを指定する必要があり、今回は左右下のキーボードが打ち込まれたら結果に基づく処理を関数内に記載した。
        - event.keysymで処理に紐づけるキーボードの種類を指定。
```
def blockRot(blockList):
    global rot_list
    rot_list = [0,0]
    for i in range(3):
        y = (blockList[2+(2*i)])
        x = -(blockList[2+(2*i+1)])
        rot_list.append(x)
        rot_list.append(y)
    return rot_list

ori_tetro1 = [0,0,-1,0,1,0,0,1]
ori_tetro2 = [0,0,-1,0,-1,-1,1,0]
ori_tetro3 = [0,0,-1,0,1,0,2,0]
ori_tetro4 = [0,0,-1,0,0,1,1,1]

def resetBlock(ori_tetro_list,tetoro_list):
    for i in range(4):
        tetoro_list[i] = ori_tetro_list[i]
```
- ブロックが回転する関数を作成
1. まずはブロックを回転させる。
    1. まず前提条件として、回転の仕組みは原点を中心とした回転である。(複素数平面で考えるとわかりやすいと思う。)
    2. そのため移動させる前の(x,y)の座標を回転させた後に変化量を足し合わせることで回転を実現することができる。
    3. しかし回転の中心となる座標は回転しないため(そのために回転の中心となる座標を(0,0)として)３番目の配列から処理を始めるようにした。
        - blockList[2+(2*i)]の最初の+２はそのためである。
    4. 回転すると,x = -(blockList[2+(2*i+1)]),y = (blockList[2+(2*i)])となるため、以上の処理を施した。
2. 回転すると、配列の中身が変わったまま次に落ちてくるブロックも回転したままになってしまうため、配列の中身を一度リセットする。
    1. ori_tetroの配列を用意し、回転が終わり、ブロックが落ちきって固定されたタイミングで配列を元の配列に書き換える処理を行う。(司波達也の再生みたいなイメージ)

```
def keyPress(event):
    global pos_x,pos_y
    test_x = pos_x
    test_y = pos_y
    test_list = tetoro_list[n]
    if event.keysym == "Right":
        test_x += 1
    elif event.keysym == "Left":
        test_x -= 1
    elif event.keysym == "Down":
        test_y += 1
    elif event.keysym == "Up":
        test_list = blockRot(tetoro_list[n])
    if checkTest(test_x,test_y):
        pos_x = test_x
        pos_y  = test_y
    if checkRot(test_list):
        tetoro_list[n] = test_list

def checkTest(test_x,test_y):
    result = True
    for i in range(4):
        x = tetoro_list[n][i*2]+test_x
        y = tetoro_list[n][i*2+1]+test_y
        if field[y+1][x] != 0:
            result = False
    return result

def checkRot(test_list):
    result = True
    for i in range(4):
        x = test_list[i*2]+pos_x
        y = test_list[i*2+1]+pos_y
        if field[y][x] != 4:
            result = False
    return result
```
- 今のままでは移動させたブロックがフィールドの外まで動けてしまうので、その問題を解決するプログラムを作成
    1. イメージとしてはひとまずpos_xの値をtest_xに代入し、処理を行なったときに4つのブロック全て黒いフィールドに存在するかの判別を行い、全て黒いタイルにいた場合のみ処理を行う。
    2. checkTest関数の中で実際にtest_x、test_yを現在の座標に足し合わせ、その時の座標を配列fieldに代入した時その値が0(つまり黒いタイル)の時はそのままTrueを返す。
    3. もし2.の結果に反していた場合はfalseを返し、移動できないようにする。
        - つまりtest値を先に足し合わせておいて、その場合でもし正しい処理を行なっていたら実際に画面上に動かすということである。
```
def dropBlock():
    global pos_y
    pos_y += 1
    can.after(800,dropBlock)
```
- ブロックが時間で落ちていく関数を作成
    1. pos_y += 1の関数を1ずつ足し合わしていく
    2. 1.の処理をループさせたいのでafter関数を用いている。
```
def deleteBlock():
    for i in range(20):
        if field[i].count(4) == 0:
            
            j = i
            while j >= 1:
                field[j] = field[j-1]
                j -=1
```
-  1列揃ったらブロックが消える関数を作成
    1. for i in range(20):でまずブロックのフィールドを１列目から順にチェックしていく。
        - このとき範囲を21にしてしまうと1番下の白のタイルが消えてしまう。
    2. if field[i].count(4) == 0:黒いタイルが0枚であるとき、(つまり１列全てにブロックが埋まっている)ときに処理を開始する。
    3. ```j = i
            while j >= 1:
                field[j] = field[j-1]
                j -=1
        ```
         で配列を一個ずつ動かしていく。(つまり一つまえの配列を上書きすることでブロックが消えているように見せることができる。)
```
def nextBlock(test_list):
    global pos_x,pos_y,n
    for i in range(4):
        x = test_list[i*2]+pos_x
        y = test_list[i*2+1]+pos_y
        if field[y+1][x] != 4:
            for j in range(4):
                x = test_list[j*2]+pos_x
                y = test_list[j*2+1]+pos_y
                field[y][x] = n
            pos_y = 0
            pos_x = 5
            n = rd.randint(0, 3)
            resetBlock(ori_tetro_list,tetoro_list)
            drawTetoris()
```
- 全ての処理が終わったら次のブロックが落ちてくる関数を作成
    1. 4つの全てのテトリスを調べてそのy座標を+1した値が黒いタイル以外であった場合、テトリスの場所を固定し、resetBlock(ori_tetro_list,tetoro_list),drawTetoris()の2つの関数を呼び出した。
        - つまりテトリスが固定された時点で新しいテトリスが降ってくるようにした。
```
def gameloop():
    can.delete("all")
    drawField()
    drawTetoris()
    deleteBlock()
    nextBlock(tetoro_list[n])
    can.after(5,gameloop)

gameloop()
dropBlock()
```
- 以上で作った関数を繋ぎ合わせて無限ループする関数を作成
    - ここで全ての関数をループさせることでテトリスを動かす.
    1. 
        ```
        can.delete("all")
        ```
        テトリスが動いているようにするには直前の処理を消すことで成り立っている。
        - この処理がないとテトリスの面積が広がっていくように見えてしまう。
    2. 
        ```
        drawField()
        ```
        ここでテトリスが動くフィールドをまずは作る。
    3. 
        ```
        drawTetoris()
        ```
        ここでテトリスをなん度も作っていく。
        - テトリスが動くたびに描画し続ける必要があるため、何度もこの関数を呼び出す必要がある。
    4. 
        ```
        deleteBlock()
        ```
        - if文による処理関数のため、何度読み込んでも条件に反するときはすり抜けるからOK

    5. 
        ```
        nextBlock(tetoro_list[n])
        ```
        - これもif文によ条件分岐の関数のため、すり抜ける
        - この関数の最後にdrawTetoris()を一度読み込んでいるが、この関数は重複しても動きに変化がないためゲームに支障をきたさない。
    6. 
        ```
        can.after(5,gameloop)
        ```
        以上の処理をafter関数を用いて繰り返すことで、テトリスを動かすことができる。
