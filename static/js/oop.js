
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
        this.cardSrc = "images/card_images/b1fv.bmp";
		this.refreshImg();
    },
	turnUp:function ()  {
        this.cardSrc = this.cardSrc = "images/card_images/" + this.name + ".bmp";
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
	this.score = 0;
	this.tricks = 0;
	this.hand = [];
	this.isHuman = isHuman;
	this.choseTrump = false;
	this.id = "";
	
	var identifiers = ["south", "east", "north", "west"];
	this.id = identifiers[this.positionIndex];

	for(var i = 0; i < handArray.length; i++)
	{
		var tempCard = new Card(handArray[i]);
		this.addToHand(tempCard);
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
	discard:function (index) {
		if(this.hand.length == 0) 
		{
			console.log("can't discard, hand empty");
			return "";
		}
		else
		{
			if(index >= this.hand.length) 
			{
				console.log("can't discard, index: " + index + ", hand length: " + this.hand.length);;
				return "";
			}
			else if(index == this.hand.length - 1)
			{
				this.hand[this.hand.length - 1].unlinkImgObject();
				this.hand.pop();
			}
			else
			{
				var imgObjects = $(this.id).getElementsByTagName("img");
				var tempCard = this.hand[index];
				tempCard.unlinkImgObject();

				for(var j = index; j < this.hand.length - 1; j++)
				{
					this.hand[j] = this.hand[j+1];
					this.hand[j].setImgObject(imgObjects[j]);
				}
				this.hand.pop();
				return tempCard;
			}
		}		
	},
    orderUpOrPass:function ()  {
		centerCard = table.zones[4].card;
		
		if(this.isHuman)
		{
			var positionIndex = this.positionIndex;
			$(table.coms[this.positionIndex].id).innerHTML = "<button id=\"btn1\">Order Up</button><button id=\"btn2\">pass</button>";
			$("btn1").onclick=function() { table.seats[table.dealerIndex].orderUp(); }
			$("btn2").onclick=function() { table.seats[positionIndex].pass1(); }
		}
		else
		{
			var trumpCount = this.getNumberOfTrump(centerCard.suit);
			if(this.positionIndex == table.dealerIndex) trumpCount++;
			
			console.log(this.id + " player has " + trumpCount + " trump");

			if(trumpCount >= 5) table.seats[table.dealerIndex].orderUp();
			else table.seats[this.positionIndex].pass1();
		}
    },
	discardSixthCard:function(cardIndex){
		this.discard(cardIndex);

		if(this.isHuman) this.clearOnClicks();
		table.seats[(table.dealerIndex + 1)%4].chooseCardToPlay();
	},
	assignTrump:function(trumpSuit) {
		table.clearComSpaces();

		if(this.isHuman) this.clearOnClicks();

		table.trump = trumpSuit;
		this.choseTrump = true;
		console.log(table.trump + " assigned as trump");
		table.seats[table.leaderIndex].chooseCardToPlay();
	},
	getNumberOfTrump:function (suit)  {
        var trumpCount = 0;
		for(var i = 0; i < this.hand.length; i++)
		{			
			if(this.hand[i].suit == suit || this.hand[i].name == this.getLeftBauer(suit).name)
			{
				trumpCount += 1;
			}
		}
		return trumpCount;
    },
	getLeftBauer:function (suit) {
		var suitlist = ["s","d","c","h"];
		var index = 0;
		while(suitlist[index] != suit && index < 5) index++;
		var leftIndex = (index + 2)%4;
		leftBauerName = suitlist[leftIndex] + "11";
		leftBauer = new Card(leftBauerName);
		return leftBauer;
	},
	chooseCardToPlay:function(){
		if(this.positionIndex != table.leaderIndex) console.log("led card: " + table.zones[table.leaderIndex].card.name);
		else console.log("player " + this.positionIndex + " leading");

		var ledSuit = "";
		var leader = true;
		if(this.positionIndex != table.leaderIndex) 
		{
			ledSuit = table.zones[table.leaderIndex].card.suit;
			leader = false;
		}
		if(this.isHuman)
		{
			var position = this.positionIndex;
			var cardImgArray = $(this.id).getElementsByTagName("img");
			
			if(this.hand.length > 0 && (leader || !this.handContainsSuit(ledSuit) || this.hand[0].suit == ledSuit)) cardImgArray[0].onclick = function() {table.seats[position].playCard(0);}
			if(this.hand.length > 1 && (leader || !this.handContainsSuit(ledSuit) || this.hand[1].suit == ledSuit)) cardImgArray[1].onclick = function() {table.seats[position].playCard(1);}
			if(this.hand.length > 2 && (leader || !this.handContainsSuit(ledSuit) || this.hand[2].suit == ledSuit)) cardImgArray[2].onclick = function() {table.seats[position].playCard(2);}
			if(this.hand.length > 3 && (leader || !this.handContainsSuit(ledSuit) || this.hand[3].suit == ledSuit)) cardImgArray[3].onclick = function() {table.seats[position].playCard(3);}
			if(this.hand.length > 4 && (leader || !this.handContainsSuit(ledSuit) || this.hand[4].suit == ledSuit)) cardImgArray[4].onclick = function() {table.seats[position].playCard(4);}
		}
		else
		{
			if(!leader && this.handContainsSuit(ledSuit))
			{
				for(var i = 0; i < this.hand.length; i++)
				{
					
					if(this.hand[i].suit == ledSuit) 
					{
						console.log("playCard 1");
						this.playCard(i);
					}
				}
			}
			else 
			{
				console.log("playCard 2");
				this.playCard(0); //dumb AI always plays first card
			}
		}
	},
	clearOnClicks:function() {
		var cardImgArray = $(this.id).getElementsByTagName("img");
		cardImgArray[0].onclick = "";
		cardImgArray[1].onclick = "";
		cardImgArray[2].onclick = "";
		cardImgArray[3].onclick = "";
		cardImgArray[4].onclick = "";
	},
	pickCardToPlay:function(clickableArray, mailTo){
		if(this.isHuman)
		{
			var position = this.positionIndex;
			var cardImgArray = $(this.id).getElementsByTagName("img");
			
			if(this.hand.length > 0 && clickableArray[0] == 1) cardImgArray[0].onclick = function() {table.seats[position].playCard(table.seats[position].hand[0].name, mailTo);}
			if(this.hand.length > 1 && clickableArray[1] == 1) cardImgArray[1].onclick = function() {table.seats[position].playCard(table.seats[position].hand[1].name, mailTo);}
			if(this.hand.length > 2 && clickableArray[2] == 1) cardImgArray[2].onclick = function() {table.seats[position].playCard(table.seats[position].hand[2].name, mailTo);}
			if(this.hand.length > 3 && clickableArray[3] == 1) cardImgArray[3].onclick = function() {table.seats[position].playCard(table.seats[position].hand[3].name, mailTo);}
			if(this.hand.length > 4 && clickableArray[4] == 1) cardImgArray[4].onclick = function() {table.seats[position].playCard(table.seats[position].hand[4].name, mailTo);}
		}
		else
		{
			console.log("not human")
		}
	},
	playCard:function(cardName, mailTo){
		console.log("you played: " + cardName);
		this.clearOnClicks();
		post(mailTo, cardName);
	},
	chooseTrump:function(suit){
		console.log(suit + " chosen as trump");
	},
	orderUp:function (){
		console.log("Order Up");
	},
	pass1:function (){
		console.log("pass1");
	},
	pass2:function (){
		console.log("pass2");
	},
};

function Zone(positionIndex, zoneArray) {
	this.positionIndex = positionIndex;
	this.card = "";
	//this.card = [];
	this.id = "";
	
	var identifiers = ["southplay", "eastplay", "northplay", "westplay", "center"];
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
    discard:function ()  {
		if(this.card == "") return "";
		else{
			this.card.unlinkImgObject();
			var tempCard = this.card;
			this.card = "";
			return tempCard;
		}
    },
};

function ComSpace(positionIndex) {
	this.positionIndex = positionIndex;
	this.id = "";
	
	var identifiers = ["southComSpace", "eastComSpace", "northComSpace", "westComSpace"];
	this.id = identifiers[this.positionIndex];
};

ComSpace.prototype = {
    constructor: ComSpace,
    writeToCom:function (htmlStr)  {
		console.log("using writeToCom");
		$(this.id).innerHTML = htmlStr;
    },
};

function PointSpace(positionIndex) {
	this.positionIndex = positionIndex;
	this.tricks = 0;
	this.score = 0;
	this.id = "";
	
	var identifiers = ["southpoints", "eastpoints", "northpoints", "westpoints"];
	this.id = identifiers[this.positionIndex];
	
	this.updateSpace();
};

PointSpace.prototype = {
    constructor: PointSpace,
    updateTricks:function (trickNum)  {
		this.tricks = trickNum;
		this.updateSpace();
    },
    updateScore:function (pointNum)  {
		this.score = pointNum;
		this.updateSpace();
    },
    updateSpace:function ()  {

		$(this.id).innerHTML = "<p>Tricks: " + this.tricks + "</p><p>Points: " + this.score + "</p";
    },
};

function Table(nameArray, isHumanArray, dealerIndex, handArrays, zoneArrays) {
	
	this.seats = [];
	this.zones = [];
	this.coms = [];
	this.spaces = [];
	this.trump = "";
	this.dealerIndex = dealerIndex;
	this.leaderIndex = (this.dealerIndex+1)%4;

	for(var i = 0; i < 4; i++)
	{
		var player = new Player(nameArray[i], i, isHumanArray[i], handArrays[i]);
		this.seats.push(player);
		var zone = new Zone(i, zoneArrays[i]);
		this.zones.push(zone);
		var com = new ComSpace(i);
		this.coms.push(com);
		var space = new PointSpace(i);
		this.spaces.push(space);
	}
	var zone = new Zone(4, zoneArrays[4]);
	this.zones.push(zone);

	//this.deal();
};

Table.prototype = {
    constructor: Table,
    zonesAreFull:function ()  {
        if(this.zones[0].card != "" && this.zones[1].card != "" && this.zones[2].card != "" && this.zones[3].card != "") return true;
        else return false;
    },
    zonesAreEmpty:function ()  {
        if(this.zones[0].card == "" && this.zones[1].card == "" && this.zones[2].card == "" && this.zones[3].card == "") return true;
        else return false;
    },
    getTrickWinner:function (leaderIndex)  {

    	var playedCards = [this.zones[leaderIndex].card, 
    					   this.zones[(leaderIndex+1)%4].card, 
    					   this.zones[(leaderIndex+2)%4].card, 
    					   this.zones[(leaderIndex+3)%4].card];
    	var winningCardValue = 0;
    	var winningCardIndex = -1;
    	for(var i = 0; i < 4; i++)
    	{
    		var tempValue = playedCards[i].valueInt;
    		if(tempValue == 1) tempValue += 13;
    		if(playedCards[i].suit == this.trump) tempValue += 10;
    		else if(playedCards[i].suit != playedCards[0].suit) tempValue = 0;
    		if(playedCards[i].name == this.getLeftBauer().name) tempValue = 25;
    		if(playedCards[i].name == this.getRightBauer().name) tempValue = 26;
    		if(tempValue > winningCardValue)
    		{
    			winningCardIndex = i;
    			winningCardValue = tempValue;
    		}
    	}

    	var winningPlayerIndex = (leaderIndex + winningCardIndex)%4;

    	console.log("winner is " + winningPlayerIndex);


    	
    	this.clearZones();

		this.leaderIndex = winningPlayerIndex;
		this.seats[winningPlayerIndex].tricks += 1;
		this.spaces[winningPlayerIndex].updateTricks(this.seats[winningPlayerIndex].tricks);

		var tricksPlayed = 0;
		for(var i = 0; i < 4; i++)
		{
			tricksPlayed += this.seats[i].tricks;
		}
		
		if(tricksPlayed >= 5)
		{
			this.assignPoints();
		}
		else 
		{
			console.log("chooseCardToPlay 2");
			this.seats[winningPlayerIndex].chooseCardToPlay();   
		}     
    },
    assignPoints:function () {
    	console.log("round over, assigning points");
    	var teamNStricks = this.seats[0].tricks + this.seats[2].tricks;
    	var teamEWtricks = this.seats[1].tricks + this.seats[3].tricks;
    	var teamNSpoints = 0;
    	var teamEWpoints = 0;
    	var teamNScalled = this.seats[0].choseTrump || this.seats[2].choseTrump;
    	var teamEWcalled = this.seats[1].choseTrump || this.seats[3].choseTrump;

    	if(teamNStricks == 5 || teamEWcalled && teamNStricks > teamEWtricks) teamNSpoints = 2;
    	else if(teamEWtricks == 5 || teamNScalled && teamEWtricks > teamNStricks) teamEWpoints = 2;
    	else if(teamNStricks > teamEWtricks) teamNSpoints = 1;
    	else if(teamEWtricks > teamNStricks) teamEWpoints = 1;
    	else console.log("this branch shouldn't be taken");

    	this.seats[0].score += teamNSpoints;
    	this.seats[2].score += teamNSpoints;
    	this.seats[1].score += teamEWpoints;
    	this.seats[3].score += teamEWpoints;
    	this.spaces[0].updateScore(this.seats[0].score);
    	this.spaces[1].updateScore(this.seats[1].score);
    	this.spaces[2].updateScore(this.seats[2].score);
    	this.spaces[3].updateScore(this.seats[3].score);
    	console.log(this.seats[0].id + " points: " + this.seats[0].score);
    	console.log(this.seats[1].id + " points: " + this.seats[1].score);
    	console.log(this.seats[2].id + " points: " + this.seats[2].score);
    	console.log(this.seats[3].id + " points: " + this.seats[3].score);

    	this.seats[0].tricks = 0;
    	this.seats[2].tricks = 0;
    	this.seats[1].tricks = 0;
    	this.seats[3].tricks = 0;
    	this.spaces[0].updateTricks(this.seats[0].tricks);
    	this.spaces[1].updateTricks(this.seats[1].tricks);
    	this.spaces[2].updateTricks(this.seats[2].tricks);
    	this.spaces[3].updateTricks(this.seats[3].tricks);

    	this.clearZones();
    	this.clearComSpaces();

    	this.seats[0].hand = [];
    	this.seats[2].hand = [];
    	this.seats[1].hand = [];
    	this.seats[3].hand = [];

    	if(this.seats[0].score >= 5 || this.seats[1].score >= 5)
    	{
    		console.log("game over!!");
    	}
    	else
    	{
	    	this.deal();
	    	this.dealerIndex = (this.dealerIndex + 1)%4;
	    	this.leaderIndex = (this.dealerIndex + 1)%4;

	    	this.seats[this.leaderIndex].orderUpOrPass();
	    }
    },
	clearZones:function ()  {

        
        // for(var i = 0; i < 4; i++) this.zones[i].card = "";
        // for(var i = 0; i < 4; i++) this.zones[i].discard();
        if(this.zones[0].card != "") 
        {
        	this.zones[0].card.imgObject.src = "";
        	this.zones[0].card = "";
        }
        if(this.zones[1].card != "") 
        {
        	this.zones[1].card.imgObject.src = "";
        	this.zones[1].card = "";
        }
        if(this.zones[2].card != "") 
        {
        	this.zones[2].card.imgObject.src = "";
        	this.zones[2].card = "";
        }
        if(this.zones[3].card != "") 
        {
        	this.zones[3].card.imgObject.src = "";
        	this.zones[3].card = "";
        }
        if(this.zones[4].card != "") 
        {
        	this.zones[4].card.imgObject.src = "";
        	this.zones[4].card = "";
        }

    },
	clearComSpaces:function ()  {
		$("northComSpace").innerHTML = "";
		$("westComSpace").innerHTML = "";
		$("southComSpace").innerHTML = "";
		$("eastComSpace").innerHTML = "";
	},
    getLeftBauer:function () {
		var suitlist = ["s","d","c","h"];
		var index = 0;
		while(suitlist[index] != this.trump && index < 5) index++;
		var leftIndex = (index + 2)%4;
		leftBauerName = suitlist[leftIndex] + "11";
		leftBauer = new Card(leftBauerName);
		return leftBauer;
	},
	getRightBauer:function (suit) {
		rightBauerName = this.trump + "11";
		rightBauer = new Card(rightBauerName);
		return rightBauer;
	},
	deal:function() {
		var deck = createDeck();
		for(var i = 0; i < 5; i++) 
		{
			for(var j = 0; j < 4; j++) 
			{
				//if(!this.seats[j].isHuman) deck[i*4 + j].turnDown(); turn down cards in front of computer players
				this.seats[j].addToHand(deck[i*4 + j]);
			}
		}
		this.zones[4].addToZone(deck[20]);
	}
};

var createDeck = function()
{
	var deck = [];
	var suits = ["c","d","h","s"];
	var values = ["09","10","11","12","13","01"];
	for(var i = 0; i < 4; i++) for(var j = 0; j < 6; j++) deck[6*i + j] = new Card(suits[i] + values[j]);
	
	// for(var i = 0; i < 100; i++) //shuffle
	// {
	// 	var index1 = Math.floor(Math.random()*24);
	// 	var index2 = Math.floor(Math.random()*24);
		
	// 	var tempValue = deck[index1];
	// 	deck[index1] = deck[index2];
	// 	deck[index2] = tempValue;
	// }
	return deck;
};

var startGame = function()
{
	console.log("Start Game!");
}



