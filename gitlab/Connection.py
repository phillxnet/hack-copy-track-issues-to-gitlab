import json
import requests
import sys

__author__ = 'jens'


class Connection(object):
    """
    Connection to the gitlab API
    """

    def __init__(self, url, access_token):
        """

        :param url: "https://www.neuhalfen.name/gitlab/api/v3"
        :param access_token: "secretsecretsecret"
        """
        self.url = url
        self.access_token = access_token

    def milestone_by_name(self, project_id, milestone_name):
        milestones = self.get("/projects/:project_id/milestones",project_id=project_id)
        for milestone in milestones:
            if milestone['title'] == milestone_name:
                return milestone

    def project_by_name(self, project_name):
        projects = self.get("/projects")
        for project in projects:
            if project['path_with_namespace'] == project_name:
                return project

    def get(self, url_postfix, **keywords):
        return self._get(url_postfix, keywords)

    def _get(self, url_postfix, keywords):
        """
        :param url_postfix: e.g. "/projects/:id/issues"
        :param keywords:  map, e.g. { "id" : 5 }
        :return: json of GET
        """
        completed_url = self._complete_url(url_postfix, keywords)
        r = requests.get(completed_url + "&per_page=100", verify=False)
        json = r.json()
        return json

    def put(self, url_postfix, data, **keywords):
        completed_url = self._complete_url(url_postfix, keywords)
        r = requests.put(completed_url,data= data, verify=False)
        j = r.json()
        return j

    def put_json(self, url_postfix, data, **keywords):
        completed_url = self._complete_url(url_postfix, keywords)
        payload = json.dumps(data)
        r = requests.put(completed_url, payload, verify=False)
        j = r.json()
        return j

    def post_json(self, url_postfix, data, **keywords):
        completed_url = self._complete_url(url_postfix, keywords)
        payload = json.dumps(data)
        r = requests.post(completed_url, data=data, verify=False)
        j = r.json()
        return j

    def create_issue(self, dest_project_id, new_ticket):
        return self.post_json("/projects/:id/issues", new_ticket, id=dest_project_id)

    def create_milestone(self, dest_project_id, milestone_info):
    	new_milestone_data = {
        	"title" : milestone_info['title'],
        	"description" : milestone_info['description'],
        	"due_date" : milestone_info['due_date']
        }
        self.post_json("/projects/:id/milestones", new_milestone_data, id=dest_project_id)

    def comment_issue(self,project_id,ticket_id, body):
        new_note_data = {
            "id" : project_id,
            "issue_id" :ticket_id,
            "body" : body
        }
        self.post_json( "/projects/:project_id/issues/:issue_id/notes", new_note_data, project_id=project_id, issue_id=ticket_id)


    def set_issue_milestone(self,project_id,ticket_id,milestone_id):
        new_note_data = {"milestone" : milestone_id}
        print >>sys.stderr, "\nSetting issue milestone for: %s\n" % (milestone_id)
        self.put("/projects/:project_id/issues/:issue_id", new_note_data, project_id=project_id, issue_id=ticket_id)

    def close_issue(self,project_id,ticket_id):
        #new_note_data = "closed=1"
        new_note_data = {"state_event": "close"}
        self.put("/projects/:project_id/issues/:issue_id", new_note_data, project_id=project_id, issue_id=ticket_id)

    def _complete_url(self, url_postfix, keywords):
        url_postfix_with_params = self._url_postfix_with_params(url_postfix, keywords)
        complete_url = "%s%s?private_token=%s" % (self.url, url_postfix_with_params, self.access_token)
        return complete_url

    def _url_postfix_with_params(self, url_postfix, keywords):
        """

        :param url_postfix:  "/projects/:id/issues"
        :param keywords:  map, e.g. { "id" : 5 }
        :return:  "/projects/5/issues"
        """

        result = url_postfix
        for key, value in keywords.iteritems():
            k = ":" + str(key)
            v = str(value)
            result = result.replace(k, v)
        return result
