import random
import time
import copy

column = ["a","b","c","d","e","f","g","h","i"]
rule = "Enter the column followed by the row (ex: a5). To add or remove a flag, add \'f\' to the cell (ex: a5f)." 

#創造玩家遊戲格的串列
player_list=[]
for i in column:
    i=["   ","   ","   ","   ","   ","   ","   ","   ","   "]
    player_list+=[i]

def plot_table(player_list):
    #給定玩家遊戲格後，列印出table
    print("     a   b   c   d   e   f   g   h   i \n"+"   "+"+---"*9+"+")
    for i in range(9):
        print("",i+1,end=""+" |"+player_list[i][0]+"|"+player_list[i][1]+"|"+player_list[i][2]+"|"+player_list[i][3]+"|"+player_list[i][4]+"|"+player_list[i][5]+"|"+player_list[i][6]+"|"+player_list[i][7]+"|"+player_list[i][8]+"|\n")
        print("   "+"+---"*9+"+")

def new_game():
    #開始一個新的遊戲，創造一個玩家遊戲格，並列印出空白遊戲格
    player_list,mines,correct_mines=[],10,0
    for i in column:
        i=["   ","   ","   ","   ","   ","   ","   ","   ","   "]
        player_list+=[i]
    print("     a   b   c   d   e   f   g   h   i \n"+"   "+"+---"*9+"+")
    for i in range(9):
        print("",i+1,end=""+" |"+player_list[i][0]+"|"+player_list[i][1]+"|"+player_list[i][2]+"|"+player_list[i][3]+"|"+player_list[i][4]+"|"+player_list[i][5]+"|"+player_list[i][6]+"|"+player_list[i][7]+"|"+player_list[i][8]+"|\n")
        print("   "+"+---"*9+"+")
    print("\n",rule)  #說明規則
    return player_list,mines,correct_mines  #返回空白遊戲格，地雷數以及命中地雷數
    
def check_valid():
    input_s=input(" Enter the cell (%d mines left):" % (mines))  #讓玩家輸入位置
    a=True
    while a==True:
        if input_s=="help":  #若玩家輸入help，則說明規則
            plot_table(player_list)
            print("\n",rule,"\n")
            input_s=input(" Enter the cell (%d mines left):" % (mines))
            continue
        else:  #檢查玩家輸入是否符合格式
            if input_s[0]=="a" or input_s[0]=="b" or input_s[0]=="c" or input_s[0]=="d" or input_s[0]=="e" or input_s[0]=="f" or input_s[0]=="g" or input_s[0]=="h" or input_s[0]=="i":
                for i in range(1,10):
                    if len(input_s[1:])>1 and input_s[len(input_s)-1]!="f":
                        plot_table(player_list)
                        print("\n","Invalid cell.",rule,"\n")
                        input_s=input(" Enter the cell (%d mines left):" % (mines))
                        break
                    else:
                        a=False
                        break
            else:
                plot_table(player_list)
                print("\n","Invalid cell.",rule,"\n")
                input_s=input(" Enter the cell (%d mines left):" % (mines))
                continue
            continue
    #將玩家輸入的位置轉成其串列的位置
    input_no=[int(input_s[1]),0]
    for i in column:
        if input_s[0]!=i:
            input_no[1]+=1
            continue
        else:
            input_no[0]-=1
            break
    return input_s,input_no  #返回位置(字串)以及其位置(幾行幾列)

def creat_ans(input_no):
    #創造ans_list，並創造coordinate用來抽取10個放入地雷，coordinate0方便對照
    ans_list=copy.deepcopy(player_list)
    coordinate=[]
    for i in range(9):
        for j in range(9):
            coordinate.append([i,j])
    coordinate0=coordinate[:]
    #移除不可放入地雷的位置(因為第一次玩家輸入的位置一定要是0)
    _99=[[-1,0],[-1,1],[0,1],[1,1],[0,0],[1,0],[1,-1],[0,-1],[-1,-1]]
    nearby=[]
    for i in range(9):
        a=input_no[0]+_99[i][0]
        b=input_no[1]+_99[i][1]
        nearby.append([a,b])
        if nearby[i] in coordinate:
            coordinate.remove(nearby[i])
    random.shuffle(coordinate)  #隨機抽取10個放入地雷
    #計算並創造ans_list
    mines_no=coordinate[:10]
    for i in range(81):
        if coordinate0[i] in mines_no:
            ans_list[coordinate0[i][0]][coordinate0[i][1]]=" X "
    count=0
    for i in range(81):
        for j in range(9):
            a=coordinate0[i][0]+_99[j][0]
            b=coordinate0[i][1]+_99[j][1]
            if [a,b] in coordinate0:
                if [a,b] in mines_no:
                    count+=1
                else:
                    count=count
        if ans_list[coordinate0[i][0]][coordinate0[i][1]]=="   ": 
            ans_list[coordinate0[i][0]][coordinate0[i][1]]=" %d "%(count)
        count=0
    return ans_list  #返回答案list

def check_0_list(input_no,player_list,ans_list):
    #第一次玩家輸入位置判斷其九宮格是否為0，只要是0便顯示出來並存入total
    coordinate0=[]
    for i in range(9):
        for j in range(9):
            coordinate0.append([i,j])
    _99=[[-1,0],[-1,1],[0,1],[1,1],[0,0],[1,0],[1,-1],[0,-1],[-1,-1]]
    total=[]
    for i in range(9):
        a=input_no[0]+_99[i][0]
        b=input_no[1]+_99[i][1]   
        if [a,b] in coordinate0:
            if ans_list[a][b]==" 0 " and ans_list[input_no[0]][input_no[1]]==" 0 ":
                player_list[a][b]=ans_list[a][b]
                total+=[[a,b]]
    #依序判斷total中所有位置的九宮格是否為0並顯示
    t=0
    while t<len(total):
        for i in range(9):
            a=total[t][0]+_99[i][0]
            b=total[t][1]+_99[i][1]
            if [a,b] in coordinate0:
                if ans_list[a][b]==" 0 ":
                    player_list[a][b]=ans_list[a][b]
                if ans_list[a][b]==" 0 " and [a,b] not in total:  #若有新的0位置則存入total
                    total+=[[a,b]]
        t=t+1
    #顯示出total中所有位置的九宮格但不包括地雷
    for t in range(len(total)):
        for i in range(9):
            a=total[t][0]+_99[i][0]
            b=total[t][1]+_99[i][1]
            if [a,b] in coordinate0:
                if ans_list[a][b]!=" X ":
                    player_list[a][b]=ans_list[a][b]
    #若玩家輸入非0的位置，則顯示出此格
    if ans_list[input_no[0]][input_no[1]]!=" 0 " and ans_list[input_no[0]][input_no[1]]!=" X ":
        player_list[input_no[0]][input_no[1]]=ans_list[input_no[0]][input_no[1]]
    plot_table(player_list)  #print出遊戲格
    return player_list  #最後返回玩家遊戲格
def put_flag(input_s,input_no,mines,correct_mines):
    #判斷玩家輸入為長度3的字串
    if len(input_s)==3:
        if player_list[input_no[0]][input_no[1]]=="   ":  #進行插旗
            player_list[input_no[0]][input_no[1]]=" F "
            mines-=1
            plot_table(player_list)
            if ans_list[input_no[0]][input_no[1]]==" X ":  #計算是否命中地雷數
                correct_mines+=1
            else:
                correct_mines=correct_mines
        elif player_list[input_no[0]][input_no[1]]==" F ":  #進行拔旗
            player_list[input_no[0]][input_no[1]]="   "
            mines+=1
            plot_table(player_list)
            if ans_list[input_no[0]][input_no[1]]==" X ":  #計算是否命中地雷數
                correct_mines-=1
            else:
                correct_mines=correct_mines
        else:  #不能插旗
            plot_table(player_list)
            print("\n Cannot put a flag there.\n")
    return player_list,mines,correct_mines  #返回玩家遊戲格，剩餘地雷數，命中地雷數

def win_or_not(correct_mines):
    #如果命中地雷數到達10，則print出玩家花費時間，返回是否贏得遊戲
    if correct_mines==10:
        tEnd=time.time()
        a=(tEnd-tStart)//60
        b=(tEnd-tStart)%60
        if a==0:
            print("\n You win. It took you %d secounds.\n" % (b))
        else:
            print("\n You win. It took you %d minutes and %d secounds.\n" % (a,b))
        return True
    else:
        return False

def play_again(ans_list):
    #列印出答案
    print("     a   b   c   d   e   f   g   h   i \n"+"   "+"+---"*9+"+")
    for i in range(9):
        print("",i+1,end=""+" |"+ans_list[i][0]+"|"+ans_list[i][1]+"|"+ans_list[i][2]+"|"+ans_list[i][3]+"|"+ans_list[i][4]+"|"+ans_list[i][5]+"|"+ans_list[i][6]+"|"+ans_list[i][7]+"|"+ans_list[i][8]+"|\n")
        print("   "+"+---"*9+"+")
    again=input("\n Play again? (y/n): ")  #詢問玩家是否重新一局
    if again=="y":  #返回是否開新局
        return True
    else:
        return False

def flag_there(input_no):
    #判斷是否已擺放旗子，回傳是否
    if len(input_s)==2:
        if player_list[input_no[0]][input_no[1]]==" F ":
            plot_table(player_list)
            print("\n There is a flag there.\n")
            return True
        else:
            return False

def already_shown(input_no):
    #回傳輸入的位置是否已出現
    if len(input_s)==2:
        if player_list[input_no[0]][input_no[1]]!="   " and player_list[input_no[0]][input_no[1]]!=" F ":
            plot_table(player_list)
            print("\n That cell is already shown.\n")
            return True
        else:
            return False
            
game = True
while game:
    tStart = time.time() #開始計時
    player_list,mines,correct_mines = new_game() 
    input_s,input_no = check_valid() 
    ans_list = creat_ans(input_no)
    player_list = check_0_list(input_no,player_list,ans_list)
    while True: 
        input_s,input_no = check_valid()  #檢查格式是否錯誤，及是否輸入help
        player_list,mines,correct_mines = put_flag(input_s,input_no,mines,correct_mines) #判斷旗子
        if win_or_not(correct_mines):  #判斷輸贏
            game = play_again(ans_list)  #詢問是否再玩一次
            break
        if len(input_s) == 2:
            if flag_there(input_no) or already_shown(input_no):  #檢查是否可插旗和輸入位置
                continue
            elif ans_list[input_no[0]][input_no[1]] == " X ":  #判斷是否輸入到地雷的位置
                print("\n \nGame Over\n")
                game = play_again(ans_list)
                break
            else:
                player_list = check_0_list(input_no,player_list,ans_list)  #繼續遊戲