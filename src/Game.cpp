//============================================================================
// Name        : game.cpp
// Author      : Suguman Bansal
// Version     :
// Copyright   : Your copyright notice
// Description : Class for Games
//============================================================================

#include "common.h"
#include "Game.h"
#include "Graph.h"
#include "Transition.h"

using namespace std;

string stringify(int graph_state, int comp_state){
  string sep = "_";
  //cout << to_string(graph_state) + sep + to_string(comp_state) << endl;
  return to_string(graph_state) + sep + to_string(comp_state);
}

vector<string> split (const string &s) {
  char delim = '_';
  vector<string> result;
  stringstream ss (s);
  string item;

  while (getline (ss, item, delim)) {
    result.push_back (item);
  } 
  return result;
}


Game::Game(){
  this->initial = "NA";
  this->winning = {};
  this->stateToPlayer = {};
  this->transFunc = {};
  this->reverseFunc = {};
  this->allstates = 0;
}


Game::Game(Graph* gg, int df, int precision, int threshold, string relation){

  //******* Begin: Initialize********//

  this->initial = "NA";
  this->winning = {};
  this->stateToPlayer = {};
  this->transFunc = {};
  this->reverseFunc = {};
  this->allstates  = 0;
  
  unordered_map<int, vector<Transition*>>* transF = gg->getTrans();
  unordered_map<int, int>* statePlayerID = gg->getStateToPlayer();
  vector<int>* reachability = gg->getReachability();
    
  unordered_map<string, int> statetoplayeraux = {};
  unordered_map<string, vector<string>> transfuncaux = {};
  unordered_map<string, vector<string>> reversefuncaux = {};
  unordered_map<string, string> winningaux = {};
  int numstategame = 0;
  
  int resolution_inverse = int(pow(2, df+precision));
  int dffactor = int(pow(2, df));
  //******* End: Initialize********//


  //******* Begin: Get bounds for comparator automata********//

  int maxWt = gg->getWt();

  //Current assumptions:
  //     (a). Lower bound approximation (for geq)
  //          Will be different for upper bound approximation (for leq)
  //     (b). threshold = 0

  int res_temp = int(pow(2, 2*df + precision));
  int lowerbound = -1*maxWt*res_temp;
  int upperbound = 1*maxWt*res_temp + int(pow(2,df));

  
  cout << "Comparator range  : " << lowerbound << " to " << upperbound << endl;
  
  //******* End: Get bounds for comparator automata*********//

  // ******* Begin : initial state of game ********//
  string init = stringify(gg->getInitial(), 0);
  this->initial = init; 

  //cout << init << endl;
  
  // ******* End : initial state of game ********//

  
  // ******* Begin : make all states  ********//

  //Maintaining statestack to maintain all states that have to be explored
  //Mainitaining isstate to maintain all states that have already been explored
  queue<string> statestack;
  unordered_map<string, bool> isstate;

  //Special state : init
  statestack.push(init);
  numstategame += 1;
  isstate[init] = true;
  statetoplayeraux[init] = statePlayerID->at(gg->getInitial());
  winningaux[init] = "";
  reversefuncaux[init] = {};
  
  while(!statestack.empty()){
    string state = statestack.front();
    statestack.pop();
    //cout << state << endl;
    //Parts of current state
    vector<string> statetemp = split(state);
    int cur_state = stoi(statetemp[0]);
    int cur_comparator  = stoi(statetemp[1]);
    //Used to store all outgoing neighbours
    vector<string> deststatelist = {};

    vector<Transition*> translist = transF->at(cur_state);

    for(auto &trans : translist){
      //*****Begin: Make new state*****//
      // (a). Find the next state in the graph
      // (b). Find the next state in the comparator
      
      // (a). Find the next state in the graph
      int next_src = trans->getDest();
      
      // (b). Calculate the next state in the comparator
    
      int wt = trans->getWt();

      int next_comparator = 0;
      int next_comparator_temp = cur_comparator + wt*resolution_inverse + int(cur_comparator/dffactor);
      if (next_comparator_temp > upperbound){
	next_comparator = upperbound;
      }
      else if (next_comparator_temp < lowerbound){
	next_comparator = lowerbound;
      }
      else{
	next_comparator = next_comparator_temp;
      }
      
      // Make the destination state using (a) and (b)
      string new_state = stringify(next_src, next_comparator);
      
      //*****End: Make new state*****//
      
      //Check if new_state is indeed a new state
      //It is a new state if new_state is not already a key in isstate
      //If new_state is a new state, then add it to statestack
      //If new_state is a winning state, add it to winning_state_stack
      try{
        bool boolval = isstate.at(new_state);
	}
      catch(const std::out_of_range){
	isstate[new_state] = true;
	statetoplayeraux[new_state] = statePlayerID->at(next_src);
	reversefuncaux[new_state] = {};
	
	//****** Begin: make it a winning state **********//

	if (reachability->size() == 0){
	  if (relation == "geq" and next_comparator == upperbound){
	    winningaux[new_state] = "W";
	  }
	  else if (relation == "leq" and next_comparator == lowerbound){
	    winningaux[new_state] = "W";
	  }
	  else{
	    winningaux[new_state] = "";
	  }
	}
	else{
	  //if (next_src in reachability)
	  //same conditions as above
	  //else, state is not a winning state
	  vector<int>::iterator it;
	  it = find(reachability->begin(), reachability->end(), next_src);
	  if (it!=reachability->end()){
	      //new_src is a reachability objective
	      if (relation == "geq" and next_comparator == upperbound){
		winningaux[new_state] = "W";
	      }
	      else if (relation == "leq" and next_comparator == lowerbound){
		winningaux[new_state] = "W";
	      }
	      else{
		winningaux[new_state] = "";
	      }
	    }
	  else{
	    winningaux[new_state] = "";
	  }
	}
	//****** End: make it a winning state **********//
	
	statestack.push(new_state);
	numstategame += 1;
      }
      deststatelist.push_back(new_state);
      reversefuncaux[new_state].push_back(state);	
    }
    transfuncaux[state] = deststatelist;
  }
  this->stateToPlayer = statetoplayeraux;
  this->transFunc = transfuncaux;

  //cout << "Completed while" << endl;

  /*
  //Make reverse transitions
  unordered_map<string, vector<string>> :: iterator p;
  
  for (p = transfuncaux.begin(); p != transfuncaux.end(); p++){
    string srcstate = p->first;
    vector<string> temptranslist= p->second;
    for (auto & element : temptranslist){
      try{
        reversefuncaux[element].push_back(srcstate);
	}
      catch(const std::out_of_range){
        reversefuncaux[element].push_back(srcstate);      
      }
    }
  }
  */
  
  this->reverseFunc = reversefuncaux;
  this->winning = winningaux;
  this->allstates = numstategame;
}

Game::~Game(){
  //TODO
}

string Game::getInitial(){
  return this->initial;
}

unordered_map<string, string>* Game::getWinning(){
  return &(this->winning);
}

unordered_map<string, int>* Game::getStateToPlayer(){
  return &(this->stateToPlayer);
}

unordered_map<string, vector<string>>* Game::getTrans(){
  return &(this->transFunc);
}

unordered_map<string, vector<string>>* Game::getRevTrans(){
  return &(this->reverseFunc);
}

int Game::getallstates(){
  return this->allstates;
}

void Game::printInitial(){
  cout << "Initial state is " << this->getInitial() << endl;
}

void Game::printWinning(){
  cout << "Winning states are:" << endl;
  unordered_map<string, string>:: iterator p;
  unordered_map<string, string>* temp = this->getWinning(); 
  for (p = temp->begin(); p != temp->end(); p++){
    cout << p->first << ", " << p->second << endl;
  }
}

void Game::printStoPlayer(){
 cout << "State-Player mapping is " << endl;

  unordered_map<string, int>:: iterator p;
  unordered_map<string, int>* temp = this->getStateToPlayer(); 
  for (p = temp->begin(); p != temp->end(); p++){
    cout << p->first << ", " << p->second << endl;
  }
}

void Game::printTrans(){
  cout << "Transition relation is " << endl;

  unordered_map<string, vector<string>> :: iterator p;
  unordered_map<string, vector<string>>* temp = this->getTrans();

  string printbuffer = "";
  int counter = 1;
  
  for (p = temp->begin(); p != temp->end(); p++){
    vector<string> temptranslist= p->second;
    for (auto & element : temptranslist) {
      printbuffer += p->first + "-->" + element +"\n";
      counter +=1;
      if (counter%1000 == 0){
	cout << printbuffer;
	printbuffer = "";
      }
    }
  }
  cout << printbuffer;
}


void Game::printRevTrans(){
  cout << "Transition reverse relation is " << endl;

  unordered_map<string, vector<string>> :: iterator p;
  unordered_map<string, vector<string>>* temp = this->getRevTrans();
  
  for (p = temp->begin(); p != temp->end(); p++){
    vector<string> temptranslist= p->second;
    for (auto & element : temptranslist) {
      cout << p->first << "-->" << element << endl;
    }
  }
}

void Game::printstatenum(){
  cout << this->allstates << endl;
}

void Game::printAll(){
  printInitial();
  printWinning();
  printStoPlayer();
  printTrans();
}

void Game::modifywinning(string state, string gotostate){
  (this->winning)[state] = gotostate;
}

bool Game::reachabilitygame(int player, bool early_termination){
  
  unordered_map<string, vector<string>>* reverse_map = this->getRevTrans();
  unordered_map<string, vector<string>>* map = this->getTrans();
  unordered_map<string, int>* statetoplayer = this->getStateToPlayer();
  unordered_map<string, string>* winning = this->getWinning();
  string initial = this->getInitial();

  // Initially, we assume that the player doesn't win
  bool playerwins = false;
  
  //1. Count the number of outgoing transitions from each state
  //2. Insert the winning states into the stackstack
  queue<string> statestack;
  unordered_map<string, int> numtrans;
  unordered_map<string, vector<string>> :: iterator p;
  for(p = map->begin(); p != map->end(); p++){
    string statetempstring = p->first;
    numtrans[statetempstring] = (p->second).size();
    
    if (winning->at(statetempstring) == "W"){
      numtrans[statetempstring] = 0;
      statestack.push(statetempstring);
    }
  }
    
  while(!statestack.empty()){ 
    string state = statestack.front();
    statestack.pop();
    vector<string> revtranslist;
    try{
      revtranslist = reverse_map->at(state);
    }
    catch(const std::out_of_range){
      continue;
    }
    for(auto & element : revtranslist){
      int statebelongsto = statetoplayer->at(element);
      if (statebelongsto == player){
	// then element is a  winning state.	
	// if element hasn't been visited before, then add to stack. 
	// element hasn't been visited before, its numtrans != 0
	if (numtrans[element] != 0){
	  statestack.push(element);
	  numtrans[element] = 0;
	  this->modifywinning(element, state);
	}
	if (element == initial){
	  //player has won, as it is visiting  initial state, controlled by the player
	  playerwins = true;
	  if (early_termination){
	    return playerwins;
	  }
	}
      }
      else{//statebelongs to environment
	// element will be winning only when numtans turns 0
	// add element to stack only the first time numtrans turns 0
	if (numtrans[element] != 0){
	  numtrans[element] = numtrans[element]-1;
	  if (numtrans[element] == 0){//numtrans becomes 0 for the first time  winning state
	    statestack.push(element);
	    if (element == initial){
	      playerwins = true;
	      if (early_termination){
		return playerwins;
	      }
	    }
	  }
	}
      }
    }/*for ends*/
  }/* while ends*/
  return playerwins;
}

void Game::rawprint(int player){

  unordered_map<string, string>* wmap = this->getWinning();
  unordered_map<string, int>* ptosmap = this->getStateToPlayer();

  string state;
  string deststate;
  vector<string> scomp = {};
  vector<string>  dcomp = {};
  int temp;
  string printbuffer = "";
  int counter = 1;
  
  unordered_map<string, string> :: iterator p;
  for(p = wmap->begin(); p != wmap->end(); p++){
    state = p->first;
    if (ptosmap->at(state) == player){
      scomp = split(state);
      deststate = wmap->at(state);
      dcomp = split(deststate);
      temp  = dcomp.size(); 
      if (temp == 2){
	printbuffer  += scomp[0] + ", " + scomp[1] + " --> " + dcomp[0] +  ", "  + dcomp[1] + "\n";
	//cout << scomp[0] << ", " << scomp[1] << " --> " << dcomp[0] << ", " << dcomp[1] << endl; 
      }
      if (temp  == 1){
	
	printbuffer  += scomp[0] + ", " + scomp[1] + " --> " + "Any action " + "\n";
	//cout << scomp[0] << ", " << scomp[1] << " --> "  << "Any action" << endl;
      }
      if (temp == 0){
      }
    }
    counter += 1;
    if (counter%50000){
      cout << printbuffer;
      printbuffer = "";
    }
  }
  cout << printbuffer;
}
