#!/usr/bin/python3
import os,sys
if sys.version_info[0]<3:
	print('Due to unimplemented features in currently-used Python. This Python script requires Python in version at least major 3.')
	exit(1)
size_sum=0
dir=os.path.join(sys.argv[1], '')
if os.getenv('AddSizeOnDisk')!=None:
        AddSizeOnDisk=int(os.getenv('AddSizeOnDisk'))
else:
        AddSizeOnDisk=0
if os.getenv('VERBOSE')!=None:
        VERBOSE=int(os.getenv('VERBOSE'))
else:
        VERBOSE=0

def list(dir):
	global size_sum
	if AddSizeOnDisk:
		try:
			size_sum=size_sum+os.path.getsize(dir)
		except PermissionError:
			print('[Warning] Doesn\'t have permission to retrive size and list directory "'+dir+'".')
			return
		except FileNotFoundError:
			print('[Warning] Pathname of "'+dir+'" isn\'t supported by system.')
			return
	try:
		objs=os.listdir(dir)
	except PermissionError:
		print('[Warning] Doesn\'t have permission to list directory "'+dir+'".')
		return
	except FileNotFoundError:
		print('[Warning] Pathname of "'+dir+'" isn\'t supported by system.')
		return
	for obj in objs:
		path=dir+obj
		if os.path.islink(path):
			if VERBOSE:
				print('[Info] "'+path+'" is a symbolic-link file.')
			if AddSizeOnDisk:
				if os.stat(path, follow_symlinks=False)[3]==1:
					size_sum=size_sum+os.stat(path, follow_symlinks=False)[6]
				else:
					print('[Warning] "'+path+'" is a hard-link file. Size of these files wouldn\'t be counted.')
		elif os.path.isdir(path):
			if not os.path.ismount(path):
				list(path+'/')
			elif VERBOSE:
				print('[Info] "'+path+'" is a mountpoint.')
		elif os.path.isfile(path):
			if os.stat(path, follow_symlinks=False)[3]==1:
				size_sum=size_sum+os.stat(path, follow_symlinks=False)[6]
			else:
				print('[Warning] "'+path+'" is a hard-link file. Size of these files wouldn\'t be counted.')
		elif os.path.exists(path):
			if VERBOSE:
				print('[Info] "'+path+'" is a another special file.')
			if AddSizeOnDisk:
				if os.stat(path, follow_symlinks=False)[3]==1:
					size_sum=size_sum+os.stat(path, follow_symlinks=False)[6]
				else:
					print('[Warning] "'+path+'" is a hard-link file. Size of these files wouldn\'t be counted.')
		else:
			print('[Warning] Cannot retrive size or list "'+path+'".')

if not os.path.exists(dir):
	print('[Error] Selected main directory "'+dir+'" isn\'t existed.')
	exit(1)
print('Counting size of all files in "'+dir+'"...')
list(dir)
if AddSizeOnDisk:
	msg='Total Size (Filesystem metadatas are included.) = '
else:
	msg='Total Size (Only bytes from files are included.) = '
if 1000000<=size_sum<1000000000:
	print(msg+str(round(size_sum/1000000,1))+' MB ('+str(size_sum)+' B)')
elif 1000<=size_sum<1000000:
	print(msg+str(round(size_sum/1000,1))+' KB ('+str(size_sum)+' B)')
elif size_sum>=1000000000:
	print(msg+str(round(size_sum/1000000000,1))+' GB ('+str(size_sum)+' B)')
else:
	print(msg+str(size_sum)+' B')
exit(0)
