# Imports 
from api_methods import GetCourses, getAssignments, getSubmission
from gui import FindUserCourse, newassignmentlist, listStudents

courses = GetCourses() # Gets list of courses
programguireturn = FindUserCourse(courses) # Returns list with course id of course chosen and folder to store files as element 0 and element 1 respectively
if programguireturn == 'Error, classroom and save location not chosen': # Error handling when user presses close in first window
    import sys
    print('Error, classroom and save location not chosen')
    sys.exit()

courseId = programguireturn[0] # Parsing list programguireturn to obtain just the courseId
folder_url = programguireturn[1] # Parsing list with programguireturn to obtain just the folder to store the files

assignment_student_dict = getAssignments(courseId) #  Returns assignments and list of students in dict
assignmentlist = assignment_student_dict['assignments'] # Parses dict to obtain just the assignments
studentlist = assignment_student_dict['students']  # Parses dict to obtain just the students
pyguival = newassignmentlist(assignmentlist) # Filters assignments to just the ones the user chose in the second window
assignmentlist = pyguival[0] # Filters assignments to just the ones the user chose in the second window
scores_shown = pyguival[1]
studentId = listStudents(studentlist) # Gets student ids 


if True: # Initialising lists to use when making each submission
    studentnames = []
    assignments = []
    studentscore = []
    overallscores = []
    students = [] 
    courseworkIds = []
    states = []

# Getting number of assignments and number of students for loop to make pandas database later
assignment_counter = len(assignmentlist)
student_counter = len(studentlist)


class Student: # Storing all details for one student in a class, is used when making pandas database
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




j=0
for student in studentlist: # Loop to make a student class for each student and their submissions to each assignment
    studentId = student['id']
    studentnames.append(student['name']['fullName'])
    submissionlist = getSubmission(courseId, studentId)
    for submission in submissionlist:
        for assignment in assignmentlist:
            if assignment['id'] == submission['courseWorkId']:
                assignments.append(assignment['title'])
                try:
                    assignment_max = assignment['maxPoints']
                except KeyError:
                    assignment_max = 0
                assignmentid = assignment['id']
                state = submission['state']
                if state == 'RETURNED':
                    state = 'Marked'
                elif state =='TURNED_IN':
                    state = 'Submitted'
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

    # Making the class and using its methods to create the student 
    students.append((Student(student['id'], student['name']['fullName'])))
    students[j].addtoScore(studentscore)
    students[j].addToAssignments(assignments)
    students[j].setState(states)
    studentscore = []
    assignments = []
    states = []
    j+=1 

# Creating pandas dataframe for each student, and adding each one to a list      
import pandas as pd
data = []
sheets = []
dfs = []
for studentc in range(student_counter):
    for assignc in range(assignment_counter):
        mlist = [students[studentc].StudentName, students[studentc].Assignments[0][assignc], students[studentc].AssignmentStates[0][assignc], students[studentc].StudentScores[0][assignc]]
        if scores_shown == False:
            mlist.pop()
        data.append(mlist)
    if scores_shown == False:
        df = (pd.DataFrame(data, columns=("Name", "Assignment", "Submit Status")))
    else:
        df = (pd.DataFrame(data, columns=("Name", "Assignment", "Submit Status", "Score")))
    df.index = range(1, df.shape[0] + 1)
    sheets.append(df)
    data  = []
    dfs.append(df)
merged_df = pd.concat(dfs)
merged_df.to_excel(f"{folder_url}/TotalReport.xlsx")

# Creating html file for each student, containing their data frame converted to an html table
j=1
for sheet in sheets:
    sheet_name = sheet.iat[0,0]
    sheet.drop('Name', inplace=True, axis=1)
    html = sheet.to_html(index=False)
    text_file = open(f"{folder_url}/index{j}.html", "w")
    text_file.write(html)
    text_file.close()

    if True: # Adding style attribute and adding name title to html
        a = '''
         <style>
         table { 
	width: 750px; 
	border-collapse: collapse; 
	}

/* Zebra striping */
tr:nth-of-type(odd) { 
	background: #eee;
    font-family: Arial;
	}
tr:nth-of-type(even){
    background: #cccccc;
    font-family: Arial;
}

th { 
	background: #000000; 
	color: white; 
	font-weight: bold; 
    font-family: Verdana;
	}

td, th { 
	padding: 10px; 
	border: 1px solid #ccc; 
	text-align: left; 
	font-size: 18px;
	}

/* 
Max width before this PARTICULAR table gets nasty
This query will take effect for any screen smaller than 760px
and also iPads specifically.
*/
@media 
only screen and (max-width: 760px),
(min-device-width: 768px) and (max-device-width: 1024px)  {

	table { 
	  	width: 100%; 
	}

	/* Force table to not be like tables anymore */
	table, thead, tbody, th, td, tr { 
		display: block; 
	}
	
	/* Hide table headers (but not display: none;, for accessibility) */
	thead tr { 
		position: absolute;
		top: -9999px;
		left: -9999px;
	}
	
	tr { border: 1px solid #ccc; }
	
	td { 
		/* Behave  like a "row" */
		border: none;
		border-bottom: 1px solid #eee; 
		position: relative;
		padding-left: 50%; 
	}

	td:before { 
		/* Now like a table header */
		position: absolute;
		/* Top/left values mimic padding */
		top: 6px;
		left: 6px;
		width: 45%; 
		padding-right: 10px; 
		white-space: nowrap;
		/* Label the data */
		content: attr(data-column);

		color: #3498db;
		font-weight: bold;
	}

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



    # converting Html file to a jpg
    from html2image import Html2Image
    hti = Html2Image(output_path=f'{folder_url}')
    hti.screenshot(
    html_file=f'{folder_url}/index{j}.html', save_as=f'{sheet_name} Report.jpg'
)


    if True: # Converting the image to an array, and cropping it so there isn't a lot of white space
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
    new_image.save(f'{folder_url}/{sheet_name} Report.png') # Converting it to a png
    import os
    os.remove(f'{folder_url}/{sheet_name} Report.jpg') # Removing old jpg file
    os.remove(f'{folder_url}/index{j}.html') # Removing old html file

    j+=1 # Incrementing index for loop, next iteration = next student
    


# Opening folder where user stored their files on the screen (cross-platform)
import platform
import subprocess
def open_file(path):
    if platform.system() == "Windows":
        os.startfile(path)
    elif platform.system() == "Darwin":
        subprocess.Popen(["open", path])
    else:
        subprocess.Popen(["xdg-open", path])

open_file(folder_url) # Calling the open_file method with the user folder as a the parameter
