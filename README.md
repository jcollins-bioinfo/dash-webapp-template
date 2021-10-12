<center>
  <img left="1046" alt="dash-webapp-template logo" src="https://user-images.githubusercontent.com/28764103/136825065-13fadfa5-e7cc-48df-812c-a8b25059cfa3.png">
</center>

# Overview of `dash-webapp-template`
A robust, highly customized, already laid-out and professionally stylized template repo for expediting the creation of new dash web apps in Python, specifically for Bioinformatics-based projects (hence the demo name `seqapp`; though this isn't a disqualifying cutoff - the template could be useful for any data science web app, you may just not find all of the provided code as useful as a bioinformatician might). Using `dash` in Python allows a developer to create a "full-stack" highly customizable web application enormously faster than previous standard professional practices, while still delivering utmost professional quality data science software solutions in the form of easy-to-use (and fast) web app UIs with as complex as possibly could be Python-coded backends hidden away but all neatly together in the same single relatively small collection of software files. See references below to learn more about the exciting paradigm shifting changes and accelerations in possible software development Dash has brought about!

This particular template contains a custom-branded (CSS/HTML) base UI layout presenting a UX for a two-step pipeline of any sort. For example, in "Step One", several dynamically linked (interdependent) dropdown menus allow a user to select certain data as input. And then "Step Two" allows for user upload of files (as/if applicable) and launching of a custom analysis pipeline which would be a backend python source code. 

Also included are the configuration files for deploying the app using gunicorn and nginx, as well as using Linux `systemd` to create a custom service dedicated to ensuring automatic, perpetual uptime. Multiple simultaneous user sessions are possible and each separately thoroughly logged, allowing for automatic auditable user session activity log records to always be available - comprehensively: every action is recorded and logged with timestamps and username. 

Thus >90% of this full-stack web app is able to be written all in Python, significantly speeding up the required time to create new apps as new ideas / requests for automated UI (i.e., codeless/for non-developers; e.g. wetlab scientists, QC team, mfg, etc.) tools arise. 

### Useful References
1) [Plotly](https://plotly.com/)
2) [Plotly's new web framework Dash＊ (v1.0 released in 2019†)](https://plotly.com/dash/)
3) [Dash gallery](https://dash.gallery/Portal/)
4) [Dash docs](https://dash.plotly.com/)
5) [Plotly docs](https://plotly.com/python/)



# App Template Overview

## Main app page begins with user log-in
> Thus creating per-session output directories where all uploaded and newly generated data files will be saved server-side, and available from the UI during the session for the user to filter through and select any they'd like to download.
<img width="1441" alt="top of app screenshot after user log in" src="https://user-images.githubusercontent.com/28764103/136808235-446142f7-66fc-44b6-a5d8-25c436d31ebb.png">

### A "Downloads" components section reveals live, comprehensive logging
> All user activity is logged, as shown. Additionally, of course, all automated analysis / all custom algorithm should also be logged and can be easily achieved with the logging already set up as is in this template. 
<img width="1405" alt="Users can download any file created by the app; including all of them, or a subselection of them by type, with a single click as a .zip archived file" src="https://user-images.githubusercontent.com/28764103/136809385-131808e0-2e14-43e0-8646-3fd56a4e7b83.png">

#### Session files will automatically be created and saved under `/seqapp/app/prod/sessions/` by date then unique SESSION_ID (or 'RUN_ID'):
<img width="538" alt="Only .log files are shown here, but typically in a fully fleshed out app, there would be many more files of various types!" src="https://user-images.githubusercontent.com/28764103/136828025-6222d3f1-8cef-4f85-88fb-b8f4971b106e.png">

## "Step One" - Query a database (e.g., via [dynamic/interactive] network API calls)
<img width="1438" alt="Step One - Query a database and retrieve and select relevant data as needed per analysis session" src="https://user-images.githubusercontent.com/28764103/136810065-bac11922-e4d4-489a-8a28-bfd543f1006d.png">

## "Step Two" - User uploads (or selects, e.g. via step #1) data to serve as the input for a bioinformatic pipeline analysis
<img width="1412" alt="Step Two - Upload any user files, launch the pipeline with one click!" src="https://user-images.githubusercontent.com/28764103/136810723-a361d96a-53a2-4a53-8f0c-e66e2f870005.png">

### After the pipeline completes, a custom report can be immediately displayed
> For example leveraging very conveniently anything from Plotly for data visualizations to facilitate user interpretation of their results, interactive snappy fast tables (i.e., containing as many as millions of rows) with interactive functionalities such as filtering, searching, sorting - all pre-baked thanks to the open-source Dash data table library. Finally, users could interact with the displayed results and for example select certain "human QC-verified" samples whose data they could then upload properly into a central database with the click of a button. 

<br>
___________
<br>

＊ _*A Note on Plotly's clear emphasis on their "Enterprise" services offerings:*_ 
> _This template provided here is essentially intended to bypass entirely the need for using the enterprise services. It is definitely possible for a single person to be data scientist + full-stack developer + devops engineer (though admittedly that could get very difficult depending on the number of users; as a personal aside, my previous work experience has always involved very small numbers of users - a dozen or so at most - from the R&D departments of biotech companies). Surely, I bet the Dash Enterprise product is one worth considering, depending on the organization and their needs, etc. But nonetheless it's incredible what all can be done freely just from the open-source provided code. (Thank you Plotly Dash for intelligently embracing open source!) To be clear this template does **not** require paying for Dash Enterprise (or anything else; it's totally free and open source)._

† https://community.plotly.com/t/welcoming-dash-1-0-0/25148

