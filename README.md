# dash-webapp-template
Template for expediting creation of new dash web apps in Python, specifically for Biofinformatics-based projects (hence the demo name `seqapp`).

This particular template contains a custom-branded (CSS/HTML) base UI layout presenting a UX for a two-step pipeline of any sort. For example, in "Step One", several dynamically linked (interdependent) dropdown menus allow a user to select certain data as input. And then "Step Two" allows for user upload of files (as/if applicable) and launching of a custom analysis pipeline which would be a backend python source code. 

Also included are the configuration files for deploying the app using gunicorn and nginx, as well as using Linux `systemd` to create a custom service dedicated to ensuring automatic, perpetual uptime. Multiple simultaneous user sessions are possible and each separately thoroughly logged, allowing for automatic auditable user session activity log records to always be available - comprehensively: every action is recorded and logged with timestamps and username. 

Thus >90% of this full-stack web app is able to be written all in Python, significantly speeding up the required time to create new apps as new ideas / requests for automated UI (i.e., codeless/for non-developers; e.g. wetlab scientists, QC team, mfg, etc.) tools arise. 

## Main app page begins with user log-in
> Thus creating per-session output directories where all uploaded and newly generated data files will be saved server-side, and available from the UI during the session for the user to filter through and select any they'd like the download.
<img width="1441" alt="top of app screenshot after user log in" src="https://user-images.githubusercontent.com/28764103/136808235-446142f7-66fc-44b6-a5d8-25c436d31ebb.png">

### A "Downloads" components section reveals live, comprehensive logging
> All user activity is logged, as shown. Additionally, of course, all automated analysis / all custom algorithm should also be logged and can be easily achieved with the logging already set up as is in this template. 
<img width="1405" alt="Screen Shot 2021-10-11 at 07 36 55 AM" src="https://user-images.githubusercontent.com/28764103/136809385-131808e0-2e14-43e0-8646-3fd56a4e7b83.png">

## "Step One" - Query a database (e.g., via [dynamic/interactive] network API calls)
<img width="1438" alt="Screen Shot 2021-10-11 at 07 38 22 AM" src="https://user-images.githubusercontent.com/28764103/136810065-bac11922-e4d4-489a-8a28-bfd543f1006d.png">

## "Step Two" - User uploads (or selects, e.g. via step #1) data to serve as the input for a bioinformatic pipeline analysis
<img width="1412" alt="Screen Shot 2021-10-11 at 07 40 13 AM" src="https://user-images.githubusercontent.com/28764103/136810723-a361d96a-53a2-4a53-8f0c-e66e2f870005.png">

### After the pipeline completes, a custom report can be immediately displayed
> For example leveraging very conveniently anything from Plotly for data visualizations to facilitate user interpretation of their results, interactive snappy fast tables (i.e., containing as many as millions of rows) with interactive functionalities such as filtering, searching, sorting - all pre-baked thanks to the open-source Dash data table library. Finally, users could interact with the displayed results and for example select certain "human QC-verified" samples whose data they could then upload properly into a central database with the click of a button. 
