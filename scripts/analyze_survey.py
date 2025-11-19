#!/usr/bin/env python3
"""Generate descriptive statistics for the Scrum & LLM adoption survey."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "survey_data.xlsx"
OUTPUT_DIR = ROOT / "outputs"
OUTPUT_MD = OUTPUT_DIR / "descriptive_stats.md"


RENAME_MAP = {
    "Carimbo de data/hora": "timestamp",
    "Do you AGREE TO PARTICIPATE in this study under the conditions stated above?": "consent",
    "In WHAT COUNTRY do you currently work?": "country",
    "What is your AGE GROUP?": "age_group",
    "What is your ACADEMIC EDUCATION? (Select the degree)": "education",
    "How do you consider your KNOWLEDGE LEVEL in SCRUM?": "scrum_knowledge",
    "What is your EXPERIENCE in years of working on SCRUM projects?": "scrum_years",
    "Do you hold any of the following SCRUM-role certifications? (select all that apply)": "scrum_certs",
    "Do you hold any of the following Agile or related certifications? (select all that apply)": "agile_certs",
    "What is the NAME OF THE ORGANIZATION you work for?": "org_name",
    "What is the SIZE OF THE ORGANIZATION in terms of the number of employees?": "org_size",
    "HAVE YOU WORKED in a Scrum initiative/project?  ": "worked_scrum",
    "What is your PRIMARY ROLE  in the Scrum Team in your current or most recent initiative?  ": "scrum_role",
    "What is the main APPLICATION DOMAIN of your current/latest Scrum initiative?": "app_domain",
    "What is the main PROBLEM DOMAIN applied to your current/latest Scrum initiative?": "problem_domain",
    "How many MEMBERS are there in the SCRUM TEAM you currently work with — or, if you are not currently part of one, in the most recent SCRUM TEAM you worked with?": "team_size",
    "HOW LONG has the product been (or was) under development or maintenance? ": "product_duration",
    "In the last 6 months, have you employed an AI Chat Assistant to support any Scrum management work?  ": "used_ai",
    "How often do you use AI chat assistants, for Scrum management task)? ": "ai_frequency",
    "How do you consider your KNOWLEDGE LEVEL in the use of AI Chat Assistants? ": "ai_knowledge",
    "Which AI Chat Assistants do you currently use?  ": "ai_tools",
    "If you know which model(s) your AI Chat Assistant uses, please specify (for example,  GPT-4o, Gemini 2.5 Flash).": "ai_models",
    "How do you usually interact with AI Chat Assistants?": "ai_interface",
    "Does your organization have a FORMAL POLICY or guideline regarding the use of AI Chat Assistants?  ": "ai_policy",
    "HOW formally do you USE AI CHAT ASSISTANTS in your Scrum management activities?  ": "ai_formality",
    "On average, how much TIME PER DAY do you spend using AI Chat Assistants for Scrum management work?": "ai_time_per_day",
    "To what extent ARE AI CHAT ASSISTANTS HELPFUL in supporting Agile activities of the following SCRUM ACCOUNTABILITIES? [Product Owner]": "help_po",
    "To what extent ARE AI CHAT ASSISTANTS HELPFUL in supporting Agile activities of the following SCRUM ACCOUNTABILITIES? [Scrum Master]": "help_sm",
    "To what extent ARE AI CHAT ASSISTANTS HELPFUL in supporting Agile activities of the following SCRUM ACCOUNTABILITIES? [Developer]": "help_dev",
    "To what extent do you AGREE with the following statements about the BENEFITS of AI Chat Assistants in Scrum management tasks?   [LLMs help reduce cognitive load in repetitive management tasks.]": "benefit_cognitive_load",
    "To what extent do you AGREE with the following statements about the BENEFITS of AI Chat Assistants in Scrum management tasks?   [LLMs improve collaboration between Agile roles (PO, SM, Dev, QA).]": "benefit_collaboration",
    "To what extent do you AGREE with the following statements about the BENEFITS of AI Chat Assistants in Scrum management tasks?   [LLMs accelerate the preparation of Scrum events (planning, review, retrospective).]": "benefit_events",
    "To what extent do you AGREE with the following statements about the BENEFITS of AI Chat Assistants in Scrum management tasks?   [LLMs improve the quality of decision-making in my projects.]": "benefit_decisions",
    "To what extent do you AGREE with the following statements about the BENEFITS of AI Chat Assistants in Scrum management tasks?   [LLMs increase transparency and traceability in Agile processes.]": "benefit_transparency",
    "Do you believe INTENSIVE USE of AI Chat Assistants could CAUSE [Reduced understanding of processes (less deep understanding of processes)]": "risk_understanding",
    "Do you believe INTENSIVE USE of AI Chat Assistants could CAUSE [Reduced accountability (difficulty in assigning responsibility)]": "risk_accountability",
    "Do you believe INTENSIVE USE of AI Chat Assistants could CAUSE [Reduced trust (distrust in AI outputs or human–AI collaboration)]": "risk_trust",
    "Do you believe INTENSIVE USE of AI Chat Assistants could CAUSE [Reduced motivation (reduced engagement of team members when delegating to AI)]": "risk_motivation",
}


CATEGORICAL_QUESTIONS: List[Tuple[str, str]] = [
    ("country", "Country of work"),
    ("age_group", "Age group"),
    ("education", "Academic education"),
    ("scrum_knowledge", "Self-reported knowledge of Scrum"),
    ("scrum_years", "Years working with Scrum"),
    ("scrum_role", "Primary Scrum accountability"),
    ("org_size", "Organization size"),
    ("used_ai", "Used AI assistants in the last 6 months"),
    ("ai_frequency", "Frequency of AI assistant use"),
    ("ai_knowledge", "Knowledge of AI assistants"),
    ("ai_policy", "Organizational AI policy"),
    ("ai_formality", "Formality of AI use in Scrum work"),
    ("ai_time_per_day", "Daily time spent with AI assistants"),
]

HELPFULNESS_MAP = {
    "Not Helpful": 1,
    "Slightly Helpful": 2,
    "Helpful": 3,
    "Very Helpful": 4,
    "Extremely Helpful": 5,
}

HELPFULNESS_COLS: List[Tuple[str, str]] = [
    ("help_po", "Helpfulness for Product Owners"),
    ("help_sm", "Helpfulness for Scrum Masters"),
    ("help_dev", "Helpfulness for Developers"),
]

AGREEMENT_MAP = {
    "Strongly disagree": 1,
    "Disagree": 2,
    "Neutral": 3,
    "Agree": 4,
    "Strongly Agree": 5,
    "Strongly agree": 5,
}

BENEFIT_COLS: List[Tuple[str, str]] = [
    ("benefit_cognitive_load", "LLMs reduce cognitive load"),
    ("benefit_collaboration", "LLMs improve collaboration"),
    ("benefit_events", "LLMs accelerate Scrum event prep"),
    ("benefit_decisions", "LLMs improve decision quality"),
    ("benefit_transparency", "LLMs increase transparency"),
]

RISK_COLS: List[Tuple[str, str]] = [
    ("risk_understanding", "Reduced understanding of processes"),
    ("risk_accountability", "Reduced accountability"),
    ("risk_trust", "Reduced trust"),
    ("risk_motivation", "Reduced motivation"),
]


def load_data(path: Path) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Return both the raw dataframe and the consented subset."""

    df = pd.read_excel(path, engine="openpyxl")
    df = df.rename(columns=RENAME_MAP)
    consented = df[df["consent"] == "Yes, I agree and wish to continue"].copy()
    consented.reset_index(drop=True, inplace=True)
    return df, consented


def value_table(series: pd.Series, total: int) -> List[Dict[str, str]]:
    counts = series.value_counts(dropna=False)
    rows = []
    for value, count in counts.items():
        label = "Missing/No answer" if pd.isna(value) else str(value).strip()
        percent = (count / total) * 100 if total else 0
        rows.append(
            {
                "response": label,
                "count": int(count),
                "percent": f"{percent:.1f}%",
            }
        )
    return rows


def format_markdown_table(rows: Iterable[Dict[str, str]]) -> str:
    lines = ["| Response | Count | Percent |", "| --- | ---: | ---: |"]
    for row in rows:
        lines.append(f"| {row['response']} | {row['count']} | {row['percent']} |")
    return "\n".join(lines)


def summarize_likert(
    df: pd.DataFrame,
    columns: List[Tuple[str, str]],
    mapping: Dict[str, int],
) -> List[str]:
    lines = ["| Statement | n | Mean (1-5) |", "| --- | ---: | ---: |"]
    for col, label in columns:
        if col not in df:
            continue
        numeric = df[col].map(mapping)
        n = int(numeric.count())
        mean = numeric.mean()
        mean_str = f"{mean:.2f}" if pd.notna(mean) else "—"
        lines.append(f"| {label} | {n} | {mean_str} |")
    return lines


def summarize_risks(df: pd.DataFrame) -> List[str]:
    lines = ["| Risk | Yes | Total | % Yes |", "| --- | ---: | ---: | ---: |"]
    for col, label in RISK_COLS:
        if col not in df:
            continue
        counts = df[col].value_counts(dropna=True)
        yes = int(counts.get("Yes", 0))
        total = int(counts.sum())
        percent = (yes / total * 100) if total else 0
        lines.append(f"| {label} | {yes} | {total} | {percent:.1f}% |")
    return lines


def build_report(raw: pd.DataFrame, consented: pd.DataFrame) -> str:
    total_raw = len(raw)
    total_consented = len(consented)
    countries = consented["country"].nunique(dropna=True)

    lines: List[str] = [
        "# Descriptive statistics",
        "",
        f"- Total submissions: **{total_raw}**",
        f"- Valid consented responses: **{total_consented}**",
        f"- Countries represented: **{countries}**",
        f"- Data file: `{DATA_PATH.name}`",
        "",
        "## Demographics and respondent profile",
    ]

    for col, title in CATEGORICAL_QUESTIONS:
        if col not in consented:
            continue
        lines.append(f"### {title}")
        lines.append("")
        rows = value_table(consented[col], total_consented)
        lines.append(format_markdown_table(rows))
        lines.append("")

    lines.append("## Helpfulness of AI chat assistants")
    lines.append("")
    lines.extend(summarize_likert(consented, HELPFULNESS_COLS, HELPFULNESS_MAP))
    lines.append("")

    lines.append("## Perceived benefits")
    lines.append("")
    lines.extend(summarize_likert(consented, BENEFIT_COLS, AGREEMENT_MAP))
    lines.append("")

    lines.append("## Perceived risks of intensive use")
    lines.append("")
    lines.extend(summarize_risks(consented))
    lines.append("")

    lines.append(
        "_All percentages are calculated over the 70 consented respondents. Likert averages consider only non-missing answers._"
    )

    return "\n".join(lines)


def main(data_path: Path = DATA_PATH, output_path: Path = OUTPUT_MD) -> None:
    raw, consented = load_data(data_path)
    OUTPUT_DIR.mkdir(exist_ok=True)
    report = build_report(raw, consented)
    output_path.write_text(report, encoding="utf-8")
    print(f"Saved descriptive statistics to {output_path.relative_to(ROOT)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Summarize the Scrum & AI survey data.")
    parser.add_argument("--data", type=Path, default=DATA_PATH, help="Path to survey_data.xlsx")
    parser.add_argument("--output", type=Path, default=OUTPUT_MD, help="Path to write the markdown report")
    args = parser.parse_args()
    main(args.data, args.output)
