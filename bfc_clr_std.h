#define_macro }
    endif;
#endmacro
#define_macro .
    endloop;
#endmacro
#define_macro_feed ? "#endmacro"; //Only available in macros -- macro_feeds are macro special definition commands
#define_macro cout_endl str
    cout $str$;
    cout "\n";
#endmacro
