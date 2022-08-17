from email.policy import default
import PySimpleGUI as psg
def findCourse(coursedict):
    courses = coursedict['courselist']
    coursenames = []
    for course in courses:
        coursenames.append(course['name'])

    if True: # PySimpleGUI code to input from the user the course
        import PySimpleGUI as psg
        psg.theme("default1")
        left_col = [[psg.Text('Choose Folder to save student reports to:', font=('Arial', 15))],
        [psg.In(size=(25,1), enable_events=True ,key='-FOLDER-', font=('Arial', 15)), psg.FolderBrowse()]]
        layout = [[psg.Text("Please choose the classroom to retreive student data from:", font=('Arial', 15))],
                [psg.Combo(coursenames, font=('Arial', 15), default_value=coursenames[0])],
                [[psg.Column(left_col, element_justification='l')],
                [psg.Button("Submit", font=('Arial', 16)),
                psg.Button("Close", font=('Arial', 16))]
                ]]
        window = psg.Window("Classroom Report Generator", layout)
        while True:
            event, values = window.read()
            if event == psg.WIN_CLOSED or event == "Close":
                return "Error, classroom and save location not chosen"
            if event == '-FOLDER-':
                folder = values['-FOLDER-']  
            elif event == "Submit":
                print(f"Classroom chosen: {values[0]}")
                break
        window.close()
    coursename_chosen = values[0]
    for course in courses:
        if course['name'] != coursename_chosen:
            continue
        else:
            course_chosen = course['id']
            returnvalue = [course_chosen, folder]
            return returnvalue



def listAssignments(assignmentlist):
    assignmentids = []
    assignmentnames = []
    for assignment in assignmentlist:
        assignmentids.append(assignment['id'])
        assignmentnames.append(assignment['title'])
    if True: # PySimpleGUI code to input from the user the course
        import PySimpleGUI as psg
        psg.theme("default1")
        layout = [[psg.Text("Please choose the first assignment to be in the:", font=('Arial', 15))],
        [psg.Combo(assignmentnames, font=('Arial', 15), default_value=assignmentnames[-1])],
        [psg.Button("Submit", font=('Arial', 16)),
        psg.Button("Close", font=('Arial', 16))]]
        window = psg.Window("Classroom Report Generator", layout)
        while True:
            event, values = window.read()
            if event == psg.WIN_CLOSED or event == "Close":
                break
            elif event == "Submit":
                print(f"Assignment chosen: {values[0]}")
                break
        window.close()
    assignment_chosen = values[0]
    return assignment_chosen
    
    
        
    
def listStudents(studentlist):
    for student in studentlist:
        return student['id']




