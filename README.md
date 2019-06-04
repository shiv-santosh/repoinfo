# repoinfo

Problem Statement:
Input: User can input a link to any public GitHub repository  

Output : UI that displays a table with the following information -  
  - Total number of open issues 
  - Number of open issues that were opened in the last 24 hours 
  - Number of open issues that were opened more than 24 hours ago but less than 7 days ago 
  - Number of open issues that were opened more than 7 days ago   

Approach:  
  - Use github api to get issues of a repository
  - Take user credentials if necessary
  - Iterate through all issues and segregate them into types
  - Render issues using dictionary


Space for improvement:
  - Pagination for issues list
  - Features to perform git actions that are capabale using the github API
  - Two factor authentication in addition to basic authentication
  - Overall better UI


Steps to get the app running
  - Open terminal
  - Switch to project directory
  - run `python3 manage.py runserver`
  - open localhost:8000 in your browser
