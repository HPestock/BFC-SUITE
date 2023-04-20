# BFC-CLR PY
# RELEASE 04192023-2207-01-BRANCH

import sys

# program = "int a 1;int b 2;int t;set %b 3;set %a %b %t;test;";
# program = "test;";
program = "#memory 26;int a 65;cout %a;cout \"\\n\";";

varnames = [];
vartypes = [];
varinfo = [];
macronames = [];
macros = [];
macroargs = [];
macrofeednames = [];
macrofeeds = [];

def feedtype(s):
	if(s[0]=="'"):
		return "char";
	elif(s[0]=="\""):
		return "string";
	elif(s[0]=="_"):
		return "const";
	elif(s[0]=="%"):
		return "var";
	# elif(s==True or s==False):
	#     return "lit";
	else:
		return "lit";

def getlistfrcurstr(str):
	inq = False;
	temp = "";
	out = [];
	esc = False;
	qchar = "";
	for i in range(len(str)):
		if(esc):
			temp=temp+str[i];
			esc=False;
		elif(inq):
			if(str[i]=="\\"):
				esc=True;
			temp=temp+str[i];
			if(str[i]==qchar and esc==False):
				inq=False;
		elif(str[i]=="\\"):
			esc=True;
		elif(str[i]=="\"" or str[i]=="'"):
			qchar=str[i];
			temp=temp+qchar;
			inq=True;
		elif(str[i]==" "):
			out.append(temp);
			temp="";
		else:
			temp=temp+str[i];
	if(temp!=""):
		out.append(temp);
	return out;

def rmws(str):
	hitws = True;
	qws = False;
	out = "";
	esc = False;
	inq = False;
	qchar = "";
	hitany = False;
	for i in range(len(str)):
		if(inq):
			if(esc):
				if(str[i]=="n"):
					out=out+"n";
				elif(str[i]=="\""):
					out=out+"\"";
				elif(str[i]=="'"):
					out=out+"'";
				else:
					out=out+str[i];
				esc=False;
			elif(str[i]=="\\"):
				esc=True;
				out=out+"\\";
			elif(str[i]==qchar):
				inq=False;
				out=out+qchar;
				if(qws):
					qws=False;
					out=out+" ";
				hitws=False;
			else:
				out=out+str[i];
		else:
			if(esc):
				if(str[i]=="n"):
					out=out+"\n";
				elif(str[i]=="\""):
					out=out+"\"";
				elif(str[i]=="'"):
					out=out+"'";
				esc=False;
			elif(str[i]=="\\"):
				if(qws):
					qws=False;
					out=out+" ";
				hitws=False;
				esc=True;
				hitany=True;
			elif(str[i]=="\"" or str[i]=="'"):
				if(qws):
					qws=False;
					out=out+" ";
				hitws=False;
				inq=True;
				qchar=str[i];
				out=out+str[i];
				hitany=True;
			elif(str[i]=="\n" or str[i]==";"):
				if(hitany):
					hitws=True;
					qws=False;
					out=out+";";
					hitany=False;
			elif(str[i]==" " or str[i]=="\t"):
				if(False==hitws):
					hitws=True;
					qws=True;
				hitany=True;
			else:
				if(qws):
					qws=False;
					out=out+" ";
				hitws=False;
				out=out+str[i];
				hitany=True;
	return out;

def formtypetolit(s):
	i = 0;
	if(s[0]=="'"):
		if(len(s)>2):
			if(s[1:3]=="\\n"):
				return ord("\n");
		return ord(s[1]);
	elif(s[0]=="\""):
		return s[1:len(s)-1];
	elif(s[0]=="_"):
		# c = -1;
		for i in range(len(varnames)):
			if(s==varnames[i] and vartypes[i]=="_"):
				return varinfo[i];
		return -1;
	elif(s[0]=="%"):
		# v = -1;
		for i in range(len(varnames)):
			if(s==varnames[i] and (vartypes[i]=="i" or vartypes[i]=="c" or vartypes[i]=="b")):
				return varinfo[i];
		return -1;
	elif(s=="true"):
		return 1;
	elif(s=="false"):
		return 0;
	else:
		return int(s);

def addVar(name,type,info):
	if(type=="const"):
		varnames.append("_"+name);
		vartypes.append("_");
		varinfo.append(info);
		return;
	elif(type=="int"):
		varinfo.append(getnextunresvcell());
		varnames.append("%"+name);
		vartypes.append("i");
		return;
	elif(type=="char"):
		varinfo.append(getnextunresvcell());
		varnames.append("%"+name);
		vartypes.append("c");
		return;
	elif(type=="bool_cell"):
		varinfo.append(getnextunresvcell());
		varnames.append("%"+name);
		vartypes.append("b");
		return;

def getnextunresvcell():
	# return -2;
	a = 0;

	# print(len(vartypes)-len(varinfo));

	l = len(vartypes);
	i=0;
	while(i<l):
		if(vartypes[i]=="c" or vartypes[i]=="i" or vartypes[i]=="b"):
			if(varinfo[i]==a):
				a=a+1;
				i=-1;
		i=i+1;
	return a;

def retfile(dir):
	f = open(dir,'r');
	ret = f.read();
	f.close();
	return ret;

def getCLIParams(inl):
	# null_func();
	# print("Function \{getCLIParams(inl)\ has not been implemented. ");
	inpfile = "";
	outpfile = "";
	outpcli = False;
	linkfile = "";
	iskip = 0;
	for i in range(1,len(inl)):
		# switch(inl[i]){
		if(iskip>0):
			iskip=iskip-1;
			continue;
		if inl[i] == "-fi" or inl[i] == "-i":
			if(len(inl)-i>1):
				inpfile=inl[i+1];
				# i+=1;
				iskip=1;
			# break;
		if inl[i] == "-fo" or inl[i] == "-o":
			if(len(inl)-i>1):
				outpfile=inl[i+1];
				# i+=1;
				iskip=1;
			# break;
		if inl[i] == "-p":
			outpcli = True;
			# break;
		if inl[i] == "-l":
			if(len(inl)-i>1):
				linkfile+=retfile(inl[i+1]);
				#i+=1;
				iskip=1;
			# break;
	return [inpfile,outpfile,outpcli,linkfile];

def runtime_link(f_dir_relative,cur_pc,pr):
	# print("Function \{runtime_link(f_dir_relative,cur_pc,pr)\ has not been implemented. ");
	f = retfile(f_dir_relative);
	pr2=pr[0:cur_pc+1]+rmws(f)+pr[cur_pc:len(pr)];
	# //console.log(pr);
	return pr2;

def null_func():
	return;

def compile(P):
	p = rmws(P);
	ifs = [];
	loops = [];
	varnames = [];
	vartypes = [];
	varinfo = [];

	i = 0;
	curstr = "";

	inmacro = False;
	curmacro = "";

	start = 0;

	out = "";

	COND_COMP_FOR_MAIN_END = len(p);
	while(i<=COND_COMP_FOR_MAIN_END):

		if(i>=len(p)):
			break;

		if(p[i]==";" or (i==COND_COMP_FOR_MAIN_END and curstr!="")):
			l = getlistfrcurstr(curstr);

			if(inmacro):
				for j in range(len(macrofeednames)):
					if(l[0]==macrofeednames[0]):
						l[0]=macrofeeds[0];
				if(l[0]=="#endmacro"):
					inmacro=False;
					macros.append(curmacro);
				elif(l[0]=="?>"):
					curmacro=curmacro+("".join(l[1:len(l)]));
				else:
					curmacro=curmacro+curstr+";";
			else:
				if(l[0][0]=="/" and l[0][1]=="/"):
					null_func();
				elif(l[0]=="test"):
					out=out+"testsuccess\n";
					# # //console.log("test");
				elif(l[0]=="int"):
					if(len(l)==2):
						addVar(l[1],"int","");
					elif(len(l)>2):
						addVar(l[1],"int","");
						out=out+"set "+str(formtypetolit("%"+l[1]))+" "+str(formtypetolit(l[2]))+"\n";
					
					# //console.log(l);
				elif(l[0]=="char"):
					if(len(l)==2):
						addVar(l[1],"char","");
					elif(len(l)>2):
						addVar(l[1],"char","");
						out=out+"set "+str(formtypetolit("%"+l[1]))+" "+str(formtypetolit(l[2]))+"\n";
					
					# //console.log(l);
				elif(l[0]=="bool_cell"):
					if(len(l)==2):
						addVar(l[1],"bool_cell","");
					elif(len(l)>2):
						addVar(l[1],"bool_cell","");
						out=out+"set "+str(formtypetolit("%"+l[1]))+" "+str(formtypetolit(l[2]))+"\n";
					
					# //console.log(l);
				elif(l[0]=="#const"):
					if(len(l)>2):
						addVar(l[1],"const",formtypetolit(l[2]));
					
					# //console.log(l);
				elif(l[0]=="cout"):
					t = feedtype(l[1]);
					# switch(t):
					# case "char":
					if(t=="char"):
						out=out+"printaz "+str(formtypetolit(l[1]))+"\n";
						# break;
					elif t == "string":
						# for(ti=1;ti<l[1].length-1;ti++):
						iskip=False;
						# print(l[1]);
						for ti in range(1,len(l[1])-1):
							if(iskip):
								iskip=False;
								continue;
							if(ti<len(l[1])-2):
								print(l[1][ti:ti+2]);
								if(l[1][ti:ti+2]=="\\n"):
									out=out+"printaz "+str(ord("\n"))+"\n";
									iskip=True;
								elif(l[1][ti:ti+2]=="\\\""):
									out=out+"printaz "+str(ord("\""))+"\n";
									iskip=True;
								elif(l[1][ti:ti+2]=="\\\\"):
									out=out+"printaz "+str(ord("\\"))+"\n";
									iskip=True;
								else:
									out=out+"printaz "+str(ord(l[1][ti]))+"\n";
							else:
								out=out+"printaz "+str(ord(l[1][ti]))+"\n";
						# break;
					elif t == "const":
						out=out+"printaz "+str(formtypetolit(l[1]))+"\n";
						# break;
					elif t == "var":
						out=out+"printcell "+str(formtypetolit(l[1]))+"\n";
						# break;
					elif t == "lit":
						out=out+"printaz "+str(formtypetolit(l[1]))+"\n";
						# break;
					
				elif(l[0]=="if"):
					ifs.append(formtypetolit(l[1]));
					out=out+"if "+ifs[len(ifs)-1]+"\n";
				elif(l[0]=="endif"):
					out=out+"endif "+ifs[len(ifs)-1]+"\n";
					ifs.pop();
				elif(l[0]=="loop"):
					loops.append(formtypetolit(l[1]));
					out=out+"loop "+loops[len(loops)-1]+"\n";
				elif(l[0]=="endloop"):
					out=out+"endloop "+loops[len(loops)-1]+"\n";
					loops.pop();
				elif(l[0]=="#memory"):
					out=out+"setup "+str(formtypetolit(l[1]))+"\n";
				elif(l[0]=="#automemorycellz"):
					out=out+"RAW_MINUS 2\nRAW_OPBR 1\nRAW_MINUS 1\nRAW_RIGHT 1\nRAW_PLUS 1\nRAW_LEFT 1\nRAW_CLBR 1\nRAW_RIGHT 1\nRAW_MINUS 1\nRAW_OPBR 2\nRAW_RIGHT 1\nRAW_CLBR 1\nRAW_PLUS 1\nRAW_OPBR 1\nRAW_LEFT 1\nRAW_CLBR 1\nRAW_RIGHT 1\nRAW_MINUS 1\nRAW_CLBR 1\nRAW_PLUS 1\nRAW_LEFT 1\n";
				elif(l[0]=="#RAW"):
					out=out+str(formtypetolit(l[1]))+"\n";
				elif(l[0]=="#RAW_NOLF"):
					out=out+str(formtypetolit(l[1]));
				elif(l[0]=="set"):
					ft = feedtype(l[2]);
					if(ft=="char" or ft=="const" or ft=="lit"):
						out=out+"set "+str(formtypetolit(l[1]))+" "+str(formtypetolit(l[2]))+"\n";
					elif(ft=="var"):
						# //mvtr i t
						# //mvab t i o
						out=out+"mvtr "+str(formtypetolit(l[2]))+" "+str(formtypetolit(l[3]))+"\nset "+str(formtypetolit(l[1]))+" 0\nset "+str(formtypetolit(l[2]))+" 0\nmvab "+str(formtypetolit(l[3]))+" "+str(formtypetolit(l[1]))+" "+str(formtypetolit(l[2]))+"\n";
						# print(l);
				elif(l[0]=="cin"):
					out=out+"getchar "+str(formtypetolit(l[1]))+"\n";
				elif(l[0]=="#define_macro"):
					inmacro=True;
					macronames.append(l[1]);
					if(len(l)>2):
						macroargs.append(l[2:len(l)]);
						# //console.log(l[1]);
					else:
						macroargs.append(False);
					
					# //console.log(l[1]);
					# //console.log(macroargs);
					# //macros.append();
					curmacro="";
				elif(l[0]=="#domacro"):
					o = "";
					a = False;
					for j in range(len(macronames)):
						if(macronames[j]==l[1]):
							o=macros[j];
							a=macroargs[j];
							# //console.log(macroargs[j]);
							# //console.log(macroargs);
						
					
					# //console.log(a);
					# //console.log(o);
					if(a!=False):
						# //console.log(a);
						m = False;
						astr = "";
						esc = False;
						me = 0;
						# //me;
						# //mch = [];
						# //console.log(o);
						for j in range(len(o)):
							if(m):
								if(o[j]=="n" or o[j]=="\n"):
									# //console.log(o[j]+": "+j);
									null_func();
								if(o[j]=="\\"):
									astr=astr+"\\";
									esc=True;
								elif(esc):
									# //console.log(o[j]);
									# //if(o[j]=="n"):
									# //    astr+="\n";
									# //else:
										astr=astr+o[j];
										esc=False;
									# //
								elif(o[j]=="$"):
									m=False;
									k=0;
									# //console.log(a);
									# //console.log("astr: "+astr);
									for k in range(len(a)):
										if(a[k]==astr):
											# //console.log("k: "+k);
											break;
										
									
									# //console.log(l);
									# //console.log(l[k+2]);
									# //console.log(o.slice(j+1,o.length));
									# //console.log(o.slice(0,me));
									o = o[0:me]+l[k+2]+o[j+1:len(o)];
									j=j+len(l[k+1]);
									# //console.log(o);
									# //console.log(j);
								else:
									astr=astr+o[j];
								
							else:
								if(o[j]=="\\"):
									esc=True;
								elif(esc):
									esc=False;
								elif(o[j]=="$"):
									m=True;
									me=j;
								
							
						
					
					# //console.log(o);
					# //console.log(macronames);
					p=p[0:start]+o+p[i+1:len(p)];
					i=start-1;
					# //console.log(p);
				elif(l[0]=="inc"):
					out=out+"inc "+str(formtypetolit(l[1]))+" "+str(formtypetolit(l[2]))+"\n";
				elif(l[0]=="dec"):
					out=out+"dec "+str(formtypetolit(l[1]))+" "+str(formtypetolit(l[2]))+"\n";
				elif(l[0]=="mult"):
					out=out+"mult "+str(formtypetolit(l[1]))+" "+str(formtypetolit(l[2]))+" "+str(formtypetolit(l[3]))+" "+str(formtypetolit(l[4]))+"\n";
				elif(l[0]=="#include"):
					p = runtime_link(formtypetolit(l[1]),i,p);# //#include "/dir/file.ext" OR conststr="/dir/file.ext";#include _conststr -- DOES NOT ACCEPT VARIABLES, SINCE RETURNS VARPOINTER
					# //console.log(p.charAt(i));
					# //console.log(p.charAt(i+1));
				elif(l[0]=="#define_macro_feed"):
					macrofeednames.append(l[1]);
					macrofeeds.append(formtypetolit(l[2]));
				else:
					# //console.log("unidentified token, attempting macro");
					o = "";
					a = False;
					for j in range(len(macronames)):
						if(macronames[j]==l[0]):
							o=macros[j];
							a=macroargs[j];
						
					
					# //console.log(o);
					# //console.log(macronames);
					if(o!=""):
						# //a = False;
						null_func();
					# /*for(j=0;j<macronames.length;j++):
					# 	if(macronames[j]==l[1]):
					# 		o=macros[j];
					#		a=macroargs[j];
					#	
					# */
					# //console.log(o);
					# //console.log(a);
					if(a!=False):
						# //console.log(a);
						m = False;
						astr = "";
						esc = False;
						me = 0;
						# //me;
						# //mch = [];
						for j in range(len(o)):
							if(m):
								if(o[j]=="\\"):
									esc=True;
								elif(esc):
									# //if(o[j]=="n"):
									# //    astr+="\n";
									# //else:
										astr=astr+o[j];
										esc=False;
									# //
								elif(o[j]=="$"):
									m=False;
									k=0;
									# //console.log(a);
									# //console.log("astr: "+astr);
									for k in range(len(a)):
										if(a[k]==astr):
											# //console.log("k: "+k);
											break;
										
									
									# //console.log(l);
									o = o[0:me]+l[k+1]+o[j+1:len(o)];
									j=j+len(l[k+1]);
									# //console.log(o);
									# //console.log(j);
								else:
									astr=astr+o[j];
								
							else:
								if(o[j]=="\\"):
									esc=True;
								elif(esc):
									esc=False;
								elif(o[j]=="$"):
									m=True;
									me=j;
								
							
						
					
						p=p[0:start]+o+p[i+1:len(p)];
						i=start-1;
					else:
						# //Not a macro
						null_func();
					
					# //console.log(p);
				
			
			curstr="";
			start=i+1;

		elif(i<COND_COMP_FOR_MAIN_END):
			curstr=curstr+p[i];

		#END WHILE MAIN
		i=i+1;
	return out;

def main_py_impl():
	# print(rmws(program));
	# print(compile(program));
	# print(sys.argv);
	# return;
	params = getCLIParams(sys.argv);
	program = retfile(params[0]);
	outputfilecontents = compile(params[3]+program);
	if(params[2]):
		print(outputfilecontents);
	# placecheapfilelong(params[1],outputfilecontents);
	f = open(params[1],'w');
	f.write(outputfilecontents);
	f.close();

if __name__ == "__main__":
	main_py_impl();
	# print("abc");
	# print(formtypetolit("%b"));
	# print(varnames);
	# print(vartypes);
	# print(varinfo);