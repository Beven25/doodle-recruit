# Doodle Recruit 👀
This project repository is to hold all the project files and related documents of our final project of the Big Data Programming: Python (BDPP) course.

![image](https://github.com/Big-Data-Programming/bdp_apr23_exam-bdp_apr23_1/assets/43603441/179f5589-6cff-4d99-9383-4161d18bb2be)
Homepage of Doodle Recruit Web App.

## File Structure Explanation:
>Some of the file names are self-explanatory and hence not included in this explanation.

`/Datasets`<br>Contains the main raw data with 16k records.<br><br>
`/Trail_and_Error`<br>Contains all the code which we used while trying our different algorithms, fetching data, etc. Code in this folder is not part of working app.<br><br>
`/pages`<br>Contains the main sections/webpages of the app.<br><br>
`/user_credentials`<br>The user credentials (for both candidate & Recruiter Space) are stored here in YAML files. Encrption of passwords is done automatically by the authentication library (streamlit-authenticator). We just stored the encrypted passwords here in YAML.<br><br>
`streamlit_app.py`<br>The Homepage of Doodle Recruit.<br><br>
`uf_fn.py`<br>The main content of Recruiter space comes from this file.<br><br>
`Dockerfile`<br>The current version of this file is currently platform dependent. Using this docker file to create an image will only work on Linux machines.

### Link to live streamlit app hosted on Streamlit community cloud:
[Doodle Recruit Web App](https://doodle-project-j3wmuu4m34cfczs9etid72.streamlit.app/)
