type file;
app (file stdout,file stderr,file output) cleaner(file script, file input){
	cleaner @script @input @output stdout=@stdout stderr=@stderr;
}
app (file stdout,file stderr,file output) concatScript(file concatScript,file input){
	concatScript @concatScript @input @output stdout=@stdout stderr=@stderr;
}

file script<single_file_mapper; file="C:\\Rdcep Github\\Ben Git Stuff\\Cleaner.Swift.py">;
file concatScript<single_file_mapper; file="C:\\Rdcep Github\\Ben Git Stuff\concatenatingScript.py">

file inputs[] <simple_mapper;location="C:\\Rdcep Github\\EPADataFiles",prefix="d",suffix=".csv">;
file outputs[]<simple_mapper;location="C:\\Rdcep Github\\Ben Git Stuff\\CleanedFiles",prefix="Cleaned",suffix=".csv">;
file input2<single_file_mapper;location="">
file output<single_file_mapper;location="">

foreach dirtyFile,i in inputs{
	file out<single_file_mapper;file=strcat("outputs\\out",i,".out")>;
	file error<single_file_mapper;file=strcat("errors\\err",i,".err")>;
	(out,error,outputs[i])=cleaner(script,dirtyFile);
	tracef("Testing");
}
 
file outp<single_file_mapper;file=strcat("outputs\\","concatOutput",".out")>
file err<single_file_mapper;file=strcat("outputs\\","concaterr",".err")>
(outp,err,output)=concatScript(concatScript, input2);

#Run PHP sqlizing script