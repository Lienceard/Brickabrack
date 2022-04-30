BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "contenir" (
	"contenir_brique_id"	,
	"contenir_plan_id"	,
	FOREIGN KEY("contenir_brique_id") REFERENCES "brique"("brique_id"),
	FOREIGN KEY("contenir_plan_id") REFERENCES "plan"("plan_id")
);
CREATE TABLE IF NOT EXISTS "user" (
	"user_id"	INTEGER,
	"user_nom"	TEXT NOT NULL,
	"user_login"	VARCHAR(45) NOT NULL,
	"user_email"	TEXT NOT NULL,
	"user_password"	VARCHAR(100) NOT NULL,
	PRIMARY KEY("user_id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "theme" (
	"theme_id"	INTEGER,
	"theme_nom"	TEXT NOT NULL,
	PRIMARY KEY("theme_id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "plan" (
	"plan_id"	INTEGER NOT NULL,
	"plan_ensemble"	INTEGER,
	"plan_titre"	,
	"plan_date_sortie"	INTEGER NOT NULL,
	"plan_theme"	,
	"plan_source"	TEXT NOT NULL,
	FOREIGN KEY("plan_theme") REFERENCES "theme"("theme_id"),
	PRIMARY KEY("plan_id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "brique" (
	"brique_id"	INTEGER NOT NULL,
	"brique_element"	INTEGER,
	"brique_nom"	,
	PRIMARY KEY("brique_id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "authorship" (
	"authorship_id"	INTEGER NOT NULL,
	"authorship_brique_id"	INTEGER,
	"authorship_plan_id"	INTEGER,
	"authorship_theme_id"	INTEGER,
	"authorship_user_id"	INTEGER,
	"authorship_date"	datetime DEFAULT CURRENT_TIMESTAMP,
	FOREIGN KEY("authorship_user_id") REFERENCES "user"("user_id"),
	FOREIGN KEY("authorship_theme_id") REFERENCES "theme"("theme_id"),
	PRIMARY KEY("authorship_id" AUTOINCREMENT),
	FOREIGN KEY("authorship_plan_id") REFERENCES "plan"("plan_id"),
	FOREIGN KEY("authorship_brique_id") REFERENCES "brique"("brique_id")
);
INSERT INTO "contenir" VALUES (1,2);
INSERT INTO "contenir" VALUES (2,10);
INSERT INTO "contenir" VALUES (3,2);
INSERT INTO "contenir" VALUES (4,9);
INSERT INTO "contenir" VALUES (4,1);
INSERT INTO "contenir" VALUES (5,3);
INSERT INTO "contenir" VALUES (6,9);
INSERT INTO "contenir" VALUES (7,1);
INSERT INTO "contenir" VALUES (8,2);
INSERT INTO "contenir" VALUES (9,1);
INSERT INTO "contenir" VALUES (10,1);
INSERT INTO "contenir" VALUES (11,11);
INSERT INTO "contenir" VALUES (12,4);
INSERT INTO "contenir" VALUES (13,1);
INSERT INTO "contenir" VALUES (14,11);
INSERT INTO "contenir" VALUES (15,2);
INSERT INTO "contenir" VALUES (16,8);
INSERT INTO "contenir" VALUES (17,10);
INSERT INTO "contenir" VALUES (18,7);
INSERT INTO "contenir" VALUES (19,6);
INSERT INTO "contenir" VALUES (20,7);
INSERT INTO "contenir" VALUES (21,4);
INSERT INTO "contenir" VALUES (22,4);
INSERT INTO "contenir" VALUES (23,3);
INSERT INTO "contenir" VALUES (24,4);
INSERT INTO "contenir" VALUES (25,5);
INSERT INTO "contenir" VALUES (26,5);
INSERT INTO "contenir" VALUES (27,11);
INSERT INTO "contenir" VALUES (28,3);
INSERT INTO "contenir" VALUES (29,3);
INSERT INTO "contenir" VALUES (30,11);
INSERT INTO "theme" VALUES (1,'pompier');
INSERT INTO "theme" VALUES (2,'police');
INSERT INTO "theme" VALUES (3,'aérospatial');
INSERT INTO "theme" VALUES (4,'espace-naturel');
INSERT INTO "theme" VALUES (5,'divertissements');
INSERT INTO "theme" VALUES (6,'transports');
INSERT INTO "theme" VALUES (7,'chantier');
INSERT INTO "theme" VALUES (8,'centre-ville');
INSERT INTO "plan" VALUES (1,4203,'Le transporteur',2012,6,'https://www.lego.com/fr-fr/service/buildinginstructions/4203');
INSERT INTO "plan" VALUES (2,60138,'La course poursuite en hélicoptère',2017,'2','https://www.lego.com/fr-fr/service/buildinginstructions/60138');
INSERT INTO "plan" VALUES (3,60216,'Les pompiers du centre-ville',2019,'1','https://www.lego.com/fr-fr/service/buildinginstructions/60216');
INSERT INTO "plan" VALUES (4,60253,'Le camion de la marchande de glaces',2020,'8','https://www.lego.com/fr-fr/service/buildinginstructions/60253');
INSERT INTO "plan" VALUES (5,60262,'L’avion de passagers',2020,'3','https://www.lego.com/fr-fr/service/buildinginstructions/60262');
INSERT INTO "plan" VALUES (6,60265,'La base d’exploration océanique',2020,4,'https://www.lego.com/fr-fr/service/buildinginstructions/60265');
INSERT INTO "plan" VALUES (7,60292,'Le centre-ville',2021,8,'https://www.lego.com/fr-fr/service/buildinginstructions/60292');
INSERT INTO "plan" VALUES (8,60295,'L’arène de spectacle des cascadeurs',2021,5,'https://www.lego.com/fr-fr/service/buildinginstructions/60295');
INSERT INTO "plan" VALUES (9,60302,'L’opération de sauvetage des animaux sauvages',2021,4,'https://www.lego.com/fr-fr/service/buildinginstructions/60302');
INSERT INTO "plan" VALUES (10,60308,'Les garde-côtes et les marins pompiers en mission',2021,1,'https://www.lego.com/fr-fr/service/buildinginstructions/60308');
INSERT INTO "plan" VALUES (11,60351,'La base de lancement de la fusée',2022,'3','https://www.lego.com/fr-fr/service/buildinginstructions/60351');
INSERT INTO "brique" VALUES (1,4259422,'MOTOR 2X2X1 1/3');
INSERT INTO "brique" VALUES (2,4502068,'MOTOR 2X2X1 1/3');
INSERT INTO "brique" VALUES (3,4504187,'PLATE 1X2 W. SPOILER');
INSERT INTO "brique" VALUES (4,4506778,'ROCK 4X4X1 1/3 UPPER PART');
INSERT INTO "brique" VALUES (5,4512688,'WALL ELEMENT 1X6X5, ABS');
INSERT INTO "brique" VALUES (6,4539908,'RIGHT PLATE 2X3 W/ANGLE');
INSERT INTO "brique" VALUES (7,4543458,'WINDSCREEN 4X3X3 W/SHARP EDGE');
INSERT INTO "brique" VALUES (8,4560932,'PLANE FRONT 6X10X4 W. WINDOW');
INSERT INTO "brique" VALUES (9,4569407,'FUNCTION ELEMENT FEMALE');
INSERT INTO "brique" VALUES (10,4609774,'CONICAL DRILL WITH SPIKES');
INSERT INTO "brique" VALUES (11,4611927,'BOTTOM W. TURNTABLE 4X4');
INSERT INTO "brique" VALUES (12,4614195,'DOG W. DECO');
INSERT INTO "brique" VALUES (13,4616995,'CHASSIS 6X34X2 2/3');
INSERT INTO "brique" VALUES (14,4667463,'LATTICE TOWER 2X2X10 W/CROSS');
INSERT INTO "brique" VALUES (15,6025392,'INV. ROOF T.6X10X4 W.DOUBL. BOW');
INSERT INTO "brique" VALUES (16,6076604,'MOTOR 2X2X1 1/3');
INSERT INTO "brique" VALUES (17,6107827,'SHARK, JAW, NO. 1');
INSERT INTO "brique" VALUES (18,6118827,'ANGLE PLATE 1X2 / 2X4');
INSERT INTO "brique" VALUES (19,6138752,'MOUNTAIN BRICK 8X8X6');
INSERT INTO "brique" VALUES (20,6167739,'DRAGON''S FIRE');
INSERT INTO "brique" VALUES (21,6173959,'PLADE 1X1 M. 1 LOD. TAND');
INSERT INTO "brique" VALUES (22,6174272,'SKATEBOARD');
INSERT INTO "brique" VALUES (23,6203729,'MOTOR CYCLE FAIRING, NO. 4');
INSERT INTO "brique" VALUES (24,6219630,'MINI UPPER PART, NO. 4207');
INSERT INTO "brique" VALUES (25,6224370,'RAIL 2X16X3, BOW, INV., W/ 3.2 SHAFT');
INSERT INTO "brique" VALUES (26,6226630,'SUITCASE, NO. 1');
INSERT INTO "brique" VALUES (27,6236949,'BRICK 2X2 W/GROOVE A.CR.HOLE');
INSERT INTO "brique" VALUES (28,6248534,'SHOOTER W/ CROSS AXLE, NO. 1');
INSERT INTO "brique" VALUES (29,6248537,'PNEUMATIC CYLINDER, W/ CROSS AXLE, NO. 1');
INSERT INTO "brique" VALUES (30,6262086,'TUB');
COMMIT;
