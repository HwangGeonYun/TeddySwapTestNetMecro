import pyautogui as pag
import keyboard
import time
import random
import pyperclip
from datetime import datetime
import random

ADA = 0
DJEDt = 1
IUSDt = 2
TEDYt = 3
HOSKYt = 4
SELECt = 5
name = ["ADA", "DJEDt", "IUSDt", "TEDYt", "HOSKYt"]
select= ['select_ADA.png', 'select_DJEDt.png', 'select_IUSDt.png', 'select_TEDYt.png', 'select_HOSKYt.png']
ft = ['ft_ADA.png', 'ft_DJEDt.png', 'ft_IUSDt.png', 'ft_TEDYt.png', 'ft_HOSKYt.png', 'ft_SELECt.png']

from_ada_to = [DJEDt, IUSDt, TEDYt]
from_djedt_to = [ADA, IUSDt]
from_iusdt_to = [ADA, DJEDt]
from_tedyt_to = [ADA, HOSKYt]
from_hoskyt_to = [TEDYt]

from_which_to = [from_ada_to, from_djedt_to, from_iusdt_to, from_tedyt_to, from_hoskyt_to]

#처음 시작할 때는 반드시 from의 숫자칸에 수를 입력 하면 안된다!!
#나중에 공백인 from숫자칸을 스냅샷으로 찍어 뒀고, 이를 찾기 때문에
#숫자 입력해놓고 돌리면 from숫자칸을 찾지 못한다!


#from과 to를 구별하기 위해 y좌표 계산해주는 함수
def get_pointY(location):
   return int(location[location.find('y')+2:len(location)-1])

#from, to를 순서대로 리스트로 반환해주는 함수
def get_ft_token():
    num = 0
    tokens_num = []
    point_Ys = []
    for i in ft:
        from_to = pag.locateCenterOnScreen(i, confidence=0.8)
        if(from_to != None):
            #toString = str(from_to)
            tokens_num.append(num)
            point_Ys.append(get_pointY(str(from_to)))
        num += 1
    
    if(point_Ys[0]<point_Ys[1]):
        return tokens_num
    #reverse() 안먹힘ㅜㅜ
    else:
        temp = tokens_num[0]
        tokens_num[0] = tokens_num[1]
        tokens_num[1] = temp
        return tokens_num


#from에서 무슨token을 고를지 random하게 선택
def random_select_from(from_token_num):
    num = random.randrange(0, 5)
    time.sleep(0.5)
    
    
    if(num == from_token_num):
        select_from = pag.locateCenterOnScreen('trivial.png', confidence= 0.8)
    else:
        #search = pag.locateCenterOnScreen('search.png', confidence= 0.8)
        time.sleep(1)
        #pag.click(search)
        pag.typewrite(name[num])
        time.sleep(1.5)
        select_from = pag.locateCenterOnScreen(select[num], confidence= 0.8)
    
    pag.click(select_from)
    
    #새로 "선택한 from_token반환
    return num

#to에서 무슨 token을 고를지 random하게 선택
def random_select_to(from_token, to_token):
    can_select_to = from_which_to[from_token]

    num = can_select_to[random.randrange(0,len(can_select_to))]    
    time.sleep(1)
    if(to_token == num):
        select_from = pag.locateCenterOnScreen('trivial.png', confidence= 0.8)
        time.sleep(1)
        pag.click(select_from)
    else:
        pag.typewrite(name[num])
        time.sleep(1.5)
        select_from = pag.locateCenterOnScreen(select[num], confidence=0.8)
        pag.click(select_from)
    
 #balance위에 있는 버튼 선택
def click_ft(x):
    select = pag.locateCenterOnScreen(ft[x],confidence=0.8)
    return select 

while(True):
    
    #balanc위에 있는 from과 to 버튼 
    get_ft = get_ft_token()

    #이전에 선택된 from버튼
    ft_from = click_ft(get_ft[0])
    #이전에 선택된 to버튼
    ft_to = click_ft(get_ft[1])
    pag.click(ft_from)

    time.sleep(2)   
    #새로 선택한 from_token
    from_token = random_select_from(get_ft[0])

    time.sleep(1)
    
    #error가 나서 처음으로 돌아갈때 from에 숫자가 입력되어있어서 if문이 없으면
    #how_much_from이 None으로 초기화됨 
    if(pag.locateCenterOnScreen('from.PNG', confidence=0.8)!=None):
        how_much_from = pag.locateCenterOnScreen('from.PNG', confidence=0.8)

    pag.click(how_much_from)

    time.sleep(1)
    how_much = random.randrange(1, 20)
    pyperclip.copy(str(how_much))
        
    pag.hotkey("ctrl","v")

    pag.click(ft_to)

    random_select_to(from_token, get_ft[1])
    time.sleep(1)


    #인출 최대치를 넘겼을때
    while(pag.locateCenterOnScreen('insufficient.png', confidence =0.8)!=None):
        #print(1)
        pag.click(how_much_from)
        time.sleep(1)
        pag.hotkey("ctrl", "a")
        how_much = how_much/10
        pyperclip.copy(str(how_much))
        pag.hotkey("ctrl", "v")
        time.sleep(0.5)
        
    time.sleep(2)
    
    swap=pag.locateCenterOnScreen('swap.PNG', confidence=0.9)
    pag.click(swap)
    time.sleep(2)
    cs=pag.locateCenterOnScreen('confirmswap.PNG', confidence=0.9)
    pag.click(cs)
    time.sleep(5)
    
    #거래 빠꾸날때 매꾸는 용도
    if(pag.locateCenterOnScreen('error.png', confidence=0.8)):
        trivial = pag.locateCenterOnScreen('trivial.png', confidence=0.8)
        pag.click(trivial)
        pag.click(how_much_from)
        pag.hotkey("ctrl", "a")
        pag.hotkey("ctrl", "x")
        time.sleep(0.5)
        continue
    
    time.sleep(10)
    
    #이터널 용 비밀번호 입력 
    pyperclip.copy("이터널비밀번호")
    pag.hotkey("ctrl","v")
        

    sign=pag.locateCenterOnScreen('sign.png', confidence=0.9)
    pag.click(sign)
    time.sleep(5)
    ex=pag.locateCenterOnScreen('ex.png', confidence=0.5)
    pag.click(ex)
    time.sleep(3) 

    #트잭 쿨타임 때문에 오래 안 쉬면 빠꾸남
    time.sleep(75)