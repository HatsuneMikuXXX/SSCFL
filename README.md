"# SSCFLSO"

Format of instances:
|J| TAB |I|

d_1 TAB d_2 TAB ... TAB d_|I| TAB
u_1 TAB u_2 TAB ... TAB d_|J| TAB
f_1 TAB f_2 TAB ... TAB f_|J| TAB
c_{11} TAB c_{12} TAB ... TAB c{1|I|} TAB
c_{21} TAB c_{22} TAB ... TAB c{2|I|} TAB
    ...     ...     ...     ...
c_{|J|1} TAB c_{|J|2} TAB ... TAB c_{|J||I|} TAB
LEQ_1 TAB
LEQ_2 TAB
...
LEQ_|I| TAB

where:
J is the set of facilities
I is the set of clients
d_i is the demand of client i
u_j is the capacity of facility j
c_{ji} is the travel cost from facility j to client i
LEQ_i = j_i1 TAB ... TAB j_i|J| is the preference list of client i. j_i1 is the most preferred facility of client i.  

