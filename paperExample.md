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
Additionally, incorrectly initializing the variable <b>score</b> to 'A' rather than the result of the final implied <b>else</b> (i.e. 'F') fails an additional unit test.  Finally, the return types of the methods are different.  \footnote{Because Java treats chars as ints within a certain range, returning a char as a double is allowed.  This was originally an oversight in conversion, but was retained for the correct solution (and corrected for all buggy programs) to demonstrate the flexibility of this approach.}  

<b>N.B.</b> While it may sometimes be desirable to exclude methods based on type mismatches, this work seeks to find intermediate-level, language-agnostic matches so that it can be more widely applicable (e.g. to cross-language clone detection as well as program repair).  To the authors' knowledge, this type of requirement relaxation has never before been demonstrated in program repair.  This decision has no impact on the validity of results, as preprocessing to eliminate mismatches would have no effect on the method itself except to improve runtime.

Overall, this buggy program requires 5 distinct edits in a 10-line program and passes only 4 of 9 unit tests.  Debugging could be easily accomplished by a human, but this represents a case which would not be ideal for any of the existing repair techniques (as is proven by the fact that the current best performance on the Grades portion of IntroClass was accomplished by SearchRepair with 5 of 226 attempted programs successfully repaired.

### Symbolic Execution
Symbolic execution finds values which provide maximal branch coverage (subject to it being logically possible to reach all branches).  Generating constraints which define the path to each branch.  For example, in order to reach branch C (branches are here indexed by return values), the conditions would be:

```sql
score < aval
score < bval
score >= cval
```

The most common use of this information is the generation of unit tests with good coverage guarantees.  In program repair, solver-based approaches such as Angelix apply symbolic execution not to the SUT itself, but to a transformation of the SUT so that the constraints.  That is, a solution to the SAT problem no longer represents a path through the program, but instead represents a path through a corrected program.  This allows the solution of the SAT problem to be used to generate a patch.

Contrary to both of these approaches, this work uses the \emph{constraints themselves} to characterize program behavior.  A database search is then conducted to find code with similar behavior.  For maximum improvement, this database should only contain correct programs, but it is also possible to use unit tests to find which close match is a correct patch.\footnote{However, such an approach would then be subject to all the well-known criticisms of unit tests as a specification}


### Canonical Form
Once the constraints have been gathered by SPF, they must be put in a canonical form.  Previous work \cite{??} has tried using edit distance on programs to find matches, but did not have much success, as even simple variable renaming could introduce significant syntactic disparity.  The purpose of a canonical form in all fields is to have an abstract statement which transforms semantic similarity into syntactic similarity.  This is widely used in mathematics for similar purposes.  For example, there are infinitely many ways to describe a quadratic equation, but requiring the form $ax^2 + bx + c = 0$ creates a form in which similarities between syntactically distinct equations become apparent.  The normal form suggested in \cite{green??} is used here for the same reason.  Such normalization of constraints is necessary because this work is treating the constraints \emph{as themselves} the weak specification, a fundamentally different approach than any current in program repair.

Given the constraint above, the constraints are lexicographically ordered.  In this example, the constraints as given are already orderd, so no change is necessary.  Normalization to the form a_1x_1 + a_2x_2 + \cdots + a_nx_n <= 0 is given below.

```sql
score < aval  -->  score - aval + MIN <= 0
score < bval  -->  score - bval + MIN <= 0
score >= cval -->  cval - score <= 0
```

The constraints are then renamed from left to right.  This ensures that \textbf{x < y} and \textbf{a < b} will match one another.  In the case of the example, this would be

```sql
score - aval + MIN <= 0  -->  v0 - v1 + v2 <= 0
score - bval + MIN <= 0  -->  v0 - v3 + v2 <= 0
cval - score <= 0        -->  v4 - v0 <= 0 
```

The final constraint which would be saved to the database is the conjunct of these conditions (recall, this has been implicitly a conjunct the entire time).

```sql
v0 - v1 + v2 <= 0 && v0 - v3 + v2 <= 0 && v4 - v0 <= 0 
```

This would represent only one of the constraints.  The others would be derived from the paths to A, B, et al.  Together they represent the sum of all possible paths through the program.  It is assumed that this ``program shape'' is sufficient to characterize at least some method/snippet types, and the results of the experiments given below support that assumption.


### Edit Distance
Once in a canonical form, it remains to decide what is meant by ``close''.  In the quadratic example above, the ratio of the numeric values in various positions can be used to derive an extremely accurate description of relative distance between equations.  Regretably, that is not so in this case.  Because the canonical form does not retain numbers, the relationship can be merely categorical.  It is not clear whether this is a limitation inherent in the nature of code or in this particular normal form, but a  strong suspicion of the later should motivate further study in this area.

Because the constraints are essentially categorical data, string comparisons are the most natural means of calculating distance.  The standard (simple) metrics considered here were Longest Common Subsequence, Longest Common Substring, and Levenshtein (Edit) Distance.  Cosine similarity, and other metrics based upon it were not considered because their growth is exponential in the number of elements in the alphabet, and because cosine similarity does not take ordering of variables into account.\footnote{i.e. no difference between (a + b) - c and a - (b + c)}  Expanding this work to include other more exotic metrics or using n-grams as opposed to complete strings could be a useful extension for future work.
