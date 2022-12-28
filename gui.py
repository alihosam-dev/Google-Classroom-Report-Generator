# Imports
from tkinter.font import BOLD
import PySimpleGUI as psg
import os

def FindUserCourse(courses): # Returns list with course id of course chosen and folder to store files - called from callingprog.py - takes coursedict as param.
    
    coursenames = [ course['name'] for course in courses] # list comprehension to get all course names
    

    if True: # PySimpleGUI code to input from the user the course and where to store the files
        import PySimpleGUI as psg
        psg.theme("darkblue14")
        left_col = [[psg.Text('Choose Folder to save student reports to:', font=('Inter', 20))],
        [psg.In(size=(40,2), enable_events=True ,key='-FOLDER-', font=('Inter', 15)), psg.FolderBrowse(size=(6, 1),font=('Inter', 16))]]
        layout = [
            [psg.Text("Please choose the classroom to retreive student data from:", font=('Inter', 20))],
            [psg.Combo(coursenames, font=('Inter', 15), default_value=coursenames[0])],
            [[psg.Column(left_col, element_justification='l')],
            [psg.Button("Submit", font=('Inter', 16)),
            psg.Button("Close", font=('Inter', 16))]],
            [psg.Button("Sign out", font=('Inter', 16))],
            [psg.Text("© 2023 Ali Hosam - Classroom Report Generator", font=('Inter', 14))]
                ]
        window = psg.Window("Classroom Report Generator", layout, size=(650, 270))
        while True:
            event, values = window.read()
            if event == psg.WIN_CLOSED or event == "Close":
                return "Error, classroom and save location not chosen"
            if event == '-FOLDER-':
                folder = values['-FOLDER-']
            if event == "Submit":
                print(f"Classroom chosen: {values[0]}")
                folder = values['-FOLDER-']
                if os.path.exists(folder) == False:
                    psg.Popup('Error: Please enter or select a valid folder', keep_on_top=True, text_color='yellow', font=('Inter', 20))
                    continue  
                break
            elif event == 'Sign out':
                if os.path.exists('token.json'):
                    os.remove('token.json')
                    psg.Popup('Signed out successfully. Please restart the app', keep_on_top=True, text_color='yellow', font=('Inter', 20))
                    import sys
                    sys.exit()
                else:
                    psg.Popup('Error: You are not signed in.', keep_on_top=True, text_color='yellow', font=('Inter', 20))
                    
        window.close()
    coursename_chosen = values[0]
    for course in courses: # Returns list, with the course chosen and the folder to store the files
        if course['name'] != coursename_chosen:
            continue
        else:
            course_chosen = course['id']
            returnvalue = [course_chosen, folder]
            return returnvalue

def gui_layout(assignmentlist): # PSG layout with checkboxes to obtain assignments to be in report from user (is called by newassignmentlist) 
    oll_list_frame = [
        [psg.Text(" ", key="unused1", font=('Inter', 20))]
    ]

    for i in assignmentlist:
        oll_list_frame.append([psg.Checkbox((i)['title'], key=('-CB-', i['title']), enable_events=True, font=('Inter', 14))])

    column = [[psg.Frame("", oll_list_frame)]]
    

    layout = [
        [psg.Text("Select Assignments to include in the report:", font=('Inter', 15))],
        [psg.Column(column, scrollable=True, vertical_scroll_only=True,
        size=(270+16, 129*2), key='COLUMN')],
        [psg.Text("Check the box if you would like to include student marks: ", key="unused1", font=('Inter', 15))],
        [psg.Checkbox(text='',default=True, key="-IN-")],
         [psg.Button("Submit", font=('Inter', 16))], 
    [psg.Text("© 2023 Ali Hosam - Classroom Report Generator", font=('Inter', 14))]]

    return psg.Window("Assignment selection", layout=layout, finalize=True, use_default_focus=False)

def control_loop(assignmentlist): # PSG adding fucntionality to gui_layout() (is called by newassignmentlist)
    psg.theme("darkblue14")
    window = gui_layout(assignmentlist)

    returnvalue = []
    newassignments = []
    while True:
        event, values = window.read()
        if event in (psg.WIN_CLOSED, "Exit"):
            break
        elif event == "Submit":
            if len(newassignments) == 0:
                psg.Popup('Error: Please select at least one assignment', keep_on_top=True, text_color='yellow', font=('Inter', 20, BOLD))
            else:
                returnvalue.append(newassignments)
                if values["-IN-"] == True:
                    print("Scores shown")
                    returnvalue.append(values["-IN-"])
                if values["-IN-"] == False:
                    print("Scores not shown")
                    returnvalue.append(values["-IN-"])
                return returnvalue
            

        print(event)    # check what key each checkbox has by clicking on it
        if event[0] == '-CB-':
            checkbox_num = event[1]
            if checkbox_num in newassignments:
                newassignments.remove(checkbox_num)
            else:
                newassignments.append(checkbox_num)

    window.close()

def newassignmentlist(assignmentlist): # PSG final, takes from control_loop the new list of assignments and returns the modified list to controlprog.py
    final_list = []
    returnval = []
    returnedvalue = control_loop(assignmentlist)
    newassignments = returnedvalue[0]
    m = 0
    for assignment in assignmentlist:
        if assignment['title'] in newassignments:
            final_list.append(assignment)
        m+=1
    returnval = [final_list, returnedvalue[1]]
    return returnval
      
def listStudents(studentlist): # Parses studentids from the student list obtained from the quickstart.py file and passed from callingprog.py, returns to calingprog.py
    for student in studentlist:
        return student['id']




