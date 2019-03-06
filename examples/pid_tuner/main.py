from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import control as ctrl
from Connection import *
import sys
import uuid


#this represents the dynamic process of moving a particle
class MoveParticleProcess(ctrl.Process):
    """Models a dynamic system in which a particle driven by forces follows a desired trajectory. """

    def __init__(self, particle=ctrl.Particle(), pid=ctrl.PID()):
        super(MoveParticleProcess, self).__init__()
        self.particle = particle
        self.pid = pid

    def target(self, t):
        """Return setpoint position for particle to reach.
        Simple step function at t == 1. and t==15.
        """
        if t < 5. or t >= 40.:
            return np.asarray([0.])
        else:
            return np.array([1.])
    
    def sense(self, t):
        """Sense particle position."""
        return self.particle.x
    
    def correct(self, error, dt):
        """Compute correction based on error."""
        return self.pid.update(error, dt)

    def actuate(self, u, dt):
        """Update particle position. 
        Takes the correction value `u` and interprets it as force acting on the particle, 
        then upates the motion equations by `dt`.
        """
        self.particle.add_force(u)
        self.particle.update(dt)

#This is simply a simulating the system through a number of seconds with a specific PID and getting the error
def runner(pid_params):
    process = MoveParticleProcess(particle=ctrl.Particle(x0=[0], v0=[0], inv_mass=1.), pid=ctrl.PID(**pid_params))
    result = process.loop(tsim=100, dt=0.2)
    e = np.sum(np.square(result['e']))
    return e


#Implementing a tuner with ACE
def ace_tune(number_sim, costfunction, jobname):
    conn = Connection()
    params = dict(kp=0., ki=0., kd=0.)
    for i in range(number_sim):
        # 1 -  get a trial to test

        dataR = {"job": jobname,
                "unit_diversion": str(uuid.uuid4())
                }
        reqdata = conn.request(dataR)

        #2 - after receiving a trial we actually test it
        #just requesting the kp
        params['kp'] = reqdata['kp']
        params['ki'] = reqdata['ki']
        params['kd'] = reqdata['kd']
        #this simulates the system and gets the error
        e = costfunction(params)

        #3 - After we got the error we need a signal that we want to maximize. In this case is a simple normalization of -error
        reward = []
        if e>50:
            reward=0
        if e<=50:
            reward = (50 - e)/50

        #4 - we update the statistical model by logging what was the reward received in this trial
        dataL = {
            "job": jobname,
            "unit_diversion": str(uuid.uuid4()),
            'signals': {'reward': reward,
                      'kp': params['kp'],
                      'ki': params['ki'],
                      'kd': params['kd']}
        }
        conn.log(dataL)

    #5 - After a fixed number of iteration we get the optimization result
    bestarmData = {'job': jobname}
    best_params = conn.best_arm(bestarmData)
    params['kp'] = best_params['kp']
    params['ki'] = best_params['ki']
    params['kd'] = best_params['kd']

    return params


def run():

    # Various PID controller parameters to run simulation with 
    pid_params = [dict(kp=0.,ki=0.,kd=0.)]

    #Running an ACE iteration to get the best set of parameters before we
    params = ace_tune(costfunction=runner,number_sim=1000, jobname='pidtuner-lghoo')
    pid_params.append(params)

    # Run simulation for each set of PID params
    handles = []
    for idx, c in enumerate(pid_params):
        process = MoveParticleProcess(particle=ctrl.Particle(x0=[0], v0=[0], inv_mass=1.), pid=ctrl.PID(**c))
        result = process.loop(tsim=100, dt=0.1)

        if idx == 0:
            fh, = plt.step(result['t'], result['y'], label='target')    
            handles.append(fh)    

        xh, = plt.plot(result['t'], result['x'], label='pid kp {:.2f} kd {:.2f} ki {:.2f}'.format(c['kp'], c['kd'], c['ki']))
        handles.append(xh)
    
    plt.title('Particle trajectory')
    plt.legend(handles=handles, loc=1)
    plt.xlabel('Time $sec$')
    plt.ylabel('Position $m$')
    plt.show()
    

if __name__ == "__main__":
    run() 

