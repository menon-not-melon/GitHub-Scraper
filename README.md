# GitHub-Scraper
A scraper that searches GitHub Repo's and Codes for a certain keyword

## Overview
GitHub API Scraper is a powerful tool that allows users to search the GitHub API for specific keywords and retrieve repositories and source codes containing those keywords. The tool simplifies the process of finding relevant projects and source code related to specific topics, making it easier for developers and researchers to discover valuable resources on GitHub.

## Features
* Search the GitHub API for specified keywords.
* Retrieve repositories and source code containing the specified keywords.
* Save the search results in a user-friendly CSV file for further analysis.

## Getting Started
Follow these instructions to set up and run the GitHub API Scraper on your local machine.
### Prerequisites
* Python 3.x installed on your system.
* The requests library for Python.
```python
pip install requests
```
### Installation
* Clone this repository to your local machine:
```python
git clone https://github.com/menon-not-melon/GitHub-Scraper.git
```
* Navigate to the project directory:
```python
cd GitHub-Scraper
```
### Usage
* Run the github_api_scraper.py source file.
* Or Run the .exe file in dist folder.
  
* * The script will prompt you to enter the keywords you want to search for on GitHub, and the file path to store the .csv file.
* * After entering the keywords, the scraper will use the GitHub API to search for repositories and source code related to those keywords.
* * The search results will be saved in a CSV file in the mentioned directory.
* * You can open the .csv file using a spreadsheet software (e.g., Microsoft Excel, Google Sheets) for further analysis.

## Example
Suppose you want to search for repositories and source code related to "machine learning" and "data analysis." Run the script, input the keywords, and the scraper will retrieve relevant results.
