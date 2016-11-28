<!DOCTYPE html>
<%@ page import="java.io.*,java.util.*" %>
<html>
	<head>
		<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
		<meta charset = "utf-8">
    	<meta http-equiv = "X-UA-Compatible" content = "IE = edge">
    	<meta name = "viewport" content = "width = device-width, initial-scale = 1">
    	<link rel="icon" type="image/x-icon" href="images/favicon.ico">
  
		<title>Hello</title>
		<link href = "//maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css" rel = "stylesheet">
      
	</head>
	
	<body>
		<nav class="navbar navbar-inverse navbar-fixed-top">
	      <div class="container-fluid">
	        <div class="navbar-header">
	          <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
	            <span class="sr-only">Toggle navigation</span>
	            <span class="icon-bar"></span>
	            <span class="icon-bar"></span>
	            <span class="icon-bar"></span>
	          </button>
	          <a class="navbar-brand" href="#">C-STAR</a>
	        </div>
	        <div id="navbar" class="navbar-collapse collapse">
	          <ul class="nav navbar-nav navbar-right">
	            <li><a href="#">Dashboard</a></li>
	            <li><a href="#">Settings</a></li>
	            <li><a href="#">Profile</a></li>
	            <li><a href="#">Help</a></li>
	          </ul>
	          <form class="navbar-form navbar-right">
	            <input class="form-control" placeholder="Search..." type="text">
	          </form>
	        </div>
	      </div>
	    </nav>
	
		<center>
		<h1>  </h1>
		<p> ... </p>
		<h1>Well done Brian</h1>
		</center>
		Hello Cstar the best<br>
		<p>Today's date: <%= (new java.util.Date()).toLocaleString()%></p>
		<%out.println("Your IP address is " + request.getRemoteAddr());%>
		<center>
		<h2>Auto Refresh Header Example</h2>
				<%
				   // Set refresh, autoload time as 1 second
				   response.setIntHeader("Refresh", 1);
				   // Get current time
				   Calendar calendar = new GregorianCalendar();
				   String am_pm;
				   int hour = calendar.get(Calendar.HOUR);
				   int minute = calendar.get(Calendar.MINUTE);
				   int second = calendar.get(Calendar.SECOND);
				   if(calendar.get(Calendar.AM_PM) == 0)
				      am_pm = "AM";
				   else
				      am_pm = "PM";
				   String CT = hour+":"+ minute +":"+ second +" "+ am_pm;
				   out.println("Current Time is: " + CT + "\n");
				%>
		</center>
		
		<!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
    	<script src = "https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
      
    	<!-- Include all compiled plugins (below), or include individual files as needed -->
    	<script src = "//maxcdn.bootstrapcdn.com/bootstrap/3.3.1/js/bootstrap.min.js"></script>
      
	</body>
	
</html>