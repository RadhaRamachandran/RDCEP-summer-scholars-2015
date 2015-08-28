app (file stdout,file stderr,file output) geocodeScript(file geocodeScrips,file input){
	geocodeScript @geocodeScript @input @output stdout=@stdout stderr=@stderr;
}

file inputs[] <simple_mapper;location="/files/inputs/",suffix=".csv">;
file outputs[]<simple_mapper;location="/files/outputs/",prefix="Cleaned",suffix=".csv">;
file script<single_file_mapper; file="/files/geocoderPandas.py">;


foreach dirtyFile,i in inputs{
	file out<single_file_mapper;file=strcat("outputs/out",i,".out")>;
	file error<single_file_mapper;file=strcat("errors/err",i,".err")>;
	(out,error,outputs[i])=geocoder(script,dirtyFile);
}