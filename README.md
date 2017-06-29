## Useful Scripts

This is my public script repository. Some of these scripts are also in Gist, but I don't like the way Gist works, so I moved them here in stead.

Below is a brief description of the scripts in this repository. Since I mainly work on Linux, most of these are Linux scripts. However the Python scripts may or may not work on other operating systems.

### 7zBackup

An automated full or differential backup script I wrote for my Syncthing data storage on my server. The usage is straight forwards. Run the script with the folder to archive. If they are all in one location, you canm set a common root bath in the settings section of the script. Otherwise just set it to /. The backup destination is also set in the script. To request a differential backup pass DIFF as the second argument. Otherwise a full backup will be made. If a differential backup is requested, but a full reference backup is not found, it will fall back to a full backup.

A sample cron script is added, and contains my current setup.

### autoParity

A simple script that generates parity files for all files in a folder, and make sure the recovery blocks are suffucient to recreate any one missing file. It's just a wrapper for par2 that calculates the relative size of the largest file compared to the total size of all files.

### compressPDF

Simple script that reduces file size of large PDFs. I think i got it from StackExchange somewhere.

### exchangeRates

A Python script that pulls today's exchange rates for an array of currencies. It can also pull the rates for any date back to 01/01/2000. It also supports crypto currencies, but with limited history.

### ipCalc

A Simple script that will calculate the network config for a given IP/mask. I made the script to calculate the firewall settings to block IP ranges trying to brute force login on an internet-facing PC I used to work on. I got *a lot* of brute force attempts on that PC.
