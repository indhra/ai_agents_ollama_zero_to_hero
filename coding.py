
import pandas as pd

dtf = pd.read_csv('http://bit.ly/kaggletrain')
print(dtf.head(3))

import seaborn as sns
import matplotlib.pyplot as plt

sns.boxplot(data=dtf, x="Sex", y="Age", hue="Survived")
plt.show()


import io
import contextlib

def code_exec(code: str) -> str:
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        try:
            exec(code)
        except Exception as e:
            print(f"Error: {e}")
    return output.getvalue()

tool_code_exec = {'type':'function', 'function':{
  'name': 'code_exec',
  'description': 'execute python code',
  'parameters': {'type': 'object',
                'required': ['code'],
                'properties': {
                    'code': {'type':'str', 'description':'code to execute'},
}}}}

## test
print(code_exec("a=1+1; print(a)"))

prompt = '''You are an expert data scientist, and you have tools to execute python code.
First of all, execute the following code exactly as it is: 'df=pd.read_csv(path); print(df.head())'
If you create a plot, ALWAYS add 'plt.show()' at the end.
'''
messages = [{"role":"system", "content":prompt}]
start = True

while True:
    ## user input
    try:
        if start is True:
            path = input('📁 Provide a CSV path >')
            q = "path = "+path
        else:
            q = input('🙂 >')
    except EOFError:
        break
    if q == "quit":
        break
    if q.strip() == "":
        continue
   
    messages.append( {"role":"user", "content":q} )