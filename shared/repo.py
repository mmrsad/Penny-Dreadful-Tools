import datetime
import sys
import textwrap
import traceback
from typing import Dict, List, Optional

from flask import request, session
from github import Github, Issue, PullRequest

from shared import configuration, dtutil


def create_issue(content: str,
                 author: str,
                 location: str = 'Discord',
                 repo_name: str = 'PennyDreadfulMTG/Penny-Dreadful-Tools',
                 exception: Optional[Exception] = None) -> Issue:
    labels: List[str] = []
    if content is None or content == '':
        return None
    body = ''
    if '\n' in content:
        title, body = content.split('\n', 1)
        body += '\n\n'
    else:
        title = content
    body += 'Reported on {location} by {author}'.format(location=location, author=author)
    if request:
        body += textwrap.dedent("""```
            --------------------------------------------------------------------------------
            Request Method: {method}
            Path: {full_path}
            Cookies: {cookies}
            Endpoint: {endpoint}
            View Args: {view_args}
            Person: {id}
            Referrer: {referrer}
            Request Data: {safe_data}
        """.format(method=request.method, full_path=request.full_path, cookies=request.cookies, endpoint=request.endpoint, view_args=request.view_args, id=session.get('id', 'logged_out'), referrer=request.referrer, safe_data=str(safe_data(request.form))))
        body += '\n'.join(['{k}: {v}'.format(k=k, v=v) for k, v in request.headers])
        body += '\n```\n'
        ua = request.headers.get('User-Agent')
        if ua == 'pennydreadfulmagic.com cache renewer':
            labels.append(ua)
        elif 'YandexBot' in ua or 'Googlebot' in ua:
            labels.append('Search Engine')

    if exception:
        body += '--------------------------------------------------------------------------------\n'
        body += exception.__class__.__name__ + '\n'
        stack = traceback.extract_stack()[:-3] + traceback.extract_tb(exception.__traceback__)
        pretty = traceback.format_list(stack)
        body += 'Stack Trace:\n```\n' + ''.join(pretty) + '\n```\n'
    print(title + '\n' + body, file=sys.stderr)
    # Only check for github details at the last second to get log output even if github not configured.
    if not configuration.get('github_user') or not configuration.get('github_password'):
        return None
    g = Github(configuration.get('github_user'), configuration.get('github_password'))
    git_repo = g.get_repo(repo_name)
    if repo_name == 'PennyDreadfulMTG/perf-reports':
        labels.append(location)
        if exception:
            labels.append(exception.__class__.__name__)
    issue = git_repo.create_issue(title=title, body=body, labels=labels)
    return issue

def safe_data(data: Dict[str, str]) -> Dict[str, str]:
    safe = {}
    for k, v in data.items():
        if 'oauth' not in k.lower() and 'api_token' not in k.lower():
            safe[k] = v
    return safe

def get_pull_requests(start_date: datetime.datetime, end_date: datetime.datetime, max_pull_requests: int = sys.maxsize, repo_name: str = 'PennyDreadfulMTG/Penny-Dreadful-Tools'):
    g = Github(configuration.get('github_user'), configuration.get('github_password'))
    git_repo = g.get_repo(repo_name)
    pulls: List[PullRequest] = []
    for pull in git_repo.get_pulls(state='closed', sort='updated', direction='desc'):
        if not pull.merged_at:
            continue
        pull.merged_dt = pull.merged_at.astimezone(dtutil.UTC_TZ)
        pull.updated_dt = pull.updated_at.astimezone(dtutil.UTC_TZ)
        if pull.merged_dt > end_date:
            continue
        if pull.updated_dt < start_date:
            return pulls
        pulls.append(pull)
        if len(pulls) >= max_pull_requests:
            return pulls
    return pulls
