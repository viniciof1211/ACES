# Azure Certification Practice Simulator 🛠️

Welcome to the **Azure Certification Practice Simulator**! This project provides an interactive test simulator designed to help engineers and IT professionals practice for **all major Azure certifications** in a structured and user-friendly environment. It is **specifically tailored for Accenture's Expert Technology Consulting (ETC)** organization, focusing on the needs of our SMB B2B customers. 

This tool is developed **in-house for our ETC engineers**, aiming to offer a **free**, effective, and immersive way to study for Azure certifications. The simulator covers a wide range of certifications, from fundamental to advanced levels, making it ideal for **skill enhancement** across different career stages. 🚀

---

## Features 🎯

- **Comprehensive Question Bank**: Questions sourced and structured based on actual certification exams.
- **Interactive Practice Sessions**: Real-time feedback on your answers, with explanations to deepen your understanding.
- **Certification-Specific CSV Files**: Each certification has its own CSV file loaded with questions, dynamically updated based on user selection.
- **Tailored for Accenture ETC**: Custom-built for engineers in Accenture's Microsoft-focused Expert Technology Consulting (ETC) group.
- **Simple, Elegant Design**: User-friendly menu-driven interface to select the desired certification.

---

## Recent Enhancements 🌟

We are constantly improving the **Azure Certification Practice Simulator** to offer the best possible preparation experience for our users. Below are the exciting new features from our latest update:

- **Language Selection**: You can now choose to take the exam in English, Spanish, Portuguese, French, or Japanese, making the simulator accessible to a broader audience across different regions.
  
- **Test Selection and Simulated Exams**: The system now offers an intuitive menu for selecting the Azure certification exam you wish to practice, ranging from **AZ-900 to advanced levels like AZ-305** and more.

- **Accurate Answer Validation**: We've added robust validation logic to ensure that you receive immediate and precise feedback on each question. Additionally, detailed explanations are provided to help you deepen your understanding of the topics.

- **Final Scoring with Visual Feedback**: After completing a practice session, the simulator now calculates your **total score** and presents it in a clear, easy-to-understand format. Additionally, we've introduced a **visual ASCII-based bar chart** to provide an engaging representation of your performance. Here’s an example of how it looks:

    ```plaintext
    Exam completed! Your score (Microsoft Notation - Max Score is 1000, Passing Score is 700): 22/24 (916.67%)
    Congratulations! You have passed the exam.

Score breakdown by category:

        Describe cloud concepts                  : ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ 0.00

        Describe Azure architecture and services : ███████████████████████████████████████▒▒▒▒▒▒▒▒▒▒▒ 791.67

        Describe Azure management and governance : ██████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ 125.00

    ```

These updates further enhance the realism of the exam simulation and offer more insightful feedback, allowing you to track your progress and focus on areas for improvement.


---

## Supported Azure Certifications 📜

This simulator covers **all major Azure certifications**, including but not limited to:

- **AZ-900**: Microsoft Azure Fundamentals
- **AZ-104**: Microsoft Azure Administrator
- **AZ-204**: Developing Solutions for Microsoft Azure
- **AZ-305**: Designing Microsoft Azure Infrastructure Solutions
- **AZ-400**: Designing and Implementing Microsoft DevOps Solutions
- **AZ-500**: Microsoft Azure Security Technologies
- **AZ-700**: Designing and Implementing Microsoft Azure Networking Solutions
- **AZ-800**: Administering Windows Server Hybrid Core Infrastructure
- **AZ-900** to **AZ-140**: All certifications in the Azure path

---

## How It Works ⚙️

Upon launching the simulator, you are presented with a menu to choose the Azure certification you'd like to practice:

```plaintext
1. AZ-900: Microsoft Azure Fundamentals
2. AZ-104: Microsoft Azure Administrator
3. AZ-204: Developing Solutions for Microsoft Azure
4. Exit
```

After selecting a certification, the corresponding **CSV file** is loaded, and the quiz begins. You’ll receive a question, multiple-choice answers, and immediate feedback on your selection, including a detailed explanation.

---

## Key Components 🧩

1. **CSV-based Data**: The simulator uses structured CSV files to store certification-specific questions, ensuring scalability and easy updates.
   
2. **Dynamic Certification Loading**: Based on your menu selection, the simulator dynamically loads the correct question set, ensuring a smooth and tailored user experience.

3. **Real-Time Feedback**: Instant feedback on each question, with clear explanations to support continuous learning.

---

## Getting Started 🚀

### Prerequisites

- Python 3.x installed on your machine.
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
   ```

3. **Install required packages**:
    ```bash
    pip install pandas nltk googletrans requests aiohttp
    ```

4. Clone this repository to your local machine (use Visual Studio 2022):
    ```bash
    git clone git@ssh.dev.azure.com:v3/viniciof/CertTester/ETC-CertTester
    ```

5. Navigate to the project directory:
    ```bash
    cd azure_certification_simulator
    ```

6. Install any necessary dependencies (if any) and run the Python script:
    ```bash
    python3.6 azure_certification_simulator.py
    ```

### Usage

Once the simulator is running, follow the on-screen prompts to select the certification you wish to practice. After completion, you'll receive a summary of your performance.

---

## Why This Simulator? 🤔

This tool is designed as a **no-cost**, **non-paid** initiative aimed at empowering Accenture engineers, specifically those part of the **ETC organization**. It supports engineers in **certification preparation** and aligns with Accenture's goal of continuously developing our team's skills, particularly for **Microsoft-focused projects**.

Developed **by engineers, for engineers**, this simulator reflects the real-world exam environments and allows for effective self-paced learning. It also complements our broader **ETC learning strategy**, encouraging ongoing professional development and certification success.

---

## Contributing 👩‍💻👨‍💻

We welcome contributions from Accenture’s internal team! Feel free to:

- Report issues
- Submit pull requests for new features
- Suggest improvements or additional certifications

For contribution guidelines, please refer to the `CONTRIBUTING.md` file.

---

## License 📄

This project is licensed under the MIT License. See the `LICENSE.md` file for more information.

---

## Acknowledgements 🙌

Special thanks to the **Accenture ETC team** for their support and feedback during the development of this simulator. We hope this tool helps our engineers excel in their Azure certifications and beyond!

---

**Happy learning and best of luck on your Azure certification journey!** 🌟

