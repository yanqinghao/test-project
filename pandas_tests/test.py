import pandas as pd

df = pd.read_excel("private/吉利拧紧数据/Trace analysis.xlsx")
df = df[df["ROWTYPE"] == "trace_mean"]
df = df[["Torque"]]
df.columns = ["扭矩"]
df["结果 ID"] = 0
df["结果时间"] = range(len(df))
for i in range(50):
    df_tmp = pd.read_excel(f"private/吉利拧紧数据/Trace analysis ({i}).xlsx")
    df_tmp = df_tmp[df_tmp["ROWTYPE"] == "trace_mean"]
    df_tmp = df_tmp[["Torque"]]
    df_tmp.columns = ["扭矩"]
    df_tmp["结果 ID"] = i + 1
    df_tmp["结果时间"] = range(df["结果时间"].max() + 1, df["结果时间"].max() + len(df_tmp) + 1)
    df = df.append(df_tmp)
print(df)

df.to_excel("private/吉利拧紧数据.xlsx")
