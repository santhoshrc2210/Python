%matplotlib widget
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np


# generate 4 random variables from the random, gamma, exponential, and uniform distributions
#x1 = np.random.normal(-2.5, 1, 10000)
#x2 = np.random.gamma(2, 1.5, 10000)
#x3 = np.random.exponential(2, 10000)+7
#x4 = np.random.uniform(14,20, 10000)

# plot the histograms
#plt.figure(figsize=(9,3))
#plt.hist(x1, density=True, bins=20, alpha=0.5)
#plt.hist(x2, density=True, bins=20, alpha=0.5)
#plt.hist(x3, density=True, bins=20, alpha=0.5)
#plt.hist(x4, density=True, bins=20, alpha=0.5);
#plt.axis([-7,21,0,0.6])

#plt.text(x1.mean()-1.5, 0.5, 'x1\nNormal')
#plt.text(x2.mean()-1.5, 0.5, 'x2\nGamma')
#plt.text(x3.mean()-1.5, 0.5, 'x3\nExponential')
#plt.text(x4.mean()-1.5, 0.5, 'x4\nUniform');


# plotting distribution on 2*2 grids
#plt.subplot(2, 2, 1)
#plt.hist(x1, density=True, bins=20, color='skyblue',alpha=0.5)
#plt.title("Normal")

#plt.subplot(2, 2, 2)
#plt.hist(x2, density=True, bins=20, color='black',alpha=0.5)
#plt.title("Gamma")

#plt.subplot(2, 2, 3)
#plt.hist(x3, density=True, bins=20, color='green',alpha=0.5)
#plt.title("Exponential")

#plt.subplot(2, 2, 4)
#plt.hist(x4, density=True, bins=20, color='red',alpha=0.5)
#plt.title("Uniform")

#increase spacing between plots
#plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.4, hspace=0.6)

n = 1000
x1 = np.random.normal(-2.5, 1, n)
x2 = np.random.gamma(2, 1.5, n)
x3 = np.random.exponential(2, n)+7
x4 = np.random.uniform(14,20, n)

# create the function that will do the plotting, where curr is the current frame
def update(frame):
    
        # check if animation is at the last frame, and if so, stop the animation a
        if frame == n: 
            a.event_source.stop()
        # What is a? Well, it's an object that we'll define in a bit, and it will
        # sit outside of this function but we can still access it since python allows
        # us to access variables in the global scope.

        # Now on to the work. First thing we want to do is clear the current axes.
        # We can do this with plt.cla().
        plt.cla()

        # Now I jut want to plot a histogram. I'm going to set my bins to a predictable
        # value so it doesn't jump around, but you can play with this
        #bins = np.arange(-4, 4, 0.5)

        # Then we just make the hist() using the current frame number which was passed
        # into the function and our global values array
        

        #normal
        plt.subplot(2, 2, 1)
        plt.hist(x1[:frame], bins=20, color='skyblue',alpha=0.5)

        # Set the axes limits
        plt.axis([-7,5,0,200])

        # And add some nice labels throughout
        plt.gca().set_title('Normal Distribution')
        plt.gca().set_ylabel('Frequency')
        plt.gca().set_xlabel('Value')
        
        #gamma
        plt.subplot(2, 2, 2)
        plt.hist(x2[:frame], bins=20, color='black',alpha=0.5)

        # Set the axes limits
        plt.axis([-1,15,0,300])

        # And add some nice labels throughout
        plt.gca().set_title('Gamma Distribution')
        plt.gca().set_ylabel('Frequency')
        plt.gca().set_xlabel('Value')
        #plt.annotate('n = {}'.format(frame), [10,180])
               
        #exponential
        plt.subplot(2, 2, 3)
        plt.hist(x3[:frame], bins=20, color='green',alpha=0.5)

        # Set the axes limits
        plt.axis([5,21,0,400])

        # And add some nice labels throughout
        plt.gca().set_title('Exponential Distribution')
        plt.gca().set_ylabel('Frequency')
        plt.gca().set_xlabel('Value')
        #plt.annotate('n = {}'.format(frame), [18,350])
               
        
        #uniform
        plt.subplot(2, 2, 4)
        plt.hist(x4[:frame], bins=20, color='red',alpha=0.5)

        # Set the axes limits
        plt.axis([12,21,0,100])

        # And add some nice labels throughout
        plt.gca().set_title('Uniform Distribution')
        plt.gca().set_ylabel('Frequency')
        plt.gca().set_xlabel('Value')       
        #plt.annotate('n = {}'.format(frame), [18,80])

        #increase spacing between subplots
        plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.4, hspace=0.6)

        #title for all subplots
        plt.suptitle('Understanding Distributions Through Sampling', fontsize=12)

        #add text for each of the subplots
        plt.text(6, 250, 'n = {}'.format(frame), ha='center', fontsize=8)
        plt.text(19, 250, 'n = {}'.format(frame), ha='center', fontsize=8)
        plt.text(19, 80, 'n = {}'.format(frame), ha='center', fontsize=8)
        plt.text(6, 80, 'n = {}'.format(frame), ha='center', fontsize=8)



# Quick to start
a = animation.FuncAnimation(plt.figure(), update, frames=range(100, 1001), interval=0.001)

# Now tell the widget back end it's time to show!
plt.show()
