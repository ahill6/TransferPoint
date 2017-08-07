```java
// 8/8 unit tests, 3.0 edit distance
	public static int smallest(int a,int b,int c,int d){
		int x=-1;
		
		if (a>=b)
			x = b;
		else
			x = a;
		if (x>=c)
			x = c;
		if (x>=d)
			x = d;
			
		return x;
		}
```
The above code is straightforward.  The smaller of a and b is placed in a variable that should probably be named 
<i>smallest</i>.  The rest of the program is the straightforward matter of checking the current smallest against 
remaining values.  While not the most algorithmically elegant, this code covers all cases and is one of the most 
efficient implementations (in terms of lines of code).

By contrast, the code below unnecessarily sets the variable num_smallest before returning it, in addition to performing 4x
more comparisons than the first snippet to perform the same task.  

```java
 // passes 8/8 unit tests, edit distance 32.0   
 public static int smallest(int num1,int num2,int num3,int num4){
		int num_smallest;
		if ((num1 <= num2) && (num1 <= num3) && (num1 <= num4))
			{
			num_smallest = num1;
			return num_smallest;
			}
	    else if ((num2 <= num1) && (num2 <= num3) && (num2 <= num4))
	            {
			 num_smallest = num2;
	                 return num_smallest;
	                }
	        else if ((num3 <= num1) && (num3 <= num2) && (num3 <= num4))
	                {
			num_smallest = num3;
	                return num_smallest;
	                }
	        else if ((num4 <= num1) && (num4 <= num2) && (num4 <= num3))
	            	{
			num_smallest = num1;
	                return num_smallest;
	              	}
	return -1;
	}
```
There is clearly an enormous difference in terms of quality of organization, efficiency, and even basic coding practices 
between these two pieces of code, yet both are considered identical by approaches which consider only number of unit tests passed.

Now consider the difference in edit distance to the instructor solution.  The first is identified as closer to the desired answer
by an order of magnitude.  This suggests that semantic analysis with distance calculations could also act as an approximation for
soft skill metrics when provided with a suitable example of good coding practices.
