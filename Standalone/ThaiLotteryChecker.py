#!/usr/bin/python3
# Name : Thailand Government Lottery's Prize Checker Program
# Description : Checking Thailand government lottery's prize by the processing of host server and get the data for processing using this program.
# Author : Nuttapong Punpipat (NP-chaonay)
# License : MIT License
# Language : Thai

import http.client,sys
try:
	print('### โปรแกรมตรวจผลการออกรางวัลสลากกินแบ่งรัฐบาล')
	print('### (จัดทำโดย ณัฐพงศ์ พันพิพัฒน์ (NP-chaonay))\n')
	while True:
		##
		print('### การตรวจรางวัล ###')
		print('โปรดเลือกประเภทสลาก :')
		print('1) สลากกินแบ่งรัฐบาล (2 ปี)')
		print('2) สลากการกุศล (10 ปี)')
		while True:
			choice=input('(ป้อน) : ')
			if choice in ['1','2']: type=choice; break
			else: print('(ผิดพลาด) : กรุณาป้อนหมายเลขตามรายการ'); continue
		##
		print('โปรดเลือกวันที่ที่ต้องการตรวจ :')
		HTTP_C=http.client.HTTPConnection('www.glo.or.th'); HTTP_C.request('GET','/glo_seize/lottary/glo_round.php?t='+type);
		dates=HTTP_C.getresponse().read().decode().splitlines()
		msgs=[]
		c=0
		for date in dates:
			c+=1
			sep='>'.join(date.split('<')).split('>')
			msgs+=[str(c)+') '+sep[2]]
		for msg in msgs[::-1]: print(msg)
		while True:
			choice=input('(ป้อน) : ')
			if choice in map(str,range(1,len(dates)+1)): id='>'.join(dates[int(choice)-1].split('<')).split('>')[1].split()[1].split("'")[1]; break
			else: print('(ผิดพลาด) : กรุณาป้อนหมายเลขตามรายการ'); continue
		##
		print('ป้อนหมายเลขที่ต้องการตรวจ (เว้นโดยช่องว่างเท่านั้น, ป้อนเลขซ้ำได้โดยที่จะไม่ถูกตรวจซ้ำ)')
		NotCorrect=True
		while NotCorrect:
			nums=set(input('(ป้อน) : ').split())
			for num in nums:
				if len(num)!=6 and not num.isnumeric(): print('(ผิดพลาด) กรุณาป้อนหมายเลขแต่ละตัวเป็นเลขโดด 0-9 เท่านั้น'); print('(ผิดพลาด) กรุณาป้อนหมายเลขแต่ละตัวเพียงแค่หกหลัก'); break
				if len(num)!=6: print('(ผิดพลาด) กรุณาป้อนหมายเลขแต่ละตัวเพียงแค่หกหลัก'); break
				if not num.isnumeric(): print('(ผิดพลาด) กรุณาป้อนหมายเลขแต่ละตัวเป็นเลขโดด 0-9 เท่านั้น'); break
			else: break
			continue
		##
		print('\n### ผลการตรวจรางวัล ###')
		result={}
		for num in nums:
			HTTP_C=http.client.HTTPConnection('www.glo.or.th')
			HTTP_C.request('POST','/glo_seize/lottary/check_lottary.php', 'kuson='+type+'&ldate='+id+'&lnumber='+num+'&c_set=', {'Content-Type':'application/x-www-form-urlencoded'})
			result[num]=' '.join(HTTP_C.getresponse().read().decode().splitlines()[330].split('<')[1].split(' ',1)[1].split('>')[1].split())
		for msg in set(result.values()):
			print('# หมายเลข'+msg+':')
			for num in result:
				if result[num]==msg: print(num)
		print('######\n')
		#print('\n### DEBUG ###')
		#print('Nums:'+str(nums))
		#print('Type:'+type)
		#print('ID:'+id)
		#print('######')
except http.client.socket.gaierror:
	sys.stderr.write('\n(ผิดพลาด) ระบบเครือข่ายมีปัญหา ไม่สามารถเชื่อมต่อได้\n')
except KeyboardInterrupt:
	exit('')
except EOFError:
	exit('')
except Exception:
	sys.stderr.write('\n(ผิดพลาด) โปรแกรมเกิดความผิดพลาดโดยไม่ทราบสาเหตุ โปรแกรมจึงต้องหยุดการทำงาน\n')
