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
s3 = 's3cmd'
ps = 'c:/python27/scripts'
cn = '--configure'
ap = '/AppData/Roaming/'
ini = '.s3cmd.ini'
scf = '.s3cfg'
sl = '/'
brenrun = 'brenda-run'
rk = 'reset-keys'
init = 'init'
par = 'paramiko'

m = """output = utils.system_return_output(cmd, capture_stderr=capture_stderr)"""
n = """
				#new ssh on windows code-------------------------------------
				import paramiko
				#read ssh args from end of cmd object immediately following the node hostname entry
				sshArgs = " ".join(cmd[cmd.index(node)+1:])
				#get username
				user = utils.get_opt(opts.user, conf, 'AWS_USER', default='root')
				#get path to brenda private rsa key file
				brendaKeyPath =  aws.get_adaptive_ssh_identity_fn(opts, conf)
		
				k = paramiko.RSAKey.from_private_key_file(brendaKeyPath)
				c = paramiko.SSHClient()
				c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		
				c.connect( hostname = node, username = user, pkey = k )
				#change working directory on remote node to brenda diretory and execute ssh args
				commands = ["cd /mnt/brenda", sshArgs]
				for command in commands:
					stdin , stdout, stderr = c.exec_command(command)
					output = stdout.read()
				c.close()
				#new ssh on windows code-------------------------------------"""

def spacetime ():
    time.sleep(2)
    clear()
	
def spacetime2 ():
    time.sleep(10)
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
			status = os.system("""for /f "skip=2 tokens=3*" %a in ('reg query HKCU\Environment /v PATH') do @if [%b]==[] ( @setx PATH "%~a;C:\Python27\Scripts" ) else ( @setx PATH "%~a %~b;C:\Python27\Scripts" )""")
			print
			while True:
				errchk = raw_input('If this resulted in an error then enter "e" otherwise enter "c" to continue ')
				if errchk =='e':
					status = os.system('setx PATH ""')
					continue
				if errchk =='c':
					break
			break
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
			status = os.chdir(bm)
			spacetime()
			break
		
def step6 ():
	print
	print 'Step 6'
	print
	print 'Installs "s3cmd"'
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
			status = os.system(pi+sb+ins+sb+s3)
			spacetime()
			break

def step7 ():
	print
	print 'Step 7'
	print
	print 'Runs the "s3cmd" configuration'
	print
	print
	print
	while True:
		submen = raw_input('Enter "c" to continue or "s" to skip ')
		if submen =='s':		   
			break
		if submen =='c':
			clear()
			status = os.chdir(ps)
			status = os.system(py+sb+s3+sb+cn)
			spacetime()
			status = os.chdir(bm)
			break

def step8 ():
	print
	print 'Step 8'
	print
	print 'Move and rename the "s3cmd" configuration file'
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
			status = os.rename(home+ap+ini, home+sl+scf)
			spacetime()
			break
	
def step9 ():
	print
	print 'Step 9'
	print
	print 'Initiates Brenda and creates "rsa" key file with option to reset keys first'
	print
	print
	print
	while True:
		submen = raw_input('Enter "c" to continue or "s" to skip ')
		if submen =='s':		   
			break
		if submen =='c':
			clear()
			while True:
				print
				print 'Reset keys?'
				print
				print
				print
				submen = raw_input('Enter "c" to continue or "s" to skip ')
				if submen =='s':		   
					break
				if submen =='c':
					clear()
					status = os.chdir(bm)
					status = os.system(py+sb+brenrun+sb+rk)
					spacetime()
					clear()
					break
			status = os.chdir(bm)
			status = os.system(py+sb+brenrun+sb+init)
			spacetime()
			break

def step10 ():
	print
	print 'Step 10'
	print
	print 'Install "paramiko"'
	print
	print
	print
	while True:
		submen = raw_input('Enter "c" to continue or "s" to skip ')
		if submen =='s':		   
			break
		if submen =='c':
			clear()
			status = os.system(pi+sb+ins+sb+par)
			spacetime()
			break

def step11 ():
	print
	print 'Step 11'
	print
	print 'Modify tool.py'
	print
	print
	print
	while True:
		submen = raw_input('Enter "c" to continue or "s" to skip ')
		if submen =='s':		   
			break
		if submen =='c':
			clear()
			status = os.chdir(bm+sl+br)
			o = open('tool.py', 'r')
			t = open('tool.py.temp', 'w')
			for line in o:
				t.write(line.replace(m, n))
			o.close()
			t.close()
			status = os.rename('tool.py','tool_backup.py' )
			status = os.rename('tool.py.temp', 'tool.py')
			break

def step12 ():
	print
	print 'Step 12'
	print
	print 'Create "frame-template" file'
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
			file = open("frame-template", "w")
			print "Creating file"
			file.write('blender -b *.blend -F PNG -o $OUTDIR/frame_###### -s $START -e $END -j $STEP -t 0 -a')
			file.close()
			break

clear()
step1()
clear()
step2()
clear()
step3()
clear()
step4()
clear()
step5()
clear()
step6()
clear()
step7()
clear()
step8()
clear()
step9()
clear()
step10()
clear()
step11()
clear()
step12()
clear()

while True:
	print
	print 'You should now be able to run Brenda'
	print
	print '(if using the command line, you will need to run all command '
	print 'calls from the "brenda-master" folder and precede them with "python ")'
	print
	print
	print
	finish = raw_input('Press "e" to exit ')
	if finish =='e':
		break
	clear()
