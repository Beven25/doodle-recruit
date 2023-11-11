# Doodle Recruit 👀
This project repository is to hold all the project files and related documents of our final project of the Big Data Programming: Python (BDPP) course.

Problem:
Transforming Recruitment: AI-Based Inhouse Recruitment System"

In the bustling world of tech companies, there was a problem that seemed insurmountable—finding the right talent. The recruitment process had become an arduous journey, where countless hours were spent sifting through resumes and hoping to find that perfect fit. It was a quest that often felt like searching for a needle in a haystack.

To overcome this problem, As a team we came up with a solution by building an "AI-Based Inhouse Recruitment System," that showcases the incredible potential of data science in revolutionizing recruitment. Our team, comprised of data enthusiasts embarked on a journey to create this application.

In a real-world application, our system empowers recruiters to efficiently identify candidates possessing specific attributes like domain expertise, open source contributions, years of experience and proficiency in essential programming languages. Armed with this data, recruiters can seamlessly extend online assessment tests to the most promising candidates, ultimately expediting the process of selecting candidates for initial interviews.

![image](https://github.com/Big-Data-Programming/bdp_apr23_exam-bdp_apr23_1/assets/43603441/179f5589-6cff-4d99-9383-4161d18bb2be)
Homepage of Doodle Recruit Web App.

## File Structure Explanation:
>Some of the file names are self-explanatory and hence not included in this explanation.

`/Datasets`<br>Contains the 16k records of different user profiles.<br><br>
`/Trail_and_Error`<br>Contains all the code which we used while trying our different algorithms, fetching data, etc. Code in this folder is not part of working app.<br><br>
`/pages`<br>Contains the main sections/webpages of the app.<br><br>
`/user_credentials`<br>The user credentials (for both candidate & Recruiter Space) are stored here in YAML files. Encrption of passwords is done automatically by the authentication library (streamlit-authenticator). We just stored the encrypted passwords here in YAML.<br><br>
`streamlit_app.py`<br>The Homepage of Doodle Recruit.<br><br>
`uf_fn.py`<br>The main content of Recruiter space comes from this file.<br><br>
`Dockerfile`<br>The current version of this file is currently platform dependent. Using this docker file to create an image will only work on Linux machines.

### Link to live streamlit app hosted on Streamlit community cloud:
[Doodle Recruit Web App](https://doodle-project-j3wmuu4m34cfczs9etid72.streamlit.app/)
