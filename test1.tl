source test.tl
#source tl_source1.tl

#MARKER 1-Oct-2024
#MARKER 8-Nov-2024

SECTION s2 (color: blue)
THREAD t1
    point 5: 1-Jun-2024
    
THREAD t2
  point 4: 1-5-25

SECTION Project A (color: yellow)
IMPORT * FROM Regulatory
IMPORT study 1 FROM Clinical (highlight: True)

THREAD Governance
DULT meeting: 1-Jun-24


THREAD Team
Discussion: 1-May - 1-Jun
Celebration: 15-Aug
