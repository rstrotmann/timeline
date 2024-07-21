
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'ADD ALIAS ALL ASSIGN BEGIN COLOR COMMENT DATE END EQUALS IMPORT INT MARKER PARAMETER RANGE SECTION SOURCE START_SECTION START_THREAD SYMBOL_NAME THREAD TIMEUNIT\n    expression : point\n               | interval\n               | thread\n               | section\n               | chart\n               | source\n               | import\n               | marker\n    \n    source : SOURCE\n    \n    import : IMPORT\n    \n    temp_chart : BEGIN section\n               | BEGIN source\n               | BEGIN marker\n    \n    temp_chart : temp_chart section\n    \n    temp_chart : temp_chart source\n               | temp_chart marker\n    \n    chart : temp_chart END\n    \n    marker : MARKER DATE\n    \n    marker : MARKER DATE PARAMETER\n    \n    temp_section : SECTION SYMBOL_NAME\n    \n    temp_section : SECTION SYMBOL_NAME PARAMETER\n    \n    temp_section : temp_section thread\n    \n    temp_section : temp_section import\n    \n    section : temp_section\n    \n    temp_thread : THREAD SYMBOL_NAME\n    \n    temp_thread : THREAD SYMBOL_NAME PARAMETER\n    \n    temp_thread : temp_thread point\n                | temp_thread interval\n                | temp_thread marker\n    \n    thread : temp_thread\n    \n    point : SYMBOL_NAME ASSIGN DATE\n    \n    point : SYMBOL_NAME ASSIGN DATE PARAMETER\n    \n    interval : SYMBOL_NAME ASSIGN DATE RANGE DATE\n    \n    interval : SYMBOL_NAME ASSIGN DATE RANGE DATE PARAMETER\n    '
    
_lr_action_items = {'SYMBOL_NAME':([0,11,17,18,21,22,23,30,31,36,37,38,40,42,43,],[10,10,31,32,-27,-28,-29,-18,-25,-31,-19,-26,-32,-33,-34,]),'SOURCE':([0,11,12,13,14,15,19,21,22,23,24,25,27,28,29,30,31,32,33,34,35,36,37,38,39,40,42,43,],[14,-30,-24,14,-9,-10,14,-27,-28,-29,-22,-23,-14,-15,-16,-18,-25,-20,-11,-12,-13,-31,-19,-26,-21,-32,-33,-34,]),'IMPORT':([0,11,12,15,21,22,23,24,25,30,31,32,36,37,38,39,40,42,43,],[15,-30,15,-10,-27,-28,-29,-22,-23,-18,-25,-20,-31,-19,-26,-21,-32,-33,-34,]),'MARKER':([0,11,12,13,14,15,19,21,22,23,24,25,27,28,29,30,31,32,33,34,35,36,37,38,39,40,42,43,],[16,16,-24,16,-9,-10,16,-27,-28,-29,-22,-23,-14,-15,-16,-18,-25,-20,-11,-12,-13,-31,-19,-26,-21,-32,-33,-34,]),'THREAD':([0,11,12,15,21,22,23,24,25,30,31,32,36,37,38,39,40,42,43,],[17,-30,17,-10,-27,-28,-29,-22,-23,-18,-25,-20,-31,-19,-26,-21,-32,-33,-34,]),'SECTION':([0,11,12,13,14,15,19,21,22,23,24,25,27,28,29,30,31,32,33,34,35,36,37,38,39,40,42,43,],[18,-30,-24,18,-9,-10,18,-27,-28,-29,-22,-23,-14,-15,-16,-18,-25,-20,-11,-12,-13,-31,-19,-26,-21,-32,-33,-34,]),'BEGIN':([0,],[19,]),'$end':([1,2,3,4,5,6,7,8,9,11,12,14,15,21,22,23,24,25,26,30,31,32,36,37,38,39,40,42,43,],[0,-1,-2,-3,-4,-5,-6,-7,-8,-30,-24,-9,-10,-27,-28,-29,-22,-23,-17,-18,-25,-20,-31,-19,-26,-21,-32,-33,-34,]),'ASSIGN':([10,],[20,]),'END':([11,12,13,14,15,21,22,23,24,25,27,28,29,30,31,32,33,34,35,36,37,38,39,40,42,43,],[-30,-24,26,-9,-10,-27,-28,-29,-22,-23,-14,-15,-16,-18,-25,-20,-11,-12,-13,-31,-19,-26,-21,-32,-33,-34,]),'DATE':([16,20,41,],[30,36,42,]),'PARAMETER':([30,31,32,36,42,],[37,38,39,40,43,]),'RANGE':([36,],[41,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'expression':([0,],[1,]),'point':([0,11,],[2,21,]),'interval':([0,11,],[3,22,]),'thread':([0,12,],[4,24,]),'section':([0,13,19,],[5,27,33,]),'chart':([0,],[6,]),'source':([0,13,19,],[7,28,34,]),'import':([0,12,],[8,25,]),'marker':([0,11,13,19,],[9,23,29,35,]),'temp_thread':([0,12,],[11,11,]),'temp_section':([0,13,19,],[12,12,12,]),'temp_chart':([0,],[13,]),}

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
  ('expression -> marker','expression',1,'p_expression_atomic','tlparser.py',17),
  ('source -> SOURCE','source',1,'p_source','tlparser.py',27),
  ('import -> IMPORT','import',1,'p_import','tlparser.py',33),
  ('temp_chart -> BEGIN section','temp_chart',2,'p_chart','tlparser.py',42),
  ('temp_chart -> BEGIN source','temp_chart',2,'p_chart','tlparser.py',43),
  ('temp_chart -> BEGIN marker','temp_chart',2,'p_chart','tlparser.py',44),
  ('temp_chart -> temp_chart section','temp_chart',2,'p_chart1','tlparser.py',50),
  ('temp_chart -> temp_chart source','temp_chart',2,'p_chart2','tlparser.py',57),
  ('temp_chart -> temp_chart marker','temp_chart',2,'p_chart2','tlparser.py',58),
  ('chart -> temp_chart END','chart',2,'p_chart3','tlparser.py',65),
  ('marker -> MARKER DATE','marker',2,'p_marker','tlparser.py',75),
  ('marker -> MARKER DATE PARAMETER','marker',3,'p_marker1','tlparser.py',81),
  ('temp_section -> SECTION SYMBOL_NAME','temp_section',2,'p_section','tlparser.py',91),
  ('temp_section -> SECTION SYMBOL_NAME PARAMETER','temp_section',3,'p_section1','tlparser.py',97),
  ('temp_section -> temp_section thread','temp_section',2,'p_section2','tlparser.py',103),
  ('temp_section -> temp_section import','temp_section',2,'p_section3','tlparser.py',110),
  ('section -> temp_section','section',1,'p_section4','tlparser.py',117),
  ('temp_thread -> THREAD SYMBOL_NAME','temp_thread',2,'p_thread','tlparser.py',127),
  ('temp_thread -> THREAD SYMBOL_NAME PARAMETER','temp_thread',3,'p_thread1','tlparser.py',133),
  ('temp_thread -> temp_thread point','temp_thread',2,'p_thread2','tlparser.py',139),
  ('temp_thread -> temp_thread interval','temp_thread',2,'p_thread2','tlparser.py',140),
  ('temp_thread -> temp_thread marker','temp_thread',2,'p_thread2','tlparser.py',141),
  ('thread -> temp_thread','thread',1,'p_thread3','tlparser.py',148),
  ('point -> SYMBOL_NAME ASSIGN DATE','point',3,'p_point','tlparser.py',158),
  ('point -> SYMBOL_NAME ASSIGN DATE PARAMETER','point',4,'p_point1','tlparser.py',165),
  ('interval -> SYMBOL_NAME ASSIGN DATE RANGE DATE','interval',5,'p_interval','tlparser.py',176),
  ('interval -> SYMBOL_NAME ASSIGN DATE RANGE DATE PARAMETER','interval',6,'p_interval1','tlparser.py',183),
]
