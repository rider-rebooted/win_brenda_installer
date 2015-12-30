import time
import os
import urllib
import zipfile

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
ps = 'c:/Python27/Scripts'
cn = '--configure'
ap = '/AppData/Roaming/'
ini = 's3cmd.ini'
scf = '.s3cfg'
sl = '/'
brenrun = 'brenda-run'
rk = 'reset-keys'
init = 'init'
par = 'paramiko'


n = """
# Brenda -- Blender render tool for Amazon Web Services
# Copyright (C) 2013 James Yonan <james@openvpn.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import threading, time, Queue
from brenda import aws, utils

def instances(opts, conf):
    now = time.time()
    for i in aws.filter_instances(opts, conf):
        uptime = aws.get_uptime(now, i.launch_time)
        print i.image_id, aws.format_uptime(uptime), i.public_dns_name

def ssh_args(opts, conf):
    user = utils.get_opt(opts.user, conf, 'AWS_USER', default='root')
    args = ['ssh', '-o', 'UserKnownHostsFile=/dev/null',
                   '-o', 'StrictHostKeyChecking=no',
                   '-o', 'LogLevel=quiet']
    if user:
        args.extend(['-o', 'User='+user])
    args.extend(['-i', aws.get_adaptive_ssh_identity_fn(opts, conf)])
    return args

def ssh_cmd_list(opts, conf, args, instances=None):
    if instances is None:
        instances = aws.filter_instances(opts, conf)
    for i in instances:
        node = i.public_dns_name
        cmd = ssh_args(opts, conf)
        cmd.append(node)
        cmd.extend(args)
        yield node, cmd

def rsync_cmd_list(opts, conf, args, hostset=None):
    for i in aws.filter_instances(opts, conf, hostset=hostset):
        node = i.public_dns_name
        cmd = ['rsync', '-e', ' '.join(ssh_args(opts, conf))] + [a.replace('HOST', node) for a in args]
        yield node, cmd

def run_cmd_list(opts, conf, cmd_seq, show_output, capture_stderr):
    def worker():
        while True:
            try:
                item = q.get(block=False)
            except Queue.Empty, e:
                break
            else:
                node, cmd = item



                #output = utils.system_return_output(cmd, capture_stderr=capture_stderr)

                #new ssh on windows code-------------------------------------
                import paramiko
                #read ssh args from end of cmd object immediately following the node hostname entry
                sshArgs = " ".join(cmd[cmd.index(node)+1:])
                #print "sshargs: " +ssArgs
                #get username
                #print "trying new user"
                user = utils.get_opt(opts.user, conf, 'AWS_USER', default='ubuntu')
                #print "user: " + user
                #get path to brenda private rsa key file
                brendaKeyPath =  aws.get_adaptive_ssh_identity_fn(opts, conf)
                
                k = paramiko.RSAKey.from_private_key_file(brendaKeyPath)
                c = paramiko.SSHClient()
                c.set_missing_host_key_policy(paramiko.AutoAddPolicy())

                try:

                    c.connect( hostname = node, username = user, pkey = k )
                    #change working directory on remote node to brenda diretory and execute ssh args
                    commands = ["cd /mnt/brenda", sshArgs]
                    for command in commands:
                        stdin , stdout, stderr = c.exec_command(command)
                        output = stdout.read()
                    c.close()



                    data = (node, output)
                    with lock:
                        if show_output:
                            print "------- %s\\n%s" % data,
                        ret.append(data)
                    q.task_done()



                except Exception as e:
                    print e
                #new ssh on windows code-------------------------------------

                #data = (node, output)
                #with lock:
                #    if show_output:
                #        print "------- %s\\n%s" % data,
                #    ret.append(data)
                #q.task_done()

    ret = []
    q = Queue.Queue()
    for task in cmd_seq:
        #if opts.verbose:
        #    print task
        q.put(task)

    lock = threading.Lock()
    max_threads = int(conf.get('TOOL_THREADS', '64'))
    for i in range(min(max_threads, q.qsize())):
        t = threading.Thread(target=worker)
        t.start()

    q.join() # block until all tasks are done
    return ret

def ssh(opts, conf, args):
    run_cmd_list(opts, conf, ssh_cmd_list(opts, conf, args), show_output=True, capture_stderr=True)

def rsync(opts, conf, args):
    run_cmd_list(opts, conf, rsync_cmd_list(opts, conf, args), show_output=True, capture_stderr=True)

def prune(opts, conf, args):
    def keyfunc(i):
        v = -1
        s = i[1].strip()
        if s == 'SMALL':
            v = -1
        elif s == 'BIG':
            v = 1<<32
        try:
            v = int(s)
        except:
            pass
        return v

    pidfile = conf.get('REMOTE_PIDFILE', 'brenda.pid')

    try:
        prune_target = int(args[0])
    except:
        raise ValueError("need prune target argument")
    else:
        if prune_target < 0:
            raise ValueError("prune target must be >= 0")

    if prune_target >= 0:
        # bash script logic to determine sort order for prune based on presence/absense
        # of files render.pid and task_last:
        #   if render.pid && task_last : return task_last
        #   if !render.pid && task_last : return BIG
        #   if render.pid && !task_last : return SMALL
        #   if !render.pid && !task_last : return SMALL
        script = ['if', '!', '[', '-f', 'task_last', '];', 'then', 'echo', 'SMALL;', 'elif', '[', '-f', pidfile, '];', 'then', 'cat', 'task_last;', 'else', 'echo', 'BIG;', 'fi']
        data = [(keyfunc(i), i[0]) for i in run_cmd_list(opts, conf, ssh_cmd_list(opts, conf, script), show_output=False, capture_stderr=False)]
        data.sort(reverse=True)
        print "Prune ranking data"
        for d in data:
            print d
        n_shutdown = len(data) - prune_target
        if n_shutdown > 0:
            shutdown_list = [i[1] for i in data[:n_shutdown]]
            print "Shutdown list"
            for sd in shutdown_list:
                print sd
            if not opts.dry_run:
                aws.shutdown_by_public_dns_name(opts, conf, shutdown_list)

def perf(opts, conf, args):
    def task_count_last(i):
        s = i[1].split()
        try:
            count = int(s[0])
            last = int(s[1])
        except:
            return None
        else:
            return count, last

    script = ['if', '[', '-f', 'task_count', ']', '&&', '[', '-f', 'task_last', '];', 'then', 'cat', 'task_count;', 'cat', 'task_last;', 'else', 'echo', '0;', 'fi']
    instances = aws.filter_instances(opts, conf)
    idict = dict([(i.dns_name, i) for i in instances])
    sdict = aws.get_spot_request_dict(conf)
    data = {}
    for i in run_cmd_list(opts, conf, ssh_cmd_list(opts, conf, script, instances), show_output=False, capture_stderr=False):
        host = i[0]
        inst = idict.get(host)
        if inst:
            sir = sdict.get(inst.spot_instance_request_id)
            price = None
            if sir:
                price = float(sir.price)
            tasks = task_count_last(i)
            if tasks:
                task_count, task_last = tasks
                uptime = aws.get_uptime(task_last, inst.launch_time) / 3600.0
                stat = data.setdefault(inst.instance_type, dict(n=0, uptime_sum=0.0, task_sum=0, price_sum=0.0))
                stat['n'] += 1
                stat['uptime_sum'] += uptime
                stat['task_sum'] += task_count
                if price is not None:
                    stat['price_sum'] += price
    tph= []
    tpd = []
    total_tasks = 0.0
    total_uptime = 0
    total_n = 0
    for itype, stat in data.items():
        total_tasks += stat['task_sum']
        total_uptime += stat['uptime_sum']
        total_n += stat['n']
        tasks_per_hour = stat['task_sum'] / stat['uptime_sum']
        tph.append((tasks_per_hour, itype))
        if 'price_sum' in stat:
            mprice = stat['price_sum'] / stat['n']
            tasks_per_dollar = tasks_per_hour / mprice
            tpd.append((tasks_per_dollar, itype))
    tph.sort(reverse=True)
    tpd.sort(reverse=True)
    if total_n:
        print "Tasks per hour (%.02f)" % (total_tasks / total_uptime * total_n,)
        for tasks_per_hour, itype in tph:
            print "  %s %.02f" % (itype, tasks_per_hour)
        print "Tasks per US$"
        for tasks_per_dollar, itype in tpd:
            print "  %s %.02f" % (itype, tasks_per_dollar)"""

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
			clear()		   
			status = os.system("""for /f "skip=2 tokens=3*" %a in ('reg query HKCU\Environment /v PATH') do @if [%b]==[] ( @setx PATH "%~a;c:\python27" ) else ( @setx PATH "%~a %~b;c:\python27" )""")
			status = os.system("""for /f "skip=2 tokens=3*" %a in ('reg query HKCU\Environment /v PATH') do @if [%b]==[] ( @setx PATH "%~a;C:\Python27\Scripts" ) else ( @setx PATH "%~a %~b;C:\Python27\Scripts" )""")
			print
			if status ==0:
				clear()
			if status ==1:
				clear()
				print
				print 'Fixing problem...'
				time.sleep(1)
				clear()
				status = os.system('setx PATH "c:\python27;c:\Python27\Scripts"')
				time.sleep(1)
				clear()
			print
			print 'Restart your computer and start this installer again.'
			print
			print 'Make sure you skip "step 1"'
			spacetime2()
			spacetime2()
			spacetime2()
			clear()
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
			os.remove(gp)
			print
			print 'Done'
			spacetime()
			break

def step3 ():
	print
	print 'Step 3'
	print
	print 'Downloads and unzips "brenda" to the "C:\" drive then deletes the zip file'
	print
	print
	print
	while True:
		submen = raw_input('Enter "c" to continue or "s" to skip ')
		if submen =='s':		   
			break
		if submen =='c':
			clear()	   
			urllib.urlretrieve ("https://github.com/jamesyonan/brenda/archive/master.zip", "master.zip")
			with zipfile.ZipFile('master.zip', "r") as z:
				z.extractall("C:\\")
			os.remove('master.zip')
			print
			print 'Done'
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
				status = os.system('pip install boto')
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
			status = os.rename('tool.py','tool_backup.py' )
			file = open("tool.py", "w")
			print "Creating file"
			file.write(n)
			file.close()
			status = os.chdir(bm)
			spacetime()
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
