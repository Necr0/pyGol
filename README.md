# Installation

This is a python3 pipenv project so you need to have python3) and [pipenv](https://docs.pipenv.org/en/latest/install/#installing-pipenv).  

In order to install the applications dependencies execute the following command from within the project directory:  
```
$ pipenv install -e .
```

# Running

After the dependencies are installed run the following command to start the application:  
```
$ pipenv run python3 ./pygol.py
```

The controls are as follows:  
```
R: Randomize board
W: Toggle wrapping
C: Clear board
A: Load ruleset from file
0-9: Change state for drawing
Mouse Click+Drag: Draw state
Q: Quit
```