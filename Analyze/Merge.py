import pandas as pd

df_profesia = pd.read_csv("profesia_gemini.csv")
df_profession = pd.read_csv("profession_gemini.csv")
df_cvonline = pd.read_csv("cvonline_gemini.csv")

df_profesia["source"] = "Profesia"
df_profession["source"] = "Profession"
df_cvonline["source"] = "CVOnline"

preferred_order = [
    "job_id",
    "title",
    "company",
    "location",
    "salary",
    "Programming Languages",
    "Required Software / Tools",
    "Language Requirements",
    "Experience Level",
    "Work Arrangement",
    "Job Type",
    "source"
]

all_columns = list(set(df_profesia.columns) | set(df_profession.columns) | set(df_cvonline.columns))

ordered_columns = [col for col in preferred_order if col in all_columns]
remaining_columns = [col for col in all_columns if col not in ordered_columns]

final_columns = ordered_columns + remaining_columns

df_profesia = df_profesia.reindex(columns=final_columns)
df_profession = df_profession.reindex(columns=final_columns)
df_cvonline = df_cvonline.reindex(columns=final_columns)

df_all = pd.concat([df_profesia, df_profession, df_cvonline], ignore_index=True)

df_all.to_csv("all_jobs_with_source.csv", index=False, encoding="utf-8-sig")

source_counts = df_all["source"].value_counts().reset_index()
source_counts.columns = ["Source", "Count"]
source_counts.to_csv("all_jobs_source_counts.csv", index=False, encoding="utf-8-sig")

print(source_counts)
