% Step 2: Specify the input format for the 3x3 matrix
array[1..3, 1..3] of int: matrix;

% Step 4: Define the output to indicate whether the matrix is antisymmetric or not
var bool: is_antisymmetric = true;


% Step 3: Implement the constraint for antisymmetry
constraint forall(i, j in 1..3 where i < j)(
    matrix[i, j] == -matrix[j, i]
);

% Additional constraints to ensure all elements are integers (optional)
constraint forall(i, j in 1..3)(
    matrix[i, j] < 10
);

% Solve for the antisymmetry
solve satisfy;

% Output the result
output ["Matrix is antisymmetric: \(is_antisymmetric)"];