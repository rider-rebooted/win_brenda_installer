# win_brenda_installer (beta)
Python script to automate the installation of Brenda on to Windows.


**WARNING, THIS IS MY FIRST PYTHON PROJECT AND IT MAY HAVE SERIOUS ISSUES WHICH COULD POTENTIALLY COST YOU MONEY. PLEASE ONLY USE THIS IF YOU ARE FAMILIAR WITH PYTHON AND BRENDA AND YOU ARE HAPPY WITH MY CODE. ALSO MAKE SURE YOU ARE AWARE OF THE ISSUES I'VE POSTED - THERE ARE MORE!**


Step by step installer (each step is skippable) for getting James Yonan's [Brenda](https://github.com/jamesyonan/brenda) for Blender to operate on Windows instead of Linux. [Todd Mcintosh](https://www.blendernetwork.org/todd-mcintosh) spent a lot of hard work figuring all of this out and this installer automates his [directions](http://brendapro.com/forum/viewtopic.php?f=0&t=76&sid=e6bc8c5335e35bab0605da5a5a6f9965). It's my first Python project so i'm sure it has issues but seems to work ok for me.
 
#HOW TO RUN#

1.Install Python 2.7 onto Windows (with default settings) from [here](https://www.python.org/downloads/)

2.Install Microsoft Visual C++ Compiler for Python 2.7 from [here](https://www.microsoft.com/en-gb/download/details.aspx?id=44266)

3.Install [Brenda](https://github.com/jamesyonan/brenda) by unzipping the download to drive "c:\" ("step 3" which is supposed to do it automatically fails at the moment)

4.Download the zip file, extract it and move the "win_brenda_installer.py" file to your "C:\Python27" directory. 

5.Double click it to run. 

It assumes you already have s3 project and frame buckets set up and ready to go (this can be done from the AWS website). 
