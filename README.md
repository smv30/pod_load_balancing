# pod_load_balancing
Power-of-d Load Balancing

Use the following to run the code on the command line:
```
python main.py -n 1000 -m 3 -g 0.4
```
where -n is the number of servers, -m sets $d$ be the greatest integer such that $d \leq (2mn \log d)^{1/m}$. If such a $d > n$, then we use $d= n$. Lastly, -g sets the arrival rate as $n - n^{1-\gamma}$. 
