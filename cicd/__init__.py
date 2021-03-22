import jenkins

# TODO: pull username/password from admin config for operator ci/cd deployment
jenkins_server = jenkins.Jenkins(
    'https://aerpaw-ci.renci.org/jenkins',
    username='admin',
    password='xxxxx'
)
jenkins_server._session.verify = False
