#-*-coding utf-8-*-
from tkinter import *
import random
import tkinter.messagebox #引用消息窗口来做输赢提示  
import copy               #引用复制函数来做数据矩阵检测
import pygame
#设计用户界面
root = Tk()
root.title('某小仙女专用DQ版2048')
root.geometry()#主窗口和标题
#音效模块，利用pygame处理背景音乐和移动音效
pygame.init()
pygame.mixer.init()
pygame.time.delay(1000)
#bgm = pygame.mixer.Sound('C:/Python34/planegame/sound/game_music.wav')
#clash_music = pygame.mixer.Sound('C:/Python34/planegame/sound/bullet.wav')
#bgm.play()


mBar=Frame(root,relief=RAISED, bd=2)#制作菜单栏
mBar.pack(fill=X)
 

var1=StringVar()
var_score=StringVar()#创建两个字符串变量
var_era =StringVar()
l1=Label(root, textvariable=var1,bg='skyblue',fg='black')
var1.set('欢迎来到2048，WSAD控制上下左右\nQ键退出，B键返回上一步')#制作最顶层的标签用于操作说明
l1.pack(side=TOP, expand=YES, fill=X)#制作最顶层的标签用于操作说明
l2=Label(root, textvariable=var_score,bg='skyblue',fg='red')
var_score.set('目前的分数是：   目前的步数是：')
l2.pack(side=TOP, expand=YES, fill=X)#制作第二行标签用于显示分数和步数
l3 =Label(root, textvariable=var_era, bg='skyblue', fg = 'yellow')
var_era.set('现在航空事业仍处于萌芽状态')
l3.pack(side=TOP, expand=YES, fill=X)
frm= Frame(root, width=400, height=300)
frm.pack(side=TOP, expand=YES, fill=BOTH)#设计一个矩形边框用于游戏操作

square=10#定义游戏的难度，比如4*4的棋盘
str_data=[]#字符串数据列表，用于存放每个小方格的数字大小
b_list=[]#方格列表（按钮列表）
#颜色字典，通过对应关系可以实现颜色的改变，使界面看起来更为多彩

dic_color={0:'GhostWhite', 2:'AliceBlue', 4:'LightCyan', 8:'Khaki',16:'SandyBrown', 32:'Goldenrod',64:'Orange',128:'Maroon',256:'Tomato',512:'OrangeRed',1024:'FireBrick',2048:'Red',4096:'skyblue',8192:'lightgreen'}
dic_gamer={0:'',2:'风筝', 4:'孔明灯', 8:'热气球' ,16:'飞艇', 32:'双翼机', 64:'零式',128:'X-1',256:'F-100', 512:'米格21', 1024:'苏-27',2048:'F-22', 4096:'空天母舰'}
#制作方格
for i in range(square*square):
    str_data.append(StringVar())
    #每一个方格必须和字符串数据列表和颜色字典建立对应关系，并且边界必须显现
    b_list.append(Button(frm, width=6, height=3, textvariable=str_data[i],font=('Arial',10),bg=dic_color[0],bd=2))
    #给方格排序，(i//n,i%n)语句可以很好的实现由一维矩阵到二维矩阵的转变
    b_list[i].grid(row=i//square,column=i%square)

def era(k):
    t = max(k)
    if t == 8:
        l3.configure(fg='lightgreen')
        return'少年啊，天空已经离你不远了'
    if t== 16:
        l3.configure(fg='GhostWhite')
        return'就像黎明划过天边'
    if t== 32:
        l3.configure(fg='orange')
        return'被诅咒的金字塔'
    if t == 64:
        l3.configure(fg='Khaki')
        return '起风了，更要努力前行'
    if t == 128:
        l3.configure(fg='Tomato')
        return '超音速时代已经不远了'
    if t == 256:
        l3.configure(fg='Maroon')
        return '后掠翼!超声速战机上线'
    if t == 512:
        l3.configure(fg='GhostWhite')
        return '涡喷！两倍音速'
    if t == 1024:
        l3.configure(fg='SandyBrown')
        return '涡扇！鸭式！颜值与实力的巅峰'
    if t == 2048:
        l3.configure(fg='FireBrick',font=('Arial',20))
        return '隐身，失速，矢量，科幻感的结晶'
    if t == 4096 :
        l3.configure(fg='LightCyan',font=('Arial',30))
        return '未来科技，燃爆全场'
    else:
        return '现在航空事业仍处于萌芽状态'




def init():#定义初始化数据矩阵
    scr=[[0 for i in range(square)]for j in range(square)]#首先全部全部归零
    shot=random.sample(range(square*square),2)#利用随机函数在整个矩阵中随机找两个位置并初始化为2
    scr[shot[0]//square][shot[0]%square] =2
    scr[shot[1]//square][shot[1]%square] =2
    return scr#返回初始化完成的矩阵

def principle(scr):#定义游戏规则
    #这里我设计了一条备用游戏规则，可以选择使用
    '''
    if 2048 in scr:
        tkinter.messagebox.showinfo(messsage='干得漂亮，你赢了\n你的总分是%d'%score)
        exit()
    '''
    #如果整个数据矩阵还有0，即显示界面还有空方块，可以继续操作
    if 0 in scr:
        return True
    #如果扫描整个数据矩阵，发现无法合并，那么游戏结束
    for i in range(square):
        for j in range(square):
            if scr[i][j] ==0:
                return True
            if i <(square-1) and scr[i][j] == scr[i+1][j]:
                return True
            if j<(square-1) and  scr[i][j] == scr[i][j+1]:
                return True
    return False
#这就是一个比较好玩的函数了，这样可以使矩阵中的0变成空字符串，而其他的数据都不变
def T(a):
    return a if a else' '
#定义可视化函数，用于显示数据矩阵
def display(scr):
    str_tmp=[]#字符串列表用于存储字符串（包括空字符串）
    list_tmp=[]#数据列表用于存储数据（包括0）
    for i in range(square):
        for j in range(square):
            str_tmp.append(dic_gamer[scr[i][j]])
            list_tmp.append(int(scr[i][j]))
    for i in range(square*square):
        str_data[i].set(str_tmp[i])#改变方块的数字显示
        b_list[i].configure(bg=dic_color[list_tmp[i]])#相应地改变方块的颜色
    var_era.set(era(list_tmp))

def process(scr,key):#定义运动函数
    #clash_music.play(0)#播放移动音效
    score = 0#注意这里的score指运动一步的得分
    visit = []#这是访问列表，存储所有合并过的方块，保证合一产生的新方块不会再次合一
    if key == 0:#向左运动
        for i in range(square):
            for j in range(1,square):
                for k in range(j,0,-1):
                    #如果相邻的左边方块为空，那么方块左可以移
                    if scr[i][k-1] == 0:
                        scr[i][k-1] = scr[i][k]
                        scr[i][k] = 0
                    #如果遇到相同方块且这两个方块都不是刚刚产生的，那么合一，并且在访问列表中记录这两个方块
                    elif scr[i][k-1] == scr[i][k] and square*i+k-1 not in visit and square*i + k not in visit:
                        scr[i][k-1]*=2
                        scr[i][k]=0
                        score += scr[i][k-1]#分数增加合一之前方块代表的数字
                        visit.append(square*i +k)
                        visit.append(square*i + k-1)
    elif key == 1:#向下运动，类似
        for j in range(square):
            for i in range((square-1),0,-1):
                for k in range(0,i):
                    if scr[k+1][j] == 0:
                        scr[k+1][j] = scr[k][j]
                        scr[k][j] = 0
                    elif scr[k+1][j] ==scr[k][j] and (square*(k+1)+j) not in visit and (square*k + j) not in visit:
                        scr[k+1][j]*=2
                        scr[k][j]=0
                        score += scr[k+1][j]
                        visit.append(square*k +j)
                        visit.append(square*(k+1) + j)
                        
    elif key == 2:#向上运动
            for j in range(square):
                for i in range(1,square):
                    for k in range(i,0,-1):
                        if scr[k-1][j] == 0:
                            scr[k-1][j] = scr[k][j]
                            scr[k][j] = 0
                        elif scr[k-1][j] ==scr[k][j] and (square*(k-1)+j) not in visit and (square*k + j) not in visit:
                            scr[k-1][j]*=2
                            scr[k][j]=0
                            score += scr[k-1][j]
                            visit.append(square*k +j)
                            visit.append(square*(k-1) + j)            
    
    elif key == 3:#向右运动
            for i in range(square):
                for j in range((square-1),0,-1):
                    for k in range(j):
                        if scr[i][k+1] == 0:
                            scr[i][k+1] = scr[i][k]
                            scr[i][k] = 0
                        elif scr[i][k+1] ==scr[i][k] and square*i+k+1 not in visit and square*i + k not in visit:
                            scr[i][k+1]*=2
                            scr[i][k]=0
                            score += scr[i][k+1]
                            visit.append(square*i +k)
                            visit.append(square*i + k+1)

    return score#返回移动一步获得的分数
#定义更新函数，用于在每一次移动之后增加一个新的数值为2或4方块
def update(shot):
    global shot_num
    global level
    shot_pos = []#新生成方块的位置
    shot_num = [2,2,4]#随机生成2或4的概率
    for i in range(square):
         for j in range(square):
                if scr[i][j] == 0:#在空方块里选择生成位置
                     shot_pos.append(square*i+j)
    if len(shot_pos) > (level-1):#如果还有空位，那么生成方块
        for i in range(level):
            k= random.choice(shot_pos)
            n= random.choice(shot_num)
            scr[k//square][k%square]= n
#定义回退函数，用来返回上一步的操作
def backmove(scr_stk,flash_stk,scr,score,step):
    if len(scr_stk)>1:#建立两个个栈用来存储每一步操作之后的数据矩阵和分数
        scr_stk.pop()
        flash_stk.pop()#利用弹栈来实现返回矩阵和分数
        scr = copy.deepcopy(scr_stk[-1])#复制函数，用来返回矩阵
        score = flash_stk[-1]#返回分数
        step-=1#步数直接减1
        #重新显示数据矩阵，分数和步数
        display(scr)
        var_score.set('目前的分数是：'+str(score)+'目前的步数是'+str(step))
#制作菜单，用来完善和丰富整个界面功能
def menubox():
    global scr_stk
    global flash_stk
    global scr
    global score
    global step
    mainmenu=Menubutton(mBar,text='选项')#主选项
    mainmenu.pack(side=LEFT)#放在首位

    mainmenu.menu=Menu(mainmenu)#在主菜单中添加一级子菜单

    mainmenu.menu.choices=Menu(mainmenu.menu)#在一级子菜单中创建二级子菜单
    #从内到外制作菜单
    #首先定义最内层二级子菜单即难度菜单
    mainmenu.menu.choices.add_command(label='困难',command=lambda:changesize(3))
    mainmenu.menu.choices.add_command(label='正常',command=lambda:changesize(2))
    mainmenu.menu.choices.add_command(label='简单',command=lambda:changesize(1))
    #定义一级子菜单，增加主要功能（难度选择，自动模式，返回上一步，退出按钮）
    mainmenu.menu.add_cascade(label='难度',menu=mainmenu.menu.choices)
    mainmenu.menu.add_command(label='自动模式（M）',command=lambda:automode())
    mainmenu.menu.add_command(label='返回上一步（B）',command=lambda:backmove(scr_stk,flash_stk,scr,score,step))
    mainmenu.menu.add_command(label='退出（Q）',command=lambda:exit())
    #定义主选项菜单栏
    mainmenu['menu']=mainmenu.menu
    #返回菜单界面
    return mainmenu
#定义难度选择功能，通过改变2和4出现的概率来改变游戏难度
def changesize(k):
    global shot_num    
    if k == 3:#困难模式下调整2的出现概率为1/4,4的出现概率为3/4
        shot_num=[2,4,4,4]
    elif k == 2:#普通模式下调整2的出现概率为2/3,4的出现概率为1/3
        shot_num=[2,2,4]
    elif k == 1:#简单模式下调整2的出现概率为3/4,4的出现概率为1/4
        shot_num=[2,2,2,4]

#定义自动模式
def automode():
    import time#引用时间模块，用来制作时间间隔
    list_box=[0,1,2,3]#制作一个随机命令盒，用来存放命令字符
    time.sleep(0.5)#每次执行延迟0.5秒
    key=random.choice(list_box)#选择随机命令
    #以下完全复制主程序
    global scr
    global step
    global scr_stk
    global flash_stk
    global score
    if principle(scr) is True:#如果满足游戏规则
        tmp = copy.deepcopy(scr)#建立缓存区
        operations=process(scr,key)#计算每一步操作后的分数
        if tmp != scr:#判断是否为有效步，如果缓存和上一步缓存不同，那么有效
            score+=operations#将总分加上操作分
            update(scr)#更新数据矩阵
            display(scr)#更新用户界面
            tmp = copy.deepcopy(scr)#更新缓存区（包括缓存栈）
            scr_stk.append(tmp)
            flash_stk.append(int(score))
            step+=1#更新步数和分数
            var_score.set('目前的分数是：'+str(score)+'目前的步数是'+str(step))
#如果无法执行，输出失败消息提示，并告知分数
    else:
        tkinter.messagebox.showinfo(message='你输了，下次努力吧,这次的分数是%d'%score)
    
  
menu=menubox()
#mBar.tk_menuBar(menu)


    

#所有变量和显示界面的初始化    
score = 0
step  = 0
scr = init()
scr_stk = []
flash_stk = []
tmp = copy.deepcopy(scr)
scr_stk.append(tmp)
flash_stk.append(0)
display(scr)
shot_num = [2,2,4]#随机生成2或4的初始概率
level=1#定义难度系数

#最最关键也是最困难的一步，绑定键盘
def key_event(event):
    global scr
    global step
    global scr_stk
    global flash_stk
    global score#首先调用函数外我们所需的函数，这里用全局变量来实现
    key=-1#初始化key值使得key不触发时间
    #读取键盘操作
    if event.char == 'q':#Q退出程序
        exit()
    elif event.char =='m':
        automode()
    else:
        if event.char == 'a':#A左
            key=0
        if event.char == 's':#S下
            key=1
        if event.char == 'w':#W上
            key = 2
        if event.char == 'd':#D右
            key = 3
        if event.char == 'b':#返回上一步
            backmove(scr_stk,flash_stk,scr,score,step)

    if principle(scr) is True:#如果满足游戏规则
        tmp = copy.deepcopy(scr)#建立缓存区
        operations=process(scr,key)#计算每一步操作后的分数
        if tmp != scr:#判断是否为有效步，如果缓存和上一步缓存不同，那么有效
            score+=operations#将总分加上操作分
            update(scr)#更新数据矩阵
            display(scr)#更新用户界面
            tmp = copy.deepcopy(scr)#更新缓存区（包括缓存栈）
            scr_stk.append(tmp)
            flash_stk.append(int(score))
            step+=1#更新步数和分数
            var_score.set('目前的分数是：'+str(score)+'目前的步数是'+str(step))
    #如果无法执行，输出失败消息提示，并告知分数
    elif 2048 not in scr:
        tkinter.messagebox.showinfo(message='你输了，下次努力吧,这次的分数是%d'%score)
#绑定键盘
frm.bind('<Key>', key_event)
frm.focus_set()#设定光标位置
root.mainloop()#保持悬浮

    















    
        
        

