PROGRAM FIZZBUZZ;

var x , y : integer; 

BEGIN 
    FOR x := 1 ; TO 100 DO 
        IF x MOD 15 = 0 THEN
            WRITELN ( 'Fizzbuzz' );
        ELSE
            WRITELN ( x );

END.
