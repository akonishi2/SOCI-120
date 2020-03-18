# Agent-Based Model of Moving Based on Race and Income and Moving Based on Residence Length

## Summary

It is readily apparent that residential segregation is a problem in the United States (U.S.), as it increases income inequalities, health disparities, and educational inequalities (Popescu et al, 2018; Rothstein, 2014). As indicated in the book, *The Color of Law*, by Richard Rothstein, residential segregation was manufactured by the U.S. government on the state, federal, and county levels, through discriminatory laws that forced people of color to live in specific areas (Rothstein, 2017). It is vitally important to reverse the effects of these practices, as their effects are still evident today.

We will use an agent-based model to study the differences in residential segregation, when agents decide to move based on the race and income of their current or future neighbors, and when agents decide to move based on the communal trust within potential neighborhoods.

Although integration might have negative consequences (i.e. gentrification), on the whole, it is considered to be positive, and overall promotes equality. Thus, we will attempt uncover an alternative way (that discourages segregation) of selecting a neighborhood to live in through an agent-based model. Agent-based models simulate the activities of people by treating each person as an "agent" that behaves according to a decision policy that usually depends on their surroundings. 

## Installation

To install the dependencies use pip and the requirements.txt in this directory. e.g.

```
    $ pip install -r requirements.txt
```

## Interactive Model Run

To run the model interactively, use `mesa runserver` in this directory:

```
    $ mesa runserver
```

Then open your browser to [http://127.0.0.1:8889/](http://127.0.0.1:8889/), press Reset, then Start.

## Files

* ``final_model.py``: This defines the NewModel and TradModel classes.
* ``run.py``: Launches a model visualization server.

## References

I've adapted my code from various sources: [the tutorials on the Mesa website](https://mesa.readthedocs.io/en/master/tutorials/intro_tutorial.html), [this tutorial](https://towardsdatascience.com/introduction-to-mesa-agent-based-modeling-in-python-bcb0596e1c9a) on Medium, written by [Ng Wai Foong](https://towardsdatascience.com/@ngwaifoong92). I also used [this](https://www.youtube.com/watch?v=xaAzALyP6Ss&t=87s) YouTube tutorial, and [this one](https://www.youtube.com/watch?v=lcySLoprPMc) from [Jacqueline Kazil](https://github.com/jackiekazil) and [David Masad](https://github.com/dmasad).
