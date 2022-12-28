from __future__ import print_function

if True: # Google authentication parts
    
    # Imports 

    import os.path
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError

    # Scopes
    # When modifying scopes, delete the token.json file
    SCOPES = ['https://www.googleapis.com/auth/classroom.courses.readonly', 'https://www.googleapis.com/auth/classroom.coursework.students', 'https://www.googleapis.com/auth/classroom.rosters']


def GetCourses() -> list: # Returns list of courses - called from main.py
    if True: # Everything that's not classroom api (Obtains token.json file and updates credentials, saves token if it's just been created)
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
                    'ccredentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

    try: # Main part, returns list of courses by using list method
        service = build('classroom', 'v1', credentials=creds)

        # Call the Classroom API
        # courses = service.courses().list(pageSize=10).execute().get('courses', [])
        # courselist = []
        # for course in courses:
        #     courselist.append(course)
        # maindict = {
        #     'courselist': courselist}
        return service.courses().list(pageSize=10).execute().get('courses', [])

        # return maindict

    except HttpError as error: # Error exception (just in case...)
        print('An error occurred: %s' % error)

def getAssignments(courseId): # Returns assignments and list of students - called from callingprog.py - uses courseId param.
    if True: # Everything that's not classroom api (This has to be used again as we're re-building the classroom api)
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

    try: # Main part, returns dictionary of list of assignments and list of students using list methods for each respective class
        service = build('classroom', 'v1', credentials=creds)

        # Call the Classroom API

        assignments = service.courses().courseWork().list(courseId=courseId).execute().get('courseWork', [])
        students = service.courses().students().list(courseId=courseId).execute().get('students', [])
        studentlist = []
        for student in students:
            studentlist.append(student['profile'])
        
        assignments_students_dict = {
            'assignments':assignments,
            'students':studentlist
        }          
        return assignments_students_dict

    except HttpError as error: # Error handling
        print('An error occurred: %s' % error)

def getSubmission(courseId, studentId): # Returns list of submissions for a student - called multiple timnes from callingprog.py - uses courseId and studentId param.
    if True: # Everything that's not classroom api (This has to be used again as we're re-building the classroom api)
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

        return service.courses().courseWork().studentSubmissions().list(courseId=courseId, userId=studentId, courseWorkId = '-').execute().get('studentSubmissions', [])
        

    except HttpError as error: # Error handling
        print('An error occurred: %s' % error)
