/*
 * game.h
 *
 * Created on: October 31, 2019
 * Author: Suguman Bansal
 */

#ifndef GAME_H
#define GAME_H

#include "common.h"
#include "Graph.h"
#include "Transition.h"

using namespace std;

class Game{

 public:
  Game();
  Game(Graph* gg, int df, int precision, int threshold, string relation);
  virtual ~Game();

  //playing game
  bool reachabilitygame(int player);
  
  //Modify winning
  void modifywinning(string state, string gotostate);
  
  //Print winning strategie function(s)
  void rawprint(int player);
  
  //Access functions
  string getInitial();
  unordered_map<string, string>* getWinning();
  unordered_map<string, int>* getStateToPlayer();
  unordered_map<string, vector<string>>* getTrans();
  unordered_map<string, vector<string>>* getRevTrans();
  
  //Print functions
  void printInitial();
  void printWinning();
  void printStoPlayer();
  void printTrans();
  void printRevTrans();
  void printAll();

  
 private:
  string initial;
  unordered_map<string, string> winning;
  unordered_map<string, int> stateToPlayer;
  unordered_map<string, vector<string>> transFunc;
  unordered_map<string, vector<string>> reverseFunc;
  
};


#endif 