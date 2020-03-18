from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
import numpy as np
import random
from mesa.space import SingleGrid
import pandas
from IPython.display import display, Image

# Agents who follow the traditional lens: move based on race, income
class TradAgent(Agent):
    # Initialization
    def __init__(self, unique_id, model, agent_type, income):
        super().__init__(unique_id, model)
        self.agent_type = agent_type
        self.income = income
        self.happy = 0
        self.residence_length = 0
        
    # Step function
    def step(self):
        similar = 0
        # Calculate the number of similar neighbors (Moore neighborhoods)
        for neighbor in self.model.grid.neighbor_iter(self.pos, moore=True):
            if neighbor.agent_type == self.agent_type:
                similar += 1
        similar_percentage = similar/8
        self.model.similar += similar_percentage
       
        # If they are rich enough and are unhappy, they can move
        if (self.agent_type == 1 and similar_percentage < 0.75 and self.income > 50000):
                self.model.grid.move_to_empty(self)
                self.happy = 0
                self.residence_length = 0
        elif (self.agent_type == 0 and similar_percentage < 0.5 and self.income > 50000):
                self.model.grid.move_to_empty(self)
                self.happy = 0
                self.residence_length = 0
        else:
            # otherwise, they are happy
            self.happy = 1
            self.model.happy += 1
            self.residence_length += 1

# Model for traditional agents
class TradModel(Model):
    def __init__(self, width, height, num_agents):
        self.schedule = RandomActivation(self)
        self.grid = SingleGrid(width, height, torus = True)
        self.num_agents = num_agents
        # to collect info about how many agents are happy, average similarity of neighbors
        self.datacollector = DataCollector(model_reporters = {"Happy": lambda m: m.happy, "Similar": lambda m: m.similar},
            agent_reporters = {"x": lambda a: a.pos[0], "y": lambda a: a.pos[1]})
        self.happy = 0
        self.similar = 0
        self.running = True
        
        for i in range(self.num_agents):
          
            # white
            if random.random() < 0.70:
                agent_type = 1
                income = np.random.normal(54000, 41000)
            
            # black
            else:
                agent_type = 0
                income = np.random.normal(32000, 40000)

            # create agents
            agent = TradAgent(i, self, agent_type, income)
            self.schedule.add(agent)
            
            # coords of the initial locations of the agents
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)

            self.grid.position_agent(agent, (x, y))
    def step(self):
        '''Advance the model by one step.'''

        self.happy = 0
        self.schedule.step()
        #take the average of the similarity
        self.similar /= self.num_agents
        self.datacollector.collect(self)
       
        # stop model if all of the agents are happy
        if self.happy == self.schedule.get_agent_count():
            self.running = False
           
            