# Functional Specification Document:
## 1. Background
Problem Being Addressed
The PathoGUI system is designed to assist pathologists in grading and annotating tissue images. The system provides a user-friendly interface for pathologists to view images, pan and zoom, annotate images with bounding boxes, and save grading information for further analysis. Additionally, the system caters to data scientists and research assistants who need to retrieve and analyze the grading data.

## 2. User Profile
### 2.1 Technician
- Role: Software designer
* Skills: High proficiency in software development
+ Objectives: Modify, develop, and fix bugs in the PathoGUI tool. Desire a well-written and well-maintained system.
### 2.2 Pathologist
- Role: Educated evaluator of cancer imagery
* Skills: Basic computer program skills, high proficiency in grading tissue images
+ Objectives: Use the tool to grade and annotate images. Prefer a user-friendly interface without the need to interact with code.
### 2.3 Data Scientist
- Role: Educated and trained in dataset analysis
* Skills: High proficiency in data analysis, intermediate skills in functional programming
+ Objectives: Retrieve pathologist gradings, analyze tissues, and assess the accuracy of pathologists. Require data ready for analysis/training.
### 2.4 Research Assistant/Trainee
- Role: New project team member
* Skills: Varies (not educated or trained in pathology or data science, or in the process of being educated or trained)
+ Objectives: Learn to use the tool quickly, review pathologist gradings to learn tissue grading. Desire a user-friendly and well-documented tool for efficient learning and contribution to the project.
## 3. Data Sources
### Data Used
- Tissue images in the form of '.tif' files.
+ Grading data, including primary and secondary grades, coordinates, and comments.
### Data Structure
- Tissue images stored in the "../Data" folder.
+ Grading results stored in the "./Results" folder as CSV files.
## 4. Use Cases
### 4.1 Use Case: Pathologist Grading
- Objective: Grade and annotate tissue images.
+ Expected Interactions:
  1. Open the PathoGUI tool.
  1. Log in using user identification or PIN.
  1. View images and pan/zoom as needed.
  1. Annotate images with bounding boxes.
  1. Select next image to continue grading.
  1. Save and exit, with the ability to resume later.
### 4.2 Use Case: Data Scientist Analysis
- Objective: Retrieve and analyze pathologist gradings.
+ Expected Interactions:
  1. Retrieve grading data from the PathoGUI tool.
  1. Package/export data for analysis/training.
  1. Conduct data analysis using preferred tools and programming languages.
### 4.3 Use Case: Research Assistant/Trainee Learning
- Objective: Learn to use the PathoGUI tool and review pathologist gradings for learning.
+ Expected Interactions:
  1. Open the PathoGUI tool.
  1. Load pregraded data into the UI for individual training.
  1. Read training documentation.
  1. Interact with the UI to understand image grading.
  1. Use the tool as a learning resource to contribute to the project.
## 5. User Stories
### 5.1 Technician User Story
"As a software designer, I want to modify and develop the PathoGUI tool efficiently. I expect the code to be well-written and maintained to facilitate my work."

### 5.2 Pathologist User Story
"As a pathologist, I want to use the PathoGUI tool to grade and annotate tissue images without the need to interact with code. I need the tool to be user-friendly and efficient."

### 5.3 Data Scientist User Story
"As a data scientist, I want to retrieve pathologist gradings and analyze tissues. I expect the data to be packaged and exported in a format suitable for analysis and training."

### 5.4 Research Assistant/Trainee User Story
"As a research assistant/trainee, I want to learn to use the PathoGUI tool quickly and review pathologist gradings to contribute to the project. I need the tool to be user-friendly and well-documented for efficient learning."
