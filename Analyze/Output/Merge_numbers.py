import pandas as pd
import matplotlib.pyplot as plt
import os


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


def make_stacked_chart(df, label_col, filename, xlabel, source_names, top_n=10):
    data = df.head(top_n).copy()

    if data.empty:
        print(f"Nincs adat ehhez: {filename}")
        return

    x = range(len(data))

    plt.figure(figsize=(12, 6))
    plt.bar(x, data[source_names[0]], label=source_names[0], color="#1f77b4")
    plt.bar(
        x,
        data[source_names[1]],
        bottom=data[source_names[0]],
        label=source_names[1],
        color="#ff7f0e"
    )
    plt.bar(
        x,
        data[source_names[2]],
        bottom=data[source_names[0]] + data[source_names[1]],
        label=source_names[2],
        color="#2ca02c"
    )

    for i, total in enumerate(data["Total"]):
        plt.text(i, total, str(int(total)), ha="center", va="bottom", fontsize=9)

    plt.xticks(x, data[label_col], rotation=45, ha="right")
    plt.xlabel(xlabel)
    plt.ylabel("Hirdetések száma (db)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.close()


output_dir = "merged_output"
os.makedirs(output_dir, exist_ok=True)

sources = ["Profesia", "Profession", "CVOnline"]


programming_languages = merge_counts(
    "profesia_programming_languages.csv",
    "profession_programming_languages.csv",
    "cvonline_programming_languages.csv",
    "Programming Language",
    os.path.join(output_dir, "all_programming_languages.csv"),
    sources
)

tools = merge_counts(
    "profesia_tools.csv",
    "profession_tools.csv",
    "cvonline_tools.csv",
    "Tool / Technology",
    os.path.join(output_dir, "all_tools.csv"),
    sources
)

human_languages = merge_counts(
    "profesia_human_languages.csv",
    "profession_human_languages.csv",
    "cvonline_human_languages.csv",
    "Language",
    os.path.join(output_dir, "all_human_languages.csv"),
    sources
)

experience_levels = merge_counts(
    "profesia_experience_levels.csv",
    "profession_experience_levels.csv",
    "cvonline_experience_levels.csv",
    "Experience Level",
    os.path.join(output_dir, "all_experience_levels.csv"),
    sources
)

work_arrangement = merge_counts(
    "profesia_work_arrangement.csv",
    "profession_work_arrangement.csv",
    "cvonline_work_arrangement.csv",
    "Work Arrangement",
    os.path.join(output_dir, "all_work_arrangement.csv"),
    sources
)

job_types = merge_counts(
    "profesia_job_types.csv",
    "profession_job_types.csv",
    "cvonline_job_types.csv",
    "Job Type",
    os.path.join(output_dir, "all_job_types.csv"),
    sources
)

locations = merge_counts(
    "profesia_locations.csv",
    "profession_locations.csv",
    "cvonline_locations.csv",
    "Location",
    os.path.join(output_dir, "all_locations.csv"),
    sources
)

make_stacked_chart(
    programming_languages,
    "Programming Language",
    os.path.join(output_dir, "all_programming_languages.png"),
    "Programozási és leíró nyelvek",
    sources,
    top_n=20
)

make_stacked_chart(
    tools,
    "Tool / Technology",
    os.path.join(output_dir, "all_tools.png"),
    "Eszközök és technológiák",
    sources,
    top_n=20
)

make_stacked_chart(
    human_languages,
    "Language",
    os.path.join(output_dir, "all_human_languages.png"),
    "Nyelvi követelmények",
    sources,
    top_n=6
)

make_stacked_chart(
    experience_levels,
    "Experience Level",
    os.path.join(output_dir, "all_experience_levels.png"),
    "Munkatapasztalat",
    sources,
    top_n=4
)

make_stacked_chart(
    work_arrangement,
    "Work Arrangement",
    os.path.join(output_dir, "all_work_arrangement.png"),
    "Munkavégzés módja",
    sources,
    top_n=4
)

make_stacked_chart(
    job_types,
    "Job Type",
    os.path.join(output_dir, "all_job_types.png"),
    "Munka típusa",
    sources,
    top_n=4
)

make_stacked_chart(
    locations,
    "Location",
    os.path.join(output_dir, "all_locations.png"),
    "Helyszín",
    sources,
    top_n=12
)

print("Kész")
