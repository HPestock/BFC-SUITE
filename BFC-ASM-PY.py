
import sys
import os

program = "";

repldct = [
["setup n",">-<{n}><+[<+]+<"], #//setup (final allocated memory index): initializes memory format
["set c x","{c}>[-]+{x}+{c}<"], #//set (cell) (value): sets cell (cell) to (value)
["mvr c","{c}>"],#//mvr (amt): move pointer right by (amt)
["dec c x","{c}>{x}-{c}<"],#//dec (cell) (amt): decrements cell (cell) by (amt)
["inc c x","{c}>{x}+{c}<"],#//inc (cell) (amt): increments cell (cell) by (amt)
["goto c","[<]{c}>"],#//goto (cell): sets pointer to (cell)
["gotof_ncz c","<[<]{c}>"],#//gotof_ncz (cell): sets pointer to (cell), do not use if at cell 0
["mv i o","{o}>[-]+{o}<{i}>-[-{i}<{o}>+{o}<{i}>]+{i}<"],#//mv (input cell) (output cell): sets cell (output cell) to value at (input cell), then sets value at (input cell) to 0
["printaz char","{char}+.[-]"],#//printaz (character number): prints character with numerical code (character number), use when at cell 0
["printanz char","{char}+.[-]+"],#//printanz (character number): prints character with numerical code (character number), use when not at cell 0
["getchar store","{store}>,+{store}<"],#//getchar (cell): stores input char at cell (cell)
["loop x","{x}>-[+{x}<"],#//loop (cell): start of loop, will halt when value at (cell) is 0; make sure value at (cell) is not 0 or -1, otherwise issues will occur
["endloop x","{x}>-]+{x}<"],#//endloop (cell): end of loop, will halt and continue if value at (cell) is 0, otherwise jumps to start of loop
["if x","{x}>-[+{x}<"],#//if (cell): start of if statement, will execute if value at (cell) is not 0
["endif x","{x}>[-]]+{x}<"],#//endif (cell): end of if statement (cell)
["inv ct cs w","{cs}>[-]++{cs}<{w}>[-]+{w}<{ct}>-[+{ct}<{w}>[-]++{w}<{cs}>[-]+{cs}<{ct}>[-]][-]+{ct}<{w}>-[-{w}<{ct}>+{ct}<{w}>]+{w}<"],#//inv (cell i) (cell p) (cell w): if (cell i) is equal to 0 will set (cell i) to 0 and (cell p) to 1, if (cell i) is equal to 1 will set (cell i) to 1 and (cell p) to 0, uses (cell w) for temporary calculation memory allocation
["mvtr i o","{i}>-[-{i}<{o}>+{o}<{i}>]+{i}<"],#//mvtr (cell input) (cell output): will add the value at (cell input) to (cell output) and leave (cell input) set to 0
["mvab i a b","{i}>-[-{i}<{a}>+{a}<{b}>+{b}<{i}>]+{i}<"],#//mvab (cell input) (cell output a) (cell output b): will add the value at (cell input) to (cell output a) and (cell output b), leaves (cell input) set to 0
["getcharneq store comp w","{store}>[-]+{store}<{w}>,{comp}-[{w}<{store}>+{store}<{w}>[-]]+{w}<"],#//getcharneq (cell store) (comp) (cell w): gets input char, if input char is not equal to (comp) sets (cell store) to 1, otherwise sets (cell store) to 0, uses (cell w) for temporary calculation memory allocation
["mult a b o w","{a}>-[+{a}<{b}>-[-{b}<{o}>+{o}<{w}>+{w}<{b}>]+{b}<{w}>-[-{w}<{b}>+{b}<{w}>]+{w}<{a}>--]+{a}<"],#//mult (cell input a) (cell input b) (cell output) (cell w): sets (cell output) to product of (cell input a) and (cell input b), sets (cell input a) to 0 and preserves (cell input b), uses (cell w) for temporary calculation memory allocation
["printcell c","{c}>-.+{c}<"],#//printcell (cell): prints character at (cell)
["startprintcell c","{c}>-.+"],#//startprintcell (cell): prints character at (cell) without returning to cell 0, use printnext to continue, use endprint to finish
["printnext",">-.+"],#//printnext: prints next character in memory
["endprint","[<]"],#//endprint: ends print sequence
["printuntil c comp","{c}>{comp}--[{comp}++-.+>{comp}--]{comp}++<[<]"],#//printuntil (cell) (comp): print all characters starting from (cell) until first next cell equal to (comp); (comp) must be less than all characters in sequence, (comp) = 0 is recommended
["RAW_PLUS x","{x}+"],
["RAW_MINUS x","{x}-"],
["RAW_LEFT x","{x}<"],
["RAW_RIGHT x","{x}>"],
["RAW_OPBR x","{x}["],
["RAW_CLBR x","{x}]"],
["RAW_DOT x","{x}."],
["RAW_COMMA x","{x},"]
];

def rmws(s):
    ns = "";
    hnws = False;
    qs = False;
    # print(s[1]);
    for i in range(len(s)):
        # si = s[i];
        # match(si):
        if(s[i]==" "):
            if(hnws):
                qs=True;
                hnws=False;
        elif(s[i]=="\n"):
            ns+="\n";
            qs=False;
            hnws=False;
        else:
            if(s[i]!="\t" and s[i]!="\f" and s[i]!="\r" and s[i]!="\v"):
                if(qs):
                    ns+=" ";
                    qs=False;
                ns+=s[i];
                hnws=True;
    return ns;

def getrepldct(line):
    ls = line.split(" ");
    rs = -1;
    i = 0;
    j = 0;
    for i in range(len(repldct)):
        if(ls[0]==repldct[i][0].split(" ")[0]):
            rs = i;
            break;
    if(rs==-1):
        return "";
    else:
        ref = repldct[rs][0].split(' ');
        str = repldct[rs][1];
        newstr = "";
        brm = False;
        br = "";
        amt = 1;
        for i in range(len(str)):
            if(brm):
                if(str[i]=="}"):
                    brm=False;
                    for j in range(1, len(ref)):
                        if(br==ref[j]):
                            amt = int(ls[j]);
                else:
                    br+=str[i];
            else:
                if(str[i]=="{"):
                    brm=True;
                    br = "";
                else:
                    for j in range(amt):
                        newstr+=str[i];
                    amt = 1;
        return newstr;

def compile(p0):
    out = "";
    p = p0.split("\n");
    print(len(p));
    for i in range(len(p)):
        out+=getrepldct(p[i]);
    return out;

def getCLIParams(inl):
    inpfile = "";
    outpfile = "";
    outpcli = False;
    skip=0;
    for i in range(1, len(inl)):
        if(inl[i]=="-fi" or inl[i]=="-i") and skip==0:
            if(len(inl)-i>1):
                inpfile=inl[i+1];
                # skip=1;
        elif(inl[i]=="-fo" or inl[i]=="-o") and skip==0:
            if(len(inl)-i>1):
                outpfile=inl[i+1];
                # skip=1;
        elif(inl[i]=="-p") and skip==0:
            outpcli=True;
        if(skip!=0):
            skip=skip-1;
    return [inpfile,outpfile,outpcli];

if __name__ == "__main__":
    # print(sys.argv[0]);
    # print(repldct);

    # print(rmws(" a   b   c  \n   A   b   C"));
    # print("a b c d e".split(" ")[0]);

    # print(compile( rmws("setup 1\ngoto 1\n") ));
    # print(sys.argv);

    params = getCLIParams(sys.argv);
    # print(params);
    f_obj = open(params[0], 'r');
    # fo_obj= open(params[1], 'x');
    program = f_obj.read();
    outputfilecontents = compile(rmws(program));
    if(params[2]):
        print(outputfilecontents);
    # if(os.path.exists(params[1])):
    #     os.remove(params[1]);
    fo_obj = open(params[1], 'w');
    fo_obj.write(outputfilecontents);
    f_obj.close();
    fo_obj.close();