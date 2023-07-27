from math import sqrt,log
import random

n=3
start='-'*(n*n)

class Node():
    def __init__(self,state,player=None,pos=None,parent=None):
        self.state=state
        self.player=player
        self.pos=pos
        self.parent=parent
        self.nwin=0
        self.nvisit=0
        self.untried=get_empty(state)
        self.children=[]

    def UCTselect(self):
        s=sorted(self.children, key=lambda c: c.nwin/c.nvisit+sqrt(log(self.nvisit)/c.nvisit))
        return s[-1]

    def makeChild(self,state,pos,player):
        node=Node(state,player,pos,parent=self)
        self.untried.remove(pos)
        self.children.append(node)
        return node

    def update(self,winner):
        self.nvisit+=1
        if winner=='T': # 비긴 경우
            self.nwin+=0.5
        elif winner==self.player:
            self.nwin+=1

    def __repr__(self):
        return str(self.state)+" "+str(self.nwin)+"/"+str(self.nvisit)

def Move(state,pos,player):
    return state[:pos]+player+state[pos+1:]

def switch_player(player):
    return 'X' if player=='O' else 'O'

def print_board(state):
    print('  0123456789012345'[:n+2])
    for i in range(n):
      print(chr(i+97)+':'+state[n*i:n*(i+1)])
        

def get_empty(state):
    if decide_winner(state) in ['O','X','T']: # 승자가 정해지면
        return []
    empty=[]
    for i in range(len(start)):
        if state[i]=='-':
            empty.append(i)
    return empty

def decide_winner(state):
    for (a,b,c) in [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]:
        if state[a]==state[b]==state[c]:
            if state[a]=='O': return 'O'
            elif state[a]=='X': return 'X'
    if [i for i in range(n*n) if state[i]=='-']==[]: return 'T' # Tie (비김)
    return 'N' # 아직 승자 정해지지 않음

def mcts(state,player):
    root=Node(state)

    for i in range(10000):
        node=root
        state=node.state
        roll_player=player
        while node.untried==[] and node.children!=[]: # 선택
            node = node.UCTselect()
            state=Move(state,node.pos,roll_player)
            roll_player=switch_player(roll_player)

        if node.untried!=[]: # 확장
            pos=random.choice(node.untried)
            state=Move(state,pos,roll_player)
            node=node.makeChild(state,pos,roll_player)
            roll_player=switch_player(roll_player)

        while True: # 시뮬레이션
            e=get_empty(state)
            if e==[]: break
            state=Move(state,random.choice(e),roll_player)
            roll_player=switch_player(roll_player)

        winner=decide_winner(state) # 백트랙킹
        while node!=None:
            node.update(winner);
            node = node.parent

    return sorted(root.children,key=lambda c:c.nwin/c.nvisit)[-1].pos

def tictactoe_play(first_mover):
    state=start
    player=first_mover
    print_board(state)
    while True:
        if player=='X':
            print("컴퓨터 차례입니다.")
            pos=mcts(state,player)
        elif player=='O':
            x,y=input("사람 차례입니다. (x와 y를 공백 구분하여 입력하세요.예: 0 c) ").split()
            pos=(ord(y)-97)*n+int(x)
            if state[pos]!='-':
                print("둘 수 없는 곳입니다.")
                continue
        state=Move(state,pos,player)
        print_board(state)
        winner=decide_winner(state)
        if winner in ['O','X','T']:
            if winner=='T': print('비겼습니다.')
            else: print(winner,'가 이겼습니다.')
            break
        player=switch_player(player)

# 틱택토를 시작하는 main
# 사람이 먼저할려면 'O'
# 컴퓨터가 먼저할려면 'X' 
tictactoe_play('O')