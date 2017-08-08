```java
public static int smallest(int num1,int num2,int num3,int num4){
  int	bigger, bigger2, biggest;
  
  if (num1 < num2)
    bigger = num1;
  else
    bigger = num2;
  if (num4 < num3)
    bigger2 = num4;
  else
    bigger2 = num3;
  if (bigger < bigger2)
    biggest = bigger;
  else biggest = bigger2;

	return biggest;
	}
```
