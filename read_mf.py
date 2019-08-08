import pandas as pd
import numpy as np


######Dealing with mf.YEAR files
Types = (float, str)

def tokenize(line):
    if("Stanford" in line):
        return []
    if("Jan" in line):
        return []
    
    line = line.strip()
    line = line.replace("           ", "     D     ").replace(".","NA")
    line = line.split("    ")
    line = list(map(lambda x: x.strip(), line))
    tmp = []
    for el in line:
        for e in el.split("  "):
            tmp.append(e)
    line = tmp
    if(len(line) not in [1,13]):
        print("A", len(line))
        print(line)
    result = line
    return result

def parse_line(tokens: str, debug=False) -> list:
    if(len(tokens) in [0]):
        return False
    if(len(tokens) == 1):
        try:
            if(int(tokens[0]) in range(1950, 2020)):
                return int(tokens[0])
        except:
            return False

    if(len(tokens) != 13):
        print("!")
    result = []
    for token in tokens:
        for Type in Types:
            try:
                token = Type(token)
                result.append(token)
                break
            except ValueError:
                continue
    #Check if first column is correct day number
    if(result[0] not in range(1,31)):
        if(debug):
            raise SyntaxError
        else:
            return False
    
    #transform 
    row = {

    }

    for i, token in enumerate(result):
        if(i == 0):
            continue
        if(token == 'D'):
            continue
        row[
            "-".join(
                [str(i).rjust(2,'0'),str(int(result[0])).rjust(2,'0')]
                )
            ] = token

    return row

def parse(file: list) -> dict:
    result = {
        "year": 0,
        "data": {}
    }
    for i,line in enumerate(file):
        line = line.strip()
        if(line == None):
            continue
        if(len(line) == 0):
            continue
        line = parse_line(tokenize(line))
        if(not line):
            continue
        if(type(line) is int):
            result["year"] = line
        else:
            result["data"].update(line)
    return result

def read_mf(filelist: list) -> pd.DataFrame:
    result = []
    result_string = "date;mf\n"
    for file in filelist:
        file = open(file, "r")
        year_data = parse(file)
        for key in year_data['data'].keys():
            result_string += (str(year_data['year'])+"-"+key+";"+ str(year_data['data'][key]).strip()+"\n")
    from io import StringIO
    result_string = StringIO(result_string)
    result = pd.read_csv(
        result_string,
        sep=";",
        header=0,
        parse_dates=['date'],
        index_col="date"
        ).sort_values(by='date')
    return result

#Example
mf_data = read_mf(["mf.1975", "mf.1976"])
mf_data.plot()
