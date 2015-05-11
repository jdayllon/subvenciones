# From http://stackoverflow.com/a/28682959 thanks to @mfitzp http://stackoverflow.com/users/754456/mfitzp
import re
import pandas 
import warnings

myfile = 'data/datos_subvenciones.csv'
target_type = str  # The desired output type

with warnings.catch_warnings(record=True) as ws:
    warnings.simplefilter("always")

    mydata = pandas.read_csv(myfile, sep=",", decimal=",", header=None)
    print("Warnings raised:", ws)
    # We have an error on specific columns, try and load them as string
    for w in ws:
        s = str(w.message)
        print("Warning message:", s)
        match = re.search(r"Columns \(([0-9,]+)\) have mixed types\.", s)
        if match:
            columns = match.group(1).split(',') # Get columns as a list
            columns = [int(c) for c in columns]
            print("Applying %s dtype to columns:" % target_type, columns)
            mydata.iloc[:,columns] = mydata.iloc[:,columns].astype(target_type)