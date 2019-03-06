import numpy as np
from Connection import *
import uuid


def draw_sixhump_camelback(input_array, noise=True, scale=0.02):
    """
    :param input_array: x.
    :return: result of the six hump camelback function.
    """
    x1 = input_array[0]
    x2 = input_array[1]

    value = -1 * ((4.0 - 2.1 * (x1 ** 2) + (x1 ** 4) / 3.0) * x1 ** 2 + x1 * x2 + (-4 + 4 * (x2 ** 2)) * (x2 ** 2))
    # now add some noise
    if noise:
        value_noisy = np.random.normal(loc=value, scale=scale, size=1)
        return value_noisy[0]
    else:
        return value

def run(nsim,jobname):
    conn = Connection()
    for i in range(nsim):
        # 1 -  get a trial to test

        dataR = {"job": jobname,
                 "unit_diversion": str(uuid.uuid4())
                 }
        reqdata = conn.request(dataR)

        # 2 - after receiving a trial we actually test it

        input_array = [1, 1]
        input_array[0] = reqdata['x1']
        input_array[1] = reqdata['x2']

        #3 - we want the maximum of the function so we just evaluate it
        reward = draw_sixhump_camelback(input_array, noise=True, scale= 0.02)


        # 4 - we update the statistical model by logging what was the reward received in this trial
        dataL = {
            "job": jobname,
            "unit_diversion": str(uuid.uuid4()),
            'signals': {'reward': reward,
                        'x1': input_array[0],
                        'x2': input_array[1]
                        }
        }
        conn.log(dataL)

    # 5 - After a fixed number of iteration we get the optimization result
    bestarmData = {'job': jobname}
    best_params = conn.best_arm(bestarmData)
    print('The six-hump Camel function is usually evaluated on the rectangle x1 ∈ [-3, 3], x2 ∈ [-2, 2]. ')
    print('Known maximum is at: (0.0898, -0.7126) or (-0.0898, 0.7126) without noise')
    print("Found maximum at: (",best_params['x1'],',',best_params['x2'],')')





if __name__ == "__main__":
    run(nsim=1000,jobname='sixhumpcamel-lghoo')