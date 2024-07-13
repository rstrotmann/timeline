
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'ADD ASSIGN BEGIN COLOR COMMENT DATE END EQUALS IMPORT INT PARAMETER RANGE SOURCE START_SECTION START_THREAD SYMBOL_NAME TIMEUNIT\n    expression : point\n               | interval\n               | thread\n               | section\n               | chart\n               | source\n               | import\n    \n    source : SOURCE\n    \n    import : IMPORT\n    \n    temp_chart : BEGIN section\n               | BEGIN source\n    \n    temp_chart : temp_chart section\n    \n    chart : temp_chart END\n    \n    temp_section : START_SECTION thread\n    \n    temp_section : START_SECTION COLOR thread\n    \n    temp_section : temp_section thread\n    \n    section : temp_section\n    \n    temp_thread : START_THREAD point\n                | START_THREAD interval\n    \n    temp_thread : temp_thread point\n                | temp_thread interval\n    \n    thread : temp_thread\n    \n    point : SYMBOL_NAME ASSIGN DATE\n    \n    point : SYMBOL_NAME ASSIGN DATE PARAMETER\n    \n    interval : SYMBOL_NAME ASSIGN DATE RANGE DATE\n    \n    interval : SYMBOL_NAME ASSIGN DATE RANGE DATE PARAMETER\n    '
    
_lr_action_items = {'SYMBOL_NAME':([0,10,15,19,20,24,25,30,32,34,35,],[9,9,9,-20,-21,-18,-19,-23,-24,-25,-26,]),'SOURCE':([0,17,],[13,13,]),'IMPORT':([0,],[14,]),'START_THREAD':([0,10,11,16,19,20,21,24,25,26,27,30,31,32,34,35,],[15,-22,15,15,-20,-21,-16,-18,-19,-14,15,-23,-15,-24,-25,-26,]),'START_SECTION':([0,10,11,12,13,17,19,20,21,23,24,25,26,28,29,30,31,32,34,35,],[16,-22,-17,16,-8,16,-20,-21,-16,-12,-18,-19,-14,-10,-11,-23,-15,-24,-25,-26,]),'BEGIN':([0,],[17,]),'$end':([1,2,3,4,5,6,7,8,10,11,13,14,19,20,21,22,24,25,26,30,31,32,34,35,],[0,-1,-2,-3,-4,-5,-6,-7,-22,-17,-8,-9,-20,-21,-16,-13,-18,-19,-14,-23,-15,-24,-25,-26,]),'ASSIGN':([9,],[18,]),'END':([10,11,12,13,19,20,21,23,24,25,26,28,29,30,31,32,34,35,],[-22,-17,22,-8,-20,-21,-16,-12,-18,-19,-14,-10,-11,-23,-15,-24,-25,-26,]),'COLOR':([16,],[27,]),'DATE':([18,33,],[30,34,]),'PARAMETER':([30,34,],[32,35,]),'RANGE':([30,],[33,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'expression':([0,],[1,]),'point':([0,10,15,],[2,19,24,]),'interval':([0,10,15,],[3,20,25,]),'thread':([0,11,16,27,],[4,21,26,31,]),'section':([0,12,17,],[5,23,28,]),'chart':([0,],[6,]),'source':([0,17,],[7,29,]),'import':([0,],[8,]),'temp_thread':([0,11,16,27,],[10,10,10,10,]),'temp_section':([0,12,17,],[11,11,11,]),'temp_chart':([0,],[12,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> expression","S'",1,None,None,None),
  ('expression -> point','expression',1,'p_expression_atomic','tlparser.py',10),
  ('expression -> interval','expression',1,'p_expression_atomic','tlparser.py',11),
  ('expression -> thread','expression',1,'p_expression_atomic','tlparser.py',12),
  ('expression -> section','expression',1,'p_expression_atomic','tlparser.py',13),
  ('expression -> chart','expression',1,'p_expression_atomic','tlparser.py',14),
  ('expression -> source','expression',1,'p_expression_atomic','tlparser.py',15),
  ('expression -> import','expression',1,'p_expression_atomic','tlparser.py',16),
  ('source -> SOURCE','source',1,'p_source','tlparser.py',24),
  ('import -> IMPORT','import',1,'p_import','tlparser.py',30),
  ('temp_chart -> BEGIN section','temp_chart',2,'p_chart','tlparser.py',38),
  ('temp_chart -> BEGIN source','temp_chart',2,'p_chart','tlparser.py',39),
  ('temp_chart -> temp_chart section','temp_chart',2,'p_chart2','tlparser.py',45),
  ('chart -> temp_chart END','chart',2,'p_chart1','tlparser.py',52),
  ('temp_section -> START_SECTION thread','temp_section',2,'p_section','tlparser.py',62),
  ('temp_section -> START_SECTION COLOR thread','temp_section',3,'p_section_color','tlparser.py',69),
  ('temp_section -> temp_section thread','temp_section',2,'p_section1','tlparser.py',77),
  ('section -> temp_section','section',1,'p_section2','tlparser.py',86),
  ('temp_thread -> START_THREAD point','temp_thread',2,'p_thread','tlparser.py',96),
  ('temp_thread -> START_THREAD interval','temp_thread',2,'p_thread','tlparser.py',97),
  ('temp_thread -> temp_thread point','temp_thread',2,'p_thread1','tlparser.py',104),
  ('temp_thread -> temp_thread interval','temp_thread',2,'p_thread1','tlparser.py',105),
  ('thread -> temp_thread','thread',1,'p_thread2','tlparser.py',113),
  ('point -> SYMBOL_NAME ASSIGN DATE','point',3,'p_point','tlparser.py',122),
  ('point -> SYMBOL_NAME ASSIGN DATE PARAMETER','point',4,'p_point1','tlparser.py',130),
  ('interval -> SYMBOL_NAME ASSIGN DATE RANGE DATE','interval',5,'p_interval','tlparser.py',141),
  ('interval -> SYMBOL_NAME ASSIGN DATE RANGE DATE PARAMETER','interval',6,'p_interval1','tlparser.py',148),
]
