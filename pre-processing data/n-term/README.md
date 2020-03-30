# How to use

#### explanation of directory content 
This directory contains a directory [links_to_n-terms](links_to_n-terms) with txt files that contain all the 
links to the n-terms of every degree in the Netherlands from 2012 to 2019.

The program [n_term_to_csv.py](n-terms.py) scrapes these websites and extracts all the information needed.

the [config.json](../../config.json) file contains configurations for the years and degrees the user wants to process.

#### how to use the program n-terms.py
The program should do all the hard work. You only need to provide the links to the n-term websites. 
(links to n-terms in 2012 to 2019 are already provided.)
These n-term websites can be found online, and will be published about a month after the exam every year. 
If you want to for example add the n-term of havo in year 2020, you will have to provide the link to those 
n-terms in the links_to_n-terms directory. Obviously you need to put the havo n-terms in the havo.txt file and so on.

>Finding the n-terms on [examenblad.nl](https://www.examenblad.nl/) is really hard if you don't know how. 
>The steps you have to take are:
>- in the top left corner, select the desired year and degree.
>- Then in the left sidebar 'Nieuws' find something like 'Normering (degree goes here) 1e tijdvak (year goes here)'
>- Then after the text 'Ontsluitende tabellen (degree) 1e tijdvak (year)' you can find a link to the table with the n-terms

You can also configure some settings in the config.json file like years and degrees. To continue on the example:
You need to add 2020 to the list of years.

run: 
```python
python n-terms.py
```
This will create 3 csv files (if they don't exist):
- one with all the n-terms of the given configurations in the config.json file.
- one with the filtered n-terms.
- one with the complete version including average n-terms.
 
The configs used for this research: (see current config)

- years = 2012 - 2019
- degrees = vmbo BB, KB, GL en TL, havo and vwo

The date on which the n-terms were created and used is 19-03-2020