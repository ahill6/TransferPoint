### Setup

```java
public static char grade(double one, double two, double three, double four, double grade){
		
		char score = 'A';
		
		  if(grade > one)
			  score = 'A';
		  else if (grade > two)
			  score = 'B';
		  else if (grade > three)
			  score = 'C';
		  else if (grade > four)
			  score = 'D';
		  
		  return score;
		}
```

Above is the example for the paper, below is the instructor solution it is trying to find.  For ease of explanation, this
example will treat the entire method as the System Under Test (SUT).
	
```java
public static double grade(double aval, double bval, double cval, double dval, double score){
  if(score >= aval)
     return 'A';
  else if (score >= bval)
     return 'B';
  else if (score >= cval)
     return 'C';
  else if (score >= dval)
     return 'D';
  else  return 'F';
}
```

As you can see, the variables have different names, all four of the conditionals are incorrect (> rather than >=), and
the approach in the former is to set an answer variable in each conditional rather than immediately return the answer.

The incorrect conditional is a relatively minor error from a conceptual point of view, but results 4 of 9 unit tests failing.
Additionally, incorrectly initializing the variable to 'A' rather than the result of the final implied <i>else<\i> (i.e. 'F')
fails an additional unit test.

Thus, although this effort is easily and quickly corrected by a human, the method passes only 4 of 9 unit tests and requires 5
distinct edits to patch.

### Symbolic Execution

### Canonical Form

### Edit Distance
