'''
	Author 	:	Nandeshwar Gupta	<guptanandeshwar553@gmail.com>
	Notes 	:	The output file should not be already present.
'''

from datetime import datetime
import re

print('Start Time is: ',datetime.now())

#Enter the path of the input file here.
input_path = '2student.txt' 
#Enter the path of the output file here.
output_path = 'formatted.txt'

with open(input_path,'r') as f :
	
	for temp0 in f :
		
		if bool(re.findall('(?<=: )\w(.*)',temp0)) :
			temp1 = temp0.split(' : ')
			temp2 = temp1[1].split(',')
			
			if len(temp2) > 1 :
				temp0 = temp1[0]+' : '+'"'+temp2[0].strip().replace('"',"'")+'"'+',\n'
			else :
				temp0 = temp1[0]+' : '+'"'+temp2[0].strip().replace('"',"'")+'"'+'\n'

		with open(output_path,'a') as fo :
			fo.write(temp0)

with open(output_path,'r+') as foo :
	temp3 = foo.read()
	foo.seek(0)
	foo.truncate()
	temp4 = re.sub('}\n{','},\n{',temp3)
	foo.write(temp4)

print('End Time is  : ',datetime.now())
