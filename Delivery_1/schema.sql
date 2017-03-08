drop table if exists Medication;
drop table if exists MedPackage;
drop table if exists Product;
drop table if exists Ingredient;
drop table if exists Batch;
drop table if exists PackageContent;




create table Medication (
    id varchar(255) not null unique,
    text varchar(255),
    manufacturer varchar(255),
	isBrand Boolean, 
	code varchar(255),
	display varchar(255),
	system varchar(255),
    primary key(id)
);	
	
create table Product (
    id varchar(255) not null unique,
	code varchar(255),
	display varchar(255),
	system varchar(255),
    primary key(id),
	foreign key(id) references Medication(id) ON DELETE CASCADE ON UPDATE CASCADE	

);
	
	
create table MedPackage (
	id varchar(255) not null unique, 
	code varchar(255),
	display varchar(255),
	system varchar(255),
	primary key(id),
	foreign key(id) references Medication(id) ON DELETE CASCADE ON UPDATE CASCADE	
);

create table PackageContent (
	packageID varchar(255) not null unique,
    itemReference varchar(255),
	ammountValue varchar(255),
	ammountUnit varchar(255),
	ammountSystem varchar(255),
    primary key(packageID,itemReference, amountValue, ammountUnit, ammountSystem),
    foreign key(packageID) references MedPackage(id) ON DELETE CASCADE ON UPDATE CASCADE	
);


create table Ingredient (
	productID varchar(255) not null unique,
	itemDisplay varchar(255),
	ammountType varchar(255), 
	ammountValue varchar(255),
	ammountUnit varchar(255),
	ammountSystem varchar(255),
	primary key (productID, itemDisplay),
	foreign key (productID) references Product(id) ON DELETE CASCADE ON UPDATE CASCADE
);

create table Batch (
	--Weak entity of a product
	productID varchar(255) not null unique,
	lotNumber varchar(255),
	expirationDate varchar(255),
	primary key (productID,lotNumber),
	foreign key (productID) references Product(id) ON DELETE CASCADE ON UPDATE CASCADE	
);