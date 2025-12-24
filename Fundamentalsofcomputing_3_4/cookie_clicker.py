"""
Cookie Clicker Simulator
"""

import simpleplot
import math

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

import poc_clicker_provided as provided

# Constants
SIM_TIME = 10000000000.0

class ClickerState:
    """
    Simple class to keep track of the game state.
    """
    
    def __init__(self):
        self.sum_cookies=0.0
        self.current_num_cookies=0.0
        self.cur_time=0.0
        self.cur_cps=1.0
        self.history_lst=[(0.0, None, 0.0, 0.0)]
        
        
    def __str__(self):
        """
        Return human readable state
        
        """
        return ("Total cookies: " + str(self.sum_cookies)+
                ". \nCurrent cookies: " + str(self.current_num_cookies) + 
                ". \nCurrent CPS: " + str(self.cur_cps) + 
                ". \nCurrent time: " + str(self.cur_time))
    
    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        return self.current_num_cookies
    
    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self.cur_cps
    
    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self.cur_time
    
    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: [(0.0, None, 0.0, 0.0)]

        Should return a copy of any internal data structures,
        so that they will not be modified outside of the class.
        """
        return self.history_lst

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0.0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        if self.current_num_cookies>=cookies:
            return 0.0
        else:
            time_till=(cookies-self.current_num_cookies)/self.cur_cps
            time_till=math.ceil(time_till)        
            return time_till
    
    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0.0
        """
        if self.cur_time>=0.0:           
            self.cur_time+=time
            self.current_num_cookies+=time*self.cur_cps
            self.sum_cookies+=time*self.cur_cps            
               
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        if self.current_num_cookies>=cost:
            self.cur_cps+=additional_cps
            self.current_num_cookies-=cost
            self.history_lst.append([(self.cur_time, item_name, cost, self.sum_cookies)])
   
    
def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to the final state of the game.
    """
    info = build_info.clone()
    new_clicker = ClickerState() 
    while new_clicker.get_time() <= duration:
        if new_clicker.get_time() > duration:
            break
        left_time = duration - new_clicker.get_time()    
        strateg_item = strategy (new_clicker.get_cookies(), new_clicker.get_cps(), 
                  new_clicker.get_history(), left_time, info)
        if strateg_item == None:
            break
        time_elapse = new_clicker.time_until(info.get_cost(strateg_item))
        if time_elapse > left_time:
            break
        else:
            new_clicker.wait(time_elapse)
            while new_clicker.get_cookies() >= info.get_cost(strateg_item):
                new_clicker.buy_item(strateg_item, info.get_cost(strateg_item),
                             info.get_cps(strateg_item))
                info.update_item(strateg_item)    
    new_clicker.wait(left_time)
    return new_clicker 

def strategy_cursor_broken(cookies, cps, history, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic (and broken) strategy does not properly
    check whether it can actually buy a Cursor in the time left.  Your
    simulate_clicker function must be able to deal with such broken
    strategies.  Further, your strategy functions must correctly check
    if you can buy the item in the time left and return None if you
    can't.
    """
    return "Cursor"

def strategy_none(cookies, cps, history, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that will never buy anything, but
    that you can use to help debug your simulate_clicker function.
    """
    return None

def strategy_cheap(cookies, cps, history, time_left, build_info):
    """
    Always buy the cheapest item you can afford in the time left.
    """
    cookies += time_left * cps   
    items_lst=build_info.build_items()
    cost_lst=[]
    for item in items_lst:
        cost_lst.append(build_info.get_cost(item))
    idx_cheapest_item=cost_lst.index(min( cost_lst))
    cheapest_item=items_lst[idx_cheapest_item]
    if build_info.get_cost(cheapest_item)<=cookies:
        return cheapest_item


def strategy_expensive(cookies, cps, history, time_left, build_info):
    """
    Always buy the most expensive item you can afford in the time left.
    """
    cookies += time_left * cps   
    items_lst=build_info.build_items()
    cost_lst=[]
    for item in items_lst:
        cost_lst.append(build_info.get_cost(item))
    
    idx_lst=[]
    aff_cost_lst=[]
    for cost in cost_lst:
        if cost<=cookies:
            aff_cost_lst.append(cost)
            idx_lst.append(cost_lst.index(cost))
    
    idx=aff_cost_lst.index(max(aff_cost_lst)) 
    idx_expensive_item=idx_lst[idx]
    return items_lst[idx_expensive_item]

def strategy_best(cookies, cps, history, time_left, build_info):
    """
    The best strategy that you are able to implement.
    """
    #assuming the cps is proportional to cost                       
    cookies += time_left * cps
    items_lst=build_info.build_items()
    cps_lst=[]
    cost_lst=[]
    max_pos_cps_lst=[]                       
    for item in items_lst:
        item_cps=build_info.get_cps(item)
        cps_lst.append(item_cps)
        item_cost=build_info.get_cost(item)
        cost_lst.append(item_cost)
        pos_cps=round(cookies/float(item_cost))* item_cps
        max_pos_cps_lst.append(pos_cps)
                           
    idx_best_item=max_pos_cps_lst.index(max(max_pos_cps_lst)) 
    return items_lst[idx_best_item]                       
    
                                                      
def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation for the given time with one strategy.
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    # history = state.get_history()
    # history = [(item[0], item[3]) for item in history]
    # simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

def run():
    """
    Run the simulator.
    """    
    #run_strategy("Cursor", SIM_TIME, strategy_cursor_broken)

    # Add calls to run_strategy to run additional strategies
    # run_strategy("Cheap", SIM_TIME, strategy_cheap)
    # run_strategy("Expensive", SIM_TIME, strategy_expensive)
    run_strategy("Best", SIM_TIME, strategy_best)
    
run()
    


