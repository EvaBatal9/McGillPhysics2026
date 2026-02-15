import Animal as a
import copy
from math import pi, e

maze=[['x','x',0,'x','x'],
      [0,0,0,0,0],
      ['x',0,'x','x',0],
      ['x',0,0,'x','x'],
      ['x',0,'x','x','x']]

NEWmaze=[['x', 'duck', 'x', 'x', 'x', 'lion', 'x', 'x'],
         ['x', 0, 'x', 0, 0, 0, 0, 'x'],
         ['cow', 0, 'fox', 0, 'pig', 'x', 0, 'dog'],
         ['x', 0, 'x', 0, 'x', 0, 0, 'x'],
         ['moose', 0, 'x', 0, 'x', 0, 'x', 'elephant'],
         ['x', 0, 0, 'start', 0, 0, 0, 0],
         ['x', 0, 'x', 'x', 0, 'x', 'x', 'x'],
         ['kathy', 0, 'x', 'x', 'cat', 'x', 'x', 'x']]

avfrequency=500

#walls will be coded as 1,2,-1,-2 from the top clockwise
def bounce(x,y,strength,wallHitting,wallEntering, emptycount):
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
        freqcomplement=[0.1, 0.05, 0.06, 0.07, 0.09]
        freq=[125, 250, 500, 1000, 2000]
        for f in freq:
            if avfrequency<=f:
                dissipation=(1-freqcomplement[freq.index(f)])
            else:
                dissipation=0.91
        strength*=dissipation*(e**-((5.95**-10)*(pi**2)*(avfrequency**2)*emptycount))
        emptycount=1
        print('strength is ',strength)
        if wallHitting+wallEntering==0:
            emptycount+=1
            if abs(wallEntering)==2:
                dirs=(-1,1)
            else:
                dirs=(-2,2)
            print(dirs)
            for dir in dirs:
                next=findNextPlace(dir,x,y)
                print(next[1],next[2])
                if next[0]=='x':
                    bounce(next[1],next[2],strength*dissipation*(e**-((5.95**-10)*(pi**2)*(avfrequency**2)*emptycount)),wallHitting*-1,dir,emptycount)
                else:
                    bounce(next[1],next[2],strength,wallEntering,dir*-1,emptycount)
        else:
            barrier=wallEntering*-1
            next=findNextPlace(barrier,x,y)
            if next[0]=='x':
                bounce(next[1],next[2],strength*dissipation*(e**-((5.95**-10)*(pi**2)*(avfrequency**2)*emptycount)),wallHitting*-1,barrier,emptycount)
            else:
                bounce(next[1],next[2],strength,wallHitting*-1,wallEntering,emptycount)
    else:
        strength*=e**-((5.95**-10)*(pi**2)*(avfrequency**2*emptycount))
        if wallEntering+wallHitting==0:
            emptycount+=1
            bounce(directNext[1],directNext[2],strength,wallHitting,wallEntering,emptycount)
        else:
            bounce(directNext[1],directNext[2],strength,wallHitting*-1,wallEntering*-1,emptycount)
        

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
        
animals=[a.Animal("Duck","sound","frequency","image",6,(2,0),copy.deepcopy(maze)),a.Animal("Cow","sound","frequency","image",8,(1,4),copy.deepcopy(maze))]
dirs={(1,0):(-2,2),(-1,0):(2,-2),(0,1):(-1,1),(0,-1):(1,-1),(1,1):(-1,2),(-1,-1):(1,-2),(1,-1):(1,2),(-1,1):(-1,-2)}

for animal in animals:
    maze=animal.maze
    for dir,orientation in dirs.items():
        if len(maze[0])>animal.location[0]+dir[0]>0 and len(maze)>animal.location[1]+dir[1]>0:
            if maze[animal.location[1]+dir[1]][animal.location[0]+dir[0]]!='x':
                print("sent out")
                bounce(animal.location[0],animal.location[1],animal.soundStrength,orientation[1],orientation[0])

    for row in maze:
        print(row)
