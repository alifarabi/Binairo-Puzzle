from copy import deepcopy, copy
from email import iterators
import math
from os import stat
import re
from threading import local
from tkinter.messagebox import NO
import State
import numpy as np
from collections import Counter, deque

        

def check_Adjancy_Limit(state: State):
    #check rows
    for i in range(0,state.size):
        for j in range(0,state.size-2):
            if(state.board[i][j].value.upper()==state.board[i][j+1].value.upper() and 
            state.board[i][j+1].value.upper()==state.board[i][j+2].value.upper() and
            state.board[i][j].value !='_'and 
            state.board[i][j+1].value !='_'and
            state.board[i][j+2].value !='_' ):
                
                return False
    #check cols
    for j in range(0,state.size): # cols
        for i in range(0,state.size-2): # rows
            if(state.board[i][j].value.upper()==state.board[i+1][j].value.upper() 
            and state.board[i+1][j].value.upper()==state.board[i+2][j].value.upper() 
            and state.board[i][j].value !='_'
            and state.board[i+1][j].value !='_'
            and state.board[i+2][j].value !='_' ):
               
                return False
    
    return True

def check_circles_limit(state:State): # returns false if number of white or black circles exceeds board_size/2
    #check in rows
    for i in range(0,state.size): # rows
        no_white_row=0
        no_black_row=0
        for j in range(0,state.size): # each col
            # if cell is black or white and it is not empty (!= '__')
            if (state.board[i][j].value.upper()=='W' and state.board[i][j].value != '_'): no_white_row+=1
            if (state.board[i][j].value.upper()=='B' and state.board[i][j].value != '_'): no_black_row+=1
        if no_white_row > state.size/2 or no_black_row > state.size/2:
            
            return False
        no_black_row=0
        no_white_row=0

    # check in cols
    for j in range(0,state.size):#cols
        no_white_col=0
        no_black_col=0
        for i in range(0,state.size): # each row
            # if cell is black or white and it is not empty (!= '__')
            if (state.board[i][j].value.upper()=='W' and state.board[i][j].value != '_'): no_white_col+=1
            if (state.board[i][j].value.upper()=='B' and state.board[i][j].value != '_'): no_black_col+=1
        if no_white_col > state.size/2 or no_black_col > state.size/2:
            
            return False
        no_black_col=0
        no_white_col=0
    
    return True

def is_unique(state:State): # checks if all rows are unique && checks if all cols are unique
    # check rows
    for i in range(0,state.size-1):
        for j in range(i+1,state.size):
            count = 0
            for k in range(0,state.size):
                if(state.board[i][k].value.upper()==state.board[j][k].value.upper()
                and state.board[i][k].value!='_'
                and state.board[j][k].value!='_'):
                    count+=1
            if count==state.size:
                
                return False
            count=0

    # check cols
    for j in range(0,state.size-1):
        for k in range(j+1,state.size):
            count_col =0 
            for i in range(0,state.size):
                 if(state.board[i][j].value.upper()==state.board[i][k].value.upper()
                 and state.board[i][j].value != '_'
                 and state.board[i][k].value != '_' ):
                    count_col+=1
            if count_col == state.size:
               
                return False
            count_col=0 
   
    return True

def is_assignment_complete(state:State): # check if all variables are assigned or not
    for i in range(0,state.size):
        for j in range(0,state.size):
            if(state.board[i][j].value == '_'): # exists a variable wich is not assigned (empty '_')
                
                return False

    
    return True

def is_consistent(state:State):
    return check_Adjancy_Limit(state)  and check_circles_limit(state) and is_unique(state)

def check_termination(state:State):
    
    return is_consistent(state) and is_assignment_complete(state)

def mrv(state:State):
    stack_candide = []
    for row in state.board:
        for cell in row:
            if not cell.isEmpty():
                continue
            deleted = False
            cell.dl = len(cell.domain)
            for vv in cell.domain:
                cell.value = vv
                if not is_consistent(state):
                    cell.dl -= 1
                    deleted = True
                cell.value = '_'
            if deleted:
                stack_candide.append(cell)
    if len(stack_candide) == 0:
        return None
    stack_candide.sort(key=lambda x:x.dl)
    return stack_candide[0]


def backtrack_ok(state):
    forward_check(state,state.board[1][9])

def forward_check(state, cell):
    # copy state 
    local_state = deepcopy(state)
    # save row and col index
    row = cell.x
    col = cell.y
    # use numpy to map board and easly count it
    board = np.array([list(map(lambda n: n.value.upper(), x)) for x in local_state.board])
    row_tbl_count = Counter(board[row, :])
    col_tbl_count = Counter(board[:, col])
    # for col and row check same color
    for idx, el in enumerate([row_tbl_count,col_tbl_count]):
        del el['_']
        color, count = el.most_common(1)[0]
        if count == local_state.size / 2:
            if idx == 0: # we check row
                for cell in local_state.board[row]:
                    if cell.isEmpty():
                        # check if cell hasn't any color we set opposit color for cell
                        cell.value = 'b' if color == 'W' else 'w'
                        board[cell.x][cell.y] = 'B' if color == 'W' else 'W'
            elif idx == 1: # we check col
                for cell in list(zip(*local_state.board))[col]:
                    if cell.isEmpty():
                        # check if cell hasn't any color we set opposit color for cell
                        cell.value = 'b' if color == 'W' else 'w'
                        board[cell.x][cell.y] = 'B' if color == 'W' else 'W'
    i = 0 
    while i < local_state.size - 2:
        if local_state.board[row][i].isEmpty():
            if ( not local_state.board[row][i+1].isEmpty() and 
            local_state.board[row][i+1].value.upper() == local_state.board[row][i+2].value.upper()):
                local_state.board[row][i].value = 'W' if local_state.board[row][i+1].value.upper() == 'B' else 'B'
        else:
            if local_state.board[row][i].value.upper() == local_state.board[row][i+1].value.upper() and local_state.board[row][i+2].isEmpty():
                local_state.board[row][i+2].value = 'W' if local_state.board[row][i].value.upper() == 'B' else 'B'

        if local_state.board[i][col].isEmpty():
            if ( not local_state.board[i+1][col].isEmpty() and 
            local_state.board[i+1][col].value.upper() == local_state.board[i+2][col].value.upper()):
                local_state.board[i][col].value = 'W' if local_state.board[i+1][col].value.upper() == 'B' else 'B'
        else:
            if local_state.board[i][col].value.upper() == local_state.board[i+1][col].value.upper() and local_state.board[i+2][col].isEmpty():
                local_state.board[i+2][col].value = 'W' if local_state.board[i][col].value.upper() == 'B' else 'B'
        i+=1
    
    return local_state


    white_colored, black_colored = [0,0]

    for cell in local_state.board[row]:
        value = cell.value.upper()
        if value == 'W':
            white_colored += 1
        elif value == 'B':
            black_colored += 1
    if white_colored == local_state.size / 2:
        for cell in local_state.board[row]:
            if cell.isEmpty():
                cell.value = 'b'
    elif black_colored == local_state.size / 2:
        for cell in local_state.board[row]:
            if cell.isEmpty():
                cell.value = 'w'

    white_colored, black_colored = [0,0]

    for cell in local_state:
        pass


def backtrack_jon(state: State):
    if check_termination(state):
        return state

    limited_item = mrv(state)

    if limited_item is None:
        for row in state.board:
            for cell in row:
                if cell.isEmpty():
                    limited_item = cell
                    break
            else:
                # Continue if the inner loop wasn't broken.
                continue
            # Inner loop was broken, break the outer.
            break


    if len(limited_item.domain) == 1:
        local_state = deepcopy(state)
        local_state.board[limited_item.x][limited_item.y].value = limited_item.domain[0]
        new_state = forward_check(local_state, limited_item)
        if is_consistent(new_state):
            res = backtrack_jon(new_state)
            if res is not None:
                return res
    
    row = limited_item.x
    col = limited_item.y

    # use numpy to map board and easly count it
    board = np.array([list(map(lambda n: n.value.upper(), x)) for x in state.board])
    row_tbl_count = Counter(board[row, :])
    col_tbl_count = Counter(board[:, col])


    white_count = row_tbl_count['W'] + col_tbl_count['W']
    black_count = row_tbl_count['B'] + col_tbl_count['B']

    if white_count > black_count:
        limited_item.domain.reverse()
    
    for domain in limited_item.domain:
        local_state = deepcopy(state)
        local_state.board[limited_item.x][limited_item.y].value = domain
        new_state = forward_check(local_state, limited_item)

        if is_consistent(new_state):
            res = backtrack_jon(new_state)
            if res is not None:
                return res
    return None    

    # if limited_item:
    #     state.board[limited_item.x][limited_item.y].value = state.board[limited_item.x][limited_item.y].domain.pop(0)
    #     backtrack_jon(state)

def backtrack_mrv(state):
    if is_assignment_complete(state):
        return state

    fCell = mrv(state)
    if not fCell:
        for i in range(state.size):
            for j in range(state.size):
                if state.board[i][j].isEmpty():
                    fCell = state.board[i][j]
                    break
            else:
                continue
            break
    for domain in fCell.domain:
        local_state = deepcopy(state)
        local_state.board[fCell.x][fCell.y].value = domain
        if is_consistent(local_state):
            res = backtrack_mrv(local_state)
            if res is not None:
                return res
    return None


# def ac3(state):
#     local_state = deepcopy(state)
#     q = deque()

#     for row in state.board:
#         for cell in row:
#             if cell.isEmpty():
#                 for c in range(state.size):
#                     if c != cell.x:
#                         q.append((cell,local_state.board[cell.x][c]))
#                 for r in range(state.size):
#                     if r != cell.y:
#                         q.append((cell,local_state.board[r][cell.y]))

#     while q:
#         arc = q.popleft()
#         first_cell = arc[0]
#         secound_cell = arc[1]
#         if first_cell.isEmpty():
#             for d in first_cell.domain:
#                 new_state = deepcopy(state)
#                 new_state.board[first_cell.x][first_cell.y].value = d
#                 not_consistent = True
#                 if secound_cell.isEmpty():
#                     for d2 in secound_cell.domain:
#                         new_state.board[secound_cell.x][secound_cell.y].value = d2
#                         if is_consistent(new_state):
#                             not_consistent = False
#                             break
#                 else:
#                     if is_consistent(new_state):
#                         not_consistent = False
#                 if not_consistent:
#                     if len(first_cell.domain) == 1:
#                         continue
#                     first_cell.domain.remove(d)
#                     first_cell.value = first_cell.domain[0]

#                     for c in range(state.size):
#                         if c != first_cell.y:
#                             q.append((local_state.board[first_cell.x][c], first_cell))
#                     for r in range(state.size):
#                         if r != first_cell.x:
#                             q.append((local_state.board[r][first_cell.y], first_cell))
#     return state
    