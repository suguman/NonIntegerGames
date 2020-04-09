//============================================================================
// Name        : graph.cpp
// Author      : Suguman Bansal
// Version     :
// Copyright   : Your copyright notice
// Description : Class for Graph
//============================================================================

#include "Graph.h"

using namespace std;

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
