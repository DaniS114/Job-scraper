import pandas as pd


def merge_counts(file1, file2, file3, col_name, out_file, source_names):
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)
    df3 = pd.read_csv(file3)

    df1 = df1.rename(columns={"Count": source_names[0]})
    df2 = df2.rename(columns={"Count": source_names[1]})
    df3 = df3.rename(columns={"Count": source_names[2]})

    merged = df1.merge(df2, on=col_name, how="outer")
    merged = merged.merge(df3, on=col_name, how="outer")

    merged = merged.fillna(0)

    merged[source_names[0]] = merged[source_names[0]].astype(int)
    merged[source_names[1]] = merged[source_names[1]].astype(int)
    merged[source_names[2]] = merged[source_names[2]].astype(int)

    merged["Total"] = (
        merged[source_names[0]]
        + merged[source_names[1]]
        + merged[source_names[2]]
    )

    merged = merged.sort_values("Total", ascending=False)

    merged.to_csv(out_file, index=False, encoding="utf-8-sig")
    return merged


sources = ["Profesia", "Profession", "CVOnline"]


# Programozási nyelvek
merge_counts(
    "profesia_programming_languages.csv",
    "profession_programming_languages.csv",
    "cvonline_programming_languages.csv",
    "Programming Language",
    "all_programming_languages.csv",
    sources
)

# Eszközök és technológiák
merge_counts(
    "profesia_tools.csv",
    "profession_tools.csv",
    "cvonline_tools.csv",
    "Tool / Technology",
    "all_tools.csv",
    sources
)

# Nyelvi követelmények
merge_counts(
    "profesia_human_languages.csv",
    "profession_human_languages.csv",
    "cvonline_human_languages.csv",
    "Language",
    "all_human_languages.csv",
    sources
)

# Experience level
merge_counts(
    "profesia_experience_levels.csv",
    "profession_experience_levels.csv",
    "cvonline_experience_levels.csv",
    "Experience Level",
    "all_experience_levels.csv",
    sources
)

# Munkavégzés módja
merge_counts(
    "profesia_work_arrangement.csv",
    "profession_work_arrangement.csv",
    "cvonline_work_arrangement.csv",
    "Work Arrangement",
    "all_work_arrangement.csv",
    sources
)

# Munka típusa
merge_counts(
    "profesia_job_types.csv",
    "profession_job_types.csv",
    "cvonline_job_types.csv",
    "Job Type",
    "all_job_types.csv",
    sources
)

# Lokáció
merge_counts(
    "profesia_locations.csv",
    "profession_locations.csv",
    "cvonline_locations.csv",
    "Location",
    "all_locations.csv",
    sources
)

print("Az összesített CSV-k elkészültek.")
