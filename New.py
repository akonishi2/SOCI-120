from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
import numpy as np
import random
from mesa.space import SingleGrid
import pandas
from IPython.display import display, Image

# Agents who follow the new lens:
# move based on length of residence, a proxy for trust within a neighborhood
class NewAgent(Agent):
     # Initialization
    def __init__(self, unique_id, model, agent_type, income):
        super().__init__(unique_id, model)
        self.agent_type = agent_type
        self.income = income
        self.residence_length = 0
        self.neighbor_residence = 0
        self.happy = 0
        
    def calculate_similar(self):
        similar = 0
        # Calculate the number of similar neighbors (Moore neighborhoods)
        for neighbor in self.model.grid.neighbor_iter(self.pos, moore=True):
            if neighbor.agent_type == self.agent_type:
                similar += 1
        # percentage of similar neighbors
        similar_percentage = similar/8
        # add these together (and make it a model variable) we will divide by the number of agents later (take the average)
        self.model.similar += similar_percentage
        return self.model.similar
    
    def calculate_residence(self):
        self.neighbor_residence = 0
        for neighbor in self.model.grid.neighbor_iter(self.pos, moore=True):
            # calculate the residence length of the neighbors
            self.neighbor_residence += neighbor.residence_length
        # take the average of the residence length of the neighbors
        self.neighbor_residence = self.neighbor_residence/8
        
    def new_move(self):
        counter = 0
        while True:
            new_pos = self.model.grid.find_empty()
            neighbor_residence = 0
            for neighbor in self.model.grid.neighbor_iter(new_pos, moore=True):
                # calculate the residence length of the neighbors
                neighbor_residence += neighbor.residence_length
            # take the average of the residence length of the neighbors
            neighbor_residence = neighbor_residence/8
            
            counter = counter + 1
            
            # move anyways if you have looked in 5 spots 
            if (counter > 5):
                break
            if (neighbor_residence > self.neighbor_residence):
                break
           
         
        self.model.grid._place_agent(new_pos, self)
        self.model.grid._remove_agent(self.pos, self)
        self.pos = new_pos

        
    # Step function
    def step(self):
        self.calculate_similar()
        self.calculate_residence()
       
        # If they are rich enough, they can move
        if (self.income > 50000 and self.neighbor_residence < self.model.avg_residence):
            self.residence_length = 0
            self.new_move()
            self.happy = 0
        else:
            self.happy = 1
            self.model.happy += 1
            self.residence_length += 1
            self.model.avg_residence += self.residence_length

# Model for new agents
class NewModel(Model):
    def __init__(self, width, height, num_agents):
        self.schedule = RandomActivation(self)
        self.grid = SingleGrid(width, height, torus = True)
        self.num_agents = num_agents
        
        # to collect info about how many agents are happy, average similarity of neighbors, length of residence
        self.datacollector = DataCollector(model_reporters = {"Happy": lambda m: m.happy, "Similar": lambda m: m.similar, "Residence": lambda m: m.avg_residence}, agent_reporters = {"x": lambda a: a.pos[0], "y": lambda a: a.pos[1]})
        
        self.avg_residence = 0
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

            # add new agents
            agent = NewAgent(i, self, agent_type, income)
            self.schedule.add(agent)
            
            # assign the initial coords of the agents
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)

            self.grid.position_agent(agent, (x, y))
            
    def step(self):
        '''Advance the model by one step.'''

        self.happy = 0
        self.schedule.step()
        # get the average similarity
        self.similar /= self.num_agents
        # get the average length of residence
        self.avg_residence /= self.num_agents
        self.datacollector.collect(self)
       
        if self.happy == self.schedule.get_agent_count():
            self.running = False