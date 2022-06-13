board = [
    [7,8,0,4,0,0,1,2,0],
    [6,0,0,0,7,5,0,0,9],
    [0,0,0,6,0,1,0,7,8],
    [0,0,7,0,4,0,2,6,0],
    [0,0,1,0,5,0,9,3,0],
    [9,0,4,0,6,0,0,0,5],
    [0,7,0,3,0,0,0,1,2],
    [1,2,0,0,0,7,4,0,0],
    [0,4,9,2,0,6,0,0,7]
]

def find_zero(board:list[list[int]]):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j]==0:
                return [i,j]

    return None

def solver(board:list[list[int]]):
    
    position=find_zero(board)
    #all spots are full
    if position==None:
        return True
    
    for i in range(1,10):
        if checker(board,position,i):
            board[position[0]][position[1]]=i
            if solver(board):
                return True
            
            board[position[0]][position[1]]=0
    
    return False
    
def checker( board:list[list[int]], position: list, num:int)->bool:
    #row checker
    for i,input in enumerate(board[position[0]]):
        if input==num and i!=position[1]:
            return False
    
    #Col Checker
    for j in range(len(board[0])):
        if board[j][position[1]]==num and position[0]!=j:
            return False

    #box checker
    boundx=position[1]//3
    boundy=position[0]//3
    for i in range(boundy*3,boundy*3 + 3):
        for j in range(boundx*3,boundx*3+3):
            if num==board[i][j] and [i,j]!=position:
                return False
    return True

