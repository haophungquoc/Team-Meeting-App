"""The main process. Starts the program."""
import meetingTimer
import calendarBooking

def run():
    timer = meetingTimer.Timer()

    print("Welcome to the Team Meeting Timer")

    # Menu dialogue for user choice
    while True:
        print("\nWhat would you like to do?")
        userChoice = input("[A] Add task\n\
[S] Start timer\n\
[E] Export sub-tasks configuration to csv file\n\
[I] Import existing sub-task configuration from a csv file\n\
[V] View tasks\n\
[M] Manage tasks\n\
[C] Create an Google Calendar event for your future meeting using existing agenda\n\
[Q] Quit\n").upper()

        if userChoice == "A":       # Add task to timer list
            timer.addTask()

        elif userChoice == "S":     # Starts tasks
            timer.start()

        elif userChoice == "E":     # Export to csv
            dir_name = input("Enter the dicrectory's name location where you want to export csv configuration: ")
            timer.df.export_data(dir_name)

        elif userChoice == "I":     # Import csv
            file_name = input("Enter the file's name location where you want to import csv configuration: ")
            timer.tasks = timer.df.import_data(file_name)
            
        elif userChoice == "V":     # Prints tasks as a numbered list with relevent information
            print("Tasks currently scheduled:")
            timer.df.display_table()
        
        elif userChoice == "M":
            timer.editTasks()

        elif userChoice == "C":
            calendarBooking.create_event(timer.df.df)

        elif userChoice == "Q":     # Quits program
            print("Thanks for using the Team Meeting Timer!")
            break  # Breaks loop, ends program (didn't use exit() as it may be used as a module)

        else:
            # If user input doesn't match the above, continues loop 
            print("Incorrect input.")

if __name__ == '__main__':
    run() # Only necessary if program isn't being imported as a module