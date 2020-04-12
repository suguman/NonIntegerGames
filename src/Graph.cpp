//============================================================================
// Name        : graph.cpp
// Author      : Suguman Bansal
// Version     :
// Copyright   : Your copyright notice
// Description : Class for Graph
//============================================================================

#include "common.h"
#include "Graph.h"

using namespace std;
using namespace boost;
using namespace boost::algorithm;

Graph::Graph(){
  this->numState = 0;
  this->initState = 0;
  this->maxWt = 0;
  this->stateToPlayer = {};
  this->transFunc = {};
}


Graph::Graph(int num, int initial, int wt, unordered_map<int, int>* stateToP, unordered_map<int, vector< Transition*>>* transMap){
  this->numState = num;
  this->initState = initial;
  this->maxWt = wt;
  this->stateToPlayer = *stateToP;
  this->transFunc = *transMap;  
}


Graph::Graph(string filename){

  int stateNum = 0;
  int initial = 0;
  int maxweight = 0;
  unordered_map<int, int> stateToP = {};
  unordered_map<int, vector<Transition*>> transMap = {};
  

  ifstream inFile;
  inFile.open(filename);
  if (!inFile){
    cerr << "Unable to open file" << endl;
    exit(1);
  }

  string output;

  int len;
  int src;
  int dest;
  int wt;
  int partition;
  
  while(!inFile.eof()){
    //output
    getline(inFile, output);
 
    trim(output);
    if (output[0] == '#'){
	//IGNORE COMMENT
      }
    else{
      
      //Split the sequence at the whitespace
      // If split-sequence has
      // (a). single element -- iniital state
      // (b). two elements -- state and player affiliation
      // (c). three elements -- transition

      vector<string> splitparts;
      split(splitparts, output, [](char c){return c == ' ';});
      len = splitparts.size();

      switch(len){
      case 1:
	if (!(splitparts[0]=="" or splitparts[0]=="\n" or splitparts[0]=="\t" or splitparts[0]=="\r")){
	    initial = stoi(splitparts[0]);
	}	
	break;
	
      case 2:
	src = stoi(splitparts[0]);
	partition = stoi(splitparts[1]);
	//Set up the state-partition 
	stateToP.insert({src, partition});
	//Set up the transition relation
        transMap.insert({src, {}});
        stateNum +=1;
	break;
	
      case 3:
	src = stoi(splitparts[0]);	
	dest = stoi(splitparts[1]);
        wt = stoi(splitparts[2]);
	//cout << src << " " << dest << " " << wt << endl;
        Transition* tempTrans = new Transition(src, dest, wt);
	//tempTrans->toString();
        transMap[src].push_back(tempTrans);
	if (abs(wt)> maxweight){
	  maxweight = wt;
	  }
	break;	
      }
    }
  }

  inFile.close();
  
  this->numState = stateNum;
  this->initState = initial;
  this->maxWt = maxweight;
  this->stateToPlayer = stateToP;
  this->transFunc = transMap;  
}

Graph::~Graph(){
  //TODO
}
int Graph::getInitial(){
  return this->initState;
}

int Graph::getStateNum(){
  return this->numState;
}

int Graph::getWt(){
  return this->maxWt;
}

unordered_map<int, int>* Graph::getStateToPlayer(){
  return &(this->stateToPlayer);
}

unordered_map<int, vector<Transition*>>* Graph::getTrans(){
  return &(this->transFunc);
}

int Graph::getTransNum(){
  //TODO
}

void Graph::printInitial(){
  cout << "Initial state: " << this->getInitial() << endl;
}

void Graph::printMaxWt(){
  cout << "Max Wt: " << this->getWt() << endl;
}

void Graph::printStoPlayer(){
  cout << "State-Player mapping is " << endl;

  unordered_map<int, int>:: iterator p;
  unordered_map<int, int>* temp = this->getStateToPlayer();
  
  for (p = temp->begin(); p != temp->end(); p++){
    cout << p->first << ", " << p->second << endl;
  }
}

void Graph::printTrans(){
  cout << "Transition relation is " << endl;

  unordered_map<int, vector<Transition*>> :: iterator p;
  unordered_map<int, vector<Transition*>>* temp = this->getTrans();
  for (p = temp->begin(); p != temp->end(); p++){
    vector<Transition*> temptranslist= p->second;
    for (auto & element : temptranslist) {
      element->toString();
    }
  }
}

void Graph::printAll(){
  this->printInitial();
  this->printStoPlayer();
  this->printTrans();
  this->printMaxWt();
}
