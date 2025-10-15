# Time Robustness for Point-Based Semantics of MITL

This repository contains the implementation of the **monitoring algorithm for time robustness and quantitative semantics** of **Metric Interval Temporal Logic (MITL)** under **point-based semantics**, as presented in the paper:

> *Time Robustness for Point-Based Semantics of Metric Interval Temporal Logic*  
> (Submitted at TACAS 2025)

The repository provides a Python implementation of the proposed **time robustness monitoring algorithm** and its **validation on two use cases**: a *Drone Surveillance* system and a *Smart Hospital Multi-Agent* system.

---

## 🧩 Repository Structure

```
.
├── mitl/
│   ├── monitor.py
│   ├── semantics.py
│   ├── utils.py
│   └── __init__.py
│
├── use_cases/
│   ├── drone/
│   │   ├── main.py
│   │   └── data/
│   │       └── trajectories.json
│   │
│   ├── hospital/
│   │   ├── main.py
│   │   ├── param.py        # (modified file)
│   │   ├── data/
│   │   │   └── hospital_traces.json
│   │   └── coordinate/     # external trajectory generation tool (not our contribution)
│   │       ├── ...
│   │       └── README.md
│
├── requirements.txt
├── environment.yml
├── LICENSE
└── README.md
```

### Folder Description

- **`mitl/`**  
  Contains the implementation of the **MITL monitoring algorithm**, including the Boolean and quantitative (robustness-based) semantics for point-based event traces.

- **`use_cases/`**  
  Includes the two main evaluation scenarios:
  - **`drone/`** — Toy example demonstrating robustness analysis on ordered, time-constrained drone trajectories.  
  - **`hospital/`** — Simulation of a multi-agent smart hospital environment.  
    - **`coordinate/`** — External tool used to generate agent trajectories.  
      > ⚠️ *This folder is **not part of our contribution**; only `param.py` was modified.*

---

## ⚙️ Installation

You can set up the Python environment either using **`venv`** or **Conda**.

### Option 1 — Using `venv` (standard virtual environment)

```bash
git clone https://github.com/<your-username>/time-robustness-mitl.git
cd time-robustness-mitl

python3 -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

pip install -r requirements.txt
```

### Option 2 — Using Conda

```bash
conda env create -f environment.yml
conda activate mitl-robustness
```

---

## ▶️ Execution

Once the environment is ready, you can run the main use cases:

### Drone Use Case
```bash
cd use_cases/drone
python main.py
```

### Smart Hospital Use Case
```bash
cd use_cases/hospital
python main.py
```

---

## 🧠 Description

The monitoring algorithm implements the **quantitative time robustness semantics** for MITL formulas over **finite event traces**, as defined in the paper.  
Given an MITL formula φ and an event trace σ, the algorithm computes:

- The **Boolean satisfaction**: whether (σ, i) ⊨ φ.
- The **quantitative robustness value** ρ(φ, σ, i): a real-valued metric quantifying the tolerance of φ to timing perturbations in σ.

The implementation is modular, allowing the definition and evaluation of custom MITL formulas and event traces.

---

## 📊 Use Cases

### 1. Drone Surveillance System
A toy scenario where a drone must visit regions A, B, and C in a predefined temporal order:
```text
ψ_d = F[10,20](enterA ∧ F[40,50](enterB ∧ F[20,30] enterC))
```
Used to demonstrate the relationship between **time robustness** and **probability of satisfaction under temporal perturbations**.

### 2. Smart Hospital Multi-Agent System
A large-scale simulation of autonomous hospital robots delivering medical items.  
Three MITL properties are monitored:
```text
φ_a = G(created → F[0,20] startLoading)
φ_b = G(startLoading → F[L,U] delivered)
φ_c = G(fail → X[0,2500] recovered)
```
The **coordinate** module generates agent trajectories (external), while our modified `param.py` adjusts environment parameters for robustness evaluation.

---

## 🧾 Citation

If you use this repository, please cite:

```
@inproceedings{TimeRobustnessMITL2025,
  title={Time Robustness for Point-Based Semantics of Metric Interval Temporal Logic},
  booktitle={Tools and Algorithms for the Construction and Analysis of Systems (TACAS)},
  year={2025}
}
```

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.