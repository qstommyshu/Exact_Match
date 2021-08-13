#Author: Tommy Shu
#Date: Aug 12, 2021

import time
import os
import PySimpleGUI as sg
import pandas as pd

supportedextensions = ['.csv']

layout = [
    [sg.Text('Select two CSV files to compare')],
    [sg.Text('File 1'), sg.InputText(), sg.FileBrowse()],
    [sg.Text('File 2'), sg.InputText(), sg.FileBrowse()],
    #Output box
    [sg.Output(size=(61, 5))],
    [sg.Submit('Proceed'), sg.Cancel('Exit')]
]

unified = {
    "CW GUID": "cwguid",
    "Identifier": "rid",
    "Risk Name": "name",
    "Entities": "rentity",
    "Date Identified": "dateid",
    "Risk Description": "desc",
    "What Can Go Wrong": "whatwrong",
    "Financial Statement Areas": "fsa",
    "Assertions": "assert",
    "Business Cycles": "bc",
    "Significant Risk Indicators": "sri",
    "Significant Risk": "significant",
    "Likelihood to Occur": "likelihood",
    "Monetary Impact": "m_impact",
    "Inherent Risk": "inherent",
    "Control Risk": "ctrl_r",
    "Potential RMM": "p_rmm",
    "Residual Risk": "residual",
    "RMM": "rmm",
    "Procedures Other Than Substantive": "procedures",
    "Management Response": "m_response",
    "Risk Treatment/Mitigation": "treatment",
    "Audit Response": "a_response",
    "Source/Reference": "source",
    "Addressed": "addressed",
    "Associated Controls": "assocd_ctrl",
    "Associated Reportable Items": "assocd_item",
    "Audit has properly addressed this risk": "aud_addressed",
    "Roll forward": "r_forward"
}

window = sg.Window('Compare CSV file', layout)
while True:    # The Event Loop
    event, values = window.read()
    # print(event, values)  # debug
    if event in (None, 'Exit', 'Cancel'):
        secondwindow = 0
        break

    elif event == 'Proceed':
        #define some flags
        file1_check = file2_check = is_ready = proceedwithfindcommonkeys = None
        file1, file2 = values[0], values[1]
        _, extension1 = os.path.splitext(file1)
        _, extension2 = os.path.splitext(file2)

        #Check file path and extensions
        #Both files are loaded
        if file1 and file2:
            file1_check = os.path.exists(file1) #Check if file path is valid
            file2_check = os.path.exists(file2)
            is_ready = 0 #This is just a Flag

            if extension1 in supportedextensions:
                #Both files extensions should be the same
                if extension1 == extension2:
                    #Can't be the same file
                    if file1 != file2:
                        is_ready = 1
                    else:
                        print('Error: The files need to be different')
                else:
                    print(f"First file extension is {extension1}") 
                    print(f"Second file extenstion is {extension2}")
                    print(f'Error: The two files have different file extensions. Please correct')
            else:
                print('Error: File format currently not supported. At the moment only CSV files are supported.')

            #Both files paths are valid
            if is_ready == 1:
                print('Info: Filepaths correctly defined.')
                try:
                    print('Info: Attempting to access files.')

                    df1, df2 = pd.read_csv(file1).rename(columns=unified), pd.read_csv(file2).rename(columns=unified)
                    df1_renamed = df1.reindex(sorted(df1.columns),axis=1)
                    df2_renamed = df2.reindex(sorted(df2.columns),axis=1)
                    print(all(df1_renamed.columns == df2_renamed.columns))

                    # time.sleep(100)
                    proceedwithfindcommonkeys = 1

                except IOError:
                    print("Error: File not accessible. You are probably using the file")
                    proceedwithfindcommonkeys = 0
                except UnicodeDecodeError:
                    print("Error: File includes a unicode character that cannot be decoded with the default UTF decryption.")
                    proceedwithfindcommonkeys = 0
                except Exception as e:
                    print('Error: ', e)
                    proceedwithfindcommonkeys = 0
        else:
            print('Error: Please choose 2 files.')

        if proceedwithfindcommonkeys == 1:
            formlists = [] #This will be the list to be displayed on the UI
            #Check columns

            if all(df1_renamed.columns == df2_renamed.columns):
                keyslist = list(df1_renamed.columns)
                secondwindow =1

            else:
                print('The column names are different in this two files, you probably selected the wrong files')
                secondwindow = 0

            window.close()
            break

#################################################
# First screen completed, moving on to second one
if secondwindow != 1:
    exit()

    #------------------------------------------------------------------need to optimize
#To align the three columns on the UI, we need the max len
#Note: This could be made better by having the max len of each column
maxlen = 0
for header in keyslist:
    if len(str(header)) > maxlen:
        maxlen = len(str(header))   #Get the longest length of headers
if maxlen > 25:
    maxlen = 25     #25 a good max display distance between each checkbox
elif maxlen < 10:
    maxlen = 15
#we need to split the keys to four columns
for index,item in enumerate(keyslist):
    if index == 0: i =0
    if len(keyslist) >= 4 and i == 0:
        formlists.append([
            sg.Checkbox(keyslist[i], size=(maxlen,None)),
            sg.Checkbox(keyslist[i+1], size=(maxlen,None)),
            sg.Checkbox(keyslist[i+2], size=(maxlen,None)),
            sg.Checkbox(keyslist[i+3], size=(maxlen,None))
            ])
        i += 4
    elif len(keyslist) > i:
        if len(keyslist) - i - 4>= 0:
            formlists.append([
                sg.Checkbox(keyslist[i], size=(maxlen,None)),
                sg.Checkbox(keyslist[i+1], size=(maxlen,None)),
                sg.Checkbox(keyslist[i+2], size=(maxlen,None)),
                sg.Checkbox(keyslist[i+3], size=(maxlen,None))
                ])
            i += 4
        elif len(keyslist) - i - 3>= 0:
            formlists.append([
                sg.Checkbox(keyslist[i], size=(maxlen,None)),
                sg.Checkbox(keyslist[i+1], size=(maxlen,None)),
                sg.Checkbox(keyslist[i+2], size=(maxlen,None))])
            i += 3
        elif len(keyslist)- i - 2>= 0:
            formlists.append([
                sg.Checkbox(keyslist[i], size=(maxlen,None)),
                sg.Checkbox(keyslist[i+1], size=(maxlen,None))])
            i += 2
        elif len(keyslist) - i - 1>= 0:
            formlists.append([sg.Checkbox(keyslist[i], size=(maxlen,None))])
            i += 1
        else:
            sg.Popup('Error: Uh-oh, something\'s gone wrong!')
    
#The second UI
layout2 = [
    [sg.Text('File 1'), sg.InputText(file1,disabled = True, size = (75,2))],
    [sg.Text('File 2'), sg.InputText(file2,disabled = True, size = (75,2))],
    # [sg.Text('Select the data key for the comparison:')],
    [sg.Frame(
        layout=[*formlists],
        title = 'Select what column(s) do you want to sort them by?(More columns take more time)',
        relief=sg.RELIEF_RIDGE #Checkbox selection
    )],
    [sg.Output(size=(maxlen*6, 20))],  #The info box
    [sg.Submit('Compare'), sg.Cancel('Exit')]
]

#----------------------------------------------------jump to here---------------------------------------------
window2 = sg.Window('File Compare', layout2)
datakeydefined = 0
definedkey = []
while True:  # The Event Loop
    event, values = window2.read()
    # print(event, values)  # debug
    if event in (None, 'Exit', 'Cancel'):
        break
    elif event == 'Compare':
        definedkey.clear()
        file1_check = file2_check = is_ready = None
        # print('Event', event, '\n', 'Values', values)
        for index, value in enumerate(values):
            if index not in [0,1]:
                if values[index] == True: 
                    datakeydefined = 1
                    definedkey.append(keyslist[index-2])
            # print(index, values[index],definedkey)
        #------------------------------------------------------------------------------------
        if len(definedkey) > 0:
            df1_sorted = df1.sort_values(by=definedkey)
            df2_sorted = df2.sort_values(by=definedkey)
            if len(df1_sorted) == len(df2_sorted):
                if df1_sorted.equals(df2_sorted):
                    print('The data in the two CSV files are exactly the same')
                else:
                    print('The data row numbers are the same, but there are differences in the data.')
                    print('Please compare them manaully')
                    print('The sorted version of the two files are downloaded to the current directory')

                    # print(df1_renamed.columns)
                    # print(df2_renamed.columns)
                    # print(all(df2_renamed.columns == df1_renamed.columns))
                    # print(keyslist,'\n\n') They are exactly the same
                    # print(list(df1_renamed.columns))
                    file1_name = (values[0].split('/'))[-1]
                    file2_name = (values[1].split('/'))[-1]
                    #Output sorted df as csv
                    df1_sorted.to_csv(f"Sorted_{file1_name}",  index=False)
                    df2_sorted.to_csv(f"Sorted_{file2_name}",  index=False)
            else:
                print('The number of rows of this two files are different') 
                print('There is no chance the data are equal')
        else:
            print('Error: You need to select at least one attribute as a data key')
