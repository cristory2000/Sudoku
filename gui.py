
import pygame as game
import copy

from sudoku import checker,find_zero,board
game.font.init()



class Graph:
    def __init__(self,board,rows,cols,width,height):
        self.board=board
        self.rows=rows
        self.cols=cols
        self.height=height
        self.width=width
        self.cubes=[[Block(self.board[i][j],i,j,self.width,self.height) for j in range(self.cols)]for i in range(self.rows)]
        self.selected=None
    #draw board
    def draw(self,window):
        gap=self.width / 9
        
        for i in range(self.rows+1):
            if i % 3 ==0:
                thick=4
            else:
                thick=1
            # lines across
            game.draw.line(window,(0,0,0),( 0 ,i * gap),(self.width,i*gap),thick)
            # lines down
            game.draw.line(window,(0,0,0),(i * gap,0),(i*gap,self.height),thick)
        
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] != self.cubes[i][j].value:
                    self.cubes[i][j].draw(window,(0,0,200))
                else:
                    self.cubes[i][j].draw(window,(0,0,0))
    
    def checker(self,position,window):
        
        if position[1]>600:
            
            return None
        gap=self.width/9
        col=position[0]//gap
        row=position[1]//gap
        if self.board[int(row)][int(col)]!=0:
            return None
        game.draw.rect(window,(220,220,220),(col*gap,row*gap,gap,gap))
        game.display.update()
        return (row,col)
     
    def update(self,position,key):
        self.cubes[int(position[0])] [int(position[1])].value=key
    def find_zero(self):
        for i in range(len(self.cubes)):
                for j in range(len(self.cubes[0])):
                    if self.cubes[i][j].value ==0:
                        return True
        return False
class Block:
    rows=9
    cols=9
    def __init__(self,value,row,col,width,height):
        self.row=row
        self.col=col
        self.width=width
        self.height=height
        self.value=value
    def draw(self,window,color):
        
        #set font
        fnt = game.font.SysFont("comicsans", 40)
        #get placements
        gap=self.width/9
        x=self.col*gap
        y=self.row*gap
        if self.value !=0:
            text=fnt.render(str(self.value),1,color)
            window.blit(text,((x + (gap/2 - text.get_width()/2),y + (gap/2 - text.get_height()/2))))

def draw_solve(window,position=None):
    #set font
    fnt = game.font.SysFont("comicsans", 30)
    text=fnt.render('Solve',1,(0,0,0))
    if position!=None:
        if position[0]>=600/2-text.get_width()/2 and position[0]<=600/2-text.get_width()/2+text.get_width()+10 and position[1]>=650-text.get_height()/2 and position[1]<=650+text.get_height()/2+10:
            r=game.draw.rect(window,(220,220,220),(600/2-text.get_width()/2,650-text.get_height()/2,text.get_width()+10,text.get_height()+10),3)
            window.blit(text,r.inflate(-10,-10))
            game.display.update()
            return True
    
    r=game.draw.rect(window,(0,0,0),(600/2-text.get_width()/2,650-text.get_height()/2,text.get_width()+10,text.get_height()+10),3)
    window.blit(text,r.inflate(-10,-10))
    return False
def checkend(graph,answer)-> bool:
    for i in range(len(graph.cubes)):
        for j in range(len(graph.cubes[0])):
            if graph.cubes[i][j].value!=answer[i][j]:
                 return False
    return True

def solver(board:list[list[int]],graph=None,window=None):
    
    position=find_zero(board)
    #all spots are full
    if position==None:
        return True
    
    for i in range(1,10):
        if checker(board,position,i):
            board[position[0]][position[1]]=i
            if graph!=None and window !=None:
                graph.cubes[position[0]][position[1]].value=i
                window.fill((255,255,255))
                graph.draw(window)
                game.display.update()
                game.time.delay(100)
            if solver(board,graph,window):
                return True
            
            board[position[0]][position[1]]=0
            if graph!=None and window !=None:
                graph.cubes[position[0]][position[1]].value=0
                window.fill((255,255,255))
                graph.draw(window)
                game.display.update()
                game.time.delay(100)

    return False
def main():
    #give name and icon
    game.display.set_caption("Sudoku")
    icon=game.image.load('sudoku.png')
    game.display.set_icon(icon)

    #create and init window
    window=game.display.set_mode((600,700))
    graph=Graph(board,9,9,600,600)
    window.fill((255,255,255))
    graph.draw(window)
    game.draw.rect(window,(0,0,0),(600/2,650,30,30),3)
    #game.display.update()
    running =True
    key=None
    checker=None
    position=None
    solve=False
    answer=copy.deepcopy(board)
    solver(answer)
    while running:
        for event in game.event.get():
            if event.type == game.QUIT:
                running=False
            if event.type==game.KEYDOWN:
                if event.key==game.K_0:
                    key=0
                if event.key==game.K_1:
                    key=1
                if event.key==game.K_2:
                    key=2
                if event.key==game.K_3:
                    key=3
                if event.key==game.K_4:
                    key=4
                if event.key==game.K_5:
                    key=5
                if event.key==game.K_6:
                    key=6
                if event.key==game.K_7:
                    key=7
                if event.key==game.K_8:
                    key=8
                if event.key==game.K_9:
                    key=9
            #see where on the board was pressed
            if event.type==game.MOUSEBUTTONDOWN:
                position=game.mouse.get_pos()
                window.fill((255,255,255))
                graph.draw(window)
                solve=draw_solve(window,position)
                #returns board coordinates
                checker=graph.checker(position,window)
        #add number to graph 
        if key!=None and checker!=None:
            graph.update(checker,key)
            checker=None
            key=None
        #refresh display
        if checker==None:
            window.fill((255,255,255))
            graph.draw(window)
            draw_solve(window,position)
        #solve using recursion
        if solve==True:
            solver(board,graph,window)
            solve=False
            for i in range(len(graph.cubes)):
                for j in range(len(graph.cubes[0])):
                    graph.cubes[i][j].value=board[i][j]
            graph.draw(window)
        #check if game is done
        if graph.find_zero()==False:
            if checkend(graph,answer):
                running=False
                game.display.update()
                game.time.delay(5000)       
        game.display.update()
main()
