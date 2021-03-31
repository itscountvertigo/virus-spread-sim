# Virus spread simulation
This is a simple virus spread simulation i made in a day. It's rendered and exported using matplotlib.

There are 3 files:
- no_lockdown_case.py, without lockdown effects. This is just a control.
- self_quarantine_case.py, here people will stop moving when they're infected.
- full_lockdown_case.py, this has the same self-quarantining effect as self_quarantine_case.py, but everyone is slowed.

## Results
Here are the results, exported as PNG sequences and converted to gifs with [EzGif](https://ezgif.com/). 

In the following diagrams, green is healthy, red is infected, blue is immune and grey is dead. 

### no_lockdown_case.py

![no lockdown gif](results/no_lockdown_case.gif)

The virus spreads uncontrollably in this case. This case is just a control, and it shows how quickly a virus can spread. 

- Almost half the population is at the same time, at some point
- Having this in real life would cause a lot of deaths, since the likelihood of death would increase, because hospitals can't handle half the population at a time.
- Hospital capacity is not programmed in though, so this isn't reflected in the simulation.

### self_quarantine_case.py

![self quarantine case gif](results/self_quarantine_case.gif)

This version stops people from moving when they're infected. This happens with a little delay, because COVID (the inspiration for this project) spreads asymptomatically.

### full_lockdown_case.py

![full lockdown case gif](results/full_lockdown_case.gif)

This is the harshest version, where everyone is slowed too. This is the longest of them all, this takes >700 frames for the virus to eradicate, but not many people are infected at the same time.

## Why this isn't amazing
To start off, this isn't the most efficient code. I knew that, and didn't write it to be efficient because it's main purpose is rendering/exporting and it doesn't have to run perfectly for that.

There's also the scientific perspective of what could be better:
- If you've survived the virus, you gain immunity in this simulation. That's not what happens in real life, but it's the best I could do in the time I had.
- Most values are chosen somewhat randomly, and don't properly resemble the real workings of COVID. Some were chosen with intent, i've commented sources for those in the code.
- I haven't taken population density into account, the number of people are also chosen pretty arbitrarily. You're free to try it with different values, if you'd like.
- People don't avoid infected people, even in the self-quarantining simulations.
- Lastly, we aren't bouncing balls

## How to install it
To install it, you'll need to have Python 3 installed. <ake sure you have the following modules too:
- matplotlib (you can install matplotlib with ```pip install matplotlib```)
- numpy (you can install numpy with ```pip install numpy```)

To run it, just run any one of the files to see them in action. Note that it will start rendering all the frames. If you don't want that, you'll have to comment out the following line:

```
plt.savefig('render/%s.png' %frame)
```

That's it! Thanks for reading and looking at my code :)

