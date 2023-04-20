# BFC-SUITE
Files relating to the BFC Programming Language Suite, which compiles and assembles down to BrainF***

Note: .ef files will always provide the most up-to-date releases of any programs, and .html releases (except for bfc-asm.html, which should remain unchanged indefinitely) are currently considered deprecated, though do contain useful manuals. 

# .ef files: 
bfc-asm.ef: <br>
Usage: rjef /dir/bfc-asm.ef -fi [input file] [Optional: -fo [output file]] [Optional: -p -- print output]<br>
bfc-clr.ef:<br>
Usage: rjef /dir/bfc-clr.ef -fi [input file] [Optional: -fo [output file]] [Optional: -p -- print output] [Optional: -l [file to link before code, order as code]]<br>

# .py files:
bfc-asm-py.py: <br>
Usage: python bfc-asm-py.py (-fi, -i) [input file] [Optional: (-fo, -o) [output file]] [Optional: -p -- print output]<br>
bfc-clr-py.py:<br>
Usage: python bfc-clr-py.py (-fi, -i) [input file] [Optional: (-fo, -o) [output file]] [Optional: -p -- print output] [Optional: -l [file to link before code, order as code]]<br>

# .html files:
Open them. <br>
Read. <br>

# Other files: 
bfc_clr_std.h is a heading file for bfc-clr, and can be linked either via #include or -l in the commandline parameters. 
