#Update index and maven project
Go to 	: 	windows->preferences->maven
Uncheck : 	Do not automatically update dependencies from repo
Check 	: 	Download repository index update on startup 
			Update Maven project on startup
#Restart eclipse to download index					  
Go to 	:file->Restart
And		:windows->ShowView->Other->Progress

#If Compiler Problem
Go to 	: windows->preferences->java->installed jre->Execution Environment


#Run project		
Right click on cstar project->Run As->Maven Build
Write in Goal box : "spring-boot:run"

#Browser
http://localhost:8080/hello
		