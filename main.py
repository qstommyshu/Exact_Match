#csv comparator
#Author: Tommy Shu
#Date: Aug 12, 2021

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
}

window = sg.Window('Compare CSV file', layout)
#Event loop one
while True:    # The Event Loop
    event, values = window.read()
    # print(event, values)  # debug
    if event in (None, 'Exit', 'Cancel'):
        secondwindow = 0
        break

    elif event == 'Proceed':

        file1, file2 = values[0], values[1]
        _, extension1 = os.path.splitext(file1)
        _, extension2 = os.path.splitext(file2)

        #Check file path and extensions
        #Both files are loaded
        if file1 and file2:
            file1_check = os.path.exists(file1) #Check if file path is valid
            file2_check = os.path.exists(file2)

            if extension1 in supportedextensions:
                #Both files extensions should be the same
                if extension1 == extension2:
                    #Can't be the same file
                    if file1 != file2:
                        print('Info: Filepaths correctly defined.')

                        try:
                            print('Info: Attempting to access files.')

                            df1, df2 = pd.read_csv(file1).rename(columns=unified), pd.read_csv(file2).rename(columns=unified)
                            df1_renamed = df1.reindex(sorted(df1.columns),axis=1)
                            df2_renamed = df2.reindex(sorted(df2.columns),axis=1)

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

                        except IOError:
                            print("Error: File not accessible. You are probably using the file")
                        except UnicodeDecodeError:
                            print("Error: File includes a unicode character that cannot be decoded with the default UTF decryption.")
                        except Exception as e:
                            print('Error: ', e)

                    #Check the line connect elses and ifs to quickly know which else is this is associate with
                    else:
                        print('Error: The files need to be different')
                else:
                    print(f"First file extension is {extension1}") 
                    print(f"Second file extenstion is {extension2}")
                    print(f'Error: The two files have different file extensions. Please correct')
            else:
                print('Error: File format currently not supported. At the moment only CSV files are supported.')
        else:
            print('Error: Please choose 2 files.')


#################################################
# First screen completed, moving on to second one
if secondwindow != 1:
    exit()

    #------------------------------------------------------------------need to optimize
#To align the three columns on the UI, we need the max len
#Note: This could be made better by having the max len of each column
maxlen = max(map(len, keyslist), default=15) #Get the longest length of headers, the minimum length is 15
maxlen = min(25, maxlen)


current = 0
buffer = []
#Every while access one element in the keyslist
while current < len(keyslist):
    buffer.append(keyslist[current])
    current += 1
    if len(buffer) == 4 or current == len(keyslist):
        #Append buffer in group of four to formlists
        formlists.append([sg.Checkbox(key, size=(maxlen, None)) for key in buffer])
        buffer.clear()

#----------------------------------------------------------------------------------------------------------
def IButton(*args, **kwargs):
    return sg.Col([[sg.Button(*args, **kwargs,visible=False)]], pad=(0,0))

#The second UI
layout2 = [
    [sg.Text('File 1'), sg.InputText(file1,disabled = True, size = (75,2))],
    [sg.Text('File 2'), sg.InputText(file2,disabled = True, size = (75,2))],
    [sg.Frame(
        layout=[*formlists],
        title = 'Select what column(s) do you want to sort them by?(More columns take more time)',
        relief=sg.RELIEF_RIDGE #Checkbox selection
    )],
    [sg.Output(size=(maxlen*6, 20))],  #The info box
    [sg.Submit('Compare'), sg.Cancel('Exit')
    , sg.Button('Download', visible=False), 
    # , sg.Submit('Back')
    ]
]

window2 = sg.Window('File Compare', layout2)
datakeydefined = 0
definedkey = []
while True:  # The Event Loop
    event, values = window2.read()
    # print(event, values)  # debug
    if event in (None, 'Exit'):
        break
    elif event == 'Compare':
        definedkey.clear()

        # print('Event', event, '\n', 'Values', values)
        for index, _ in enumerate(values):
            if index not in [0,1]:
                if values[index] == True: 
                    datakeydefined = 1
                    definedkey.append(keyslist[index-2])

        if len(definedkey) > 0:
            df1_sorted = df1_renamed.sort_values(by=definedkey)
            df2_sorted = df2_renamed.sort_values(by=definedkey)
            if len(df1_sorted) == len(df2_sorted):
                if df1_sorted.equals(df2_sorted):
                    print('The data in the two CSV files are exactly the same')

                else:
                    print('The data row numbers are the same, but there are differences in the data.')
                    print('Either you did not select appropriate columns to sort or there are differences in data.')
                    print('Please compare them manaully')
                    print('Click to download the sorted version of the two files.')

                    file1_name = (values[0].split('/'))[-1]
                    file2_name = (values[1].split('/'))[-1]


                    window2['Download'].update(visible=True)
            else:
                print('The number of rows of this two files are different') 
                print('There is no chance the data are equal')
        else:
            print('Error: You need to select at least one attribute as a data key')

    elif event == 'Download':
        #Output sorted df as csv
        df1_sorted.to_csv(f"Sorted_{file1_name}",  index=False)
        df2_sorted.to_csv(f"Sorted_{file2_name}",  index=False)

    # elif event == 'Back':
    #     window.close()
    #     break

