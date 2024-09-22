# Azure Certification Practice Simulator 🛠️

Welcome to the **Azure Certification Practice Simulator**! This project is designed to provide an interactive test simulator to help engineers and IT professionals practice for **Azure certifications** in a structured and user-friendly environment.

> **Disclaimer**: This project is developed independently and is not an official product of any company nor entity. The views and opinions expressed herein are solely those of the author as open-source developer.

---

## Features 🎯

- **Comprehensive Question Bank**: Questions sourced and structured based on actual certification exams.
- **Interactive Practice Sessions**: Real-time feedback on your answers, with explanations to deepen your understanding.
- **Certification-Specific CSV Files**: Each certification has its own CSV file loaded with questions.
- **User-Friendly Design**: A simple, elegant menu-driven interface for selecting the desired certification.

---

## Supported Azure Certifications 📜

This simulator covers **all major Azure certifications**, including:

- **AZ-900**: Microsoft Azure Fundamentals
- **AZ-104**: Microsoft Azure Administrator
- **AZ-204**: Developing Solutions for Microsoft Azure
- **AZ-305**: Designing Microsoft Azure Infrastructure Solutions
- **AZ-400**: Designing and Implementing Microsoft DevOps Solutions
- **AZ-500**: Microsoft Azure Security Technologies
- **AZ-700**: Designing and Implementing Microsoft Azure Networking Solutions

---

## Getting Started 🚀

### Prerequisites

- Python 3.6.12 installed on your machine.
- Basic knowledge of command-line interface (CLI) operations.

### Installation

1. **Install Python 3.6.12**:
   - For **Windows**:
     - Download the installer from the [official Python website](https://www.python.org/downloads/release/python-3612/).
     - Run the installer and ensure you check the box that says "Add Python to PATH".
   - For **macOS**:
     ```bash
     brew install python@3.6
     ```
   - For **Linux** (Debian-based):
     ```bash
     sudo apt update
     sudo apt install python3.6 python3-pip
     ```

2. **Install pip** (if not included with Python):
   ```bash
   python3.6 -m ensurepip
   
3. **Install required packages:**
  ```bash
  pip install pandas nltk googletrans requests aiohttp
  ````
4. **Clone this repository to your local machine:**
    
    ```bash
    git clone https://github.com/yourusername/azure-certification-simulator.git
    ```
5. **Navigate to the project directory:**
    
    ```
    bash
    cd azure_certification_simulator
    ```
6. **Run the Python script:**

    ```bash
      python3.6 azure_certification_simulator.py
    ```

### Usage
Follow the on-screen prompts to select the certification you wish to practice. After completion, you'll receive a summary of your performance.

## Why This Simulator? 🤔
This tool is designed to empower users in certification preparation. Developed by engineers, for engineers, this simulator aims to provide effective self-paced learning and is a no-cost initiative.

## Contributing 👩‍💻👨‍💻
Contributions are welcome! Feel free to send your PRs to https://github.com/viniciof1211/ACES.git

## Report issues
### Suggest improvements
### Submit pull requests
### For contribution guidelines, refer to the CONTRIBUTING.md file.

## License 📄
This project is licensed under the MIT License. See the LICENSE.md file for more information.

## Acknowledgements 🙌
Special thanks to the open-source and free-software community for their support and feedback during the development of this simulator. We hope this tool helps users excel in their Azure certifications!

_Happy learning and best of luck on your Azure certification journey! 🌟_
