# import math
import pandas as pd
import numpy as np


# def power(data, p):
#     return data.apply(lambda x: math.pow(x, p))


# EVAL_FUNCTIONS = {"POWER": power}
expression = "a**-1"
df = pd.DataFrame({"a": [2, 3, 4]})
print(df.dtypes)
# df['a'] = df['a'].astype(np.float)
# import math
# # try:
# def f(x):
#     return math.pow(x, -2) 
def run(df):
    exec("import math\ndef f(x):\n  return math.log(x)", globals())
    df["b"] = df["a"]
    df["b"] = df["b"].apply(globals()["f"])
    return df
    # df["b"] = df.eval(expression,
    #                   engine="python",
    #                   resolvers=[EVAL_FUNCTIONS, df])
# except (ValueError) as e:
#     print(f"catch {e}")
#     df['a'] = df['a'].astype(np.float)
#     df["b"] = df.eval(expression,
#                       engine="python",
#                       resolvers=[EVAL_FUNCTIONS, df])
print(run(df))
