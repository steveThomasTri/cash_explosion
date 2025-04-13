-- Schema to be used for MySQL;

use cedb;
drop table if exists champions ;
drop table if exists players ;
create table players (
	 id int not null auto_increment,
     date date not null,
     playerName varchar(50) not null,
     playerCity varchar(50) not null,
     ticketPurchasedStore varchar(100) not null,
     ticketPurchasedStreet varchar(100) not null,
     ticketPurchasedCity varchar(50) not null,
     number1 int not null,
     number1SpecialEvent varchar(20),
     number1score int not null,
     number2 int not null,
     number2SpecialEvent varchar(20),
     number2score int not null,
     number3 int not null,
     number3SpecialEvent varchar(20),
     number3score int not null,
     number4 int,
     number4SpecialEvent varchar(20),
     number4score int,
     bonus int,
     gameTotal int,
     isCashChallenge bool,
     isSecondChance bool,
     isChampion bool,
     primary key(id)
);

create table champions (
	id int not null auto_increment,
    date date not null,
    playerID Int,
    primary key(id),
    foreign key (playerID) references players(id)
)