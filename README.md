# Team Meeting Timer
This program runs on Python, so the software must be installed before you can run it. Install from the official Python website, python.org

## Prerequisites
1. Python modules: 
    - pandas
        - `pip install pandas`
    - numpy
        - `pip install numpy`
    - keyboard
        - `pip install keyboard`
    - tabulate
        - `pip install tabulate`
    - To run Google Developer's API
        - `pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib`

    Use the `pip install [module]` command in cmd

2. Google Calendar's API:

    - You need to have Gmail account with Google Calendar enabled.
    - Your Gmail **must be** in testing user list to have access, if you got **error 403** when authenticate with your email, contact the developer to add your Gmail to testing users list.

# Basic App Usage

After get all of packages and set up everything you need, use the command below to run program:

    python main.py

## 1. Main Menu
When starting the program, you will be met by the following.
```
What would you like to do?
[A] Add task
[S] Start timer
[E] Export sub-tasks configuration to csv file
[I] Import existing sub-task configuration from a csv file
[V] View tasks
[M] Manage tasks
[C] Create an Google Calendar event for your future meeting using existing agenda
[Q] Quit`
```
Input the associated character to the task you would like to initiate. 
For more information on each task, continue reading. 

## 2. Adding tasks
When adding a task, you will be prompted for both a title and a description. Both of these may be as long or short as the user wants. 
You will also be asked to input an amount of time. All fields must be filled, for example:
`Hours: ` 0
`Minutes: ` 0
`Seconds: ` 10 
This example is valid. Leaving the fields blank, however, will cause the program to reprompt for correct values.
When this is completed, the task will be added to the list of tasks that the timer will run from.

## 3. Starting the timer
Starting the timer will begin a countdown for each item in the list, starting from the top, or number 1. As each task countdown is completeted, the next will begin.

### 3.1. Pausing
Pressing 'p' at any time during the count down will stop the count down until you return. The following options will be available for you:
#### *3.1.1. Resume*
Pressing 'r' will simply start the countdown from where you left off.
#### *3.1.2. Extend*
Pressing 'e' will give you the ability to extend the time for the current task. This change is not permanent, and will be reset back to what the duration was before the timer was started when it is complete.
#### *3.1.3 Advance*
Pressing 'a' will give you the ability to advance the time for the current task, skipping forward in the timer. 

## 4. Exporting and Importing CSV files

### 4.1. Exporting
To export your current agenda to a csv config file, you have to write the location of the directory where you want to save your config file (It must be an existing directory). It will create a file called `config.csv` inside that directory

Note: For Linux, you have to type from root directory "/", it won't work for home directory "~"

### 4.2 Importing
To import an existing config, you have to type the whole file path (starting from root for Linux), including the .csv extension. Your config file should exactly has 3 columns: `Task`, `Description`, `Durations (in seconds)`. All cell must contain non-null values, and for `Durations (in seconds)` column, all values must be positive number, to make this work.

## 5. View tasks
A simple table with the task name and the duration in seconds will be shown on screen.

## 6. Manage tasks
When choosing this option, you will be presented by a list of tasks with more details than View Tasks, and the following options.
`[e] to Edit Task`
`[r] to Return to Menu`
Entering 'r' will send you back to the main menu.

### 6.1 Editing a task
Entering 'e' will prompt you to choose an task. Each task is preceeded by a number, desegnating its place in the list. This is the value you need to enter.

After selecting an item in the list, a sub menu will appear, showing the following:
```
What would you like to edit?
------------------------
[t] to edit title
[d] to edit description
[n] to edit duration
------------------------
[c] to duplicate task
[m] to move task
[x] to delete task
------------------------
[r] to return to menu"
```

#### 6.1.1 Duplicate task
Duplicating a task creates a copy of it after the original. These two are not linked, and can be edited independently of each other.

#### 6.1.2 Move task
This function allows you to move the task to another location on the list. Input the number you would like it to move to, and it will be shifted to take that space. The item that was previously there will be moved forward, along with all those following.

#### 6.1.3 Delete task
Removes the task permanently from the list. 

## 7. Google Calendar event

### 7.1. Instruction for first time using this feature

When using this feature the first time, the file `token.json`, there will be a pop-up window, or a link for authentication will appears, you have to follow some steps:

1. Login with your Gmail that you want to add event to
2. Click "Continue" 
3. Allow all of three services that the app want to access

### 7.2. Summary

This app's feature allows user to create blocks of events on Google Calendar based on the current agenda that user has created inside the app. After choosing the option to use this feature, you have to enter some information:

- Event's name (or the summary part), optional
- Event's location, optional
- Event's description, optional

For the date and time information, just enter the number's value. E.g: Meeting start at 8:30PM 29/06/2022

- date: 29
- month: 6
- year: 2022
- hour: 20
- minute: 30

When adding people, use their Gmail to add to the attendees list.

## 8. Quit
Closes the program.
