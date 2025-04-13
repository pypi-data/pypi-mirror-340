def execs(code,num_type=float):
	m={}
	lines=code.splitlines()
	for i in lines:
		if i.strip():
			ltk=[j.strip() for j in i.split()]
		else:
			continue
		head=ltk[0]
		if head=="WT":
			m[ltk[1]]=num_type(ltk[2])
		elif head=="ADD":
			m[ltk[1]]+=m[ltk[2]]
		elif head=="SUB":
			m[ltk[1]]-=m[ltk[2]]
		elif head=="MUL":
			m[ltk[1]]*=m[ltk[2]]
		elif head=="DIV":
			m[ltk[1]]/=m[ltk[2]]
		elif head=="MOD":
			m[ltk[1]]%=m[ltk[2]]
		elif head=="COPY":
			m[ltk[1]]=m[ltk[2]]
		elif head=="FREE":
			del m[ltk[1]]
		elif head=="POW":
			m[ltk[1]]**=m[ltk[2]]
		elif head=="RD":
			print(m.get(ltk[1]))
		else:
			print(f"Error:{repr(head)} is not in command_list.We have WT,ADD,SUB,MUL,DIV,MOD,COPY,FREE,POW,RD.Line_tokens:{ltk}")
	return m
if __name__=="__main__":
	m=execmas("""
	WT 0x01 10
	WT 0x02 2
	POW 0x01 0x02
	RD 0x01
	FREE 0x01
	FREE 0x02
	ABC 1
	""")