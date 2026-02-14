maze=[['x','x',0,'x','x'],
      [0,0,0,0,0],
      ['x',0,'x','x',0],
      ['x',0,0,'x','x'],
      ['x',0,'x','x','x']]

#walls will be coded as 1,2,-1,-2 from the top clockwise
def bounce(x,y,strength,wallHitting,wallEntering):
    global maze
    print(x,y,maze[y][x],strength)
    if strength<=0:
        print("finished a route")
        return
    maze[y][x]+=strength
    #checks if the walls are opposite i.e. the sound is moving straight
    directNext=findNextPlace(wallHitting,x,y)
    if directNext[0]=='x':
        print("hitting a wall directly")
        strength-=2
        if wallHitting+wallEntering==0:
            if abs(wallEntering)==2:
                dirs=(-1,1)
            else:
                dirs=(-2,2)
            print(dirs)
            for dir in dirs:
                next=findNextPlace(dir,x,y)
                print(next[1],next[2])
                if next[0]=='x':
                    bounce(next[1],next[2],strength-2,wallHitting*-1,dir)
                else:
                    bounce(next[1],next[2],strength,wallEntering,dir*-1)
        else:
            barrier=wallEntering*-1
            next=findNextPlace(barrier,x,y)
            if next[0]=='x':
                bounce(next[1],next[2],strength-2,wallHitting*-1,barrier)
            else:
                bounce(next[1],next[2],strength,wallHitting*-1,wallEntering)
    else:
        strength-=1
        if wallEntering+wallHitting==0:
            bounce(directNext[1],directNext[2],strength,wallHitting,wallEntering)
        else:
            bounce(directNext[1],directNext[2],strength,wallHitting*-1,wallEntering*-1)
        

def findNextPlace(wallEntering,x,y):
    global maze
    match wallEntering:
        case -1:
            if(y>0) and maze[y-1][x]!='x':
                return (maze[y-1][x],x,y-1)
            return ('x',x,y)
        case 2:
            if(x<len(maze[0])) and maze[y][x+1]!='x':
                print("moving right")
                return (maze[y][x+1],x+1,y)
            return ('x',x,y)
        case 1:
            if(y<len(maze))and maze[y+1][x]!='x':
                return (maze[y+1][x],x,y+1)
            return ('x',x,y)
        case -2:
            if(x>0) and maze[y][x-1]!='x':
                print("moving left")
                return (maze[y][x-1],x-1,y)
            return ('x',x,y)
        
bounce(2,0,6,1,-1)

for row in maze:
    print(row)