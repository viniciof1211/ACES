# Changelog

All notable changes to the ETC-CertTester Azure Exam Simulator will be documented in this file.

## [ALPHA-Stage]

### Added
- Initial release of the ETC-CertTester Azure Exam Simulator
- Support for the following Microsoft Azure and related certification exams:
  1. AZ-900: Microsoft Azure Fundamentals
  2. AZ-104: Microsoft Azure Administrator
  3. AZ-204: Developing Solutions for Microsoft Azure
  4. AZ-305: Designing Microsoft Azure Infrastructure Solutions
  5. AZ-400: Designing and Implementing Microsoft DevOps Solutions
  6. AZ-500: Microsoft Azure Security Technologies
  7. AZ-700: Designing and Implementing Microsoft Azure Networking Solutions
  8. AZ-800: Administering Windows Server Hybrid Core Infrastructure
  9. AZ-140: Configuring and Operating Microsoft Azure Virtual Desktop
  10. MS-900: Microsoft 365 Certified: Fundamentals
  11. PL-900: Microsoft Certified: Power Platform Fundamentals
- Multilingual support for exam-taking in:
  - English
  - Spanish
  - Portuguese
  - French
  - Japanese
- Implementation of Natural Language Processing (NLP) for question categorization
- Asynchronous and parallel processing for improved performance
- Spaced-Repetition (Leibniz Algorithm) and microlearning techniques
- Detailed score breakdown by category
- Integration with NLTK for improved text processing
- Support for semicolon-delimited CSV files for question input

### Changed
- Modified to include certification menu selection
- Updated to handle semicolon-delimited CSV files

### Fixed
- Improved error handling and user feedback

## [0.1.0] - 2024-09-28

### Added
- Initial version of the ETC-CertTester Azure Exam Simulator
- Basic functionality for simulating Microsoft Azure certification exams
- Support for loading questions from CSV files
- Simple scoring system

## Notes
- The simulator is under active development and may contain bugs or incomplete features.
- Future updates will focus on expanding the question database, improving translation accuracy, and enhancing the user interface.
- Each certification exam is represented by a corresponding CSV file (e.g., az900_questions.csv for AZ-900)
