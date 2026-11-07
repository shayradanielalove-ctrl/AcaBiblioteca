BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "Autores" (
	"IdAutor"	INTEGER,
	"Nombre"	TEXT NOT NULL,
	"Apellido"	TEXT NOT NULL,
	PRIMARY KEY("IdAutor" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "Editoriales" (
	"Ideditorial"	INTEGER,
	"Nombre"	INTEGER NOT NULL,
	PRIMARY KEY("Ideditorial" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "Libros" (
	"ISBN"	TEXT,
	"Titulo"	TEXT NOT NULL,
	"IdAutor"	INTEGER NOT NULL,
	"IdEditorial"	INTEGER NOT NULL,
	"Categoria"	TEXT NOT NULL,
	"Año"	INTEGER,
	"Existencias"	INTEGER NOT NULL,
	PRIMARY KEY("ISBN"),
	FOREIGN KEY("IdAutor") REFERENCES "Autores"("IdAutor"),
	FOREIGN KEY("IdEditorial") REFERENCES "Editoriales"("Ideditorial")
);
CREATE TABLE IF NOT EXISTS "Prestamos" (
	"IdPrestamo"	INTEGER,
	"IdUsuarios"	INTEGER NOT NULL,
	"ISBN"	TEXT NOT NULL,
	"FechaPrestamo"	DATE NOT NULL,
	"FechaDevolucion"	DATE,
	"Estado"	TEXT NOT NULL,
	PRIMARY KEY("IdPrestamo" AUTOINCREMENT),
	CONSTRAINT "Prestamos_Libros" FOREIGN KEY("ISBN") REFERENCES "Libros"("ISBN"),
	CONSTRAINT "Prestamos_Usuarios" FOREIGN KEY("IdUsuarios") REFERENCES "Usuarios"("IdUsuarios")
);
CREATE TABLE IF NOT EXISTS "Usuarios" (
	"IdUsuarios"	INTEGER,
	"Nombre"	TEXT NOT NULL,
	"Apellido"	TEXT NOT NULL,
	"Documento"	TEXT NOT NULL,
	"Telefono"	TEXT NOT NULL,
	"Correo"	TEXT NOT NULL,
	PRIMARY KEY("IdUsuarios" AUTOINCREMENT)
);
INSERT INTO "Autores" ("IdAutor","Nombre","Apellido") VALUES (1,'Gabriel','García Márquez');
INSERT INTO "Autores" ("IdAutor","Nombre","Apellido") VALUES (2,'Julio','Cortázar');
INSERT INTO "Autores" ("IdAutor","Nombre","Apellido") VALUES (3,'Isabel','Allende');
INSERT INTO "Autores" ("IdAutor","Nombre","Apellido") VALUES (4,'George','Orwell');
INSERT INTO "Autores" ("IdAutor","Nombre","Apellido") VALUES (5,'Miguel','de Cervantes');
INSERT INTO "Autores" ("IdAutor","Nombre","Apellido") VALUES (6,'Jane','Austen');
INSERT INTO "Autores" ("IdAutor","Nombre","Apellido") VALUES (7,'Julio','Cortázar');
INSERT INTO "Autores" ("IdAutor","Nombre","Apellido") VALUES (8,'Isabel','Allende');
INSERT INTO "Autores" ("IdAutor","Nombre","Apellido") VALUES (9,'Mario','Vargas Llosa');
INSERT INTO "Autores" ("IdAutor","Nombre","Apellido") VALUES (10,'Jorge Luis','Borges');
INSERT INTO "Autores" ("IdAutor","Nombre","Apellido") VALUES (11,'Antoine','de Saint-Exupéry');
INSERT INTO "Autores" ("IdAutor","Nombre","Apellido") VALUES (12,'Ernest','Hemingway');
INSERT INTO "Editoriales" ("Ideditorial","Nombre") VALUES (1,'Planeta');
INSERT INTO "Editoriales" ("Ideditorial","Nombre") VALUES (2,'Alfaguara');
INSERT INTO "Editoriales" ("Ideditorial","Nombre") VALUES (3,'Penguin Random House');
INSERT INTO "Editoriales" ("Ideditorial","Nombre") VALUES (4,'Debolsillo');
INSERT INTO "Editoriales" ("Ideditorial","Nombre") VALUES (5,'Anagrama');
INSERT INTO "Editoriales" ("Ideditorial","Nombre") VALUES (6,'Seix Barral');
INSERT INTO "Editoriales" ("Ideditorial","Nombre") VALUES (7,'Tusquets Editores');
INSERT INTO "Libros" ("ISBN","Titulo","IdAutor","IdEditorial","Categoria","Año","Existencias") VALUES ('9780307474728','Cien años de soledad',1,1,'Novela',1967,5);
INSERT INTO "Libros" ("ISBN","Titulo","IdAutor","IdEditorial","Categoria","Año","Existencias") VALUES ('9780451524935','1984',4,3,'Distopía',1949,4);
INSERT INTO "Libros" ("ISBN","Titulo","IdAutor","IdEditorial","Categoria","Año","Existencias") VALUES ('9780060934347','Don Quijote de la Mancha',5,1,'Novela',1605,3);
INSERT INTO "Libros" ("ISBN","Titulo","IdAutor","IdEditorial","Categoria","Año","Existencias") VALUES ('9780141439518','Orgullo y prejuicio',6,4,'Novela romántica',1813,5);
INSERT INTO "Libros" ("ISBN","Titulo","IdAutor","IdEditorial","Categoria","Año","Existencias") VALUES ('9788437604947','Rayuela',2,2,'Novela',1963,2);
INSERT INTO "Libros" ("ISBN","Titulo","IdAutor","IdEditorial","Categoria","Año","Existencias") VALUES ('9788401352836','La casa de los espíritus',3,1,'Realismo mágico',1982,4);
INSERT INTO "Libros" ("ISBN","Titulo","IdAutor","IdEditorial","Categoria","Año","Existencias") VALUES ('9788420471839','La ciudad y los perros',9,6,'Novela',1963,3);
INSERT INTO "Libros" ("ISBN","Titulo","IdAutor","IdEditorial","Categoria","Año","Existencias") VALUES ('9788420633114','Ficciones',10,7,'Cuentos',1944,2);
INSERT INTO "Libros" ("ISBN","Titulo","IdAutor","IdEditorial","Categoria","Año","Existencias") VALUES ('9780156012195','El principito',11,3,'Literatura infantil',1943,6);
INSERT INTO "Libros" ("ISBN","Titulo","IdAutor","IdEditorial","Categoria","Año","Existencias") VALUES ('9780684830490','El viejo y el mar',12,5,'Novela',1952,3);
INSERT INTO "Libros" ("ISBN","Titulo","IdAutor","IdEditorial","Categoria","Año","Existencias") VALUES ('9780307389732','El amor en los tiempos del cólera',1,1,'Novela',1985,4);
INSERT INTO "Usuarios" ("IdUsuarios","Nombre","Apellido","Documento","Telefono","Correo") VALUES (1,'Ana','Pérez','1001001001','3001234567','ana@gmail.com');
INSERT INTO "Usuarios" ("IdUsuarios","Nombre","Apellido","Documento","Telefono","Correo") VALUES (2,'Carlos','Gómez','1001001002','3012345678','carlos@gmail.com');
INSERT INTO "Usuarios" ("IdUsuarios","Nombre","Apellido","Documento","Telefono","Correo") VALUES (3,'María','Rodríguez','1001001003','3023456789','maria@gmail.com');
INSERT INTO "Usuarios" ("IdUsuarios","Nombre","Apellido","Documento","Telefono","Correo") VALUES (4,'Laura','Martínez','1001001004','3034567890','laura.martinez@gmail.com');
INSERT INTO "Usuarios" ("IdUsuarios","Nombre","Apellido","Documento","Telefono","Correo") VALUES (5,'Andrés','López','1001001005','3045678901','andres.lopez@gmail.com');
INSERT INTO "Usuarios" ("IdUsuarios","Nombre","Apellido","Documento","Telefono","Correo") VALUES (6,'Sofía','Hernández','1001001006','3056789012','sofia.hernandez@gmail.com');
INSERT INTO "Usuarios" ("IdUsuarios","Nombre","Apellido","Documento","Telefono","Correo") VALUES (7,'Daniel','Torres','1001001007','3067890123','daniel.torres@gmail.com');
INSERT INTO "Usuarios" ("IdUsuarios","Nombre","Apellido","Documento","Telefono","Correo") VALUES (8,'Mariana','Ramírez','1001001008','3078901234','mariana.ramirez@gmail.com');
INSERT INTO "Usuarios" ("IdUsuarios","Nombre","Apellido","Documento","Telefono","Correo") VALUES (9,'Felipe','Castro','1001001009','3089012345','felipe.castro@gmail.com');
INSERT INTO "Usuarios" ("IdUsuarios","Nombre","Apellido","Documento","Telefono","Correo") VALUES (10,'Valentina','Morales','1001001010','3090123456','valentina.morales@gmail.com');
COMMIT;
