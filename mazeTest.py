import Animal as a
import copy
from math import pi, e, sqrt
from FFTstandard_freq import createValues
from audiopressure import getRms

maze=[['x','x',0,'x','x'],
      [0,0,0,0,0],
      ['x',0,'x','x',0],
      ['x',0,0,'x','x'],
      ['x',0,'x','x','x']]

#NEWmaze=[['x', 'duck', 'x', 'x', 'x', 'lion', 'x', 'x'],
 #        ['x', 0, 'x', 0, 0, 0, 0, 'x'],
 #        ['cow', 0, 'fox', 0, 'pig', 'x', 0, 'dog'],
 #        ['x', 0, 'x', 0, 'x', 0, 0, 'x'],
 #        ['moose', 0, 'x', 0, 'x', 0, 'x', 'elephant'],
 #        ['x', 0, 0, 'start', 0, 0, 0, 0],
 #        ['x', 0, 'x', 'x', 0, 'x', 'x', 'x'],
 #        ['kathy', 0, 'x', 'x', 'cat', 'x', 'x', 'x']]

NEWmaze=[['x', 0, 'x', 'x', 'x', 0, 'x', 'x'],
         ['x', 0, 'x', 0, 0, 0, 0, 'x'],
         [0, 0, 0, 0, 0, 'x', 0, 0],
         ['x', 'x', 'x', 0, 'x', 0, 0, 'x'],
         [0, 0, 'x', 0, 'x', 0, 'x', 0],
         ['x', 0, 0, 0, 0, 0, 0, 0],
         ['x', 0, 'x', 'x', 0, 'x', 'x', 'x'],
         [0, 0, 'x', 'x', 0, 'x', 'x', 'x']]



#walls will be coded as 1,2,-1,-2 from the top clockwise
def bounce(x,y,strength,wallHitting,wallEntering, emptycount, mean_freq):
    global NEWmaze
    print(x,y,NEWmaze[y][x],strength)
    if strength<=0.1: #temporarily 3, but should be a number based on how long we want the wave to propagate for
        print("finished a route")
        return
    NEWmaze[y][x]+=strength
    #checks if the walls are opposite i.e. the sound is moving straight
    directNext=findNextPlace(wallHitting,x,y)
    if directNext[0]=='x':
        print("hitting a wall directly")
        #freqcomplement=[0.1, 0.05, 0.06, 0.07, 0.09]
        freqcomplement=[0.4, 0.34, 0.25, 0.19, 0.15]
        freq=[125, 250, 500, 1000, 2000]
        for f in freq:
            if mean_freq<=f:
                dissipation=(1-freqcomplement[freq.index(f)])
            else:
                dissipation=0.5
        strength*=round(dissipation*(e**-((5.95**-10)*(pi**2)*(mean_freq**2)*emptycount)),4)
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
                    bounce(next[1],next[2],round(strength*dissipation*(e**-((5.95**-10)*(pi**2)*(mean_freq**2)*emptycount)),4),wallHitting*-1,dir,emptycount,mean_freq)
                else:
                    bounce(next[1],next[2],strength,wallEntering,dir*-1,emptycount,mean_freq)
        else:
            barrier=wallEntering*-1
            next=findNextPlace(barrier,x,y)
            if next[0]=='x':
                bounce(next[1],next[2],round(strength*dissipation*(e**-((5.95**-10)*(pi**2)*(mean_freq**2)*emptycount*sqrt(2))),4),wallHitting*-1,barrier,emptycount,mean_freq)
            else:
                bounce(next[1],next[2],strength,wallHitting*-1,wallEntering,emptycount,mean_freq)
    else:
        strength*=round(e**-((5.95**-10)*(pi**2)*(mean_freq**2*emptycount)),4)
        if wallEntering+wallHitting==0:
            emptycount+=1
            bounce(directNext[1],directNext[2],strength,wallHitting,wallEntering,emptycount,mean_freq)
        else:
            bounce(directNext[1],directNext[2],strength,wallHitting*-1,wallEntering*-1,emptycount,mean_freq)
        

def findNextPlace(wallEntering,x,y):
    global NEWmaze
    match wallEntering:
        case -1:
            if(y>0):
                if NEWmaze[y-1][x]!='x':
                    return (NEWmaze[y-1][x],x,y-1)
                return ('x',x,y)
            return ('x',x,y)
        case 2:
            if(x<len(NEWmaze[0])-1):
                if NEWmaze[y][x+1]!='x':
                    print("moving right")
                    return (NEWmaze[y][x+1],x+1,y)
                return ('x',x,y)
            return ('x',x,y)
        case 1:
            if(y<len(NEWmaze)-1):
                if NEWmaze[y+1][x]!='x':
                    return (NEWmaze[y+1][x],x,y+1)
                return ('x',x,y)
            return ('x',x,y)
        case -2:
            if(x>0): 
                if NEWmaze[y][x-1]!='x':
                    print("moving left")
                    return (NEWmaze[y][x-1],x-1,y)
                return ('x',x,y)
            return ('x',x,y)
        
animals=[a.Animal("Duck","sound","frequency","image",9,(1,0),copy.deepcopy(NEWmaze)),a.Animal("Cat","sound","frequency","image",8,(4,7),copy.deepcopy(NEWmaze)),a.Animal("Cow","sound","frequency","image",8,(0,2),copy.deepcopy(NEWmaze)),a.Animal("Dog","sound","frequency","image",8,(7,2),copy.deepcopy(NEWmaze)),a.Animal("Donkey","sound","frequency","image",6,(0,4),copy.deepcopy(NEWmaze)),a.Animal("Kathy","sound","frequency","image",6,(0,7),copy.deepcopy(NEWmaze)),a.Animal("Lion","sound","frequency","image",6,(5,0),copy.deepcopy(NEWmaze)),a.Animal("Monkey","sound","frequency","image",6,(7,4),copy.deepcopy(NEWmaze)),a.Animal("Pig","sound","frequency","image",6,(4,2),copy.deepcopy(NEWmaze))]
dirs={(1,0):(-2,2),(-1,0):(2,-2),(0,1):(-1,1),(0,-1):(1,-1),(1,1):(-1,2),(-1,-1):(1,-2),(1,-1):(1,2),(-1,1):(-1,-2)}

createValues(animals)
getRms(animals)

for animal in animals:
    NEWmaze=animal.maze
    NEWmaze[animal.location[1]][animal.location[0]]+=animal.soundStrength
    for dir,orientation in dirs.items():
        if len(NEWmaze[0])>animal.location[0]+dir[0]>0 and len(NEWmaze)>animal.location[1]+dir[1]>0:
            if NEWmaze[animal.location[1]+dir[1]][animal.location[0]+dir[0]]!='x':
                print("sent out")
                print(dir)
                bounce(animal.location[0],animal.location[1],float(animal.rms*1000),orientation[1],orientation[0],1,animal.meanFreq)
                print(animal.meanFreq, animal.meanPressure)

    for row in NEWmaze:
        print(row)
    print(animal.name)
