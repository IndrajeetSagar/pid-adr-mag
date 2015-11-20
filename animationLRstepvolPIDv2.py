


import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
import math




xi=0       #time
xf=6000
dnum=1000

indres=40e-3#+uniform(0,1)*1e-5 #inductor resitance
dt=5   #wait time
L=35
R=40e-3


ri=1e-3      # voltage step
rf=10e-3
rnum=500.0
dr=(rf-ri)/rnum

# First set up the figure, the axis, and the plot element we want to animate
fig = plt.figure()
ax = plt.axes(xlim=(xi, xf),ylim=(0,10))
ax.grid()
line, = ax.plot([], [], lw=1)
line1, = ax.plot([], [], lw=1)
line2, = ax.plot([], [], lw=1)
time_template = 'step voltage = %.6f'
time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)



def indvolcal(indvol,stepvol,dt):
    
    ti=(indvol[-1]+stepvol)*math.exp(-dt*R/L)
    return ti

def indcurcalc(vol,ivol):
    curr=(vol-ivol)/indres
    return curr
Pc=0.01            #PID paramters
Ic=0.0
Dc=10

maxstep=20e-3         #limits
maxvol=250e-3
apps=1e-3                  #accuracy

sv=9   #set value

#np.trapz([1,2,3])
        
def prop(err,Pc):
        
    return Pc*err[-1]
 



def integ(err,tim,dt,Ic):
    
    Ierr=err[-1]*dt  
 
    return Ic*Ierr
#adaptive step voltage change

def diffren(err):
    Derr=0
    if err.shape[0]>1:
        Derr=(err[-1]-err[-2])/dt
        
    
    return Dc*Derr


def func(r):
    pv=[]
    vol=[]
    err=[]
    tim=[]
    indvol=[]
    initialtime=0.0
    initialvalue=0.0
    initialvol=0.0
    vol=np.append(vol,initialvol)
    indvol=np.append(indvol,initialvol)
    maxstep=r
    sv=9.0

    pv=np.append(pv,indcurcalc(vol[-1],indvol[-1])) #measured present  variable

    tim=np.append(tim,initialtime)

    #print maxstep

    svarr=[sv]
    i=1

    cerr=sv-pv[-1]
    #print math.fabs(cerr)
    flag=True
    while math.fabs(cerr)>apps and flag==True :
        cerr=sv-pv[-1]
        err=np.append(err,cerr)
        stepchange=prop(err,Pc)#+diffren(err)+integ(err,tim,dt,Ic)
        if math.fabs(stepchange)>maxstep:
            stepchange=stepchange/math.fabs(stepchange)*maxstep
         
        stepivol=indvolcal(indvol,stepchange,dt)
        if stepivol>maxvol*0.7:
            stepchange=0
        if stepivol>maxvol*0.9:
            flag=False
            #print 'Maximum  voltage limit reached'
        nvol=vol[-1]+stepchange
        stepivol=indvolcal(indvol,stepchange,dt)

        
        

        
        npv=indcurcalc(nvol,stepivol)
        vol=np.append(vol,nvol)
        pv=np.append(pv,npv)
        
        #print nvol,'   ',npv,'  ',cerr,' ',tim[-1]+dt,'     ',stepivol,'    ',stepchange
        svarr=np.append(svarr,sv)
        indvol=np.append(indvol,stepivol)
        tim=np.append(tim,tim[-1]+dt)
    print maxstep,tim[-1]
    return tim,pv,svarr,indvol

# initialization function: plot the background of each frame
def init():
    line.set_data([], [])
    line1.set_data([], [])
    line2.set_data([], [])
    
    time_text.set_text('')
    return line,line1,line2,time_text

# animation function.  This is called sequentially
def animate(i):
##    x = [xa for xa in range(xi,xf,dt)]
    rtemp=ri+i*dr
##    print rtemp,i,dr
    tim,pv,svarr,indvol=func(rtemp)
    line.set_data(tim, pv)
    line1.set_data(tim, svarr)
    line2.set_data(tim, indvol*10)
    time_text.set_text(time_template%(ri+i*dr))
    return line,line1,line2,time_text

# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=int(rnum+1), interval=20, blit=True,repeat=False)

# save the animation as an mp4.  This requires ffmpeg or mencoder to be
# installed.  The extra_args ensure that the x264 codec is used, so that
# the video can be embedded in html5.  You may need to adjust this for
# your system: for more information, see
# http://matplotlib.sourceforge.net/api/animation_api.html
##anim.save('basic_animation.mp4', fps=30, extra_args=['-vcodec', 'libx264'])

plt.show()
