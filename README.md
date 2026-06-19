# Industrial Maintenance Analytics

Industrial equipment is expected to operate reliably, but operating conditions can change over time.

Small changes in temperature, vibration, or equipment availability may indicate developing issues long before a machine reaches a critical condition.

Understanding these changes is an important part of maintenance engineering because it helps identify problems early and supports more effective maintenance planning.

## Project Overview

Industrial Maintenance Analytics is a maintenance engineering study that examines machine operating records and converts them into maintenance findings.

The project focuses on the evaluation of machine performance, operating condition, machine health status, and maintenance requirements. Information related to runtime, downtime, energy consumption, temperature, vibration, and maintenance activity is analyzed to develop a broader understanding of machine behaviour and operating condition.

A structured assessment methodology is used to review machine performance, identify unusual operating conditions, evaluate machine health status, and develop maintenance guidance. The resulting findings are presented through engineering reports and dashboards that provide a clear summary of machine condition and maintenance priority.

The project combines data preparation, engineering evaluation, and result visualization within a single workflow and demonstrates how machine operating records can be transformed into practical maintenance findings.

## Project Objective

The objective of this project is to demonstrate how machine operating records can be used to support maintenance engineering activities.

Industrial machines generate large amounts of operational information during normal operation. When reviewed systematically, this information can provide valuable insight into machine performance, operating condition, and potential maintenance requirements. The project was developed to illustrate how these observations can be organized and evaluated through a structured assessment process.

By combining multiple sources of operating information, the project provides a practical example of how engineering data can be used to support maintenance planning and machine condition evaluation.

The final outcome is a set of reports and dashboards that summarize machine condition and maintenance needs in a clear and accessible format.

## Project Architecture

The project follows a three-part structure consisting of a data source, an assessment process, and project outputs.

Machine operating records provide the operational data required for evaluation. The assessment process reviews machine performance and operating condition before producing maintenance findings. The resulting findings are presented through engineering reports and dashboards.

![Project Architecture](images/project_architecture.png)

## Assessment Methodology

The assessment methodology is used to examine machine operating records and convert them into maintenance findings.

The process combines performance review and operating condition review to develop a broader understanding of machine behaviour. Information related to reliability, efficiency, temperature, vibration, and operating interruptions is evaluated and brought together during machine health evaluation.

The resulting health status is then used to develop maintenance guidance and identify machines that require additional attention.

The methodology provides a structured approach for moving from raw operating information to practical maintenance findings.

![Assessment Methodology](images/assessment_methodology.png)

## Project Outputs

The assessment process produces a collection of reports and dashboards that summarize machine performance, operating condition, machine health status, and maintenance needs.

These outputs provide a complete record of the study findings and support comparison between the three machines.

### Generated Reports

The project generates four reports in CSV format.

| Report                            | Description                                                                |
| --------------------------------- | -------------------------------------------------------------------------- |
| `kpi_report.csv`                  | Summary of machine performance measures and reliability indicators         |
| `condition_alerts.csv`            | Records of unusual operating conditions identified during condition review |
| `asset_health_report.csv`         | Machine health status and maintenance risk evaluation                      |
| `maintenance_recommendations.csv` | Recommended maintenance actions for each machine                           |

### Representative Report Preview

The following tables provide a brief preview of selected report outputs. Complete report files are available in the project results directory.

### Key Performance Indicator (KPI) Report

The KPI report includes machine performance measures and reliability indicators.

* **MTBF (Mean Time Between Failures)** represents the average operating time between failure events.
* **MTTR (Mean Time To Repair)** represents the average time required to restore a machine after a failure event.

| Machine | Availability (%) | Failure Episodes | MTBF (hrs) | MTTR (hrs) |
| ------- | ---------------- | ---------------- | ---------- | ---------- |
| M001    | 97.85            | 0                | 1943.74    | 0.00       |
| M002    | 96.13            | 0                | 1942.05    | 0.00       |
| M003    | 97.77            | 1                | 1947.31    | 44.33      |

### Asset Health Report

| Machine | Health Status | Risk Level |
| ------- | ------------- | ---------- |
| M001    | Warning       | Medium     |
| M002    | Warning       | Medium     |
| M003    | Critical      | High       |

### Generated Dashboards

The project generates five dashboards that provide a visual summary of the assessment findings.

| Dashboard                    | Description                                      |
| ---------------------------- | ------------------------------------------------ |
| `01_max_temperature.png`     | Comparison of maximum machine temperatures       |
| `02_max_vibration.png`       | Comparison of maximum machine vibration levels   |
| `03_total_downtime.png`      | Comparison of accumulated machine downtime       |
| `04_alert_count.png`         | Summary of condition review alert activity       |
| `05_asset_health_status.png` | Summary of machine health status classifications |

### Dashboard Preview

#### Maximum Temperature Dashboard

![Maximum Temperature Dashboard](results/01_max_temperature.png)

#### Maximum Vibration Dashboard

![Maximum Vibration Dashboard](results/02_max_vibration.png)

#### Total Downtime Dashboard

![Total Downtime Dashboard](results/03_total_downtime.png)

#### Alert Episode Dashboard

![Alert Episode Dashboard](results/04_alert_count.png)

#### Asset Health Status Dashboard

![Asset Health Status Dashboard](results/05_asset_health_status.png)

## Repository Structure

The repository is organized into separate directories for data storage, analysis, visualization, project outputs, project diagrams, and supporting materials.

```text
industrial_maintenance_analytics
│
├── data
│   └── maintenance_data.csv
│
├── images
│   ├── assessment_methodology.png
│   └── project_architecture.png
│
├── notebook
│   └── project_walkthrough.ipynb
│
├── results
│   ├── 01_max_temperature.png
│   ├── 02_max_vibration.png
│   ├── 03_total_downtime.png
│   ├── 04_alert_count.png
│   ├── 05_asset_health_status.png
│   ├── asset_health_report.csv
│   ├── condition_alerts.csv
│   ├── kpi_report.csv
│   └── maintenance_recommendations.csv
│
├── src
│   ├── analytics
│   ├── data_preparation
│   └── visualization
│
├── .gitignore
│
├── LICENSE
│
├── main.py
│
├── README.md
│
└── requirements.txt
```

### Directory Description

| Directory / File   | Description                                                                                 |
| ------------------ | ------------------------------------------------------------------------------------------- |
| `data/`            | Contains `maintenance_data.csv`, which is the machine operating records used by the project |
| `images/`          | Project diagrams used in the README                                                         |
| `notebook/`        | Jupyter notebook containing the project walkthrough and analysis                            |
| `results/`         | Generated reports and dashboard outputs                                                     |
| `src/`             | Project source code                                                                         |
| `main.py`          | Main project entry point                                                                    |
| `requirements.txt` | Python package dependencies                                                                 |
| `README.md`        | Project documentation                                                                       |
| `LICENSE`          | Project license information                                                                 |

### Source Code Structure

The source code is organized into modules responsible for data preparation, analysis, and dashboard generation.

| Module              | Purpose                                                                                   |
| ------------------- | ----------------------------------------------------------------------------------------- |
| `data_preparation/` | Dataset generation and dataset validation                                                 |
| `analytics/`        | Performance review, condition review, machine health evaluation, and maintenance guidance |
| `visualization/`    | Dashboard creation and result visualization                                               |

## Jupyter Notebook Walkthrough

The repository includes a Jupyter notebook that presents the study, generated outputs, and final results in a single guided document.

The notebook is intended for readers who wish to understand how the assessment findings relate to machine behaviour, operating conditions, and maintenance decisions.

Notebook location:

`notebook/project_walkthrough.ipynb`

### Using the Notebook

1. Complete the project setup described in the **How To Run** section.

2. Ensure that all required project dependencies have been installed successfully.

3. Launch a notebook-compatible environment such as:

   * Jupyter Notebook
   * JupyterLab
   * Visual Studio Code (VS Code)

4. Open:

   ```text
   notebook/project_walkthrough.ipynb
   ```

5. Select the project Python environment as the notebook kernel.

6. Confirm that the kernel is active and connected before executing any notebook cells.

7. Run the notebook cells sequentially from top to bottom.

8. The notebook will display explanations, report previews, dashboard visualizations, and study findings as each section is executed.

### Notebook Purpose

The notebook is designed as a companion to the source code rather than a replacement for it.

Readers interested in implementation details can explore the source code modules, while readers interested in methodology, interpretation, and project results can follow the notebook as a standalone walkthrough of the study.

## How To Run

### Prerequisites

Before running the project, ensure that the following software is installed:

* Python 3.10.10
* Git

### Project Setup

Clone the repository and navigate to the project directory.

```bash
git clone https://github.com/duttakaustav/industrial_maintenance_analytics.git
cd industrial_maintenance_analytics
```

Create a Python virtual environment.

```bash
python -m venv .venv
```

Activate the virtual environment.

#### For Windows

```bash
.venv\Scripts\activate
```

#### For Linux or macOS

```bash
source .venv/bin/activate
```

Install the required project dependencies.

```bash
pip install -r requirements.txt
```

### Execute the Project

Run the project from the repository root directory.

```bash
python main.py
```

### Generated Outputs

After successful execution, the generated reports and dashboards will be available in:

```text
results/
```

### Open the Notebook

The notebook can be opened at any stage to review the study, methodology, generated outputs, and final results.

Open:

```text
notebook/project_walkthrough.ipynb
```

using Jupyter Notebook, JupyterLab, VS Code, or another notebook-compatible environment.

Select the project Python environment as the notebook kernel.

**Note for VS Code:** If prompted to install `ipykernel` when selecting the notebook kernel, complete the installation and reconnect the kernel before executing the notebook cells.

Execute the notebook cells sequentially from top to bottom.

## Assumptions and Limitations

### Assumptions

The study was developed under the following assumptions:

* The dataset represents machine operation over a ninety-day operating period.
* Machine operating records provide sufficient information for the scope of the study.
* Temperature and vibration measurements provide useful indicators of machine condition.
* Runtime and downtime records provide useful indicators of machine performance and reliability.
* The engineering thresholds used in the assessment are suitable for identifying normal and abnormal operating behaviour.
* Machine health status can be evaluated by combining performance measures, condition review results, and operating history.
* Maintenance guidance can be developed from the operating patterns present in the dataset.
* The generated dataset contains both normal and abnormal machine operating conditions.
* The three machine profiles provide different operating patterns for the assessment process.

### Limitations

The study was developed within the following limitations:

* The project uses synthetic operating data rather than measurements collected from physical equipment.
* The assessment results depend on the operating patterns intentionally introduced during dataset design.
* The study evaluates only three machines and does not represent every type of equipment found in industrial environments.
* The assessment uses fixed engineering thresholds throughout the study.
* The project evaluates machine condition using a limited set of operating indicators, including runtime, downtime, temperature, and vibration.
* Factors such as production demand, environmental conditions, equipment age, maintenance history, spare part availability, and operator practices are not considered.
* The project does not include live sensor data, real-time monitoring, or continuous data collection.
* The project does not include machine learning techniques or methods for predicting future failures.
* The generated maintenance guidance is intended for demonstration purposes and should not be used as a replacement for site-specific engineering evaluation.
* Maintenance decision making in real industrial environments requires additional engineering, operational, safety, and cost-related considerations that are outside the scope of this study.
