from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule, TextElement

from Traditional import TradModel
from New import NewModel

def agent_portrayal(agent):
    if agent is None:
        return
    portrayal = {"Shape": "circle", "r": 0.5, "Filled": "true", "Layer": 0}

    if agent.agent_type == 1:
        portrayal["Color"] = "Red"
    else:
        portrayal["Color"] = "Blue"
    return portrayal

class HappyElement(TextElement):
    def __init__(self):
        pass

    def render(self, model):
        return "Happy agents: " + str(model.happy)
    
class SimilarElement(TextElement):
    def __init__(self):
        pass

    def render(self, model):
        return "Average similarity: " + str(model.similar)
    
class ResidenceElement(TextElement):
    def __init__(self):
        pass

    def render(self, model):
        return "Average residence length: " + str(model.avg_residence)
    
happy_element = HappyElement()
similar_element = SimilarElement()
residence_element = ResidenceElement()
grid = CanvasGrid(agent_portrayal, 50, 50, 400, 400)
happy_chart = ChartModule([{"Label": "Happy", "Color": "Black"}])
similar_chart = ChartModule([{"Label": "Similar", "Color": "Red"}])
residence_chart = ChartModule([{"Label": "Residence", "Color": "Blue"}])

'''
trad_server = ModularServer(TradModel,[grid,  similar_element, similar_chart, happy_element, happy_chart], "Traditional Model", {"width":50, "height":50, "num_agents":2125})
trad_server.verbose = False
trad_server.port = 8889
trad_server.launch()
'''

new_server = ModularServer(NewModel,[grid,  similar_element, similar_chart, happy_element, happy_chart, residence_element, residence_chart], "New Model", {"width":50, "height":50, "num_agents":2125})
new_server.verbose = False
new_server.port = 8889
new_server.launch()
