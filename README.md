# 🦁 Project SPHINX: Behavioral Biometric authentication system

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Security](https://img.shields.io/badge/Type-Behavioral_Biometrics-green.svg)
![AI](https://img.shields.io/badge/Algorithm-Statistical_Anomaly_Detection-orange.svg)

> **⚠️ CONCEPT**
>
> **Project SPHINX** is a multi-factor authentication system based on **Behavioral Biometrics**.
> Unlike traditional passwords (what you *know*), SPHINX validates identity based on **who you are** (muscle memory, cognitive reflexes, and fine motor skills).

---

## 📖 Overview

Standard authentication systems are vulnerable to stolen passwords. SPHINX solves this by adding a layer of **Zero-Trust Human Verification**.
The system challenges the user with three distinct biometric trials. It analyzes the user's input patterns using statistical modeling (Z-Score analysis) to distinguish between the authorized user, an imposter, or a bot.

---

## 🛡️ The Three Trials (Defense Layers)

The system is composed of three consecutive phases. A failure in any phase triggers an immediate lockdown.

### 1. 🌌 Phase I: The Constellation (Mouse Dynamics)
* **The Task:** The user must click on a sequence of fixed targets.
* **Biometric Metrics:**
    * **Reaction Time:** Time taken to initiate movement after target appearance.
    * **Path Efficiency:** The ratio between the actual path taken and the optimal straight line.
    * **Kinematics:** Velocity and acceleration profiles.
* **Logic:** Bots move too perfectly (Efficiency = 1.0), while imposters hesitate (High Reaction Time).

### 2. ⌨️ Phase II: The Mantra (Keystroke Dynamics)
* **The Task:** The user types a secret passphrase (e.g., "hello world").
* **Biometric Metrics:**
    * **Dwell Time (30% weight):** How long a key is pressed.
    * **Flight Time (70% weight):** The time interval between releasing one key and pressing the next.
* **Logic:** Flight time represents subconscious muscle memory rhythm, which is nearly impossible to mimic consciously.

### 3. 🕹️ Phase III: The Labyrinth (Fine Motor Skills)
* **The Task:** Navigate a cursor through a narrow maze without touching the walls.
* **Biometric Metrics:**
    * **Jitter Score:** Measures micro-tremors and angular changes in the movement path.
    * **Stability:** Smoothness of the curve.
* **Logic:** Verifies human fine motor control. High stress or lack of familiarity results in high Jitter scores.

---

## 🛠️ Technical Architecture

The project follows a modular structure, separating the logic (Analyzers), UI, and Training modules for each biometric phase.

```text
📦 Project SPHINX
 ┣ 📂 data                         # Stores JSON profiles & logs
 ┃ ┣ 📜 maze_profile.json
 ┃ ┣ 📜 dots_test_proflle.json
 ┃ ┗ 📜 my_keyboard_profile.json
 ┣ 📂 Dots_test_module             # Phase 1: Mouse Constellation
 ┃ ┣ 📜 dots_test_main.py          # Logic & Scoring
 ┃ ┣ 📜 dots_test_ui.py            # GUI Implementation
 ┃ ┣ 📜 mouse_analyzer.py          # Math Engine (Vel/Accel)
 ┃ ┗ 📜 build_mouse_profile.py     # Training Script
 ┣ 📂 Password_test_module         # Phase 2: Keystroke Dynamics
 ┃ ┣ 📜 keyboard_detector.py       # Verification Logic
 ┃ ┣ 📜 password_test_ui.py        # GUI Implementation
 ┃ ┣ 📜 keyboard_analyzer.py       # Keystroke Parser
 ┃ ┗ 📜 build_keyboard_profile.py  # Training Script
 ┣ 📂 Maze_test_module             # Phase 3: Fine Motor Skills
 ┃ ┣ 📜 maze_test_main.py          # Logic & Scoring
 ┃ ┣ 📜 maze_test_ui.py            # GUI Implementation
 ┃ ┣ 📜 maze_analyzer.py           # Math Engine (Jitter/Efficiency)
 ┃ ┗ 📜 build_maze_profile.py      # Training Script
 ┗ 📜 main.py                      # Orchestrator (Main Entry Point)
```
## 🧠 The Math Behind SPHINX

The system uses **Statistical Anomaly Detection** to compare current behavior against the user's baseline profile.

### 1. Standardization (Modified Z-Score)
To normalize different metrics, we use a Z-Score formula. We apply a "clamped" standard deviation to prevent division by zero in highly precise movements:

$$Z = \frac{|Current - Mean|}{\max(StdDev, \epsilon)}$$

### 2. Key Biometric Formulas
* **Kinematics:** Calculates **Velocity** ($v = \Delta d / \Delta t$) and **Acceleration** ($a = \Delta v / \Delta t$) to distinguish between human motion and robotic inputs.
* **Path Efficiency ($\eta$):** The ratio between the actual path taken and the optimal straight line. High ratios indicate erratic behavior.
    $$\eta = \frac{\sum d_{actual}}{d_{euclidean}}$$
* **Jitter ($J$):** Measures the cumulative angular change per pixel traveled to detect hand stability and micro-tremors.
    $$J = \frac{\sum |\theta_{i} - \theta_{i-1}|}{d_{total}}$$

### 3. Weighted Scoring
The final decision is a weighted linear combination of all Z-Scores, prioritizing harder-to-mimic features (like Flight Time or Jitter):

$$FinalScore = \sum (Z_i \cdot w_i)$$

* **Score < 1.5:** Verified (Access Granted).
* **Score ≥ 1.5:** Anomaly (Access Denied).
