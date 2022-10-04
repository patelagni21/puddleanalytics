var calculation = "";
var resultDone = false;
function addToCalc(val)
{
	if(isNaN(val) && isNaN(calculation.substring(calculation.length-1, calculation.length)))
		return false;
		
	if(!isNaN(val) && resultDone)
	{
		resetCalc();
		resultDone = false;
	}
	else if(isNaN(val) && resultDone)
	{
		resultDone = false;
	}
	calculation += val;
	showResult();
}
function addToCalcDirect(val)
{
	calculation = val;
}
function resetCalc()
{
	calculation = "";
	showResult();
}
function positiveNegative()
{
	if(calculation.substring(0, 1) == "-")
		calculation = calculation.substring(1, calculation.length);
	else
		calculation = "-" + calculation;
	showResult();
}
function calculate()
{
	if(calculation != "")
	{
		try
		{
			calculation = eval(calculation);
		}
		catch(e)
		{ 
			reportError("Error!");
		}
		resultDone = true;
		showResult();
	}
	else
		return false;	
}
function percentage()
{
	try
	{
		calculation = eval(calculation) / 100;
	}
	catch(e)
	{
		reportError("Error!");
	}
  	resultDone = true;
	showResult();
}
function squareRoot()
{
	try
	{
		calculation = Math.sqrt(eval(calculation));
	}
	catch(e)
	{ 
		reportError("Error!");
	}
	resultDone = true;
	showResult();
}
function showResult()
{
	calculation = calculation.toString();
	if(calculation == "NaN")
	{
		reportError("Error!");
	}
	else
	{
		document.getElementById("result").value = calculation;
	}
}
function reportError(msg)
{
	calculation = msg;
	document.getElementById("result").value = msg;
}
function closeCalculator()
{
	document.getElementById("calculator").style.display = "none";
}
function about()
{
	msg = "CJ Floating Calculator\n=============\n\n";
	msg += "Developed by James Crooke\nhttp://www.cj-design.com";
	alert(msg);
}
var ie = document.all;
var ns6 = document.getElementById && !document.all;
var dragapproved=false;
var z, x, y;

function move(e)
{
	if (dragapproved)
	{
		z.style.left=ns6? temp1+e.clientX-x: temp1+event.clientX-x;
		z.style.top=ns6? temp2+e.clientY-y : temp2+event.clientY-y;
		return false;
	}
}

function drags(e)
{
	if (!ie&&!ns6)
	return;
	var firedobj = ns6? e.target : event.srcElement;
	var topelement = ns6? "HTML" : "BODY";
	while (firedobj.tagName != topelement&&firedobj.className != "drag")
	{
		firedobj = ns6? firedobj.parentNode : firedobj.parentElement;
	}
	if (firedobj.className == "drag")
	{
		dragapproved = true;
		z = firedobj;
		temp1 = parseInt(z.style.left+0);
		temp2 = parseInt(z.style.top+0);
		x = ns6? e.clientX: event.clientX;
		y = ns6? e.clientY: event.clientY;
		document.onmousemove=move;
		return false;
	}
}
document.onmousedown=drags;
document.onmouseup=new Function("dragapproved=false");