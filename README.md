# #####################
# \### Formula 1 IoT ###
# #####################
This is my python project with usage of docker in practise. (The project is still under construction.)
Main project assumptions:
- two docker containers communite together in bi-directional way
- every part of the project is designed with appropriate OOP solutions
- first container, which represents vehicle, sends data to pit stop with stable time intervals and second container, which represents pit stop, evaluate the data and response if the parameters are normal or the vehicle should be redirected to pit stop
- the data is randomly generated within specific range
- there are three levels of vehicle's state: 0: Normal, 1: Warning and 2: Error

Sequence communication diagram:

   /====\                                    |"""""""""""""""|
   {}/\{} ----- 1. Vehicle parameters -----> |               | 
    |F1|                                     | Pit Stop Crew |
   {}\/{} <--- 2. Parameters evaluation ---- |               |
    [__]                                     |_______________|


How to run the project in ./formula_1_iot directory (steps):
1. run script file: source_files.bash (Linux) or source_files.cmd (Windows)
2. run docker compose file: docker-compose up --build

Sources:
- dockerignore list for python projects: https://shisho.dev/blog/posts/how-to-use-dockerignore/
- base for the project: https://www.youtube.com/watch?v=PXo3AAquPy0
