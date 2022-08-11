
CREATE TABLE "Brands" (
	`brand_id` INTEGER, 
	`brand_name` VARCHAR(50) NOT NULL, 
	PRIMARY KEY  `(brand_id`) 
)


CREATE TABLE "Car_Options" (
	`option_set_id` INTEGER, 
	`model_id` INTEGER, 
	`engine_id` INTEGER NOT NULL, 
	`transmission_id` INTEGER NOT NULL, 
	`chassis_id` INTEGER NOT NULL, 
	`premium_sound_id` INTEGER, 
	`color` VARCHAR(30) NOT NULL, 
	`option_set_price` INTEGER NOT NULL, 
	PRIMARY KEY  `(option_set_id`) , 
	FOREIGN KEY `(model_id`)  REFERENCES "Models"  `(model_id`) , 
	FOREIGN KEY `(engine_id`)  REFERENCES "Car_Parts" (part_id), 
	FOREIGN KEY `(premium_sound_id`)  REFERENCES "Car_Parts" (part_id), 
	FOREIGN KEY `(transmission_id`)  REFERENCES "Car_Parts" (part_id), 
	FOREIGN KEY `(chassis_id`)  REFERENCES "Car_Parts" (part_id)
)


CREATE TABLE "Car_Parts" (
	`part_id` INTEGER, 
	`part_name` VARCHAR(100) NOT NULL, 
	`manufacture_plant_id` INTEGER NOT NULL, 
	`manufacture_start_date` DATE NOT NULL, 
	`manufacture_end_date` DATE, 
	`part_recall` INTEGER DEFAULT 0, 
	PRIMARY KEY  `(part_id`) , 
	FOREIGN KEY `(manufacture_plant_id`)  REFERENCES "Manufacture_Plant"  `(manufacture_plant_id`) , 
	CHECK (part_recall = 0 or part_recall = 1)
)


CREATE TABLE "Car_Vins" (
	`vin` INTEGER, 
	`model_id` INTEGER NOT NULL, 
	`option_set_id` INTEGER NOT NULL, 
	`manufactured_date` DATE NOT NULL, 
	`manufactured_plant_id` INTEGER NOT NULL, 
	PRIMARY KEY  `(vin`) , 
	FOREIGN KEY `(model_id`)  REFERENCES "Models"  `(model_id`) , 
	FOREIGN KEY `(manufactured_plant_id`)  REFERENCES "Manufacture_Plant" (manufacture_plant_id), 
	FOREIGN KEY `(option_set_id`)  REFERENCES "Car_Options"  `(option_set_id`) 
)


CREATE TABLE "Customer_Ownership" (
	`customer_id` INTEGER NOT NULL, 
	`vin` INTEGER NOT NULL, 
	`purchase_date` DATE NOT NULL, 
	`purchase_price` INTEGER NOT NULL, 
	`warantee_expire_date` DATE, 
	`dealer_id` INTEGER NOT NULL, 
	PRIMARY KEY (customer_id, vin), 
	FOREIGN KEY `(customer_id`)  REFERENCES "Customers"  `(customer_id`) , 
	FOREIGN KEY `(vin`)  REFERENCES "Car_Vins"  `(vin`) , 
	FOREIGN KEY `(dealer_id`)  REFERENCES "Dealers"  `(dealer_id`) 
)


CREATE TABLE "Customers" (
	`customer_id` INTEGER, 
	`first_name` TEXT(50) NOT NULL, 
	`last_name` TEXT(50) NOT NULL, 
	`gender` TEXT(20), 
	`household_income` INTEGER, 
	`birthdate` DATE NOT NULL, 
	`phone_number` INTEGER NOT NULL, 
	`email` TEXT(128), 
	PRIMARY KEY  `(customer_id`) 
)


CREATE TABLE "Dealer_Brand" (
	`dealer_id` INTEGER NOT NULL, 
	`brand_id` INTEGER NOT NULL, 
	PRIMARY KEY (dealer_id, brand_id), 
	FOREIGN KEY `(dealer_id`)  REFERENCES "Dealers"  `(dealer_id`) , 
	FOREIGN KEY `(brand_id`)  REFERENCES "Brands"  `(brand_id`) 
)


CREATE TABLE "Dealers" (
	`dealer_id` INTEGER, 
	`dealer_name` VARCHAR(50) NOT NULL, 
	`dealer_address` VARCHAR(100), 
	PRIMARY KEY  `(dealer_id`) 
)


CREATE TABLE "Manufacture_Plant" (
	`manufacture_plant_id` INTEGER, 
	`plant_name` VARCHAR(50) NOT NULL, 
	`plant_type` TEXT(7), 
	`plant_location` VARCHAR(100), 
	`company_owned` INTEGER, 
	PRIMARY KEY  `(manufacture_plant_id`) , 
	CHECK (plant_type="Assembly" or plant_type="Parts"), 
	CHECK (company_owned=0 or company_owned=1)
)


CREATE TABLE "Models" (
	`model_id` INTEGER, 
	`model_name` VARCHAR(50) NOT NULL, 
	`model_base_price` INTEGER NOT NULL, 
	`brand_id` INTEGER NOT NULL, 
	PRIMARY KEY  `(model_id`) , 
	FOREIGN KEY `(brand_id`)  REFERENCES "Brands"  `(brand_id`) 
)

