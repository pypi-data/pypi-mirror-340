CoGrid
=======
.. raw:: html

   <div style="display: flex; justify-content: center; padding-left: 40%;">
      <a href="https://www.github.com/chasemcd/cogrid">
         <img src="docs/_static/images/cogrid_logo_nobg.png" alt="CoGrid Logo" style="width: 25%; display: block;">
      </a>
   </div>

CoGrid is a library for creating grid-based multi-agent environments for multi-agent reinforcement learning research. 
It is built on top of Minigrid, a minimalistic gridworld library developed
originally by Chevalier-Boisvert et al. (2023) (https://arxiv.org/abs/2306.13831). CoGrid has several core
differentiating factors from Minigrid:

1. Multi-agent support. CoGrid supports multiple agents in the same environment, each with their own
   observation space and action space. Whereas Minigrid's environment logic is centered around a single 
   agent interacting with a ``Grid`` of ``WorldObj`` objects, CoGrid's environment logic also tracks ``Agent`` objects as
   unique objects, allowing an arbitrary number to exist in the environment.
2. ``Reward`` modularization. CoGrid allows for the creation of custom ``Reward`` objects that can be added to the
   environment. Each ``Reward`` is used to calculate the reward for each agent at each step, and can be
   used to create complex reward functions that depend on the state of the environment, the actions of
   other agents, etc.
3. ``Feature`` modularization. Similar to rewards, CoGrid allows for the creation of custom ``Feature`` objects that can be added to the
   environment. These ``Feature`` classes are used to construct each agent's observation
   space, such as the location of other agents, an image of the environment, etc. 

CoGrid utilizes the parallel PettingZoo API to standardize the multi-agent environment interface.

.. raw:: html

   <div style="display: flex; justify-content: center; margin-top: 20px;">
      <img src="docs/_static/images/sr_example.gif" alt="Example GIF" style="width: 75%; display: block;">
   </div>

Installation
------------

Install from the PyPi distribution:
   
      .. code-block:: bash
   
         pip install cogrid


Citation
---------

If you use CoGrid in your research, please cite the following paper:

    .. code-block:: bash

        @article{mcdonald2024cogrid,
         author  = {McDonald, Chase and Gonzalez, Cleotilde},
         title   = {CoGrid and Interactive Gym: A Framework for Multi-Agent Experimentation},
         year    = {forthcoming},
         }
