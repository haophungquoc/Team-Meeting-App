### OSTC Assessment 1
### Team Meeting Timer

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

try:
    from lib2to3.pytree import type_repr
    import time 
    import data
    import keyboard
    import copy
    import warnings
except:
    print("Modules missing. Please review the user manual.")


# Time conversion functions
"""Asks user for length of time, returns as integer."""
def recieveTime():
    while True:
        try:
            hour = input("Hours: ")
            minute = input("Minutes: ")
            second = input("Seconds: ")
            duration = int(hour)*3600 + int(minute)*60 + int(second)
            return duration
        except:
            print("Time must be a valid number")

"""Converts time from integer to time format."""
def convertTime(seconds):
    hour = int(seconds/3600)
    minute = int((seconds - 3600 * hour) / 60)
    seconds -= (hour * 3600 + minute * 60)
    return hour, minute, seconds


# Manages Tasks
class Timer:
    def __init__(self):
        self.tasks = []
        self.df = data.Data()

    """Add new task for the timer"""
    def addTask(self):
        title = input("Title: ")
        description = input("Description: ")
        print("Duration of the task: ")
        duration = recieveTime()
        self.tasks.append(Task(title, description, duration))
        self.df.add_task(title, description, duration)

    """Starting countdown for all task(s), start from the task that has been set first."""
    def start(self):
        print("\nStarting countdown")
        for x in self.tasks:
            x.countDown()
    
    """Sub menu to edit tasks."""
    def editTasks(self):
        print("\nTasks currently scheduled:")
        for x in range(len(self.tasks)):
            print(f"[{x+1}] {self.tasks[x]}")
        print("--------------------------")
        
        menuChoice = input("[e] to Edit Task\n[r] to Return to Menu\n").lower()

        if menuChoice == "e":
            edit = True
            try:
                taskChoice = int(input("\nWhich task would you like to edit?\n"))
                while edit == True:
                    if taskChoice > 0 and taskChoice < len(self.tasks)+1:
                        taskChoice -= 1
                        editChoice = input("\nWhat would you like to edit?\n\
------------------------\n\
[t] to edit title\n\
[d] to edit description\n\
[n] to edit duration\n\
------------------------\n\
[c] to duplicate task\n\
[m] to move task\n\
[x] to delete task\n\
------------------------\n\
[r] to return to menu\n").lower()

                        if editChoice == "t":
                            self.tasks[taskChoice].title = input("Title: ")
                            self.df.update_task(taskChoice, self.tasks[taskChoice].title, self.tasks[taskChoice].description, self.tasks[taskChoice].duration )
                            print(self.tasks[taskChoice]) 

                        elif editChoice == "d":
                            self.tasks[taskChoice].description = input("Description: ")
                            self.df.update_task(taskChoice, self.tasks[taskChoice].title, self.tasks[taskChoice].description, self.tasks[taskChoice].duration )
                            print(self.tasks[taskChoice]) 

                        elif editChoice == "n":
                            self.tasks[taskChoice].setDuration()
                            self.df.update_task(taskChoice, self.tasks[taskChoice].title, self.tasks[taskChoice].description, self.tasks[taskChoice].duration )
                            print(self.tasks[taskChoice]) 
                        
                        elif editChoice == "c":
                            self.tasks.insert(taskChoice, copy.deepcopy(self.tasks[taskChoice]))
                            self.df.add_task(self.tasks[taskChoice].title, self.tasks[taskChoice].description, self.tasks[taskChoice].duration)
                            edit = False

                        elif editChoice == "m":
                            self.reorderTasks(taskChoice)
                            edit = False

                        elif editChoice == "x":
                            self.tasks.remove(self.tasks[taskChoice])    

                             # Remaking df with new order
                            self.df.delete_data()

                            for x in self.tasks:
                                self.df.add_task(x.title, x.description, x.duration)
                            move = False
                            edit = False                    
                        
                        elif editChoice == "r":
                            edit = False

                        else:
                            raise TypeError

                    else:
                        raise TypeError

                    taskChoice += 1 # So loop continues properly without raising error.

            except TypeError as e:
                print("Incorrect input.")

        elif menuChoice == "r":
            edit = False    # Exit loop

    def reorderTasks(self, taskPos):
        try:
            move = True
            while move == True:
                print("\nWhere would you like to move the task?")
                targetPos = int(input())-1
                if targetPos > 0 and targetPos < len(self.tasks)+1:
                    self.tasks.insert(targetPos, self.tasks.pop(taskPos))

                    # Remaking df with new order
                    self.df.delete_data()

                    for x in self.tasks:
                        self.df.add_task(x.title, x.description, x.duration)
                    move = False
                    
                else:
                    raise TypeError
        
        except TypeError as e:
            print("Incorrect input.")


# The individual tasks being scheduled
class Task:
    def __init__(self, title, description, duration):
        self.hour, self.minute, self.second = convertTime(duration)
        self.duration = duration
        self.tempDuration = self.duration   # Used for tracking temporary changes (extend, advance etc)
        
        self.description = description
        self.title = title
        
        self.startTime = None
        self.timePassed = 0
    
    """Counts down the duration of the task"""
    def countDown(self):
        print(f"Counting down for task: {self.title}")
        print(self)

        self.startTime = time.time()

        # Used to remove unecessary duplicated lines
        oldTime = None
        newTime = None

        while self.timePassed < self.tempDuration: # While the difference between the start time and current time is less than the duration, count down
            try:
                self.timePassed = time.time() - self.startTime # Update time passed to reflect current time
                newTime = time.strftime('%H:%M:%S', time.gmtime(self.tempDuration - self.timePassed))   #Checking output hasn't previously been printed

                # If a second has passed, print the time left. Checking output hasn't previously been printed.
                if newTime == "00:00:00":
                    break

                elif newTime != oldTime:
                    oldTime = newTime
                    print(time.strftime('%H:%M:%S', time.gmtime(self.tempDuration - self.timePassed)))
                
                # Actions to edit current countdown without interupting count. No permanent changes to task.
                if keyboard.is_pressed("p"):
                    raise KeyboardInterrupt

            except KeyboardInterrupt:   # Pause timer if interupted/'p' is pressed
                self.pauseCount()
                self.startTime = time.time() - self.timePassed  # Changes start time to account for pause

        self.tempDuration = self.duration   # Resetting duration after timer is up.
        print("Task ended!")
    


    """Pause function for countdown of task."""
    def pauseCount(self):
        print("Countdown paused.")

        pauseText = "Press [r] to resume\n\
        [e] to extend \n\
        [a] to advance"

        print(pauseText)

        paused = True
        while paused == True:
            # Resume
            if keyboard.is_pressed("r"):
                print("Countdown resumed")
                time.sleep(0.1) # To avoid accidental spam
                paused = False

            # Extend
            elif keyboard.is_pressed("e"):
                print("How much time do you want to add to the task?")
                self.extendCount()
                print(pauseText)

            # Advance
            elif keyboard.is_pressed("a"):
                print("How much time do you want to skip in the task?")
                self.advanceCount()
                print(pauseText)

    """Extend function for countdown of task by the specified amount of time."""
    def extendCount(self):
        extendTime = recieveTime()
        self.tempDuration += extendTime
        print(f"Total duration is now {time.strftime('%H:%M:%S', time.gmtime(self.tempDuration))}.")
    
    """Adcance function for countdown of task by the specified amount of time."""
    def advanceCount(self):
        advanceTime = recieveTime()
        self.tempDuration -= advanceTime
        print(f"Total duration is now {time.strftime('%H:%M:%S', time.gmtime(self.tempDuration))}.")
    
    """Set the duration for the task."""
    def setDuration(self):
        self.duration = recieveTime()
        print(f"Duration set to {time.strftime('%H:%M:%S', time.gmtime(self.duration))}")



    """Returns task string as 'Title | Duration: _ hour(s), _ minute(s), _ second(s)'"""
    def __str__(self):
        result = (f"{self.title} | Duration: {self.hour} hour(s), {self.minute} minute(s), {self.second} second(s)")

        # If description is blank, print N/A instead of a blank line
        if self.description != "":
            result += (f"\n    Description: {self.description}")
        else:
            result += (f"\n    Description: N/A")
        return result