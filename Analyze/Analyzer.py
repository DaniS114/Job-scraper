import pandas as pd
import matplotlib.pyplot as plt
import os

# CSV beolvasása
df = pd.read_csv("all_jobs_with_source.csv")

output_dir = "Analyzed"
os.makedirs(output_dir, exist_ok=True)

sources = ["Profesia", "Profession", "CVOnline"]


# Segédfüggvények
def split_values(value):
    if pd.isna(value) or str(value).strip() == "":
        return []
    return [x.strip() for x in str(value).split(",") if x.strip()]


def get_languages_only(value):
    if pd.isna(value) or str(value).strip() == "":
        return []

    result = []

    for part in str(value).split(","):
        part = part.strip()
        if not part:
            continue

        if ":" in part:
            result.append(part.split(":")[0].strip())
        else:
            result.append(part)

    return result


def count_items(df, list_col, label_col):
    exploded = df[["source", list_col]].explode(list_col).dropna()
    exploded = exploded.rename(columns={list_col: label_col})
    exploded = exploded[exploded[label_col] != ""]

    grouped = exploded.groupby([label_col, "source"]).size().unstack(fill_value=0)

    for source in sources:
        if source not in grouped.columns:
            grouped[source] = 0

    grouped = grouped[sources]
    grouped["Total"] = grouped.sum(axis=1)
    grouped = grouped.sort_values("Total", ascending=False)

    return grouped.reset_index()


def count_column(df, col_name, label_col):
    grouped = df.groupby([col_name, "source"]).size().unstack(fill_value=0)

    for source in sources:
        if source not in grouped.columns:
            grouped[source] = 0

    grouped = grouped[sources]
    grouped["Total"] = grouped.sum(axis=1)
    grouped = grouped.sort_values("Total", ascending=False)

    return grouped.reset_index().rename(columns={col_name: label_col})


def make_stacked_chart(df_counts, label_col, xlabel, filename, top_n=10):
    data = df_counts.head(top_n).copy()

    if data.empty:
        print(f"Nincs adat: {xlabel}")
        return

    x = range(len(data))

    plt.figure(figsize=(10, 5))
    plt.bar(x, data["Profesia"], label="Profesia", color="#1f77b4")
    plt.bar(
        x,
        data["Profession"],
        bottom=data["Profesia"],
        label="Profession",
        color="#ff7f0e"
    )
    plt.bar(
        x,
        data["CVOnline"],
        bottom=data["Profesia"] + data["Profession"],
        label="CVOnline",
        color="#2ca02c"
    )

    for i, total in enumerate(data["Total"]):
        plt.text(i, total, str(int(total)), ha="center", va="bottom", fontsize=9)

    plt.xticks(x, data[label_col], rotation=45, ha="right")
    plt.xlabel(xlabel)
    plt.ylabel("Hirdetések száma (db)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, filename), dpi=300)
    plt.close()


# Normalizálás
def normalize_programming_language(value):
    value = str(value).strip()
    lower = value.lower()

    if lower in ["python", "py", "python 3"]:
        return "Python"
    elif lower in ["java", "java 8", "java 11", "java 17", "java 21"]:
        return "Java"
    elif lower in ["javascript", "js"]:
        return "JavaScript"
    elif lower in ["typescript", "ts"]:
        return "TypeScript"
    elif lower in ["powershell", "power shell"]:
        return "PowerShell"
    elif lower in ["nodejs", "node.js", "node js"]:
        return "Node.js"
    elif lower in ["html5", "html"]:
        return "HTML"
    elif lower in ["css3", "css"]:
        return "CSS"
    elif lower in ["c ++", "c++"]:
        return "C++"
    else:
        return value


def normalize_tool(value):
    value = str(value).strip()
    lower = value.lower()

    if lower in ["aws", "amazon web services", "amazon web services (aws)", "amazon aws", "cloud aws", "aws cloud", "aws services"]:
        return "AWS"
    elif lower in ["azure", "microsoft azure"]:
        return "Azure"
    elif lower in ["gcp", "google cloud", "google cloud platform"]:
        return "Google Cloud"
    elif lower in ["jira", "jirasoftware", "jira software"]:
        return "Jira"
    elif lower in ["git", "git scm"]:
        return "Git"
    elif lower in ["gitlab", "git lab"]:
        return "GitLab"
    elif lower in ["github", "git hub"]:
        return "GitHub"
    elif lower in ["power bi", "powerbi", "microsoft power bi"]:
        return "Power BI"
    elif lower in ["ms office", "microsoft office", "microsoft office 365", "microsoft 365"]:
        return "Microsoft Office"
    elif lower in ["excel", "ms excel", "microsoft excel"]:
        return "Microsoft Excel"
    elif lower in ["word", "microsoft word"]:
        return "Microsoft Word"
    elif lower in ["postgres", "postgresql"]:
        return "PostgreSQL"
    elif lower in ["mssql", "ms sql", "microsoft sql server"]:
        return "MS SQL"
    elif lower in ["mysql", "my sql"]:
        return "MySQL"
    elif lower in ["argocd", "argo cd"]:
        return "Argo CD"
    elif lower in ["ci/cd", "cicd"]:
        return "CI/CD"
    elif lower in ["rest api", "rest"]:
        return "REST API"
    else:
        return value


def normalize_human_language(value):
    value = str(value).strip()
    lower = value.lower()

    if lower in ["english", "anglický jazyk"]:
        return "English"
    elif lower in ["german", "nemecký jazyk"]:
        return "German"
    elif lower in ["slovak", "slovenský jazyk"]:
        return "Slovak"
    elif lower in ["czech", "český jazyk"]:
        return "Czech"
    else:
        return value


def normalize_experience(value):
    if pd.isna(value) or str(value).strip() == "":
        return "Nincs megadva"

    value = str(value).strip()
    lower = value.lower()

    if lower in ["not specified", "nan"]:
        return "Nincs megadva"

    if "junior" in lower:
        return "Junior"
    if "medior" in lower:
        return "Medior"
    if "senior" in lower:
        return "Senior"

    if lower in ["0-1 years"]:
        return "Junior 0-1 év"

    if lower in ["1-3 years", "2", "2 years", "2+ years", "2-3 years", "2-4 years", "2-5 years", "3+ years", "3-5 years", "4+ years", "4-7 years"]:
        return "Medior 1-5 év"

    if lower in ["5+ years", "5-7 years", "8-10 years", "7+ years", "7-10+ years", "10+ years", "8-12 years", "8+ years", "5-10 years"]:
        return "Senior 5-10+ év"

    return value


def normalize_work_arrangement(value):
    if pd.isna(value) or str(value).strip() == "":
        return "Nincs megadva"

    value = str(value).strip()
    lower = value.lower()

    if "remote" in lower or "home-office" in lower or "home office" in lower or "práca z domu" in lower:
        return "Távoli munkavégzés"

    if "on-site with home office" in lower:
        return "Hibrid munkavégzés"

    if "hybrid" in lower:
        return "Hibrid munkavégzés"

    if "on-site" in lower:
        return "Helyszíni munkavégzés"

    if "remote-first" in lower:
        return "Távoli munkavégzés"

    if "full remote" in lower:
        return "Távoli munkavégzés"

    if lower == "full-time":
        return "Nincs megadva"

    return value


def normalize_job_type(value):
    if pd.isna(value) or str(value).strip() == "":
        return "Nincs megadva"

    value = str(value).strip()
    lower = value.lower()

    if lower in ["full-time", "plný úväzok"]:
        return "Teljes munkaidő"

    if lower in ["half-time", "part-time", "part time"]:
        return "Részmunkaidő"

    if "short-term" in lower:
        return "Határozott idejű"

    if "full-time" in lower and ("half-time" in lower or "part-time" in lower):
        return "Teljes vagy részmunkaidő"

    if "full-time" in lower and "short-term" in lower:
        return "Teljes munkaidő / határozott idejű"

    return value

def normalize_location(value):
    if pd.isna(value) or str(value).strip() == "":
        return "Nincs megadva"

    value = str(value).strip()
    lower = value.lower()

    if lower in ["remote", "práca z domu", "home office"]:
        return "Remote"

    if lower in ["bratislava", "bratislavský kraj", "bratislava region"]:
        return "Bratislava"

    if lower in ["kosice", "košice"]:
        return "Košice"

    if lower in ["praha", "prague"]:
        return "Prague"

    if lower == "banskobystrický kraj":
        return "Banská Bystrica"

    if lower == "trnavský kraj":
        return "Trnava"

    if lower == "trenčiansky kraj":
        return "Trenčín"

    if lower == "žilinský kraj":
        return "Žilina"

    return value


# Oszlopok feldolgozása
df["Programming Languages"] = df["Programming Languages"].apply(split_values)
df["Programming Languages"] = df["Programming Languages"].apply(lambda items: [normalize_programming_language(x) for x in items])

df["Required Software / Tools"] = df["Required Software / Tools"].apply(split_values)
df["Required Software / Tools"] = df["Required Software / Tools"].apply(lambda items: [normalize_tool(x) for x in items])

df["Language Requirements Detailed"] = df["Language Requirements"].apply(split_values)

df["Language Requirements"] = df["Language Requirements"].apply(get_languages_only)
df["Language Requirements"] = df["Language Requirements"].apply(lambda items: [normalize_human_language(x) for x in items])

df["Experience Level"] = df["Experience Level"].apply(normalize_experience)
df["Work Arrangement"] = df["Work Arrangement"].apply(normalize_work_arrangement)
df["Job Type"] = df["Job Type"].apply(normalize_job_type)
df["Location"] = df["Location"].apply(normalize_location)


# Összesítés forrás szerint
programming_languages = count_items(df, "Programming Languages", "Programming Language")
tools = count_items(df, "Required Software / Tools", "Tool / Technology")
language_requirements = count_items(df, "Language Requirements", "Language")
language_requirements_detailed = count_items(df, "Language Requirements Detailed", "Language Requirement")

experience_levels = count_column(df, "Experience Level", "Experience Level")
work_arrangements = count_column(df, "Work Arrangement", "Work Arrangement")
job_types = count_column(df, "Job Type", "Job Type")
locations = count_column(df, "Location", "Location")


# CSV mentés
programming_languages.to_csv(os.path.join(output_dir, "all_programming_languages.csv"), index=False, encoding="utf-8-sig")
tools.to_csv(os.path.join(output_dir, "all_tools.csv"), index=False, encoding="utf-8-sig")
language_requirements.to_csv(os.path.join(output_dir, "all_human_languages.csv"), index=False, encoding="utf-8-sig")
language_requirements_detailed.to_csv(os.path.join(output_dir, "all_languages_detailed.csv"), index=False, encoding="utf-8-sig")
experience_levels.to_csv(os.path.join(output_dir, "all_experience_levels.csv"), index=False, encoding="utf-8-sig")
work_arrangements.to_csv(os.path.join(output_dir, "all_work_arrangement.csv"), index=False, encoding="utf-8-sig")
job_types.to_csv(os.path.join(output_dir, "all_job_types.csv"), index=False, encoding="utf-8-sig")
locations.to_csv(os.path.join(output_dir, "all_locations.csv"), index=False, encoding="utf-8-sig")


# Grafikonok
make_stacked_chart(programming_languages, "Programming Language", "Programozási nyelvek", "all_programming_languages.png", 20)
make_stacked_chart(tools, "Tool / Technology", "Eszközök és technológiák", "all_tools.png", 20)
make_stacked_chart(language_requirements, "Language", "Elvárt nyelvismeret", "all_human_languages.png", 6)
make_stacked_chart(experience_levels, "Experience Level", "Munkatapasztalat", "all_experience_levels.png", 4)
make_stacked_chart(work_arrangements, "Work Arrangement", "Munkavégzés módja", "all_work_arrangement.png", 4)
make_stacked_chart(job_types, "Job Type", "Munka típusa", "all_job_types.png", 4)
make_stacked_chart(locations, "Location", "Munkavégzés helye", "all_locations.png", 15)

print("Kész. Mentve az Analyzed mappába")
