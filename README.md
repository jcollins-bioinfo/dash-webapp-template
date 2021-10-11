# dash-webapp-template
Template for expediting creation of new dash web apps in Python, specifically for Biofinformatics-based projects (hence the demo name `seqapp`).

This particular template contains a custom-branded (CSS/HTML) base UI layout presenting a UX for a two-step pipeline of any sort. For example, in "Step One", several dynamically linked (interdependent) dropdown menus allow a user to select certain data as input. And then "Step Two" allows for user upload of files (as/if applicable) and launching of a custom analysis pipeline which would be a backend python source code. 

Also included are the configuration files for deploying the app using gunicorn and nginx, as well as using Linux `systemd` to create a custom service dedicated to ensuring automatic, perpetual uptime. Multiple simultaneous user sessions are possible and each separately thoroughly logged, allowing for automatic auditable user session activity log records to always be available - comprehensively: every action is recorded and logged with timestamps and username. 

Thus >90% of this full-stack web app is able to be written all in Python, significantly speeding up the required time to create new apps as new ideas / requests for automated UI (i.e., codeless/for non-developers; e.g. wetlab scientists, QC team, mfg, etc.) tools arise. 


<img width="1441" alt="top of app screenshot after user log in" src="https://user-images.githubusercontent.com/28764103/136808235-446142f7-66fc-44b6-a5d8-25c436d31ebb.png">
