import time
import os
import urllib

clear = lambda: os.system('cls')
	
py = 'python'
sb = ' '
gp = 'get-pip.py'
pi = 'pip'
ins = 'install'
br = 'brenda'
bm = 'c:/brenda-master'
bs = 'setup.py'
qu = '"'

def spacetime ():
    time.sleep(2)
    clear()
	
def spacetime2 ():
    time.sleep(6)
    clear()

def step1 ():
	print
	print 'Step 1'
	print
	print 'Adds "python27" and "python27/scripts" folders to the PATH environment variable'
	print
	print
	print
	while True:
		submen = raw_input('Enter "c" to continue or "s" to skip ')
		if submen =='s':		   
			break
		if submen =='c':		   
			status = os.system("""for /f "skip=2 tokens=3*" %a in ('reg query HKCU\Environment /v PATH') do @if [%b]==[] ( @setx PATH "%~a;c:\python27" ) else ( @setx PATH "%~a %~b;c:\python27" )""")
			spacetime()
			status = os.system("""for /f "skip=2 tokens=3*" %a in ('reg query HKCU\Environment /v PATH') do @if [%b]==[] ( @setx PATH "%~a;C:\Python27\Scripts" ) else ( @setx PATH "%~a %~b;C:\Python27\Scripts" )""")
			clear()
			print 'continue'
			spacetime()
			break
		
def step2 ():
	print
	print 'Step 2'
	print
	print 'Downloads and runs the "pip" installer then deletes the installer file'
	print
	print
	print
	while True:
		submen = raw_input('Enter "c" to continue or "s" to skip ')
		if submen =='s':		   
			break
		if submen =='c':
			clear()	   
			urllib.urlretrieve ("https://bootstrap.pypa.io/get-pip.py", "get-pip.py")
			status = os.system(py+sb+gp)
			spacetime()
			os.remove(gp)
			break

def step3 ():
	print
	print 'Step 3'
	print
	print 'Installs "brenda" using "pip". This creates a "brenda-master" directory'
	print
	print
	print
	while True:
		submen = raw_input('Enter "c" to continue or "s" to skip ')
		if submen =='s':		   
			break
		if submen =='c':
			clear()
			status = os.system(pi+sb+ins+sb+br)
			spacetime()
			break
		
def step4 ():
	print
	print 'Step 4'
	print
	print 'Continues "brenda" installation by running the "setup" file'
	print
	print
	print
	while True:
		submen = raw_input('Enter "c" to continue or "s" to skip ')
		if submen =='s':		   
			break
		if submen =='c':
			clear()
			status = os.chdir(bm)
			status = os.system(py+sb+bs+sb+ins)
			spacetime()
			break
		
def step5 ():
	print
	print 'Step 5'
	print
	print 'Creates a ".brenda.conf" file in your user home directory'
	print
	print
	print
	while True:
		submen = raw_input('Enter "c" to continue or "s" to skip ')
		if submen =='s':		   
			break
		if submen =='c':
			clear()
			from os.path import expanduser
			home = expanduser("~")
			status = os.chdir(home)
			print
			print 'Default instance type set to "c3.large"'
			spacetime()
			while True:
				print
				probuc = raw_input('Enter the name of your project bucket ')
				clear()
				print
				frabuc = raw_input('Enter the name of your frame bucket ')
				clear()
				print
				proj = raw_input('Enter the name of your project file (e.g. "suzanne.zip") ')
				clear()
				print
				print 'Your project file named '+qu+proj+qu,'is in the project bucket named '+qu+probuc+qu
				print 'and your frame bucket is named '+qu+frabuc+qu
				print
				qconf = raw_input('Are these values correct, y or n? ')  
				if qconf=='y':
					clear()
					break
				if qconf=='n':
					clear()
			file = open(".brenda.conf", "w")
			print "Creating file"
			u = """INSTANCE_TYPE=c3.large
BLENDER_PROJECT=s3://"""
			v = '/'
			w = """
WORK_QUEUE=sqs://"""
			x = """
RENDER_OUTPUT=s3://"""
			y = """
DONE=shutdown
\n"""
			file.write(u+probuc+v+proj+w+probuc+x+frabuc+y)
			file.close()
			spacetime()
			break


step1()
clear()
step2()
clear()
step3()
clear()
step4()
clear()
step5()
