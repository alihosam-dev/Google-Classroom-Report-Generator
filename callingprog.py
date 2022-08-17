

from quickstart import mainprog, getAssignments, getSubmission
from programgui import findCourse, listAssignments, listStudents

coursedict = mainprog()
programguireturn = findCourse(coursedict)
if programguireturn == 'Error, classroom and save location not chosen':
    import sys
    print('Error, classroom and save location not chosen')
    sys.exit()
courseId = programguireturn[0] 
folder_url = programguireturn[1]

assignment_student_dict = getAssignments(courseId)
assignmentlist = assignment_student_dict['assignments']
# assignments_chosen = listAssignments(assignmentlist)
studentlist = assignment_student_dict['students']
studentId = listStudents(studentlist)
k= 0
# for assignment in assignmentlist:
#     if assignment['title'] == assignments_chosen:
#         break
#     else:
#         del(assignmentlist[k])
#     k+=1

studentnames = []
assignments = []
studentscore = []
overallscores = []
states = []
student_counter = 0
assignment_counter = len(assignmentlist)

for student in studentlist:
    student_counter+=1


class Student:
    def __init__(self, studentId, name):
        self.StudentID = studentId
        self.StudentName = name
        self.Assignments = [] * assignment_counter
        self.AssignmentStates = [] * assignment_counter
        self.StudentScores = [] * assignment_counter
        
    def addtoScore(self, score):
        self.StudentScores.append(score)

    def addToAssignments(self, assignment):
        self.Assignments.append(assignment)

    def setState(self, state):
        self.AssignmentStates.append(state)

students = []
courseworkIds = []

# for assignment in assignmentlist:
#     courseworkIds.append(assignment['id'])
# for submission in submissionlist:
#     if submission['courseWorkId'] not in courseworkIds:
#             del(submission)

j=0

for student in studentlist:
    studentId = student['id']
    studentnames.append(student['name']['fullName'])
    submissionlist = getSubmission(courseId, studentId)
    for submission in submissionlist:
        for assignment in assignmentlist:
            if assignment['id'] == submission['courseWorkId']:
                assignments.append(assignment['title'])
                assignment_max = assignment['maxPoints']
                assignmentid = assignment['id']
                state = submission['state']
                if state == 'RETURNED':
                    state = 'Marked'
                else:
                    state = "Not Submitted"
                states.append(state)
                if submission['userId'] == studentId and state == 'Marked':
                    userscore = f"{submission['assignedGrade']}/{assignment_max}"
                    studentscore.append(userscore)
                    break
                if state != 'Marked':
                    userscore = 'NA'
                    studentscore.append(userscore)

                    break
                else:
                    continue
            else:
                continue
    students.append((Student(student['id'], student['name']['fullName'])))
    students[j].addtoScore(studentscore)
    students[j].addToAssignments(assignments)
    students[j].setState(states)
    studentscore = []
    assignments = []
    states = []
    j+=1


        
import pandas as pd
data = []
sheets = []
for studentc in range(student_counter):
    for assc in range(assignment_counter):
        mlist = [students[studentc].StudentName, students[studentc].Assignments[0][assc], students[studentc].AssignmentStates[0][assc], students[studentc].StudentScores[0][assc]]
        data.append(mlist)
    df = (pd.DataFrame(data, columns=("Name", "Assignment", "Submit Status", "Score")))
    df.index = range(1, df.shape[0] + 1)
    sheets.append(df)
    data  = []

j=1
for sheet in sheets:
    sheet_name = sheet.iat[0,0]
    sheet.drop('Name', inplace=True, axis=1)
    html = sheet.to_html(index=False)
    text_file = open(f"{folder_url}/index{j}.html", "w")
    text_file.write(html)
    text_file.close()

    if True: # Linking style sheet and adding name title to html
        a = '''
        <style>
    html,
    tbody {
    height: 100%;
    }
    tbody {
    margin: 0;
    background: linear-gradient(45deg, #49a09d, #5f2c82);
    font-family: sans-serif;
    font-weight: 100;
    }
    .container {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    }
    table {
    width: 800px;
    border-collapse: collapse;
    overflow: hidden;
    box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
    }
    th,
    td {
    padding: 15px;
    background-color: rgba(255, 255, 255, 0.2);
    color: #fff;
    }
    th {
    text-align: left;
    }
    thead th {
    background-color: #55608f;
    }
    tbody tr:hover {
    background-color: rgba(255, 255, 255, 0.3);
    }
    tbody td {
    position: relative;
    }
    tbody td:hover:before {
    content: "";
    position: absolute;
    left: 0;
    right: 0;
    top: -9999px;
    bottom: -9999px;
    background-color: rgba(255, 255, 255, 0.2);
    z-index: -1;
    }
</style>
        '''
        with open(f"{folder_url}/index{j}.html", 'r+') as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                if line.startswith('  <thead>'):   # find a pattern so that we can add next to that line
                    lines[i] = lines[i+1]+a
            f.truncate()
            f.seek(0)                                           # rewrite into the file
            for line in lines:
                f.write(line)

        b = f"    <tbody>\n     <h1 style='text-align:left;font-family:sans-serif;color:white;text-shadow:-1px -1px 0 #000000,1px -1px 0 #000000,-1px 1px 0 #000000,1px 1px 0 #000000,  -2px 0 0 #000000,2px 0 0 #000000,0 2px 0 #000000,0 -2px 0 #000000;'>{sheet_name} Report</h1>\n"
        with open(f"{folder_url}/index{j}.html", 'r+') as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                if line.startswith('  <tbody>'):   # find a pattern so that we can add next to that line
                    lines[i] = lines[i+1]+b
            f.truncate()
            f.seek(0)                                           # rewrite into the file
            for line in lines:
                f.write(line)  


    from html2image import Html2Image
    hti = Html2Image(output_path=f'{folder_url}')
    hti.screenshot(
    html_file=f'{folder_url}/index{j}.html', save_as=f'{sheet_name} Report.jpg'
)


    from PIL import Image
    import numpy as np
    image=Image.open(f'{folder_url}/{sheet_name} Report.jpg')
    image.load()
    image_data = np.asarray(image)
    image_data_bw = image_data.max(axis=2)
    non_empty_columns = np.where(image_data_bw.max(axis=0)>0)[0]
    non_empty_rows = np.where(image_data_bw.max(axis=1)>0)[0]
    cropBox = (min(non_empty_rows), max(non_empty_rows), min(non_empty_columns), max(non_empty_columns))
    image_data_new = image_data[cropBox[0]:cropBox[1]+1, cropBox[2]:cropBox[3]+1 , :]
    new_image = Image.fromarray(image_data_new)
    new_image.save(f'{folder_url}/{sheet_name} Report.png')
    import os
    os.remove(f'{folder_url}/{sheet_name} Report.jpg')
    os.remove(f'{folder_url}/index{j}.html')

    
    

    
    
    j+=1    
import os
import platform
import subprocess

def open_file(path):
    if platform.system() == "Windows":
        os.startfile(path)
    elif platform.system() == "Darwin":
        subprocess.Popen(["open", path])
    else:
        subprocess.Popen(["xdg-open", path])

open_file(folder_url)
