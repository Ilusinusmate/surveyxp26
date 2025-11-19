# Adoption of Large Language Models in Scrum Management

Supplementary material for the article **“Adoption of Large Language Models in Scrum Management: Insights from Brazilian Practitioners”** (XP 2026). This repository contains the anonymized survey responses, descriptive statistics, and the analysis script used to characterize how Scrum practitioners in Brazil are experimenting with AI chat assistants.

## Repository structure

```
.
├── data/
│   └── survey_data.xlsx      # Raw form responses
│   └── analysis.xlsx         # Analysis done by researchers
├── scripts/
│   └── analyze_survey.py     # Script that produces descriptive statistics in Markdown
├── outputs/
│   └── descriptive_stats.md  # Descriptive statistics tables
├── columns.md                # Column dictionary describing every survey question
├── README.md
└── LICENSE
```

## Data structure

See [`columns.md`](columns.md) for the complete dictionary of the 103 survey questions/columns. Each entry lists the question text, response scale, and any special notes so researchers can confidently interpret every field inside `data/survey_data.xlsx`.

## Data collection recap

- **Population:** Brazilian professionals with at least some experience working in Scrum teams.
- **Sampling:** Convenience sampling by distributing the questionnaire through Agile communities in Oct–Nov 2025.
- **Instrument:** 103-question survey covering demographics, Scrum experience, intensity/formality of AI use, benefits, risks, and open-text examples.
- **Responses:** 70 submissions, that provided informed consent and are retained for analysis in this repository.
- **Ethics:** Participation was voluntary and anonymous. Only aggregate statistics are published here; the raw file contains no directly identifying data beyond optional organization name/email fields (left blank in the shared dataset).

## Key descriptive insights (consented sample, _n_ = 70)

- **Geography & demographics:** All respondents work in Brazil; 82.9 % are younger than 40 and 52.9 % have not finalized a bachelor’s degree yet.
- **Scrum expertise:** 44.3 % self-identify as “Qualified,” another 14.3 % as “Proficient,” while 20.0 % report no prior Scrum experience (mostly students in training programs). Time working with Scrum is concentrated in the 0–5 year range (60.0 %).
- **Roles:** Developers are the largest group (32.9 %), followed by Scrum Masters (8.6 %) and Product Owners (4.3 %). Remaining answers are spread across QA, coaching, and management roles, but 30.0 % skipped the question.
- **AI adoption:** 47.1 % used an AI chat assistant in the previous six months. Of those who answered, usage skews towards frequent interaction (21.4 % daily, 10.0 % weekly). Policies are uncommon—only 17.1 % report a formal organizational guideline.
- **Perceived usefulness:** Mean scores (1–5 Likert) suggest assistants are moderately helpful for Developers (3.59) and Scrum Masters (3.56), slightly less for Product Owners (3.21).
- **Perceived benefits:** Agreement is strongest for “LLMs reduce cognitive load” (mean 4.38) and “LLMs accelerate Scrum event preparation” (4.03). Collaboration, decision quality, and transparency also rate positively (>3.6).
- **Perceived risks:** Among respondents who answered, none agreed that intensive AI use necessarily reduces understanding, accountability, trust, or motivation—highlighting enthusiasm but also the need to explore risks qualitatively in the article.

A full set of frequency tables is available in [`outputs/descriptive_stats.md`](outputs/descriptive_stats.md).

## Reproducing the descriptive analysis

1. **Create a virtual environment (recommended)**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the analysis script**
   ```bash
   python scripts/analyze_survey.py --data=./data/survey_data.xlsx
   ```
   The script reads `survey_data.xlsx`, filters consenting respondents, and rewrites `outputs/descriptive_stats.md` with updated tables.

## Suggested citation

```
M. Perkusich, et al. (2026). Adoption of Large Language Models in Scrum Management: Insights from Brazilian Practitioners. XP 2026 Conference. Supplementary dataset v1.0. https://github.com/Ilusinusmate/surveyxp26
```

## Authors

- Mirko Perkusich¹
- Danyllo Albuquerque¹
- Allysson Allex Araújo²
- Matheus Paixão²
- Rohit Gheyi¹
- Marcos Kalinowski³
- Angelo Perkusich¹

> ¹,²,³ superscripts follow the author affiliations as defined in the corresponding XP 2026 article.

## BibTeX citation

If you use this dataset or analysis script in academic work, please cite it as:

```bibtex
@misc{xp_2026_llm_scrum_survey,
  author       = {Perkusich, Mirko and Others},
  title        = {Adoption of Large Language Models in Scrum Management: Insights from Brazilian Practitioners --- Supplementary Dataset and Scripts},
  year         = {2026},
  howpublished = {\url{https://github.com/Ilusinusmate/surveyxp26}},
  note         = {XP 2026 Conference, supplementary material v1.0},
}
```

## License

The survey dataset, generated tables, and accompanying documentation are released under the Creative Commons Attribution 4.0 International (CC BY 4.0) license. See [LICENSE](LICENSE).
