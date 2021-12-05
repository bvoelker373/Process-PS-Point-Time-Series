"""Merges two excel files by a common key, with a 'left join' by default. Resulting table is saved as CSV.
from https://www.geeksforgeeks.org/joining-excel-data-from-multiple-files-using-python-pandas/"""

# importing the module
import pandas
  
# reading the files
f1 = pandas.read_excel("OR_PS_Within_LS.xls")
f2 = pandas.read_excel("TS_PRE.xlsx")
  
# merging the files
f3 = f1.merge(f2, on = "Point_ID", how = "left")
  
# creating a new file
f3.to_csv('merged.csv', index=False)
