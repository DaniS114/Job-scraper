import pandas as pd
import matplotlib.pyplot as plt

#CSV beolvasása

df = pd.read_csv("profesia_gemini.csv")

#Függvények

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


def count_items(series):
    return series.explode().dropna().value_counts()


def save_counts(series, filename, first_col_name):
    out = series.reset_index()
    out.columns = [first_col_name, "Count"]
    out.to_csv(filename, index=False, encoding="utf-8-sig")


def make_chart(series, xlabel, filename, top_n=10):
    data = series.head(top_n)

    if data.empty:
        print(f"Nincs adat: {title}")
        return

    plt.figure(figsize=(10, 6))
    data.plot(kind="bar")
    plt.xlabel(xlabel)
    plt.ylabel("Hirdetések száma (db)")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
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
        return "Not specified"

    value = str(value).strip()
    lower = value.lower()

    if lower in ["not specified", "nan"]:
        return "Not specified"

    if "junior" in lower:
        return "Junior"

    if "medior" in lower:
        return "Medior"

    if "senior" in lower:
        return "Senior"

    if lower in ["0-1 years"]:
        return "Junior 0-1 years"

    if lower in ["1-3 years", "2", "2 years", "2+ years", "2-3 years","2-4 years", "2-5 years", "3+ years", "3-5 years","4+ years","4-7 years"]:
        return "Medior 1-5 years"

    if lower in ["5+ years", "5-7 years", "8-10 years","7+ years","7-10+ years","10+ years","8-12 years","8+ years","5-10 years"]:
        return "Senior 5-10+ years"

    return value


def normalize_work_arrangement(value):
    if pd.isna(value) or str(value).strip() == "":
        return "Not specified"

    value = str(value).strip()
    lower = value.lower()

    if "remote" in lower or "home-office" in lower or "home office" in lower or "práca z domu" in lower:
        return "Remote"

    if "on-site with home office" in lower:
        return "Hybrid"

    if "hybrid" in lower:
        return "Hybrid"

    if "on-site" in lower:
        return "On-site"

    if "remote-first" in lower:
        return "Remote"

    if "full remote" in lower:
        return "Remote"

    if lower == "full-time":
        return "Not specified"

    return value


def normalize_job_type(value):
    if pd.isna(value) or str(value).strip() == "":
        return "Not specified"

    value = str(value).strip()
    lower = value.lower()

    if lower in ["full-time", "plný úväzok"]:
        return "Full-time"

    if lower in ["half-time", "part-time", "part time", "part-time".lower()]:
        return "Part-time"

    if "short-term" in lower:
        return "Short-term"

    if "full-time" in lower and "half-time" in lower:
        return "Full-time / Part-time"

    if "full-time" in lower and "short-term" in lower:
        return "Full-time / Short-term"

    return value


def normalize_location(value):
    if pd.isna(value) or str(value).strip() == "":
        return "Not specified"

    value = str(value).strip()
    lower = value.lower()

    if lower in ["remote", "práca z domu", "home office"]:
        return "Remote"

    if lower in [
        "bratislava",
        "bratislavský kraj",
        "bratislava region",]:
        return "Bratislava"

    if lower == "kosice":
        return "Košice"

    if lower == "košice":
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
df["Programming Languages"] = df["Programming Languages"].apply(
    lambda items: [normalize_programming_language(x) for x in items]
)

df["Required Software / Tools"] = df["Required Software / Tools"].apply(split_values)
df["Required Software / Tools"] = df["Required Software / Tools"].apply(
    lambda items: [normalize_tool(x) for x in items]
)

df["Language Requirements Detailed"] = df["Language Requirements"].apply(split_values)

df["Language Requirements"] = df["Language Requirements"].apply(get_languages_only)
df["Language Requirements"] = df["Language Requirements"].apply(
    lambda items: [normalize_human_language(x) for x in items]
)

df["Experience Level"] = df["Experience Level"].apply(normalize_experience)
df["Work Arrangement"] = df["Work Arrangement"].apply(normalize_work_arrangement)
df["Job Type"] = df["Job Type"].apply(normalize_job_type)
df["Location"] = df["Location"].apply(normalize_location)

# Gyakoriságok számolása

programming_languages = count_items(df["Programming Languages"])
tools = count_items(df["Required Software / Tools"])
language_requirements = count_items(df["Language Requirements"])
language_requirements_detailed = count_items(df["Language Requirements Detailed"])

experience_levels = df["Experience Level"].value_counts()
work_arrangements = df["Work Arrangement"].value_counts()
job_types = df["Job Type"].value_counts()
locations = df["Location"].value_counts()

# CSV mentés

save_counts(programming_languages, "profesia_programming_languages.csv", "Programming Language")
save_counts(tools, "profesia_tools.csv", "Tool / Technology")
save_counts(language_requirements, "profesia_human_languages.csv", "Language")
save_counts(language_requirements_detailed, "profesia_languages_detailed.csv", "Language Requirement")
save_counts(experience_levels, "profesia_experience_levels.csv", "Experience Level")
save_counts(work_arrangements, "profesia_work_arrangement.csv", "Work Arrangement")
save_counts(job_types, "profesia_job_types.csv", "Job Type")
save_counts(locations, "profesia_locations.csv", "Location")


# Grafikonok
'''
make_chart(programming_languages, "Programozási és leíró nyelvek", "cvonline_programming_languages.png", 20)
make_chart(tools, "Eszközök és technológiák", "cvonline_tools.png", 20)
make_chart(language_requirements, "Nyelvi követelmények", "cvonline_human_languages.png", 6)
make_chart(experience_levels, "Experience level", "cvonline_experience_levels.png", 4)
make_chart(work_arrangements, "Munkavégzés módja", "cvonline_work_arrangement.png", 4)
make_chart(job_types, "Munka típusa", "cvonline_job_types.png", 4)
make_chart(locations, "Helyszín", "cvonline_locations.png", 15)
'''

# Eredmények kiírása

print("Top programozási nyelvek:")
print(programming_languages.head(15))
print()

print("Top eszközök és technológiák:")
print(tools.head(15))
print()

print("Top nyelvek:")
print(language_requirements.head(10))
print()

print("Experience level:")
print(experience_levels.head(10))
print()

print("Munkavégzés módja:")
print(work_arrangements.head(10))
print()

print("Munka típusa:")
print(job_types.head(10))
print()

print("Top lokációk:")
print(locations.head(15))
print()

print("Kész")
