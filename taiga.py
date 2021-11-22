import os
import json
import time
from github import Github


class User_story():
    def __init__(self, ref, subject, owner, created, desc = None, labels = None,
                 assigned_to = None, finish = None, closed = None, comments = None):
        self.ref = ref
        self.subject = subject
        self.owner = owner
        self.created = created
        self.description = desc
        self.labels = labels
        self.assigned_to = assigned_to
        self.finish = finish
        self.closed = closed
        self.comments = comments    

git = Github('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') # Enter GitHub token
repo = git.get_repo('BenCapper/taiga-stories') # Enter GitHub namespace
t = open('fedora_iot.json') # Enter json file
taiga_export = json.load(t)
user_stories = taiga_export["user_stories"]
count = 0
ref_list = []
if os.path.exists('done.temp'): # done.temp keeps track of already created issues in case of fail / stop
    open_temp = open('done.temp', 'r')
    read_temp = open_temp.read()
    ref_list = read_temp.splitlines()
else:
    os.mknod('done.temp')
for story in user_stories:
    ref = story['ref']
    comments = []
    user = User_story(story['ref'],story['subject'],story['owner'].split('@')[0],story['created_date'][:-5],
                    story['description'],story['tags'],story['assigned_users'],story['finish_date'],
                    story['is_closed'],comments)
    if str(ref) not in ref_list: # Reference num isn't in list, create the issue
        ref_list.append(ref)
        open_temp = open('done.temp', 'a')
        for history in story['history']:
            if history['comment'] == '':
                pass
            else:
                details = [history['user'][0].split('@')[0], history['comment'], history['created_at']]
                user.comments.append(details)
        count += 1
        repo.create_issue(title=user.subject, body="On " + user.created[0:10] + " at " + user.created[11:]  
                        + ", **" + user.owner + "**" + " said: \n\n" + user.description, labels=user.labels)
        time.sleep(10) # Avoids hitting GitHub secondary rate limits
        issue = repo.get_issue(count) # Must be a fresh board to start (Taiga user story ref doesn't match GitHub issue No.)

        if user.closed is True:
            issue.edit(state='closed')
        else:
            issue.edit(state='open')
        if user.comments == []:
            pass
        else:
            for comm in user.comments:
                issue.create_comment("On " + comm[2][0:10] + " at " + comm[2][11:-5] + ", **" + comm[0] + "**" + " said: \n\n" + comm[1])
                time.sleep(10)
        open_temp.write(str(ref) + '\n')
        print("\nUSER == \nREF: ", user.ref, "\nSUBJECT == ", user.subject,
             "\nOWNER == ", user.owner, "\nCREATED == ", user.created, "\nDESCRIPTION == ", user.description, 
            "\nLABELS == ", user.labels, "\nASSIGNED_TO == ", user.assigned_to,
             "\nFINISH == ", user.finish, "\nCLOSED == ", user.closed, "\nCOMMENTS == ", user.comments, "\n\n\n\n")
    if str(ref) in ref_list: 
        pass