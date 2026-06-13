# Big Data Analysis Simulation

By: Louis Filiepe Tio Jansel
Streamlit link: https://simulation-big-data-analysis.streamlit.app/

A short and simple simulation of big data processing and analysis, focusing specifically on simulating several key points:
1. Big Data processing
2. Big Data analysis
3. Big Data streaming
4. Risk classification and flagging

---

## Step-by-Step Process for Running the Code
1. Make sure all necessary libraries are installed (Steps to install libraries are provided later in this document).
2. Run UAS_PBD.ipynb file, in order to create or update necessary files for opening the dashboard.
3. Open terminal and run: streamlit run streamlit_home.py
4. Click the link provided by the previous command, if the web does not automatically open.

---

## Library installation
1. Method 1: run the following command -> pip install -r requirements.txt
2. Method 2: run the following command -> pip install ipykernel scikit-learn pandas numpy matplotlib seaborn xgboost streamlit

Note: 
- **Only use method 2 if method 1 does not work**
- The streamlit app and code in general was created locally, and as such, it would be best if the program is run locally and run within a local virtual environment (run 'python -m venv venv' to create a new python virtual environment), or simply see the app in the provided link.
- The ipykernel library may have to be installed separately from the rest of the libraries.