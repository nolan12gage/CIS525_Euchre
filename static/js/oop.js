
var $ = function (id) { return document.getElementById(id); };

var table;

function Card(name) {  //name format is "c01" for A of clubs	
	this.name = name;
	this.cardSrc = "static/images/card_images/" + this.name + ".bmp";
	this.imgObject = "";
}

Card.prototype = {
    constructor: Card,
    setImgObject:function (imgObject)  {
		this.imgObject.src = "";
        this.imgObject = imgObject;
		this.refreshImg();
    },
	unlinkImgObject:function ()  {
		this.imgObject.src = "";
		this.imgObject = "";
		this.refreshImg();
    },
	turnDown:function ()  {
        this.cardSrc = "static/images/card_images/b1fv.bmp";
		this.refreshImg();
    },
	turnUp:function ()  {
        this.cardSrc = this.cardSrc = "static/images/card_images/" + this.name + ".bmp";
		this.refreshImg();
    },
	refreshImg:function ()  {

        this.imgObject.src = this.cardSrc;
    },
	showInfo:function ()  {
        console.log("name: " + this.name);
		console.log("cardSrc: " + this.cardSrc);
		if(this.imgObject == "")console.log("container: not assigned");
		else console.log("container: " + this.imgObject.parentElement.id);
    },
}

function Player(name, positionIndex, isHuman, handArray) {
	this.name = name;
	this.positionIndex = positionIndex;
	this.hand = [];
	this.isHuman = isHuman;
	this.id = "";
	
	var identifiers = ["south", "west", "north", "east"];
	this.id = identifiers[this.positionIndex];

	for(var i = 0; i < handArray.length; i++)
	{
		var tempCard = new Card(handArray[i]);
		this.addToHand(tempCard);
	}

	if(!this.isHuman)
	{
		for(var i = 0; i < handArray.length; i++)
		{
			this.hand[i].turnDown();
		}
	}
}

Player.prototype = {
    constructor: Player,
    addToHand:function (card)  {
        this.hand.push(card);
		var cardPosition = this.hand.length - 1;
		var imgObjects = $(this.id).getElementsByTagName("img");
		this.hand[cardPosition].setImgObject(imgObjects[cardPosition]);
    },
	clearOnClicks:function() {
		var cardImgArray = $(this.id).getElementsByTagName("img");
		cardImgArray[0].onclick = "";
		cardImgArray[1].onclick = "";
		cardImgArray[2].onclick = "";
		cardImgArray[3].onclick = "";
		cardImgArray[4].onclick = "";
		cardImgArray[5].onclick = "";
	},
	pickCardToPlay:function(clickableArray, mailTo){
		if(this.isHuman)
		{
			var position = this.positionIndex;
			var cardImgArray = $(this.id).getElementsByTagName("img");
			
			if(this.hand.length > 0 && clickableArray[0] == 1) cardImgArray[0].onclick = function() {table.seats[position].playCard('' + 0);}
			if(this.hand.length > 1 && clickableArray[1] == 1) cardImgArray[1].onclick = function() {table.seats[position].playCard('' + 1);}
			if(this.hand.length > 2 && clickableArray[2] == 1) cardImgArray[2].onclick = function() {table.seats[position].playCard('' + 2);}
			if(this.hand.length > 3 && clickableArray[3] == 1) cardImgArray[3].onclick = function() {table.seats[position].playCard('' + 3);}
			if(this.hand.length > 4 && clickableArray[4] == 1) cardImgArray[4].onclick = function() {table.seats[position].playCard('' + 4);}
		}
		else
		{
			console.log("not human")
		}
	},
	playCard:function(cardIndex){
		//console.log("you played: " + cardIndex);
		this.clearOnClicks();
		post('/get', cardIndex);
	},
	pickCardToDiscard()
	{
		if(this.isHuman)
		{
			var position = this.positionIndex;
			var cardImgArray = $(this.id).getElementsByTagName("img");
			
			cardImgArray[0].onclick = function() {table.seats[position].discardCard('' + 0);}
			cardImgArray[1].onclick = function() {table.seats[position].discardCard('' + 1);}
			cardImgArray[2].onclick = function() {table.seats[position].discardCard('' + 2);}
			cardImgArray[3].onclick = function() {table.seats[position].discardCard('' + 3);}
			cardImgArray[4].onclick = function() {table.seats[position].discardCard('' + 4);}
			cardImgArray[5].onclick = function() {table.seats[position].discardCard('' + 5);}
		}
		else
		{
			console.log("not human")
		}
	},
	discardCard:function(cardIndex){
		console.log("you discarded: " + cardIndex);
		this.clearOnClicks();
		post('/discard', cardIndex);
	},
};

function Zone(positionIndex, zoneArray) {
	this.positionIndex = positionIndex;
	this.card = "";
	this.id = "";
	
	var identifiers = ["southplay", "westplay", "northplay", "eastplay", "center"];
	this.id = identifiers[this.positionIndex];

	if(zoneArray != "")
	{
		var tempCard = new Card(zoneArray);
		this.addToZone(tempCard);
	}
};

Zone.prototype = {
    constructor: Zone,
    addToZone:function (card)  {
		if(this.card != "")
		{
			console.log("zone " + this.id + " already full");
		}
		else
		{
			this.card = card;
			var imgObject = $(this.id).getElementsByTagName("img")[0];
			this.card.setImgObject(imgObject);
		}
    },
};

function PointSpace(positionIndex, tricks, points, name) {
	this.positionIndex = positionIndex;
	this.tricks = tricks;
	this.score = points;
	this.name = name;
	this.id = "";
	
	var identifiers = ["southpoints", "westpoints", "northpoints", "eastpoints"];
	this.id = identifiers[this.positionIndex];
	
	this.updateSpace();
};

PointSpace.prototype = {
    constructor: PointSpace,
    updateSpace:function ()  {

		$(this.id).innerHTML = "<p>" + this.name + "</p><p>Tricks: " + this.tricks + "</p><p>Points: " + this.score + "</p";
    },
};

function Table(nameArray, isHumanArray, handArrays, zoneArrays, trickArray, pointArray) {
	this.seats = [];
	this.zones = [];
	this.spaces = [];

	for(var i = 0; i < 4; i++)
	{
		var player = new Player(nameArray[i], i, isHumanArray[i], handArrays[i]);
		this.seats.push(player);
		var zone = new Zone(i, zoneArrays[i]);
		this.zones.push(zone);
		var space = new PointSpace(i, trickArray[i], pointArray[i], nameArray[i]);
		this.spaces.push(space);
	}
	var zone = new Zone(4, zoneArrays[4]);
	this.zones.push(zone);
};

Table.prototype = {
    constructor: Table,
};

