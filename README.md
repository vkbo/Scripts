## Useful Scripts

This is my public script repository. Some of these scripts are also in Gist, but I don't like the
way Gist works, so I moved them here in stead.

Below is a brief description of some of the scripts in this repository. Since I mainly work on
Linux, most of these are Linux scripts. However the Python scripts may or may not work on other
operating systems.

### 7zBackup

An automated full or differential backup script I wrote for my Syncthing data storage on my server.
The usage is straight forwards. Run the script with the folder to archive. If they are all in one
location, you can set a common root path in the settings section of the script. Otherwise just set
it to /.

The backup destination is also set in the script.

To request a differential backup pass DIFF as the second argument. Otherwise a full backup will be
made. If a differential backup is requested, but a full reference backup is not found, it will fall
back to a full backup.

A sample cron script is added, and contains my current setup.

### autoParity

A simple script that generates parity files for all files in a folder, and make sure the recovery
blocks are sufficient to recreate any one missing file. It's just a wrapper for par2 that
calculates the relative size of the largest file compared to the total size of all files.

### autoShutdown

A simple Python script that monitors the network connection, and shut down the host if the network
has been down for a certain amount of time.

This is a simple way to shut down in case of power loss when the machine itself is on a simple UPS,
and the network is not. I.e. if the netfork is down, the power is likely out.

### checkSha

A simple script to check a file against it's shasum when you have the shasum on the clipboard.

### compressPDF

A simple script that reduces file size of large PDFs. I think i got it from StackExchange
somewhere.

### ipCalc

A Simple script that will calculate the network config for a given IP/mask. I made the script to
calculate the firewall settings to block IP ranges trying to brute force login on an 
nternet-facing PC I used to work on. I got *a lot* of brute force attempts on that PC.

### webm2gif

Convert a webm video file (like the one generated from the screencast tool in Gnome) to an animated
gif. It also tries to make the gif small.
