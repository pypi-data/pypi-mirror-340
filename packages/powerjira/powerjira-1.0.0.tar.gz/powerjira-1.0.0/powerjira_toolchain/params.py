from os import getenv

user_name = getenv('JIRA_USERNAME')
token = getenv('JIRA_TOKEN')
domain = getenv('JIRA_DOMAIN')
home_dir = getenv('HOME')

ticket_excerpt_length = 60
default_powerjira_directory = f'{home_dir}/powerjira'
default_shell = '/bin/zsh'
default_editor = 'vscode'
default_powerjira_table_style = 'rounded_outline'

templates = {
  'ticket.yml': '''# pj --help

#───TICKET───────────────────
reporter: iyep
assignee: iyep

init_status: to do # new, to do, in progress, done, backlog

project: QUANT # QUANT, HYP, CS
priority: Medium # Low, Medium, High (ignored for Epic)
issue_type: Task # Task, Epic
parent_epic: '' # Leave empty for standalone task or epic


#───GIT──────────────────────
branch_suffix: 'implement_thing'
parent_branch: main''',

  'summary.txt': '''Implement the thing''',

  'description.txt': '''This is the ticket's title, which jira calls the "summary"''',
}


#TODO: move to ticket.yml
branch_naming_convention = 'feature/<ticket_key>_<branch_suffix>'
#TODO: implement override in sleepyconfig.yml
result_table_style = default_powerjira_table_style if True else ''
powerjira_directory = default_powerjira_directory if True else ''
powerjira_shell = default_shell if True else ''
powerjira_editor = default_editor if True else ''