﻿'''
Created on 19 jan. 2016

@author: Bunyamin Sakar
'''
from enum import Enum

class PlayerCards(Enum):
    RockyBelboa = {
            1:{
                1:{"damage":10,"condition":-2},
                2:{"damage":20,"condition":-5},
                3:{"damage":30,"condition":-8}
              },
            2:{
                1:{"damage":8,"condition":-3},
                2:{"damage":13,"condition":-4},
                3:{"damage":17,"condition":-5}
             },
            3:{
                1:{"damage":3,"condition":-1},
                2:{"damage":9,"condition":-2},
                3:{"damage":19,"condition":-3}
            },
            4:{
                1:{"damage":5,"condition":-2},
                2:{"damage":11,"condition":-3},
                3:{"damage":15,"condition":-5}
            },
            5:{
                1:{"damage":7,"condition":-2},
                2:{"damage":12,"condition":-3},
                3:{"damage":16,"condition":-4}
            },
            6:{
                1:{"damage":2,"condition":-1},
                2:{"damage":4,"condition":-2},
                3:{"damage":6,"condition":-3}
             }
        }
    
    MannyPecquiao = {
            1:{
                1:{"damage":8,"condition":-3},
                2:{"damage":13,"condition":-4},
                3:{"damage":17,"condition":-5}
              },
            2:{
                1:{"damage":10,"condition":-2},
                2:{"damage":20,"condition":-5},
                3:{"damage":30,"condition":-8}
             },
            3:{
                1:{"damage":5,"condition":-2},
                2:{"damage":11,"condition":-3},
                3:{"damage":15,"condition":-5}
            },
            4:{
                1:{"damage":3,"condition":-1},
                2:{"damage":9,"condition":-2},
                3:{"damage":19,"condition":-3}
            },
            5:{
                1:{"damage":2,"condition":-1},
                2:{"damage":4,"condition":-2},
                3:{"damage":6,"condition":-3}
            },
            6:{
                1:{"damage":7,"condition":-2},
                2:{"damage":12,"condition":-3},
                3:{"damage":16,"condition":-4}
             }
        }  
    
    MikeTysen = {
            1:{
                1:{"damage":5,"condition":-2},
                2:{"damage":11,"condition":-3},
                3:{"damage":15,"condition":-5}
              },
            2:{
                1:{"damage":3,"condition":-1},
                2:{"damage":9,"condition":-2},
                3:{"damage":19,"condition":-3}
             },
            3:{
                1:{"damage":2,"condition":-1},
                2:{"damage":4,"condition":-2},
                3:{"damage":6,"condition":-3}
            },
            4:{
                1:{"damage":7,"condition":-2},
                2:{"damage":12,"condition":-3},
                3:{"damage":16,"condition":-4}
            },
            5:{
                1:{"damage":8,"condition":-3},
                2:{"damage":13,"condition":-4},
                3:{"damage":17,"condition":-5}
            },
            6:{
                1:{"damage":10,"condition":-3},
                2:{"damage":20,"condition":-3},
                3:{"damage":30,"condition":-3}
             }
        }
    
    MohammedAli = {
            1:{
                1:{"damage":1,"condition":-1},
                2:{"damage":9,"condition":-2},
                3:{"damage":19,"condition":-3}
              },
            2:{
                1:{"damage":5,"condition":-2},
                2:{"damage":11,"condition":-3},
                3:{"damage":15,"condition":-4}
             },
            3:{
                1:{"damage":7,"condition":-2},
                2:{"damage":12,"condition":-3},
                3:{"damage":16,"condition":-4}
            },
            4:{
                1:{"damage":2,"condition":-1},
                2:{"damage":4,"condition":-2},
                3:{"damage":6,"condition":-3}
            },
            5:{
                1:{"damage":10,"condition":-2},
                2:{"damage":20,"condition":-5},
                3:{"damage":30,"condition":-8}
            },
            6:{
                1:{"damage":8,"condition":-3},
                2:{"damage":13,"condition":-4},
                3:{"damage":17,"condition":-5}
             }
        }