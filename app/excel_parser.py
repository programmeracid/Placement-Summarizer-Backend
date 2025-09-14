import pandas as pd
import re

# df1 = pd.DataFrame({0:["dj","acid","nob","nihilist","narayanan"],
                #    1:["22BAI1092","22BAI10099","22BAI1037","22BAI1325","22BCE5207"],
                #    2:["a@gmail.com","b@vitstudent.ac.in","c@gmail.com","d@vitstudent.ac.in","e@gmail.com"]})

# df2 = pd.read_excel("JSW-Advanced-Cognitive---R2-Students-VIT.xlsx", header=None)

def parse_excel(dataframe):
    regno_pattern = r"^2\d[A-Za-z]{3}\d{4,5}$"
    email_pattern = r'^[A-Za-z0-9._%+-]+@(gmail\.com|vitstudent\.ac\.in)$'
    regno_col = None
    regno_row = None
    email_col = None
    email_row = None
    for col in dataframe.columns:
        for j,i in enumerate(dataframe[col][:5]):
            if re.match(regno_pattern, str(i).strip()):
                regno_col = col
                regno_row = j
                break
            if re.match(email_pattern, str(i).strip()):
                email_col = col
                email_row = j
                break
        if regno_col is not None or email_col is not None:
            break
    if regno_col is not None:
        return {"regno":dataframe[regno_col][regno_row:].tolist()}
    elif email_col is not None:
        print(email_col, email_row)
        return {"email":dataframe[email_col][email_row:].tolist()}
    else:
        return None
    
        

if __name__ == "__main__":
    # print(parse_excel(df1))
    # print(parse_excel(df2))
    pass