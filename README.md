# n_term_influences
All programs and data sources used in the research: 
"What is the influence of the N-Term on different high school degrees in the Netherlands?" By Korné Venema

## data used
#### N-terms
In the directory [pre-processing data/n-term](pre-processing data/n-term/) you can find how the n-terms are obtained. 
Read the [README.md](pre-processing data/n-term//README.md) for more instructions.
#### Results
In the directory [pre-processing data/exam results](pre-processing data/exam results/) you can find how the n-terms are obtained. 
Read the [README.md](pre-processing data/exam results//README.md) for more instructions.

The results of all the high schools in the Netherlands can be found on 
[this webpage](https://www.duo.nl/open_onderwijsdata/databestanden/vo/leerlingen/) in the sections 8 to 10.
#### research results
The research results can be found in [main.ipynb](main.ipynb). 
In Jupyter Notebook, navigate to this directory and open [main.ipynb](main.ipynb) 
and run all the cells to get the results.
You first need to execute 2 other programs in order to proceed. (the order does matter)
This can be done by navigation to [n-term](pre-processing data/n-term) and execute:

```
python n-terms.py
```
More explanation in this [README.md](pre-processing data/n-term/README.md).
The second file can be found in  
and should be navigated to [exam results](pre-processing data/exam results) and then execute the following:
```
python exam_results.py
```
More explanation in this [README.md](pre-processing data/exam results/README.md) 

### notes
Execution times might be a little long. Some indication of progress is provided, but some steps take some time.

## libraries imported which are not standard
- requests
- bs4 (BeautifulSoup)
- pandas
