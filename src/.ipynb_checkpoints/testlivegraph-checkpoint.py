import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import json
from scipy.stats import norm

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)
agg_risk = {}

def get_last_pit(pit_times, car, time):
    lp = max([t for t in pit_times[car] if t <= time])
    return (time - lp) / 60

def get_risk_score(x):
    MEAN1 = 0
    STD1 = 21.751478190190515
    return norm.pdf(x, MEAN1, STD1)*10

def animate(i):

    f = open('./current_time.json', 'r')
    current_time = json.load(f)['0']
    f.close()
    f = open('./result.json', 'r')
    pit_times = json.load(f)
    f.close()
#     risk = 0
#     for driver in pit_times:
#         risk += get_risk_score(get_last_pit(pit_times, driver, current_time))
#     agg_risk[current_time] = risk
    f = open('scores.json', 'r')
    agg_risk = json.load(f)
    f.close()
    xar = list(agg_risk.keys())
    yar = list(agg_risk.values())
    ax1.clear()
    ax1.plot(xar,yar)
#     with open('scores.json', 'w') as fp:
#         json.dump(dict(agg_risk), fp)

ani = animation.FuncAnimation(fig, animate, interval=1000)

plt.show()

