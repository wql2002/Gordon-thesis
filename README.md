# thu-Gordon
Localised bottlenecks for server transport layer protocol analysis.  

## Dependancies:
```Scripts/quick_dependancies.sh```

## Runnning tests:
### Single runs 
1. Launch a delay shell  
```$ mm-delay 50```  
2. The scripts for running the necessary tests are in *Scripts/*  
```mm-delay 50 $ cd Scripts/```  
3. Launching the test  
```mm-delay 50 $ ./launch.sh <target_URL>```  
4. Ending all processes *(not necessary)*
```mm-delay 50 $ ./clean.sh```

## Running tests with multiple trials per RTT (for cleaner results)
1. Launch a delay shell  
```$ mm-delay 50```  
2. The scripts for running the necessary tests are in *Scripts/*  
```mm-delay 50 $ cd Scripts/```  
3. Launching the test  
```mm-delay 50 $ ./multi-launch.sh <target_URL> <number of trials per RTT>```  
each trial's data will be stored in Gordon/Data/windows<trail_num>.csv  
cleaned data is stored in Gordon/Data/windows.csv  
4. Ending all processes *(not necessary)*
```mm-delay 50 $ ./clean.sh```


## Reference

- Ayush Mishra, Xiangpeng Sun, Atishya Jain, Sameer Pande, Raj Joshi, and Ben Leong. ["The Great Internet TCP Congestion Control Census"](https://www.comp.nus.edu.sg/~bleong/publications/sigmetrics2020-gordon.pdf). Proceedings of the ACM on Measurement and Analysis of Computing Systems (SIGMETRICS 2019). Volume 3. Issue 3. December 2019.  
