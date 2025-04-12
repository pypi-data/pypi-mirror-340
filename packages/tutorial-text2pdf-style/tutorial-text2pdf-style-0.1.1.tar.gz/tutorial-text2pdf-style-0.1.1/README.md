[![Use this template](https://img.shields.io/badge/-Use%20this%20template-brightgreen?style=for-the-badge)](https://github.com/adhikaripb/coding-scripting-tutorial-pdf-generator/generate)
<p align="center">
  <img src="assets/banner.png" width="80%" alt="Repo Banner"/>
</p>
# 📄 Text-to-Colored-PDF Converter

![Python](https://img.shields.io/badge/Python-3.7+-blue?logo=python)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-active-brightgreen)
![Stars](https://img.shields.io/github/stars/adhikaripb/workflow-text-to-colored-pdf?style=social)
![Last Commit](https://img.shields.io/github/last-commit/adhikaripb/workflow-text-to-colored-pdf)

A stylish and minimal Python script that converts cleanly formatted `.txt` documentation into beautifully styled PDFs — ideal for sharing protocols, tutorials, coding steps, or structured instructions.

---
## 🧭 Table of Contents

- [Features](#️features)
- [Input Format Example](#input-format-example)
- [How to Use](#how-to-use)
- [Sample Output](#sample-output)
- [Project Structure](#project-structure)
- [Credits](#credits)
- [License](#license)

---

## 🖋️ Features

- 🪄 Converts step-based text into structured colored PDFs
- 🎨 Syntax-highlighted script blocks
- ✍️ Instruction + code separation with visual hierarchy
- 📦 Automatically wraps long lines inside script blocks
- 📜 Supports project titles and contributor metadata from the `.txt`
- 📤 Outputs PDF in the same directory as input

---

## 📝 Input Format Example

```text
Title: GitHub Push Workflow from PyCharm (Styled Script Format)
[Prepared by AdhikariPB with ChatGPT]

Step 1: Create a Proper PyCharm Project
- Structure cleanly (e.g., ~/PyCharmProjects/my_project)
- Include a README.md and .gitignore if needed.

"""
$ git init
"""
```

---

## 🚀 How to Use

### 1. Clone the Repository

```bash
git clone https://github.com/adhikaripb/coding-scripting-tutorial-pdf-generator.git
cd coding-scripting-tutorial-pdf-generator
```

### 2. [Optional] Install Required Package

The script auto-checks and installs prerequisite modules. However, if you'd like to do it manuyally,

```bash
pip install fpdf
```

### 3. Run the Script

Once installed (or after setup locally), you can run it from anywhere using:

```bash
tutorial-txt2pdf-style
```

- You'll be prompted to provide a path to a `.txt` file.
- A color-styled PDF will be generated in the same folder.

---

## 📷 Sample Output

<p align="center">
  <img src="samples/sample_output.png" alt="Sample Output Preview" width="100%" />
</p>
