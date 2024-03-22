CREATE TABLE `server_coin` (
	`reserves` INT NOT NULL DEFAULT '0',
	`emission_limit` INT NOT NULL DEFAULT '50000',
	`burned_coins` INT NOT NULL DEFAULT '0'
);
INSERT INTO `server_coin` (`emission_limit`) VALUES('50000');

CREATE TABLE `admin_registry` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`admin_name` varchar(255) NOT NULL DEFAULT 'Unknow',
	`action_name` varchar(255) NOT NULL DEFAULT 'None',
	`filter` varchar(255) NOT NULL DEFAULT 'None',
	`date` DATETIME NOT NULL DEFAULT NOW(),
	PRIMARY KEY (`id`)
);

CREATE TABLE `shop_products` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`country` varchar(255) NOT NULL DEFAULT 'ALL',
	`name` varchar(255) NOT NULL DEFAULT 'GS Monedas',
	`price` INT NOT NULL DEFAULT '1',
	`currency` varchar(255) NOT NULL DEFAULT 'ARS',
	`image` varchar(255) NOT NULL DEFAULT 'default.png',
	`type` INT NOT NULL DEFAULT '0',
	`extra` INT NOT NULL DEFAULT '5',
	PRIMARY KEY (`id`)
);
ALTER TABLE `shop_products` ADD `invalid`  INT NOT NULL DEFAULT '0';
ALTER TABLE `shop_products` ADD `offer`  INT NOT NULL DEFAULT '0';

ALTER TABLE `FACTORIES` ADD `EMPLOYEE_PAY` INT NOT NULL DEFAULT '10000';

CREATE TABLE `payments` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`product_id` INT NOT NULL,
	`state` INT NOT NULL DEFAULT '0',
	`admin_id` INT NOT NULL DEFAULT '0',
	`method` varchar(255) NOT NULL DEFAULT 'PayPal',
	`response` varchar(255) NOT NULL DEFAULT '0',
	`user_id` INT NOT NULL DEFAULT '0',
	`start_date` DATETIME NOT NULL DEFAULT NOW(),
	`end_date` DATETIME NULL,
	PRIMARY KEY (`id`)
);
ALTER TABLE `payments` ADD `response` varchar(255) NOT NULL DEFAULT '0';

CREATE TABLE `gift_codes` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`code` varchar(64) NOT NULL UNIQUE,
	`type` INT NOT NULL DEFAULT '1',
	`extra` INT NOT NULL DEFAULT '10',
	`user_id` INT NOT NULL DEFAULT '0',
	PRIMARY KEY (`id`)
);
INSERT INTO `gift_codes` (`code`, `type`, `extra`) VALUES ('lmao422', '1', '10');
INSERT INTO `gift_codes` (`code`, `type`, `extra`) VALUES ('mamaguebo', '1', '10');
INSERT INTO `gift_codes` (`code`, `type`, `extra`) VALUES ('atom', '1', '10');
INSERT INTO `gift_codes` (`code`, `type`, `extra`) VALUES ('maikplay', '1', '10');
INSERT INTO `gift_codes` (`code`, `type`, `extra`) VALUES ('gsrp', '1', '10');
INSERT INTO `gift_codes` (`code`, `type`, `extra`) VALUES ('puto', '1', '10');
INSERT INTO `gift_codes` (`code`, `type`, `extra`) VALUES ('nigger', '1', '10');
INSERT INTO `gift_codes` (`code`, `type`, `extra`) VALUES ('hitler', '1', '10');
INSERT INTO `gift_codes` (`code`, `type`, `extra`) VALUES ('vipgold', '2', '3');

CREATE TABLE `mystery_boxes` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`quality` INT NOT NULL DEFAULT '1',
	`amount` INT NOT NULL DEFAULT '10',
	`user_id` INT NOT NULL DEFAULT '0',
	PRIMARY KEY (`id`)
);
INSERT INTO `mystery_boxes` (`quality`, `user_id`) VALUES ('1', '81045');

-- All country products
INSERT INTO `shop_products` (
	`country`, `name`, `price`, `currency`, `image`, `type`, `extra`
)
VALUES (
	'AR', 'Taza oficial + 100', '2000', 'ARS', 'tazags1.png', '422000', '100'
);


INSERT INTO `shop_products` (
	`country`, `name`, `price`, `currency`, `image`, `type`, `extra`
)
VALUES (
	'US', 'Puñado de GS (10 monedas)', '5', 'USD', 'punado.png', '0', '10'
);


INSERT INTO `shop_products` (
	`country`, `name`, `price`, `currency`, `image`, `type`, `extra`
)
VALUES (
	'US', 'Billetera de GS (20 monedas)', '8', 'USD', 'monedero.png', '0', '20'
);


INSERT INTO `shop_products` (
	`country`, `name`, `price`, `currency`, `image`, `type`, `extra`
)
VALUES (
	'US', 'Maleta de GS (50 monedas)', '20', 'USD', 'meletin.png', '0', '50'
);


INSERT INTO `shop_products` (
	`country`, `name`, `price`, `currency`, `image`, `type`, `extra`
)
VALUES (
	'US', 'Cofre de GS (100 monedas)', '35', 'USD', 'caja.png', '0', '100'
);


INSERT INTO `shop_products` (
	`country`, `name`, `price`, `currency`, `image`, `type`, `extra`
)
VALUES (
	'US', 'Furgón de GS (500 monedas)', '100', 'USD', 'furgon.png', '0', '500'
);


INSERT INTO `shop_products` (
	`country`, `name`, `price`, `currency`, `image`, `type`, `extra`
)
VALUES (
	'US', 'VIP Silver', '3', 'USD', 'silver.png', '1', '1'
);


INSERT INTO `shop_products` (
	`country`, `name`, `price`, `currency`, `image`, `type`, `extra`
)
VALUES (
	'US', 'VIP Bronze', '5', 'USD', 'bronze.png', '1', '2'
);


INSERT INTO `shop_products` (
	`country`, `name`, `price`, `currency`, `image`, `type`, `extra`
)
VALUES (
	'US', 'VIP Gold', '6', 'USD', 'gold.png', '1', '3'
);


INSERT INTO `shop_products` (
	`country`, `name`, `price`, `currency`, `image`, `type`, `extra`
)
VALUES (
	'US', 'VIP Diamond', '12', 'USD', 'diamond.png', '1', '4'
);

-- Argentina products
INSERT INTO `shop_products` (
	`country`, `name`, `price`, `currency`, `image`, `type`, `extra`
)
VALUES (
	'AR', 'Puñado de GS (15 monedas)', '300', 'ARS', 'punado.png', '0', '15'
);


INSERT INTO `shop_products` (
	`country`, `name`, `price`, `currency`, `image`, `type`, `extra`
)
VALUES (
	'AR', 'Billetera de GS (25 monedas)', '500', 'ARS', 'monedero.png', '0', '25'
);


INSERT INTO `shop_products` (
	`country`, `name`, `price`, `currency`, `image`, `type`, `extra`
)
VALUES (
	'AR', 'Maleta de GS (50 monedas)', '900', 'ARS', 'meletin.png', '0', '50'
);


INSERT INTO `shop_products` (
	`country`, `name`, `price`, `currency`, `image`, `type`, `extra`
)
VALUES (
	'AR', 'Cofre de GS (100 monedas)', '1800', 'ARS', 'caja.png', '0', '100'
);


INSERT INTO `shop_products` (
	`country`, `name`, `price`, `currency`, `image`, `type`, `extra`
)
VALUES (
	'AR', 'Furgón de GS (500 monedas)', '8000', 'ARS', 'furgon.png', '0', '500'
);


INSERT INTO `shop_products` (
	`country`, `name`, `price`, `currency`, `image`, `type`, `extra`
)
VALUES (
	'AR', 'VIP Silver', '300', 'ARS', 'silver.png', '1', '1'
);


INSERT INTO `shop_products` (
	`country`, `name`, `price`, `currency`, `image`, `type`, `extra`
)
VALUES (
	'AR', 'VIP Bronze', '700', 'ARS', 'bronze.png', '1', '2'
);


INSERT INTO `shop_products` (
	`country`, `name`, `price`, `currency`, `image`, `type`, `extra`
)
VALUES (
	'AR', 'VIP Gold', '1050', 'ARS', 'gold.png', '1', '3'
);


INSERT INTO `shop_products` (
	`country`, `name`, `price`, `currency`, `image`, `type`, `extra`
)
VALUES (
	'AR', 'VIP Diamond', '1400', 'ARS', 'diamond.png', '1', '4'
);

INSERT INTO `shop_products` (
	`country`, `name`, `price`, `currency`, `image`, `type`, `offer`
)
VALUES (
	'AR', 'VIP Diamond (OFERTA 2X1, 62 DIAS)', '1400', 'ARS', 'diamond.png', '2', '1'
);



INSERT INTO `shop_products` (
	`country`, `name`, `price`, `currency`, `image`, `type`, `extra`, `offer`
)
VALUES (
	'AR', 'RC Bandit', '100', 'ARS', 'bandit.png', '10', '441', '1'
);

INSERT INTO `shop_products` (
	`country`, `name`, `price`, `currency`, `image`, `type`, `extra`, `offer`
)
VALUES (
	'AR', 'RC Baron', '500', 'ARS', 'barron.png', '10', '464', '1'
);

INSERT INTO `shop_products` (
	`country`, `name`, `price`, `currency`, `image`, `type`, `extra`, `offer`
)
VALUES (
	'AR', 'RC Raider', '250', 'ARS', 'raider.png', '10', '465', '1'
);

INSERT INTO `shop_products` (
	`country`, `name`, `price`, `currency`, `image`, `type`, `extra`, `offer`
)
VALUES (
	'AR', 'RC Goblin', '250', 'ARS', 'goblin.png', '10', '501', '1'
);

INSERT INTO `shop_products` (
	`country`, `name`, `price`, `currency`, `image`, `type`, `extra`, `offer`
)
VALUES (
	'AR', 'RC Tiger', '100', 'ARS', 'tiger.png', '10', '564', '1'
);

INSERT INTO `shop_products` (
	`country`, `name`, `price`, `currency`, `image`, `type`, `extra`, `offer`
)
VALUES (
	'AR', 'RC Cam', '250', 'ARS', 'cam.png', '10', '594', '1'
);








INSERT INTO `shop_products` (
	`country`, `name`, `price`, `currency`, `image`, `type`, `extra`, `offer`
)
VALUES (
	'AR', 'Caja Normal', '30', 'ARS', '0.png', '50', '1', '1'
);

INSERT INTO `shop_products` (
	`country`, `name`, `price`, `currency`, `image`, `type`, `extra`, `offer`
)
VALUES (
	'AR', 'Caja Dorada', '70', 'ARS', '1.png', '51', '1', '1'
);

INSERT INTO `shop_products` (
	`country`, `name`, `price`, `currency`, `image`, `type`, `extra`, `offer`
)
VALUES (
	'AR', 'Caja Especial', '200', 'ARS', '2.png', '52', '1', '1'
);


INSERT INTO `shop_products` (
	`country`, `name`, `price`, `currency`, `image`, `type`, `extra`, `offer`
)
VALUES (
	'AR', 'PACK X5 CAJAS NORMALES', '100', 'ARS', '0.png', '50', '5', '1'
);


INSERT INTO `shop_products` (
	`country`, `name`, `price`, `currency`, `image`, `type`, `extra`, `offer`
)
VALUES (
	'AR', 'PACK X5 CAJAS DORADAS', '300', 'ARS', '1.png', '51', '5', '1'
);

INSERT INTO `shop_products` (
	`country`, `name`, `price`, `currency`, `image`, `type`, `extra`, `offer`
)
VALUES (
	'AR', 'PACK X5 CAJAS ESPECIALES', '900', 'ARS', '2.png', '52', '5', '1'
);





INSERT INTO `shop_products` (
	`country`, `name`, `price`, `currency`, `image`, `type`, `extra`, `offer`
)
VALUES (
	'CO', 'Caja Normal', '3000', 'COP', '0.png', '50', '1', '1'
);

INSERT INTO `shop_products` (
	`country`, `name`, `price`, `currency`, `image`, `type`, `extra`, `offer`
)
VALUES (
	'CO', 'Caja Dorada', '3500', 'COP', '1.png', '51', '1', '1'
);

INSERT INTO `shop_products` (
	`country`, `name`, `price`, `currency`, `image`, `type`, `extra`, `offer`
)
VALUES (
	'CO', 'Caja Especial', '7000', 'COP', '2.png', '52', '1', '1'
);


INSERT INTO `shop_products` (
	`country`, `name`, `price`, `currency`, `image`, `type`, `extra`, `offer`
)
VALUES (
	'CO', 'PACK X5 CAJAS NORMALES', '5000', 'COP', '0.png', '50', '5', '1'
);


INSERT INTO `shop_products` (
	`country`, `name`, `price`, `currency`, `image`, `type`, `extra`, `offer`
)
VALUES (
	'CO', 'PACK X5 CAJAS DORADAS', '12000', 'COP', '1.png', '51', '5', '1'
);

INSERT INTO `shop_products` (
	`country`, `name`, `price`, `currency`, `image`, `type`, `extra`, `offer`
)
VALUES (
	'CO', 'PACK X5 CAJAS ESPECIALES', '19500', 'COP', '2.png', '52', '5', '1'
);














INSERT INTO `shop_products` (
	`country`, `name`, `price`, `currency`, `image`, `type`, `extra`, `offer`
)
VALUES (
	'AR', 'VIP Silver', '150', 'ARS', 'silver.png', '1', '1', '1'
);


INSERT INTO `shop_products` (
	`country`, `name`, `price`, `currency`, `image`, `type`, `extra`, `offer`
)
VALUES (
	'AR', 'VIP Bronze', '50', 'ARS', 'bronze.png', '1', '2', '1'
);


INSERT INTO `shop_products` (
	`country`, `name`, `price`, `currency`, `image`, `type`, `extra`, `offer`
)
VALUES (
	'AR', 'Puñado de GS (15 monedas)', '150', 'ARS', 'punado.png', '0', '15', '1'
);


INSERT INTO `shop_products` (
	`country`, `name`, `price`, `currency`, `image`, `type`, `extra`, `offer`
)
VALUES (
	'AR', 'Billetera de GS (25 monedas)', '250', 'ARS', 'monedero.png', '0', '25', '1'
);


INSERT INTO `shop_products` (
	`country`, `name`, `price`, `currency`, `image`, `type`, `extra`, `offer`
)
VALUES (
	'AR', 'Maleta de GS (50 monedas)', '450', 'ARS', 'meletin.png', '0', '50', '1'
);


INSERT INTO `shop_products` (
	`country`, `name`, `price`, `currency`, `image`, `type`, `extra`, `offer`
)
VALUES (
	'AR', 'Cofre de GS (100 monedas)', '900', 'ARS', 'caja.png', '0', '100', '1'
);


INSERT INTO `shop_products` (
	`country`, `name`, `price`, `currency`, `image`, `type`, `extra`, `offer`
)
VALUES (
	'AR', 'Furgón de GS (500 monedas)', '2500', 'ARS', 'furgon.png', '0', '500', '1'
);


INSERT INTO `shop_products` (
	`country`, `name`, `price`, `currency`, `image`, `type`, `offer`
)
VALUES (
	'AR', 'VIP Diamond (OFERTA ESPECIAL)', '800', 'ARS', 'diamond.png', '2', '1'
);


INSERT INTO `shop_products` (
	`country`, `name`, `price`, `currency`, `image`, `type`, `offer`
)
VALUES (
	'VE', 'VIP Diamond (OFERTA 2X1, 62 DIAS)', '50', 'VES', 'diamond.png', '2', '1'
);

-- Colombia products
INSERT INTO `shop_products` (
	`country`, `name`, `price`, `currency`, `image`, `type`, `extra`
)
VALUES (
	'CO', 'Puñado de GS (10 monedas)', '20000', 'COP', 'punado.png', '0', '10'
);


INSERT INTO `shop_products` (
	`country`, `name`, `price`, `currency`, `image`, `type`, `extra`
)
VALUES (
	'CO', 'Billetera de GS (20 monedas)', '32000', 'COP', 'monedero.png', '0', '20'
);


INSERT INTO `shop_products` (
	`country`, `name`, `price`, `currency`, `image`, `type`, `extra`
)
VALUES (
	'CO', 'Maleta de GS (50 monedas)', '80000', 'COP', 'meletin.png', '0', '50'
);


INSERT INTO `shop_products` (
	`country`, `name`, `price`, `currency`, `image`, `type`, `extra`
)
VALUES (
	'CO', 'Cofre de GS (100 monedas)', '140000', 'COP', 'caja.png', '0', '100'
);


INSERT INTO `shop_products` (
	`country`, `name`, `price`, `currency`, `image`, `type`, `extra`
)
VALUES (
	'CO', 'Furgón de GS (500 monedas)', '300000', 'COP', 'furgon.png', '0', '500'
);


INSERT INTO `shop_products` (
	`country`, `name`, `price`, `currency`, `image`, `type`, `extra`
)
VALUES (
	'CO', 'VIP Silver', '12000', 'COP', 'silver.png', '1', '1'
);


INSERT INTO `shop_products` (
	`country`, `name`, `price`, `currency`, `image`, `type`, `extra`
)
VALUES (
	'CO', 'VIP Bronze', '20000', 'COP', 'bronze.png', '1', '2'
);


INSERT INTO `shop_products` (
	`country`, `name`, `price`, `currency`, `image`, `type`, `extra`
)
VALUES (
	'CO', 'VIP Gold', '22000', 'COP', 'gold.png', '1', '3'
);


INSERT INTO `shop_products` (
	`country`, `name`, `price`, `currency`, `image`, `type`, `extra`
)
VALUES (
	'CO', 'VIP Diamond', '30000', 'COP', 'diamond.png', '1', '4'
);


INSERT INTO `shop_products` (
	`country`, `name`, `price`, `currency`, `image`, `type`, `extra`
)
VALUES (
	'AR', 'RC Bandit', '1000', 'ARS', 'bandit.png', '10', '441'
);

INSERT INTO `shop_products` (
	`country`, `name`, `price`, `currency`, `image`, `type`, `extra`
)
VALUES (
	'AR', 'RC Baron', '1800', 'ARS', 'barron.png', '10', '464'
);

INSERT INTO `shop_products` (
	`country`, `name`, `price`, `currency`, `image`, `type`, `extra`
)
VALUES (
	'AR', 'RC Raider', '1000', 'ARS', 'raider.png', '10', '465'
);

INSERT INTO `shop_products` (
	`country`, `name`, `price`, `currency`, `image`, `type`, `extra`
)
VALUES (
	'AR', 'RC Goblin', '1000', 'ARS', 'goblin.png', '10', '501'
);

INSERT INTO `shop_products` (
	`country`, `name`, `price`, `currency`, `image`, `type`, `extra`
)
VALUES (
	'AR', 'RC Tiger', '1000', 'ARS', 'tiger.png', '10', '564'
);

INSERT INTO `shop_products` (
	`country`, `name`, `price`, `currency`, `image`, `type`, `extra`
)
VALUES (
	'AR', 'RC Cam', '1000', 'ARS', 'cam.png', '10', '594'
);


-- Venezuela products
INSERT INTO `shop_products` (
	`country`, `name`, `price`, `currency`, `image`, `type`, `extra`
)
VALUES (
	'VE', 'Puñado de GS (10 monedas)', '20', 'VES', 'punado.png', '0', '10'
);


INSERT INTO `shop_products` (
	`country`, `name`, `price`, `currency`, `image`, `type`, `extra`
)
VALUES (
	'VE', 'Billetera de GS (20 monedas)', '35', 'VES', 'monedero.png', '0', '20'
);


INSERT INTO `shop_products` (
	`country`, `name`, `price`, `currency`, `image`, `type`, `extra`
)
VALUES (
	'VE', 'Maleta de GS (50 monedas)', '90', 'VES', 'meletin.png', '0', '50'
);


INSERT INTO `shop_products` (
	`country`, `name`, `price`, `currency`, `image`, `type`, `extra`
)
VALUES (
	'VE', 'Cofre de GS (100 monedas)', '160', 'VES', 'caja.png', '0', '100'
);


INSERT INTO `shop_products` (
	`country`, `name`, `price`, `currency`, `image`, `type`, `extra`
)
VALUES (
	'VE', 'Furgón de GS (500 monedas)', '400', 'VES', 'furgon.png', '0', '500'
);


INSERT INTO `shop_products` (
	`country`, `name`, `price`, `currency`, `image`, `type`, `extra`
)
VALUES (
	'VE', 'VIP Silver', '15', 'VES', 'silver.png', '1', '1'
);


INSERT INTO `shop_products` (
	`country`, `name`, `price`, `currency`, `image`, `type`, `extra`
)
VALUES (
	'VE', 'VIP Bronze', '20', 'VES', 'bronze.png', '1', '2'
);


INSERT INTO `shop_products` (
	`country`, `name`, `price`, `currency`, `image`, `type`, `extra`
)
VALUES (
	'VE', 'VIP Gold', '25', 'VES', 'gold.png', '1', '3'
);


INSERT INTO `shop_products` (
	`country`, `name`, `price`, `currency`, `image`, `type`, `extra`
)
VALUES (
	'VE', 'VIP Diamond', '50', 'VES', 'diamond.png', '1', '4'
);

-- Peru
INSERT INTO `shop_products` (
	`country`, `name`, `price`, `currency`, `image`, `type`, `extra`
)
VALUES (
	'PE', 'Puñado de GS (10 monedas)', '19', 'SOL', 'punado.png', '0', '10'
);


INSERT INTO `shop_products` (
	`country`, `name`, `price`, `currency`, `image`, `type`, `extra`
)
VALUES (
	'PE', 'Billetera de GS (20 monedas)', '30', 'SOL', 'monedero.png', '0', '20'
);


INSERT INTO `shop_products` (
	`country`, `name`, `price`, `currency`, `image`, `type`, `extra`
)
VALUES (
	'PE', 'Maleta de GS (50 monedas)', '75', 'SOL', 'meletin.png', '0', '50'
);


INSERT INTO `shop_products` (
	`country`, `name`, `price`, `currency`, `image`, `type`, `extra`
)
VALUES (
	'PE', 'Cofre de GS (100 monedas)', '130', 'SOL', 'caja.png', '0', '100'
);


INSERT INTO `shop_products` (
	`country`, `name`, `price`, `currency`, `image`, `type`, `extra`
)
VALUES (
	'PE', 'Furgón de GS (500 monedas)', '375', 'SOL', 'furgon.png', '0', '500'
);


INSERT INTO `shop_products` (
	`country`, `name`, `price`, `currency`, `image`, `type`, `extra`
)
VALUES (
	'PE', 'VIP Diamond', '45', 'SOL', 'diamond.png', '1', '4'
);




-- Mexico
INSERT INTO `shop_products` (
	`country`, `name`, `price`, `currency`, `image`, `type`, `extra`
)
VALUES (
	'MX', 'Puñado de GS (10 monedas)', '100', 'Pesos', 'punado.png', '0', '10'
);


INSERT INTO `shop_products` (
	`country`, `name`, `price`, `currency`, `image`, `type`, `extra`
)
VALUES (
	'MX', 'Billetera de GS (20 monedas)', '150', 'Pesos', 'monedero.png', '0', '20'
);


INSERT INTO `shop_products` (
	`country`, `name`, `price`, `currency`, `image`, `type`, `extra`
)
VALUES (
	'MX', 'Maleta de GS (50 monedas)', '350', 'Pesos', 'meletin.png', '0', '50'
);


INSERT INTO `shop_products` (
	`country`, `name`, `price`, `currency`, `image`, `type`, `extra`
)
VALUES (
	'MX', 'Cofre de GS (100 monedas)', '650', 'Pesos', 'caja.png', '0', '100'
);


INSERT INTO `shop_products` (
	`country`, `name`, `price`, `currency`, `image`, `type`, `extra`
)
VALUES (
	'MX', 'Furgón de GS (500 monedas)', '1800', 'Pesos', 'furgon.png', '0', '500'
);


INSERT INTO `shop_products` (
	`country`, `name`, `price`, `currency`, `image`, `type`, `extra`
)
VALUES (
	'MX', 'VIP Diamond', '270', 'Pesos', 'diamond.png', '1', '4'
);

-- Republica dominicana
INSERT INTO `shop_products` (
	`country`, `name`, `price`, `currency`, `image`, `type`, `extra`
)
VALUES (
	'DO', 'Puñado de GS (10 monedas)', '270', 'Pesos', 'punado.png', '0', '10'
);


INSERT INTO `shop_products` (
	`country`, `name`, `price`, `currency`, `image`, `type`, `extra`
)
VALUES (
	'DO', 'Billetera de GS (20 monedas)', '432', 'Pesos', 'monedero.png', '0', '20'
);


INSERT INTO `shop_products` (
	`country`, `name`, `price`, `currency`, `image`, `type`, `extra`
)
VALUES (
	'DO', 'Maleta de GS (50 monedas)', '1080', 'Pesos', 'meletin.png', '0', '50'
);


INSERT INTO `shop_products` (
	`country`, `name`, `price`, `currency`, `image`, `type`, `extra`
)
VALUES (
	'DO', 'Cofre de GS (100 monedas)', '1890', 'Pesos', 'caja.png', '0', '100'
);


INSERT INTO `shop_products` (
	`country`, `name`, `price`, `currency`, `image`, `type`, `extra`
)
VALUES (
	'DO', 'Furgón de GS (500 monedas)', '5400', 'Pesos', 'furgon.png', '0', '500'
);


INSERT INTO `shop_products` (
	`country`, `name`, `price`, `currency`, `image`, `type`, `extra`
)
VALUES (
	'DO', 'VIP Diamond', '648', 'Pesos', 'diamond.png', '1', '4'
);