from django.shortcuts import render
from django.http import HttpResponse
from github import Github
import logging

repo_url = None # repository url
github_obj = Github() # Github object without authentication

# helper method for rendering error messages on any exceptions
def render_with_error(request, e):
    return render(request=request,
                  template_name="details.html",
                  context={"error_message": str(e)})

def register_user(request):
    global github_obj
    user_name = request.POST.get('user_name', None)
    password = request.POST.get('password', None)
    github_obj = Github(user_name, password)
    try:
        return index(request)
    except Exception as e:
        return render_with_error(request, e.data["message"])

def read_repo(request):
    if request.method == 'POST':
        url = request.POST.get('repourl', None)
        global repo_url
        try:
            repo_url = get_repo_name_from_url(url)
            return index(request)
        except Exception as e:
            return render_with_error(request,e.data["message"])

def get_repo_name_from_url(url):
    # get repository name and user name from url provided by the user
    # for "https://github.com/user_name/repository_name" returns "user_name/repository_name"
    return '/'.join(url.split('/')[-2:])

def get_issue_dict(issue):
    return {
        "issue_title": issue.title,
        "issue_url": issue.html_url,
        "issue_created_at": issue.created_at
    }

def index(request):
    global repo_url
    global github_obj
    if repo_url==None:
        return render_with_error(request,"Enter a public repository Url")
    try:
        issues = github_obj.get_repo(repo_url).get_issues(state="open")
    except Exception as e:
        # reset github_obj if bad credentials were provided
        if e.data["message"] == "Bad credentials":
            github_obj = Github()
        return render_with_error(request, e.data["message"])
    total_issues = 0
    issues_opened_last_24hr = []
    total_issues_opened_last_24hr = 0
    issues_opened_last_week = []
    total_issues_opened_last_week = 0
    issues_opened_older_than_a_week =[]
    total_issues_opened_older_than_a_week = 0

    issues_dict = \
    {
        "issues_opened_last_24hr":
           {
               "title":"Issues opened in the last 24 hours: ",
               "issues":[],
               "total":0
           },
       "issues_opened_last_week":
           {
               "title": "Issues opened in the last week later than 24 hours: ",
               "issues":[],
               "total":0
           },
       "issues_opened_older_than_a_week":
           {
               "title": "Issues opened before last week: ",
               "issues":[],
               "total":0
           }
    }

    # Classification of all issues in repository to types and counter for all classifications
    for issue in issues:
        total_issues = total_issues + 1
        time_between = issue.created_at.now() - issue.created_at
        if time_between.days==0:
            issues_opened_last_24hr.append(get_issue_dict(issue))
            total_issues_opened_last_24hr = total_issues_opened_last_24hr + 1
        elif time_between.days<7:
            issues_opened_last_week.append(get_issue_dict(issue))
            total_issues_opened_last_week = total_issues_opened_last_week + 1
        else:
            issues_opened_older_than_a_week.append(get_issue_dict(issue))
            total_issues_opened_older_than_a_week = total_issues_opened_older_than_a_week + 1

    issues_dict["issues_opened_last_24hr"]["total"] = total_issues_opened_last_24hr
    issues_dict["issues_opened_last_week"]["total"] = total_issues_opened_last_week
    issues_dict["issues_opened_older_than_a_week"]["total"] = total_issues_opened_older_than_a_week
    issues_dict["issues_opened_last_24hr"]["issues"] = issues_opened_last_24hr
    issues_dict["issues_opened_last_week"]["issues"] = issues_opened_last_week
    issues_dict["issues_opened_older_than_a_week"]["issues"] = issues_opened_older_than_a_week

    return render(request=request,
                  template_name="details.html",
                  context={"total_issues": total_issues,
                           "issue_dict":issues_dict})
