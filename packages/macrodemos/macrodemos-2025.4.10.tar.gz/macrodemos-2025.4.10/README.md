# MACRODEMOS

## Macroeconomics Demos: A Python package to teach macroeconomics and macroeconometrics

The purpose of this package is to provide tools to teach concepts of macroeconomics and macroeconometrics.

To date, the package provides these functions:

* **ARMA( )**: Demo for learning about  ARMA processes. It creates a dash consisting of 7 plots to study the theoretical properties of ARMA(p, q) processes, as well as their estimated counterparts. The plots display
    1. a simulated sample
    2. autocorrelations
    3. partial autocorrelations
    4. impulse response function
    5. spectral density
    6. AR inverse roots
    7. MA inverse roots.
*  **Markov('state_0',...,'state_n')**: a demo to illustrate Markov chains. User sets the number of states, the transition matrix, and the initial distribution. The demo creates a dash consisting of 2 plots:
    1. a simulated sample
    2. the time evolution of the distribution of states
*  **Solow( )**: this demo illustrates the Solow-Swan model. Users can simulate the dynamic effect of a shock in a exogenous variable or a change in a model parameter. You will find 6 figures about the Solow-Swan model:
    1. Capital stock, per capita
    2. Output per capita,
    3. Savings per capita,
    4. Consumption per capita,
    5. Change in capital stock, and
    6. Output growth rate 
   
    It also presents plots to illustrate how steady-state capital is determined, and the golden rule. 
*  **filters( )**: to illustrate the use of the Hodrick-Prescott, Baxter-King, Christiano-Fitzgeral and Hamilton filters.

In a near future, I expect to add a few more demos:

* **Bellman( )**: to illustrate the solution of a Bellman equation by value function iteration
* **BoxJenkins( )**: to illustrate the Box-Jenkins methodology, by fitting two ARIMA models side-by-side to user-provided data.  
* **FilterMyData( )**: to filter user-supplied data with several methodologies, comparing their resulting cycles. 
 
### Instructions
To use the demos, just install this package `pip install macrodemos` and then run any of the demos you want.

    import macrodemos
    macrodemos.ARMA()
    macrodemos.Markov()
    macrodemos.Solow()
    macrodemos.filter()
 
This will open a new tab in your default Internet browser with a Plotly dash. A current limitation is that you can only run 
one demo at a time.

### Disclaimer 
This program illustrates basic concepts of macroeconomics and time series econometrics. It was developed for teaching purposes 
only: you are free to use it in your own lectures or to learn about these topics.  

If you have any suggestions, please send me an email at randall.romero@ucr.ac.cr
                          
**Copyright 2016-2024 Randall Romero-Aguilar**
