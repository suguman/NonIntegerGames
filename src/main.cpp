#include "common.h"
#include "Game.h"
#include "Graph.h"
#include "Transition.h"

static struct opt_t
{
  const char* filename = nullptr;
        
  int df = 1;
  int precision = 1;
  int thresh = 0;
  string relation = "geq";
  bool synthesis = false;
  int playerid = 0;

}* opt;


void print_opt(){
  cout << "Filename          : " << opt->filename << endl;
  cout << "Discount factor   : " << "1+2^-" << opt->df << endl;
  cout << "Precision         : " << "2^-" << opt->precision << endl;
  cout << "Treshold          : " << opt->thresh << endl;
  cout << "Relation          : " << opt->relation << endl;
  //cout << "Synthesis is       " << opt->synthesis << endl;
  cout << "Player id         : " << opt->playerid << endl;
}

void print_usage(){
  cout << "Usage: game [OPTION...] [FILENAME]" << endl;
  cout << "Read gamegraph file and options for solving game" << endl;
  cout << "Input options:" << endl;
  cout << " -h  " << "                   show this help page" << endl;
  cout << " -df " << " <int>             discount factor value is 1+2^{-df}. Default is 1" << endl;
  cout << " -p  " << " <int>             approximation factor is 2^{-p}. Default is 1 " << endl;
  cout << " -th " << " <int>             threshold value. Default is 0 " << endl;
  cout << " -rel" << " <string>          options are \"leq\" or \" geq\". Default is \"geq\"" << endl;
  cout << " -syn" << "                   evaluate a winning strategy, if exists" << endl;
  cout << " -id " << " <int>             player id. can be 0 or 1. Default is 0." << endl;
  cout << " -f  " << " <filename>        filename specifying the game graph" << endl;
}


//Command line input is <filename> <df> <value>
void parse_opt(int argc, char** argv){

  if (argc == 1){
    print_usage();
  }
  for (int i=1; i< argc; i++){
    string s(argv[i]);
    //cout << argv[i] << endl;

    if (s.size() == 0){
      continue;
    }
    if (s == "-df" and i+1 < argc){
      int temp = stoi(argv[i+1]);
      if (temp>0){
	opt->df = temp;
	i++;
	continue;
      }
      else{
	cout << "DF must be a positive int" << endl;
	print_usage();
	exit(-1);
      }
    }
    if (s == "-p" and i+1 < argc){
      int temp = stoi(argv[i+1]);
      if (temp>0){
        opt->precision = temp;
	i++;
	continue;
      }
      else{
	cout << "P must be a positive int" << endl;
	print_usage();
	exit(-1);
      }
    }
    if (s == "-th" and i+1 < argc){
      opt->thresh = stoi(argv[i+1]);
      i++;
      continue;
    }
    if (s == "-rel" and i+1 < argc){
      string temp = argv[i+1];
      if (temp == "geq" or temp == "leq"){
	  opt->relation = temp;
	  i++;
	  continue;
	}
      else{
	cout << "relation input is invalid" << endl;
	print_usage();
	exit(-1);
      }
      }
    if (s == "-f" and i+1 < argc){
      opt->filename = argv[i+1];
      i++;
      continue;
    }
    if( s == "-h"){
      print_usage();
      exit(0);
    }
    if( s == "-syn"){
      opt->synthesis = true;
      continue;
    }
    if ( s== "-id" and i+1<argc){
      int id = stoi(argv[i+1]);
      i++;
      if (id == 0 or id ==1){
	opt->playerid = id;
	continue;
      }
      else{
	cout << "Error in player id. Can be 0 or 1" << endl;
	print_usage();
	exit(-1);
      }
    }
    else{
      cout << "Error in input options" << endl;
      print_usage();
      exit(-1);
    }
  }
}


int  main(int argc, char** argv){

  opt_t o;
  opt = &o;

  //print_opt();
  parse_opt(argc, argv);
  print_opt();

  //create game graph from file

  Graph* gg = new Graph(opt->filename);
  //gg->printAll();

  //create and solve reachability game

  clock_t creategraph_s = clock();
  Game* qg = new Game(gg, opt->df, opt->precision, opt->thresh, opt->relation);
  clock_t creategraph_e = clock();
  double creategraph = ((double) (creategraph_e- creategraph_s)) / CLOCKS_PER_SEC;
  
  //qg->printAll();
  //qg->printRevTrans();

  //cout << "Created game" << endl;

  clock_t playgame_s = clock();
  bool playerwins = qg->reachabilitygame(opt->playerid);
  clock_t playgame_e = clock();
  double playgame = ((double) (playgame_e- playgame_s)) / CLOCKS_PER_SEC;

  cout << " " << endl;
  cout << "Input quant. game : " << gg->getStateNum() << " states " << endl;
  cout << "Reachability game : " << qg->getallstates() << " states " << endl;
  cout << "Game creation     : " <<  creategraph << " seconds" << endl;
  cout << "Game play         : " <<  playgame << " seconds" << endl;
  cout << " " << endl;
    
  if (!playerwins){
    cout << "Player " << opt->playerid << " does not win" <<  endl;
  }
  else{
    cout << "Player " << opt->playerid << " wins " <<  endl;
    if (opt->synthesis){
      qg->rawprint(opt->playerid);

    }
  }

  return 0;
}

