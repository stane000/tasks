# CitySummaryApp

Application for creating short summary file for given city.

## Table of Contents

1. [Installation](#installation)
2. [Usage](#usage)
3. Run tests


1. Installation

   If you don't have installed packages request nad python on your pc you can use
   virtual environment to run app inside environment or you can skip this step

   -> run: create_env_and_install_packages.bat, this creates app-env and installs packages

2. Usage

   Inside terminal 1.run -> activate_app_venv.bat, to activate virtual env you created in step 1. Installation
                   2.run -> python path/to/ city_summary_app.py Zagreb, this creates zagreb.txt (replace Zagreb with city you need)
   
        
3. Run Tets

   To run unit test just run: run_unit_tests.bat

   To run pytest test just run: run_city_summary_app_test.bat, pytest it's necessary

   You can run test from terminal just run: pytest city_summary_app_test.py, you can add marker to select sucres test or error tests, (example: pytest city_summary_app_test.py -m success)