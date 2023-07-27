from math import sqrt,log
import random
import time
#import winsound

n=10
k=5
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
        s=sorted(self.children,key=lambda c:c.nwin/c.nvisit+sqrt(log(self.nvisit)/c.nvisit))
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

def randomAroundCenter(n):
    c=n*(n//2)+n//2
    return random.choice([c,c-1,c+1,c-n,c+n])

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
        if state[i]=='-': continue
        r,c=i//n,i%n
        for (y,x) in [(r-1,c-1),(r-1,c),(r-1,c+1),(r,c-1),(r,c+1),(r+1,c-1),(r+1,c),(r+1,c+1)]:
            if y>=0 and y<=n-1 and x>=0 and x<=n-1 and state[y*n+x]=='-' and y*n+x not in empty:
                empty.append(y*n+x)
    return empty

def decide_winner(state):
    nvoid=0
    for i in range(n*n):
        s=state[i]
        if s=='-': nvoid+=1; continue

        r,c=i//n,i%n

        c1=c-1; c2=c+1
        while c1>=0 and state[r*n+c1]==s: c1-=1
        while c2<=n-1 and state[r*n+c2]==s: c2+=1
        if c2-c1-1==k: return s

        r1=r-1; r2=r+1
        while r1>=0 and state[r1*n+c]==s: r1-=1
        while r2<=n-1 and state[r2*n+c]==s: r2+=1
        if r2-r1-1==k: return s

        r1=r-1; c1=c-1; r2=r+1; c2=c+1
        while r1>=0 and c1>=0 and state[r1*n+c1]==s: r1,c1=r1-1,c1-1
        while r2<=n-1 and c2<=n-1 and state[r2*n+c2]==s: r2,c2=r2+1,c2+1
        if r2-r1-1==k: return s
        
        r1=r-1; c1=c+1; r2=r+1; c2=c-1
        while r1>=0 and c1<=n-1 and state[r1*n+c1]==s: r1,c1=r1-1,c1+1
        while r2<=n-1 and c2>=0 and state[r2*n+c2]==s: r2,c2=r2+1,c2-1
        if r2-r1-1==k: return s

    if nvoid==0: return 'T' # Tie(비김)
    return 'N' # 아직 승자 정해지지 않음

def mcts(state,player):
    root=Node(state)

# 1000 이면 저수준 평균 6초 걸림
# 5000 이면 직관적(그런대로 둠) 평균 35초 걸림

    for i in range(1000):
        node=root
        state=node.state
        roll_player=player
        while node.untried==[] and node.children!=[]: # 선택
            node=node.UCTselect()
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

def omok_selfplay(first_mover):
    state=start
    player=first_mover
    print_board(state)
    while True:
        t1=time.time()
        if player=='X':
            if state==start:
                pos=randomAroundCenter(n)
            else:
                pos=mcts(state,player)
        elif player=='O':
            if state==start:
                pos=randomAroundCenter(n)
            else:
                pos=mcts(state,player)
        state=Move(state,pos,player)
        print_board(state)
        winner=decide_winner(state)
        if winner in ['O','X','T']:
            if winner=='T': print('비겼습니다.')
            else: print(winner,'가 이겼습니다.')
            break
        print('(',player,'가',round(time.time()-t1,3),'초를 썼습니다.)')
        player=switch_player(player)
#        winsound.Beep(frequency=500, duration=250)

omok_selfplay('O')