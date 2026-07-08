# 🤖 AI Agent Decision Support System (AI Agent DSS)

> A Decision Support System (DSS) for analyzing and recommending AI Agent investments in Computer Science based on the WORKBank dataset.

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![Streamlit](https://img.shields.io/badge/Framework-Streamlit-red)
![Plotly](https://img.shields.io/badge/Visualization-Plotly-green)
![Status](https://img.shields.io/badge/Status-Completed-success)

---

# 📖 Project Overview

Choosing which AI Agent to deploy is becoming a major challenge for organizations.

Instead of relying on subjective judgment, this project builds a **Decision Support System (DSS)** that quantitatively evaluates different AI Agent categories and recommends suitable investment priorities based on:

- WORKBank task characteristics
- Organizational business profile
- AI adoption strategy
- Statistical confidence
- Estimated Return on Investment (ROI)

The system provides an explainable ranking process instead of a black-box recommendation.

---

# 🎯 Objectives

The project aims to:

- Analyze Computer Science task characteristics from WORKBank.
- Map thousands of tasks into functional AI Agent categories.
- Build a configurable Decision Engine.
- Estimate Decision Score and ROI.
- Recommend suitable AI Agent investment priorities.
- Generate personalized deployment recommendations for organizations.

---

# 📂 Dataset

Source:

**WORKBank Dataset (Stanford University)**

Main information extracted:

- Automation Capability
- Automation Desire
- Human Agency
- Communication Requirement
- Domain Expertise Requirement
- Involved Uncertainty

These indicators describe how suitable each task is for AI automation.

---

# 🏗 System Architecture

```
WORKBank Dataset
        │
        ▼
 Task Feature Extraction
        │
        ▼
 AI Agent Mapping
        │
        ▼
 Business Profile
        │
        ▼
 Weight Generator
        │
        ▼
 Decision Engine
        │
        ├────────► Decision Score
        │
        ├────────► Confidence Factor
        │
        └────────► Estimated ROI
                     │
                     ▼
          AI Agent Ranking
                     │
                     ▼
     Final Investment Recommendation
```

---

# 🧠 AI Agent Categories

The original WORKBank dataset contains task-level information.

This project maps similar tasks into functional AI Agent categories:

- Backup Agent
- Documentation Agent
- Testing Agent
- Monitoring Agent
- Code Review Copilot
- Database Agent
- Analytics Agent
- DevOps Agent
- Planning Agent
- Security Agent

---

# 🏢 Business Profile

To personalize recommendations, users configure:

- Business Goal
- AI Adoption Strategy
- Company Size
- Available Budget

Different configurations generate different recommendation results.

---

# ⚙ Decision Engine

Decision Score is calculated from multiple components.

## Components

Positive

- Automation Capability
- Automation Desire

Negative

- Human Agency
- Communication Requirement
- Domain Expertise Requirement
- Involved Uncertainty

Business

- Company Size
- Budget

---

## Confidence Factor

Confidence is introduced to reduce statistical bias caused by different sample sizes.

Example:

| Number of Tasks | Confidence |
|-----------------|------------|
| ≥30 | 100% |
| 20–29 | 98% |
| 10–19 | 96% |
| 5–9 | 94% |
| <5 | 92% |

Confidence represents **statistical reliability**, not AI quality.

---

## Final Decision Score

```
Final Decision Score

=

Raw Decision Score

×

Confidence Factor
```

---

## Estimated ROI

```
Estimated ROI

=

Final Decision Score × 0.95

+

Budget Modifier

+

Company Size Modifier
```

ROI is a comparative indicator rather than actual financial ROI.

---

# 📊 Dashboard Pages

## Page 1

### Task Overview

- Dataset statistics
- AI Agent distribution
- Task characteristics

---

## Page 2

### Decision System Configuration

Configure:

- Business Goal
- AI Adoption Strategy
- Company Size
- Budget

Also introduces:

- Weight tables
- Confidence model
- Decision Engine
- ROI estimation model

---

## Page 3

### Decision Engine

Visualization includes:

- Radar Chart
- Decision Gauge
- Feature Contribution Analysis
- ROI Comparison

Users can understand why scores increase or decrease.

---

## Page 4

### AI Agent Ranking

For every AI Agent:

- Decision Score
- ROI
- Confidence
- Deployment Model
- Investment Decision

---

## Page 5

### Final Recommendation

Personalized recommendations including:

- Top-ranked AI Agents
- Deployment strategy
- Expected benefits
- Operational considerations

---

# 📈 Technologies

- Python
- Streamlit
- Pandas
- Plotly
- NumPy

---

# 📁 Project Structure

```
AI_AGENT_DSS/

│

├── app.py

├── dashboard.py

├── utils.py

├── requirements.txt

│

├── data/

│ ├── domain_worker_desires.csv

│ ├── expert_rated_technological_capability.csv

│ ├── task_statement_with_metadata.csv

│ └── domain_worker_metadata.csv

│

├── assets/

├── README.md

└── screenshots/
```

---

# 🚀 Installation

Clone repository

```bash
git clone https://github.com/ddnthu-hub/ai_agent.git
```

Go to project

```bash
cd ai_agent
```

Install packages

```bash
pip install -r requirements.txt
```

Run

```bash
streamlit run app.py
```

---

# 💡 Key Contributions

✔ Built a configurable Decision Support System.

✔ Proposed AI Agent Mapping from WORKBank tasks.

✔ Designed Decision Score and Confidence models.

✔ Developed explainable AI investment recommendations.

✔ Personalized recommendations through business profiles.

---

# ⚠ Limitations

- Confidence mapping is heuristic rather than statistically estimated.
- ROI is an estimation index instead of real financial ROI.
- Weight tables are manually designed based on decision logic.
- Results depend on the current WORKBank dataset.

---

# 🔮 Future Work

Future improvements include:

- Learning weights using machine learning.
- Integrating real enterprise operational data.
- Supporting multi-objective optimization.
- Adding LLM-powered recommendation explanations.
- Dynamic AI Agent generation.

---

# 👨‍💻 Author

**Vo Thi Thu**

Computer Science Student

Project:

**AI Agent Decision Support System**

```

---

## Mình gợi ý thêm

Bạn nên tạo thêm thư mục:

```
screenshots/
```

và chụp:

- `page1.png`
- `page2.png`
- `page3.png`
- `page4.png`
- `page5.png`

Sau đó thêm vào README các ảnh như:

```markdown
# 📷 Dashboard Preview

## Page 1

![Page1](screenshots/page1.png)

## Page 2

![Page2](screenshots/page2.png)

## Page 3

![Page3](screenshots/page3.png)

## Page 4

![Page4](screenshots/page4.png)

## Page 5

![Page5](screenshots/page5.png)
```

README sẽ chuyên nghiệp hơn rất nhiều và giống các dự án trên GitHub của sinh viên hoặc kỹ sư dữ liệu.
