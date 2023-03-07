# 점수 게임
# 1. 인원 2 (옵션 ~4)
# 2. 역순으로 처음지점 선택
# 3. 처음지점에서 좌,우,상,하 이동 (옵션 대각이동)
# 4. 선택한 곳의 점수를 더함
# 5. 다음에 갈곳이 없으면 게임 종료
# 6. 종료 시 점수가 높은쪽이 승
# 7. 게임판 기본 5*5 (옵션 n)
# 8. 게임판에는 1~칸수까지 번호가 적혀있음
# 9. 다른 사람이 선택한 곳은 지나갈 수 없음
import numpy as np
import random as rm
import torch
import torch.nn as nn

class com:
    def __init__(self,input_X,result_Y,outcome_Y):
        pass
    





class point_game():
    def __init__(self,place_n=5,player_n=2):
        self.place_n = place_n
        self.player_n = player_n
        self.player = {}
        print('-- 참가 플레이어 --')
        for i in range(1,player_n+1):
            self.player[f'{i} player'] = []
            print(f'{i} player')
        pla = np.array(range(1, place_n*place_n+1))
        rm.shuffle(pla)
        self.place = pla.reshape(place_n,place_n).tolist()
        way_list = self.matinit(place_n)
        self.main(way_list)

    def matinit(self,place_n):
        way_list = np.ones((place_n+2,place_n+2))
        way_list[1:place_n+1,1:place_n+1] = 0
        return way_list
        

    def main(self,way_list):
        way = ''
        way_p = []
        while True: 
            if len(self.player[f'1 player'])==0:
                for i in sorted(range(1,self.player_n+1),reverse=True):
                    self.display()
                    while True:
                        try:
                            x,y=map(int,input(f'[{i}player] 좌표를 입력하세요').split())
                            if self.condition(way,way_list,x,y)== True:                                
                                break
                        except: pass               
                    self.player[f'{i} player'].append(self.place[x-1][y-1])
                    self.player[f'{i} player'].append([[x,y]])
                    way_list[x,y] = i*100
                    self.place[x-1][y-1] = i*100
                    #print(f'위치 선택 후 위치 점수 : {self.place[x][y]}\n플레이어번호 : {i}')
            else :
                turn = 0
                while True:
                    turn += 1
                    print(f'-----{turn} round ------')
                    for i in range(1,self.player_n+1):
                        while True:
                            self.display()
                            x,y = self.player[f'{i} player'][1][-1]
                            way=input(f'[{i} player] 방향을 입력하세요(종료x)')
                            #print(f'방향 입력 후 입력 : {way}\n입력리스트 \n{way_list}\n현재위치 : {x},{y}\n이동가능여부 : {self.condition(way,way_list,x,y)}')
                            if self.condition(way,way_list,x,y) == True:
                                if way == '8': 
                                    self.player[f'{i} player'][1].append([x-1,y])
                                    break
                                elif way == '4': 
                                    self.player[f'{i} player'][1].append([x,y-1])
                                    break
                                elif way == '6': 
                                    self.player[f'{i} player'][1].append([x,y+1])
                                    break
                                elif way == '2': 
                                    self.player[f'{i} player'][1].append([x+1,y])
                                    break
                            if way == 'x': break
                            print('방향을 다시 입력해주세요')
                        if way == 'x': break
                        x,y = self.player[f'{i} player'][1][-1]
                        self.player[f'{i} player'][0] +=self.place[x-1][y-1]
                        self.place[x-1][y-1] = i*100
                        way_list[x,y] = i*100
                        for p in range(1,self.player_n+1):
                            way_p = []
                            x,y = self.player[f'{p} player'][1][-1]
                            for l,m in [[x+1,y],[x-1,y],[x,y+1],[x,y-1]]:
                                way_p.append(way_list[l,m] != 0)
                                #print(f'이동후 방향 : {l},{m}\n이동 가능 여부 : {way_list[l,m]}\n이동리스트 : \n{way_list}')
                            #print(f'이동불가방향 : {way_p}')
                            if way_p == [True,True,True,True] :
                                way_p = True
                                break
                        if way_p == True: break                
                    if way_p == True: break
                    if way == 'x': break
            if way_p == True: break
            if way == 'x': break
        self.exit(turn,way,i)

    def exit(self,turn,way,i):
        self.display()
        print(f'{turn} round로 게임이 끝났습니다.')
        if way == 'x' :
            self.player[f'{i} player'][0] = 0 
            print(f'{i}player 의 기권입니다.')
        if len(self.player[f'1 player'])!=0 :
            win_p = 0
            for i in range(1,self.player_n+1):
                p = self.player[f'{i} player']
                print(f'{i}P :',p[0],'점',end='\t')
                if win_p < p[0]:
                    win_p = p[0]
                    win_n = i

        print(f'\n승자는 {win_n} player 입니다.')


    def display(self):
        for x in range(self.place_n):
            for y in range(self.place_n):
                print(f'{self.place[x][y]:3d}',end=' ')
            print()
        print('------------------')
        if len(self.player[f'1 player'])!=0 :
            for i in range(1,self.player_n+1):
                p = self.player[f'{i} player']
                print(f'{i}P :',p[0],'점 ,',f'[{p[1][-1][0],p[1][-1][1]}]',end='\t')
                print()

    def condition(self,way,way_list,x,y):
        if way == '8' and way_list[x-1,y] != 0:
            print('(8) 갈수 없는 곳입니다.')
            return False
        elif way == '4' and way_list[x,y-1] != 0:
            print('(4) 갈수 없는 곳입니다.')
            return False
        elif way == '6' and way_list[x,y+1] != 0:
            print('(6) 갈수 없는 곳입니다.')
            return False
        elif way == '2' and way_list[x+1,y] != 0:
            print('(2) 갈수 없는 곳입니다.')
            return False   
        elif len(self.player[f'1 player'])==0 and way_list[x,y] != 0:
            print('(5) 갈수 없는 곳입니다.')
            return False                    
        else : 
            #print(f'현재위치 : {x},{y}')
            return True



point_game(7)