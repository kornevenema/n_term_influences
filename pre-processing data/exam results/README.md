# Exam results processing
#### explanation of directory content 
This directory contains a directory [links_to_results](links_to_results) with txt files that contain all the 
links to the results of every degree in the Netherlands from 2012 to 2019.

The program [exam_results.py](exam_results.py) extracts all the information needed.

the [config.json](../../config.json) file contains configurations for the years and degrees the user wants to process.

#### how to use the program exam_results.py
The program should do all the hard work. You only need to provide the links to the results. 
(links to results in 2012 to 2019 are already provided.)
If you want to for example add the results of havo in year 2020, 
you will have to provide the link to those results in the links_to_results directory. 
Obviously you need to put the havo results in the havo.txt file and so on.
The program will create some directories and 
download all the needed csv file according to the configurations you provided in the [config file](../../config.json).


>###### This is only needed if you provide your own data
>When providing your own data, you can create a directory in this directory with the name "results". 
>After that, in that directory you have to create 3 more directories "havo_grades", "vmbo_grades" and "vwo_grades".
>There you can place the corresponding results. Havo results go in the "havo_grades" directory etc. 
>There should not be any other file then the exam results. 

After having done at least one of the 2 previous steps, you can run the program process_exam_results.py like this:
```
python process_exam_results.py path_to_results_directory
```
leave 'path_to_results_directory' empty when NOT providing your own data!!
The program will use [these links](links_to_results) to download the data.

The path to the directory with all the results is needed if it is not in the current directory. 
(e.g. C:\Users\user_name\Desktop) 
Leave empty if it is in the current directory.