"use strict";

var $ = function (id) { return document.getElementById(id); };

// var testFun = function()
// {
// 	console.log("testFun");
// };

var createTable = function()
{
	var html = "";
	html += "<div id=\"north\"></div>" +
			"<div id=\"west\"></div>" +
			"<div id=\"east\"></div>" +
			"<div id=\"south\"></div>" +
			"<div id=\"center\"></div>" +
			"<div id=\"northplay\"></div>" +
			"<div id=\"westplay\"></div>" +
			"<div id=\"eastplay\"></div>" +
			"<div id=\"southplay\"></div>" + 
			"<div id=\"northComSpace\"></div>" + 
			"<div id=\"westComSpace\"></div>" + 
			"<div id=\"eastComSpace\"></div>" + 
			"<div id=\"southComSpace\"></div>" + 
			"<div id=\"northpoints\"></div>" + 
			"<div id=\"westpoints\"></div>" + 
			"<div id=\"eastpoints\"></div>" + 
			"<div id=\"southpoints\"></div>";
	$("game_table").innerHTML = html;
	
	html = "";
	for(var i = 1; i <= 6; i++) html += "<a href=\"#\" id=\"handNcard" + i + "\"><img></a>";
	$("north").innerHTML = html;
	
	html = "";
	for(var i = 1; i <= 6; i++) html += "<a href=\"#\" id=\"handWcard" + i + "\"><img></a>";
	$("west").innerHTML = html;
	
	var html = "";
	for(var i = 1; i <= 6; i++) html += "<a href=\"#\" id=\"handEcard" + i + "\"><img></a>";
	$("east").innerHTML = html;
	
	html = "";
	for(var i = 1; i <= 6; i++) html += "<a href=\"#\" id=\"handScard" + i + "\"><img></a>";
	$("south").innerHTML = html;
	
	$("northplay").innerHTML = "<a href=\"#\" id=\"zoneN\"><img></a>";
	$("westplay").innerHTML = "<a href=\"#\" id=\"zoneW\"><img></a>";
	$("eastplay").innerHTML = "<a href=\"#\" id=\"zoneE\"><img></a>";
	$("southplay").innerHTML = "<a href=\"#\" id=\"zoneS\"><img></a>";
	$("center").innerHTML = "<a href=\"#\" id=\"zoneC\"><img></a>";
};
	
var styleTable = function()
{
	var tableLength = 500; //can be edited, minimum should be 500
	var fanDistance = 40; //can be edited, allows overlapping of cards in players' hands. Minimum of 10 to still see cards
	
	var cardWidth = 71;
	var cardHeight = 96;
	var playSpaceVertical = Math.floor((tableLength - cardHeight)/4);
	var playSpaceHorizontal = Math.floor((tableLength - cardWidth)/2);
	var centerVertical = Math.floor((tableLength - cardHeight)/2);
	var centerHorizontal = Math.floor((tableLength - cardWidth)/2);
	var handLength = 5*fanDistance + cardWidth;
	var handHorizontal = Math.floor((tableLength - handLength)/2);
	
	$("game_table").style.height = tableLength + "px";
	$("game_table").style.width = tableLength + "px";
	
	$("north").style.height = cardHeight + "px";
	$("north").style.width = handLength + "px";
	$("north").style.top = "0px";
	$("north").style.left = handHorizontal + "px";
	
	$("west").style.height = handLength + "px";
	$("west").style.width = cardHeight + "px";
	$("west").style.top = handHorizontal + "px";
	$("west").style.left = "0px";
	
	$("east").style.height = handLength + "px";
	$("east").style.width = cardHeight + "px";
	$("east").style.bottom = handHorizontal + "px";
	$("east").style.right = "0px";
	
	$("south").style.height = cardHeight + "px";
	$("south").style.width = handLength + "px";
	$("south").style.bottom = "0px";
	$("south").style.left = handHorizontal + "px";
	
	$("center").style.height = cardHeight + "px";
	$("center").style.width = cardWidth + "px";
	$("center").style.top = centerVertical + "px";
	$("center").style.left = centerHorizontal + "px";
	
	$("northplay").style.height = cardHeight + "px";
	$("northplay").style.width = cardWidth + "px";
	$("northplay").style.top = playSpaceVertical + "px";
	$("northplay").style.left = playSpaceHorizontal + "px";
	
	$("westplay").style.height = cardWidth + "px";
	$("westplay").style.width = cardHeight + "px";
	$("westplay").style.top = playSpaceHorizontal + "px";
	$("westplay").style.left = playSpaceVertical + "px";
	
	$("eastplay").style.height = cardWidth + "px";
	$("eastplay").style.width = cardHeight + "px";
	$("eastplay").style.top = playSpaceHorizontal + "px";
	$("eastplay").style.right = playSpaceVertical + "px";
	
	$("southplay").style.height = cardHeight + "px";
	$("southplay").style.width = cardWidth + "px";
	$("southplay").style.bottom = playSpaceVertical + "px";
	$("southplay").style.left = playSpaceHorizontal + "px";

	$("northComSpace").style.height = cardHeight + "px";
	$("northComSpace").style.width = cardWidth + "px";
	$("northComSpace").style.top = 0;
	$("northComSpace").style.left = 0;

	$("westComSpace").style.height = cardWidth + "px";
	$("westComSpace").style.width = cardHeight + "px";
	$("westComSpace").style.bottom = 0;
	$("westComSpace").style.left = 0;

	$("eastComSpace").style.height = cardWidth + "px";
	$("eastComSpace").style.width = cardHeight + "px";
	$("eastComSpace").style.top = 0;
	$("eastComSpace").style.right = 0;

	$("southComSpace").style.height = cardHeight + "px";
	$("southComSpace").style.width = cardWidth + "px";
	$("southComSpace").style.bottom = 0;
	$("southComSpace").style.right = 0;

	$("northpoints").style.height = 40 + "px";
	$("northpoints").style.width = 90 + "px";
	$("northpoints").style.top = playSpaceVertical + "px";
	$("northpoints").style.left = 110 + "px";

	$("westpoints").style.height = 40 + "px";
	$("westpoints").style.width = 90 + "px";
	$("westpoints").style.bottom = 150 + "px";
	$("westpoints").style.left = 110 + "px";

	$("eastpoints").style.height = 40 + "px";
	$("eastpoints").style.width = 90 + "px";
	$("eastpoints").style.top = playSpaceVertical + "px";
	$("eastpoints").style.right = 110 + "px";

	$("southpoints").style.height = 40 + "px";
	$("southpoints").style.width = 90 + "px";
	$("southpoints").style.bottom = 150 + "px";
	$("southpoints").style.right = 110 + "px";

	var cards = $("north").getElementsByTagName("img");
	for(var i = 0; i < cards.length; i++)
	{
		cards[i].parentElement.style.position = "absolute";
		cards[i].parentElement.style.top = "0px";
		cards[i].parentElement.style.left = i*fanDistance + "px";
		// cards[i].parentElement.style.right = i*fanDistance + "px";
	}
	cards = $("west").getElementsByTagName("img");
	for(var i = 0; i < cards.length; i++)
	{
		cards[i].parentElement.style.position = "absolute";
		cards[i].parentElement.style.top = i*fanDistance + "px";
		cards[i].parentElement.style.left = cardHeight + "px";
	}
	cards = $("east").getElementsByTagName("img");
	for(var i = 0; i < cards.length; i++)
	{
		cards[i].parentElement.style.position = "absolute";
		cards[i].parentElement.style.top = i*fanDistance + "px";
		// cards[i].parentElement.style.bottom = i*fanDistance-25 + "px";
		cards[i].parentElement.style.right = cardHeight + "px";
	}
	cards = $("south").getElementsByTagName("img");
	for(var i = 0; i < cards.length; i++)
	{
		cards[i].parentElement.style.position = "absolute";
		cards[i].parentElement.style.top = "0px";
		cards[i].parentElement.style.left = i*fanDistance + "px";
	}
	
	cards = $("northplay").getElementsByTagName("img");
	cards[0].parentElement.style.position = "absolute";
	cards[0].parentElement.style.top = "0px";
	cards[0].parentElement.style.left = "0px";
	
	cards = $("westplay").getElementsByTagName("img");
	cards[0].parentElement.style.position = "absolute";
	cards[0].parentElement.style.top = "0px";
	cards[0].parentElement.style.left = cardHeight + "px";
	
	cards = $("eastplay").getElementsByTagName("img");
	cards[0].parentElement.style.position = "absolute";
	cards[0].parentElement.style.top = "0px";
	cards[0].parentElement.style.right = cardHeight + "px";
	
	cards = $("southplay").getElementsByTagName("img");
	cards[0].parentElement.style.position = "absolute";
	cards[0].parentElement.style.top = "0px";
	cards[0].parentElement.style.left = "0px";

	

};

