# win_brenda_installer (beta)
Python script to automate the installation of Brenda on to Windows. Brenda is an open source piece of software which lets you render Blender projects with very low cost (compared to render farms) AWS Amazon computing instances.


**WARNING, THIS IS MY FIRST PYTHON PROJECT AND IT MAY HAVE SERIOUS ISSUES WHICH COULD POTENTIALLY COST YOU MONEY. PLEASE ONLY USE THIS IF YOU ARE FAMILIAR WITH PYTHON AND BRENDA AND YOU ARE HAPPY WITH MY CODE. ALSO MAKE SURE YOU ARE AWARE OF THE ISSUES I'VE POSTED - THERE ARE MORE!**

*Video tutorial coming soon*

Step by step installer (each step is skippable) for getting James Yonan's [Brenda](https://github.com/jamesyonan/brenda) for Blender to operate on Windows instead of Linux. [Todd Mcintosh](https://www.blendernetwork.org/todd-mcintosh) spent a lot of hard work figuring all of this out and this installer automates his [directions](http://brendapro.com/forum/viewtopic.php?f=0&t=76&sid=e6bc8c5335e35bab0605da5a5a6f9965). It's my first Python project so i'm sure it has issues but seems to work ok for me.
 
#HOW TO RUN#

1.Install Python 2.7 onto Windows (with default settings) from [here](https://www.python.org/downloads/)

2.Install Microsoft Visual C++ Compiler for Python 2.7 from [here](https://www.microsoft.com/en-gb/download/details.aspx?id=44266)

3.Download the win_brenda_installer zip file, extract it and move the "win_brenda_installer.py" file to your "C:\Python27" directory. 

4.Double click it to run and follow the steps.

It assumes you already have s3 project and frame buckets set up and ready to go (this as well as uploading your zipped Blender project can be done from the AWS management [console](https://aws.amazon.com/)). 

I also wrote a very simple program called [win_brenda_console](https://github.com/rider-rebooted/win_brenda_console) to make Brenda calls on Windows without using command lines.

Tested on Windows 8.1 and Windows 10
