## C:\path\to\your\script.py
## Need to do following

'''
Open Task Scheduler → Create Basic Task.

Set a schedule (e.g., daily at 8 AM).

In Action, select Start a Program → Browse for python.exe.

Add script path as argument:

Save and enable the task.

FOR LINUX
crontab -e
0 8 * * * /usr/bin/python3 /path/to/your_script.py
'''