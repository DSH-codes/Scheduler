
import tkinter as mt

import time as tm

from tkinter.ttk import *

from tkinter import messagebox as mb

import sys as sst

import os


# We pass to -join- func , a HOMEDRIVE environmental variable, to get ProgramData in user's system drive
# Then we pass this concatenated path to -append- func, and it will be added to PATH
# So we will be able to import from ProgramData folder, our Scheduler_FW_2023.py log, which we're going to create below
sst.path.append(os.path.join(os.getenv("HOMEDRIVE"), "\\ProgramData\\"))


try:
    # So the path to ProgramData is already added to PATH, so we are going to create our Scheduler_FW_2023.py file
    # If it does not exist already, if it does, we do nothing. After creation, some initial warning records, and
    # Empty variables are added into the file
    with open(os.path.join(os.getenv("HOMEDRIVE"), "\\ProgramData\\Scheduler_FW_2023.py"), "x") as f: # Create a new file, if a file does not exist   ??????? PROBLEM?

        f.write("# This variable log is for Scheduler !This is not a malware or a trojan file!\n")
        f.write("# For correct work of the App, please do not delete this log!\n")
        f.write("# But if you have to delete it cause off some reason, please abort your last Scheduler procedure,\n")
        f.write("# to avoid an error during next use of Scheduler!\n")

        f.write("\n\ntask = 'Task'\n")
        f.write("last_procedure = 'None'\n")

except FileExistsError: # If there is a file exists, do nothing
    ...

# then, we import Scheduler_FW_2023.py aka our variable log, we had created above
import Scheduler_FW_2023 as log




# These to variables, keep data about procedure name and task info, during runtime
# After restarting of the App, these two variables get their initial values, from
# Scheduler_FW_2023.py aka our variable log
procedure = log.last_procedure
task = log.task





# FUNCTIONS ************************************************************************************************************

def procedure_and_task_recorder(Record: str, sch = None, day = None, month = None, hour = None, minute = None):

    """This func is used in -schedule- func below, there, it called, with passing a procedure name,
    one off shutdown/hibernate/log-off/restart/. And then, through Record argument, value, being recorded
    into Scheduler_FW_2023.py and global scope -procedure- variable. Task info record is also made using a
    procedure name, and will be stored into global -task- var and Scheduler_FW_2023.py.

    Sch is time for scheduling passed by -schedule- func using -scheduling_time- func below.
    """

    global procedure, task

    # IF sch is not None! Sch is a time, passed by -scheduling_time- func below. Sch is needed for -hibernation- ->
    # and -log-off- brunches of -schedule- func. So, if sch is None, stream goes to else brunch below

    if sch:
        with open(os.path.join(os.getenv("HOMEDRIVE"), "\\ProgramData\\Scheduler_FW_2023.py"), "a") as file:
            file.write(f"\nlast_procedure = '{Record}'\n")
            procedure = Record
            file.write(f"task = \"{Record} was scheduled for {day}/{month}/{sch.tm_year} at {hour}:{minute}\"\n")
            task = f"{Record} was scheduled for {day}/{month}/{sch.tm_year} at {hour}:{minute}"

    # Else brunch is for -shutdown- and -restart- brunches from -schedule- func, because they need no day, month, ->
    # hour, minute and year values to be passed, as -hibernate- and -log-off- do for their scheduling

    else:
        with open(os.path.join(os.getenv("HOMEDRIVE"), "\\ProgramData\\Scheduler_FW_2023.py"), "a") as file:
            file.write(f"\nlast_procedure = '{Record}'\n")
            procedure = Record
            file.write(f"task = '{Record} was scheduled for {round(return_time() / 60, 2)} minutes at {tm.asctime()}'\n")
            task = f"{Record} was scheduled for {round(return_time() / 60, 2)} minutes at {tm.asctime()}"

def abort_record():

    """This func will be called by -abort- func,
    simply to record into global vars -procedure- and -task-
    and also into same ones off Scheduler_FW_2023.py, that task = No task
    and procedure = None"""

    global procedure, task

    with open(os.path.join(os.getenv("HOMEDRIVE"), "\\ProgramData\\Scheduler_FW_2023.py"), "a") as file:
        file.write("\nlast_procedure = 'None'\n")
        procedure = "None"
        file.write("task = '-No tasks-'\n")
        task = "-No tasks-"

def return_time() -> int:

    """Returns a time for
    scheduled shutdown from all
    the counters from the counter
    section below"""

    time_out = (
            (int(year_counter.get()) * 31_556_926) +
            (int(month_counter.get()) * 2_629_743.83) +
            (int(days_counter.get()) * 24 * 60 * 60) +
            (int(hours_counter.get()) * 60 * 60) +
            (int(minutes_counter.get()) * 60)
    )

    return int(time_out)

def scheduling_time() -> dict:

    """Here we count up a time in seconds from start off the Epoch,
    then we add to it our time, and by it canculate future time, for scheduling!
    Time entered by a user, will be returned in seconds by -return_time- func,
    from Years/Months/Weeks/Days/Hours/Minutes counters of GUI

    Also, we have to add -0- at the begging of values, if their len is == 1,
    because cmd command we're using for scheduling, accepts data values only in
    00/00/0000 aka day/month/year. Year values passed by -localtime- has 4 digits,
    so we have no problem with it.
    """


    sch = tm.localtime(tm.time() + return_time() + 23)
    day = sch.tm_mday if len(str(sch.tm_mday)) == 2 else "0" + str(sch.tm_mday)
    month = sch.tm_mon if len(str(sch.tm_mon)) == 2 else "0" + str(sch.tm_mon)
    hour = sch.tm_hour if len(str(sch.tm_hour)) == 2 else "0" + str(sch.tm_hour)
    minute = sch.tm_min if len(str(sch.tm_min)) == 2 else "0" + str(sch.tm_min)
    return {"sch": sch, "day": day, "month": month, "hour": hour, "minute": minute}

def turn_off():
    """A func a fast shutdown button"""
    if mb.askyesno(title = "Turning off", message = "Turn off computer?"):
        os.system("shutdown -a")
        os.system("shutdown -s -t 1")
    else:
        ...

def hibernate():
    """A func a fast hibernation button"""
    if mb.askyesno(title = "Hibernation", message = "Hibernate computer?"):
        os.system("shutdown -a")
        os.system("shutdown -h")
    else:
        ...

def abort():
    global procedure, task
    # Getting procedure and task to change them at every procedure selection, task is for info
    # messages, deletion off it, won't crush the program, but there will be a mess in info messages

    if procedure == 'Shutdown' or procedure == 'Restart':
        os.system("shutdown -a")
        mb.showinfo(title = "Done!", message = procedure + " has been aborted")
        abort_record()

    elif procedure == "Hibernation":
        os.system("schtasks /delete /f /tn scheduled_hibernation_fw")
        mb.showinfo(title = "Done!", message = procedure + " has been aborted")
        abort_record()

    elif procedure == "Log-off":
        os.system("schtasks /delete /f /tn scheduled_hibernation_fw")
        mb.showinfo(title = "Done!", message = procedure + " has been aborted")
        abort_record()

    elif procedure == "None":
        mb.showinfo(title = "No task!", message = "No task to abort!")

def schedule():

    """This func checks what is procedure name in shutdown_switcher combobox,
    and then, corresponding the value, runs a definite brunch off belows,
    in selected brunch, it calls -procedure_and_task_recorder- func, to make
    records

    Window's -schtasks- command is used here to schedule hibernation and log-off,
    because -shutdown- command can't set a timer for them! I tried and found so!?!

    Window's -shutdown- command is used to schedule shutdown and restart of PC.
    """

    global procedure, task
    sds = shutdown_switcher # a combobox, given to sds for convenience
    time = return_time()


    if sds.get() == sds["values"][0]: # No procedure or no time selected
        mb.showwarning(title = "No procedure selected!",
                       message = "Please select one of the procedures:\nShutdown\\Hibernate\\Log-off\\Restart!")
    elif time == 0:
        mb.showwarning(title = "Timeout is 0!",
                       message = "Please, set a timeout for shutdown in the counter above!")


    # IF TIME AND PROCEDURE ABOVE, ARE SELECTED PROPERLY, WE GO TO PROCEDURE CREATIONS THAT STARTS FROM HERE
    else:


        # RESTART SECTION ----------------------------------------------------------------------------------------------
        if sds.get() == sds["values"][4]:
            if procedure == 'None':
                os.system(f"shutdown -r -t {time}")
                procedure_and_task_recorder("Restart")
                mb.showinfo(title = "SUCCESS",
                            message = f"{procedure} has been scheduled!")
            else:
                mb.showinfo(title = f"{procedure} is already scheduled!",
                            message = "Please, abort procedure, using -abort- button!\n\n " + task)


        # SHUTDOWN SECTION ---------------------------------------------------------------------------------------------
        if sds.get() == sds["values"][1]:
            if procedure == 'None':
                os.system(f"shutdown -s -t {time}")
                procedure_and_task_recorder('Shutdown')
                mb.showinfo(title = "SUCCESS!",
                            message = f"{procedure} has been scheduled!")
            else:
                mb.showinfo(title = f"{procedure} is already scheduled!",
                               message = "Please, abort procedure, using -abort- button!\n\n " + task)


        # HIBERNATION SECTION ------------------------------------------------------------------------------------------
        if sds.get() == sds["values"][2]:
            st = scheduling_time()
            if procedure == 'None':
                os.system(f"schtasks /create /f /tn scheduled_hibernation_fw /tr \"shutdown -h\" /sc once /sd {st['day']}/{st['month']}/{st['sch'].tm_year} /st {st['hour']}:{st['minute']}")
                procedure_and_task_recorder("Hibernation", st["sch"], st["day"], st["month"], st["hour"], st["minute"])
                mb.showinfo(title = "SUCCESS!",
                            message = f"{procedure} has been scheduled!")
            else:
                mb.showinfo(title = f"{procedure} is already scheduled!",
                            message = "Please, abort procedure, using -abort- button!\n\n " + task)


        # LOG-OFF SECTION ----------------------------------------------------------------------------------------------
        if sds.get() == sds["values"][3]:
            st = scheduling_time()
            if procedure == 'None':
                os.system(f"schtasks /create /f /tn scheduled_hibernation_fw /tr \"shutdown -l\" /sc once /sd {st['day']}/{st['month']}/{st['sch'].tm_year} /st {st['hour']}:{st['minute']}")
                procedure_and_task_recorder("Log-off", st["sch"], st["day"], st["month"], st["hour"], st["minute"])
                mb.showinfo(title = "SUCCESS!",
                            message = f"{procedure} has been scheduled")
            else:
                mb.showinfo(title = f"{procedure} is already scheduled",
                            message = "Please, abort procedure, using -abort- button\n\n " + task)

def help_window():
    hw = mt.Tk()
    hw.geometry("670x670")
    hw.title("Help")
    hw.iconbitmap("icon.ico")
    hw.resizable(0, 0)

    info_message = """
This is a simple app, for scheduling ✔turn_off, ✔restart, ✔hibernation or ✔log-off on your PC!
This app is made by a newbie programmer, and I am not sure, that it will work on your machine
properly. Anyway, I had no problems by using it at my PC with Windows 7 Professional, I hope
you won't either. Data format for scheduling [hibernate] and [log-off] options is DD/MM/YYYY,
so if you have different data format on your machine, these options probably won't work, but
I hope they will. 

So, let me explain how it works!

1. Set a timer for a procedure, using Years/Months/Weeks/Days/Hours/Minutes 
   counters at the top off the window.

2. Then, select a procedure you want to schedule.

3. Push [Schedule procedure] button 

4. To reset a procedure, abort any previous one, 
   using [Abort procedure] button!

5. Hibernate button is for instant hibernation

6. Turn-off button is for instant turning-off 

7. Help button is for this help window

Good luck!

Icons used in this App are downloaded from flaticon.com 
Authors: ✔BomSymbols and ✔Irfansusanto20

Used online tools:
https://www.freeconvert.com/ico-converter
    """
    hw_label = Label(hw, text = info_message)
    hw_label.pack()


# ROOT *****************************************************************************************************************

root = mt.Tk()
root.title("Scheduler")
root.geometry("300x370")
root.iconbitmap("icon.ico")
root.resizable(0, 0)

# FRAMES ***************************************************************************************************************

timer_frame = Frame(root)
timer_frame.pack(pady = 3)

switchers_frame = Frame(root)
switchers_frame.pack(pady = 3)

buttons_frame = Frame(root)
buttons_frame.pack(pady = 3)

# COUNTERS *************************************************************************************************************

counters_width = 3

# r - read only state for spinbox
year_label = Label(timer_frame, text = "Years")
year_label.grid(row = 0, column = 0)
year_counter = Spinbox(timer_frame, from_ = 0, to = 6, width = counters_width, state = "r")
year_counter.set(0)
year_counter.grid(row = 1, column = 0, pady = 7, padx = 3)

month_label = Label(timer_frame, text = "Months")
month_label.grid(row = 0, column = 1)
month_counter = Spinbox(timer_frame, from_ = 0, to = 12, width = counters_width, state = "r")
month_counter.set(0)
month_counter.grid(row = 1, column = 1, pady = 7, padx = 3)

days_label = Label(timer_frame, text = "Days")
days_label.grid(row = 0, column = 2)
days_counter = Spinbox(timer_frame, from_ = 0, to = 30, width = counters_width, state = "r")
days_counter.set(0)
days_counter.grid(row = 1, column = 2, pady = 7, padx = 3)

hours_label = Label(timer_frame, text = "Hours")
hours_label.grid(row = 0, column = 3)
hours_counter = Spinbox(timer_frame, from_ = 0, to = 24, width = counters_width, state = "r")
hours_counter.set(0)
hours_counter.grid(row = 1, column = 3, pady = 7, padx = 3)

minutes_label = Label(timer_frame, text = "Minutes")
minutes_label.grid(row = 0, column = 4)
minutes_counter = Spinbox(timer_frame, from_ = 0, to = 60, width = counters_width, state = "r")
minutes_counter.set(0)
minutes_counter.grid(row = 1, column = 4, pady = 7, padx = 3)

# SWITCHER ************************************************************************************************************

values = ("No procedure", "Shutdown", "Hibernate", "Log-off", "Restart") # CHECK log-off

shutdown_switcher = Combobox(switchers_frame, width = 25, state = "r", values = values)
shutdown_switcher.set(shutdown_switcher["values"][0])
shutdown_switcher.grid(row = 0, column = 0, pady = 5)

# BUTTONS **************************************************************************************************************

buttons_width = 27

schedule_button = Button(buttons_frame, text = "Schedule procedure", width = buttons_width, command = schedule)
schedule_button.pack()

abort_button = Button(buttons_frame, text = "Abort procedure", width = buttons_width, command = abort)
abort_button.pack()

blank_label = Label(buttons_frame, text = "-" * 37)
blank_label.pack()

hibernate_button = Button(buttons_frame, text ="Hibernate", width = buttons_width, command = hibernate)
hibernate_button.pack()

fast_off_button = Button(buttons_frame, text = "Turn off", width = buttons_width, command = turn_off)
fast_off_button.pack()

help_button = Button(buttons_frame, text = "Help", width = buttons_width, command = help_window)
help_button.pack()

company_logo = Label(buttons_frame, text = f"FreeWind Interactive © {tm.localtime()[0]} \nAll rights reserved", justify = "center")
company_logo.pack(pady = 15)




root.mainloop()
