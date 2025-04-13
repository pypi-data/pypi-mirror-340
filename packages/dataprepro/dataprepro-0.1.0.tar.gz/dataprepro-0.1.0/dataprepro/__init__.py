def addition(numbers: list) -> float:
    return sum(numbers)
def show_code():
    code = '''
import pandas as pd
data = pd.read_csv("employees.csv")
df = pd.DataFrame(data)
# Checking for missing values using isnull()
missing_values = df.isnull()
print(missing_values)


#For missing values by boolean:-

bool_series = pd.isnull(data["Gender"])
missing_gender_data = data[bool_series]
print(missing_gender_data)

#For missing values:-
missing_values = df.isnull()
print(missing_values)


#For non missing values:-
non_missing_values = df.notnull()
print(non_missing_values)

    '''
    print(code)