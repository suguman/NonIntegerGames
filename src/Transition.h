/*
 * Transition.h
 *
 * Created on: October 26, 2019
 * Author: Suguman Bansal
 */

//#include <string>

#ifndef TRANSITION_H
#define TRANSITION_H

#include "common.h"

using namespace std;

class Transition{

public:

  Transition();
  Transition(int s, int d);
  Transition(int s, int d, int wt);
  ~Transition();
  
  int getSrc();
  int getDest();
  int getWt();
  
  void setSrc(int s);
  void setDest(int d);
  void setWt(int a);
  
  virtual void toString();

private:
  int srcState;
  int destState;
  int wt;
  
};


#endif
