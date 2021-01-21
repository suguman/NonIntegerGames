# NonIntegerGames

Dependencies
--------------------

* BOOST

Install Boost
    
    sudo apt-get install libboost-dev
    
Compile and run
---------------------

Make source: 

    cd src/
    make
    
Pull up the -help options:   
    
    ./game -h
    
Example run:
    
    ./game -f ../benchmarks/eg1.txt -df 2 -p 1 -id 0 -syn
    
# Robotics benchmarks

Dependencies
---------------------
* python3

Run
---------------------
    cd benchmarks/
    python3 create_game.py <num rows> <num_cols> <pos_reward> <neg_reward>

Run
---------------------
    cd scripts/
    python3 run_conveyor.py
    python3 run_sd.py