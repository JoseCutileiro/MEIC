include alldifferent;

int : S;
int : N = S*S;

...


%INITIAL BOARD 

constraint forall (i)

% all diff rows 
constraint forall(i in PuzzleRange) (
    alldifferent( [puzzle[i,j] | j in PuzzleRange]);
)

% all diff cols 
constraint forall(j in PuzzleRange) (
    alldifferent( [puzzle[i,j] | i in PuzzleRange]);
)




