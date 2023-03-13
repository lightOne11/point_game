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
from copy import deepcopy


class point_game():
    def __init__(self,place_n=5,player_n=2,siege=True):
        self.place_n,self.player_n,self.siege = place_n,player_n,siege

        # 턴 초기화
        self.turn = 0
        self.encircle = -1
        # self.start_ = 0

        # 플레이어 초기화
        self.player = {}
        print('-- 참가 플레이어 --')
        for i in range(1,player_n+1):
            self.player[f'{i} player'] = []
            print(f'{i} player')

        # 필드 초기화
        pla = np.array(range(1, place_n*place_n+1))
        rm.shuffle(pla)
        self.place = pla.reshape(place_n,place_n).tolist()
        self.place_o = deepcopy(self.place)
        self.way = ''
        self.way_p = []
        
        # 필드 외곽 설정
        self.way_list = self.matinit(place_n)

        # 게임 실행
        self.main()
        # self.dir_x1,self.dir_y1 = 0,0

    def matinit(self,place_n):

        # 필드 외곽 설정
        way_list = np.ones((place_n+2,place_n+2),dtype='object')
        way_list[1:place_n+1,1:place_n+1] = 0
        return way_list
        
    def main(self):
        while True: 
            if self.turn == 0:                
                for i in sorted(range(1,self.player_n+1),reverse=True):
                    self.play = i
                    self.start()
            else :  
                self.play = (self.turn%self.player_n)+1
                self.move()
            if self.way_p == True: break
            if self.way == 'x': break
            self.dischange()
        if self.siege == True and self.way == 'x' : self.move()
        self.exit()
        self.gamesave()

    def dischange(self):
        if self.turn > self.player_n*2 :
            palyer = self.player[f'{self.play} player']
            last_way = [palyer[1][-1][0] - palyer[1][-2][0],palyer[1][-1][1] - palyer[1][-2][1]]
            if last_way == [-1,0]: self.place[palyer[1][-2][0]-1][palyer[1][-2][1]-1] = '^'
            elif last_way == [0,-1]: self.place[palyer[1][-2][0]-1][palyer[1][-2][1]-1] = '<'
            elif last_way == [0,1]: self.place[palyer[1][-2][0]-1][palyer[1][-2][1]-1] = '>'
            elif last_way == [1,0]: self.place[palyer[1][-2][0]-1][palyer[1][-2][1]-1] = 'v'

    def start(self):
        self.display()
        while True:
            try:
                self.way = input(f'[{self.play}player] 좌표를 입력하세요(종료x)')
                if self.way == 'x': break
                x,y=map(int,self.way.split('.'))
                if self.condition(x,y)== True:                                
                    break                        
            except: pass
        if self.way == 'x': return               
        self.player[f'{self.play} player'].append(int(self.place[x-1][y-1]))
        self.player[f'{self.play} player'].append([[x,y]])
        self.way_list[x,y] = str(self.play)+'P'
        self.place[x-1][y-1] = str(self.play)+'P'
        #print(f'위치 선택 후 위치 점수 : {self.place[x][y]}\n플레이어번호 : {i}')
        self.turn += 1

    def move(self):
        self.turn += 1
        print(f'-----{self.turn//self.player_n} round ------')
        if self.play == self.encircle: return
        else :
            while True:
                self.display()
                x,y = self.player[f'{self.play} player'][1][-1]
                self.way=input(f'[{self.play} player] 방향을 입력하세요(종료x)')
                #print(f'방향 입력 후 입력 : {way}\n입력리스트 \n{way_list}\n현재위치 : {x},{y}\n이동가능여부 : {self.condition(way,way_list,x,y)}')
                if self.condition(x,y) == True:
                    if self.way == '8': 
                        self.player[f'{self.play} player'][1].append([x-1,y])
                        break
                    elif self.way == '4': 
                        self.player[f'{self.play} player'][1].append([x,y-1])
                        break
                    elif self.way == '6': 
                        self.player[f'{self.play} player'][1].append([x,y+1])
                        break
                    elif self.way == '2': 
                        self.player[f'{self.play} player'][1].append([x+1,y])
                        break
                if self.way == 'x': break
                print('방향을 다시 입력해주세요')
            if self.way == 'x': return
            x,y = self.player[f'{self.play} player'][1][-1]
            self.player[f'{self.play} player'][0] +=int(self.place[x-1][y-1])
            self.place[x-1][y-1] = str(self.play)+'P'
            self.way_list[x,y] = str(self.play)+'P'
            for p in range(1,self.player_n+1):
                way_p = []
                x,y = self.player[f'{p} player'][1][-1]
                for l,m in [[x+1,y],[x-1,y],[x,y+1],[x,y-1]]:
                    way_p.append(self.way_list[l,m] != 0)
                    #print(f'이동후 방향 : {l},{m}\n이동 가능 여부 : {way_list[l,m]}\n이동리스트 : \n{way_list}')
                #print(f'이동불가방향 : {way_p}')
                if way_p == [True,True,True,True] :
                    self.way_p = True
                    self.encircle = self.play
                    break
            if self.way_p == True: return


    def gamesave(self):
        pass
        #print(self.place_o)
        #print(self.player)
        #pd.DataFrame(self.place_o+list(self.player)).to_csv('https://drive.google.com/drive/folders/17OdUEiltOKPB4v65Fk5euoJSNOJRmEyr?usp=share_link')

    def exit(self):
        self.display()
        print(f'{self.turn//self.player_n} round로 게임이 끝났습니다.')
        if self.way == 'x' : # and not self.turn == 0 :
            self.player[f'{self.play} player'][0] = 0 
            print(f'{self.play}player 의 기권입니다.')
        #if len(self.player[f'1 player'])!=0 :
        win_p = 0
        for i in range(1,self.player_n+1):
            p = self.player[f'{i} player']
            print(f'{i}P :',p[0],'점',end='\t')
            if win_p < p[0]:
                win_p = p[0]
                win_n = i

        #if not self.turn == 0 : 
        print(f'\n승자는 {win_n} player 입니다.')


    def display(self):
        for x in range(self.place_n):
            for y in range(self.place_n):
                print(f'{str(self.place[x][y]):3s}',end=' ')
            print()
        print('------------------')
        if len(self.player[f'1 player'])!=0 :
            for i in range(1,self.player_n+1):
                p = self.player[f'{i} player']
                print(f'{i}P :',p[0],'점 ,',f'[{p[1][-1][0],p[1][-1][1]}]',end='\t')
                print()

    def condition(self,x,y):
        if self.way == '8' and self.way_list[x-1,y] != 0:
            print('(8) 갈수 없는 곳입니다.')
            return False
        elif self.way == '4' and self.way_list[x,y-1] != 0:
            print('(4) 갈수 없는 곳입니다.')
            return False
        elif self.way == '6' and self.way_list[x,y+1] != 0:
            print('(6) 갈수 없는 곳입니다.')
            return False
        elif self.way == '2' and self.way_list[x+1,y] != 0:
            print('(2) 갈수 없는 곳입니다.')
            return False   
        elif len(self.player[f'1 player'])==0 and self.way_list[x,y] != 0:
            print('(5) 갈수 없는 곳입니다.')
            return False                    
        else : 
            #print(f'현재위치 : {x},{y}')
            return True



point_game(7)