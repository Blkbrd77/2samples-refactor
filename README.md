# 2samples-refactor

## Overview
This project sets up a new 2Samples site using Python with the Flask web framework, transitioning from a WordPress site to a modern, custom application. It serves as a portfolio piece showcasing Flask development, Test-Driven Development (TDD), and responsive web design.

## Related Sites
- [Flask Example on Replit](https://replit.com/)

## Next Tasks
Here are the upcoming priorities for this project:

1. ~~Automation for Codespaces~~ *Completed*
2. Bootstrapping
3. Add content (pictures, YouTube)
4. ~~Enhance Theme~~ *Completed* 
5. AWS Preparation 

## Getting Started
To run this project locally or in Codespaces:

1. **Clone the Repository:**

  bash
```
   git clone https://github.com/Blkbrd77/2samples-refactor.git
   cd 2samples-refactor
```
2. **Set Up Environment:**
  - Install Python 3.9+.
  - Create a virtual environment:
 
  bash 
```
  python3 -m venv venv
  source venv/bin/activate  # On macOS/Linux
  venv\Scripts\activate     # On Windows
```
3. **Run the Application:**

  bash
```
  python3 app/main.py
```
Open http://localhost:5000 in you browser.
4. **Run Tests:**  

bash
```
  pytest
```
## Project Structure

  - **app/:** Contains Flask application files (main.py, templates/, static/).
  - **requirements.txt:** Lists Python dependencies.
  - **.devcontainer/:** Configures Codespaces automation.

## Contributing

Feel free to fork this repository, make improvements, and submit pull requests. This project is a learning tool for Flask, TDD, and CI/CD preparation.


