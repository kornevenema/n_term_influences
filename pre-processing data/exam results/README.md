# Exam results processing

The exam results of all the exams in the Netherlands in the past 8 year will be processed in this directory.
These should be a shell script and when executed, it should create a directory with 3 subdirectories 
containing all the exam results of high school in the Netherlands from 2012 to 2019.
 
When providing your own data, you can create a directory in this directory with the name "results". 
After that, in that directory you have to create 3 more directories "havo_grades", "vmbo_grades" and "vwo_grades".
There you can place the corresponding results. Havo results go in the "havo_grades" directory etc. 
There should not be any other file then the exam results. 

After having done at least one of the 2 previous steps, you can run the program process_exam_results.py like this:
```
python process_exam_results.py path_to_results_directory
```

path to results directory is needed if it is not in the current directory. (e.g. C:\Users\user_name\Desktop) 
Leave empty if it is in the current directory. 