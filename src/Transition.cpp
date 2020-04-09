//============================================================================
// Name        : Transition.cpp
// Author      : Suguman Bansal
// Version     :
// Copyright   : Your copyright notice
// Description : Class for transitions
//============================================================================

#include "common.h"
#include "Transition.h"

using namespace std;


Transition::Transition(){
  srcState = 0;
  destState = 0;
  wt = 0;
}

//Unweighted transition
Transition::Transition(int src, int dest){
  srcState = src;
  destState = dest;
  wt = 0;
}

Transition::Transition(int src, int dest, int w){
  srcState = src;
  destState = dest;
  wt = w;
}

Transition::~Transition(){
  //TODO
}

int Transition::getSrc(){
  return srcState;
}

int Transition:: getDest(){
  return destState;
}

int Transition::getWt(){
  return wt;
}

void Transition::setSrc(int s){
  srcState = s;
}

void Transition::setDest(int d){
  destState = d;
}

void Transition::setWt(int w){
  wt = w;
}

void Transition::toString(){
  cout << getSrc();
  cout << "-->" ;
  cout << getDest() << ", ";
  cout << getWt() << endl;
}

