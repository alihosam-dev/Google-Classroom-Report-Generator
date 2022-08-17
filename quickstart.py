from __future__ import print_function
from mmap import PAGESIZE

import os.path
from unicodedata import name

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/classroom.courses.readonly', 'https://www.googleapis.com/auth/classroom.coursework.students', 'https://www.googleapis.com/auth/classroom.rosters']


def mainprog():
    if True: # Everything that's not classroom api
        creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('classroom', 'v1', credentials=creds)

        # Call the Classroom API
        courses = service.courses().list(pageSize=10).execute().get('courses', [])
        courselist = []
        for course in courses:
            courselist.append(course)
        maindict = {
            'courselist': courselist}

        return maindict

    except HttpError as error:
        print('An error occurred: %s' % error)

def getAssignments(courseId):
    if True: # everything that's not classroom api
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
    
    try:
        service = build('classroom', 'v1', credentials=creds)

        # Call the Classroom API

        assignments = service.courses().courseWork().list(courseId=courseId).execute().get('courseWork', [])
        students = service.courses().students().list(courseId=courseId).execute().get('students', [])
        assignmentlist = []
        studentlist = []
        for assignment in assignments:
            assignmentlist.append(assignment)
        for student in students:
            studentlist.append(student['profile'])
        assignments_students_dict = {
            'assignments':assignmentlist,
            'students':studentlist
        }          
        return assignments_students_dict

    except HttpError as error:
        print('An error occurred: %s' % error)

def getSubmission(courseId, studentId):
    if True: # everything that's not classroom api
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
    
    try:
        service = build('classroom', 'v1', credentials=creds)

        # Call the Classroom API

        submissions = service.courses().courseWork().studentSubmissions().list(courseId=courseId, userId=studentId, courseWorkId = '-').execute().get('studentSubmissions', [])
        
        submissionList = []
        for submission in submissions:
            submissionList.append(submission)
        return submissionList

    except HttpError as error:
        print('An error occurred: %s' % error)
