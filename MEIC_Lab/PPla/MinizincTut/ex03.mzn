% MORE ABOUT CONDITIONS

var int: z = 0;
var int: r;

constraint if z == 0 then r == 1 else r == 0 endif;

solve satisfy;