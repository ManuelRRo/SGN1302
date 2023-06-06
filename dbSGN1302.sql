drop table if exists ALUMNO;

drop table if exists CATEGORIA;

drop table if exists DOCENTE;

drop table if exists EVALUACION;

drop table if exists EVALUACIONALUMNO;

drop table if exists FICHAALUMNO;

drop table if exists FICHADOCENTE;

drop table if exists GRADO;

drop table if exists GRADOSECCION;

drop table if exists GRADOSECCIONMATERIA;

drop table if exists MATERIA;

drop table if exists SECCION;

drop table if exists TRIMESTRE;

create table ALUMNO
(
   ID_ALUMNO            int not null AUTO_INCREMENT,
   ID_GRADOSECCION      int,
   NIE                  char(7),
   APELLIDOS_ALUMNO     char(50),
   NOMBRES_ALUMNO       char(50),
   primary key (ID_ALUMNO)
);

create table CATEGORIA
(
   ID_CATEGORIA         int not null AUTO_INCREMENT,
   NOMBRE_CATEGORIA     varchar(30) not null,
   primary key (ID_CATEGORIA)
);

create table DOCENTE
(
   ID_DOCENTE           int not null AUTO_INCREMENT,
   NUMIDENTIFICACION    char(8),
   DUI                  char(8),
   NOMBRE_DOCENTE       char(50),
   APELLIDO_DOCENTE     char(50),
   primary key (ID_DOCENTE)
);

create table EVALUACION
(
   ID_EVALUACION        int not null AUTO_INCREMENT,
   ID_CATEGORIA         int,
   ID_GRADOSECCIONMATERIA int,
   ID_TRIMESTRE         int,
   NOMBRE_EVALUACION    char(50),
   PORCENTAJE           char(50),
   primary key (ID_EVALUACION)
);

create table EVALUACIONALUMNO
(
   ID_EVALUACIONALUMNO  int not null AUTO_INCREMENT,
   ID_EVALUACION        int,
   ID_ALUMNO            int,
   NOTA                 float not null,
   primary key (ID_EVALUACIONALUMNO)
);

create table FICHAALUMNO
(
   ID_FICHAALUMNO       int not null AUTO_INCREMENT,
   primary key (ID_FICHAALUMNO)
);

create table FICHADOCENTE
(
   ID_FICHADOCENTE      int not null AUTO_INCREMENT,
   primary key (ID_FICHADOCENTE)
);

create table GRADO
(
   ID_GRADO             int not null AUTO_INCREMENT,
   GRADO                char(50),
   primary key (ID_GRADO)
);

create table GRADOSECCION
(
   ID_GRADOSECCION      int not null AUTO_INCREMENT,
   ID_GRADO             int,
   ID_SECCION           int,
   TURNO_GRADOSECCION   char(1) not null,
   primary key (ID_GRADOSECCION)
);

create table GRADOSECCIONMATERIA
(
   ID_GRADOSECCIONMATERIA int not null AUTO_INCREMENT,
   ID_GRADOSECCION      int,
   ID_MATERIA           int,
   primary key (ID_GRADOSECCIONMATERIA)
);

create table MATERIA
(
   ID_MATERIA           int not null AUTO_INCREMENT,
   ID_DOCENTE           int,
   NOMBRE_MATERIA       char(100),
   primary key (ID_MATERIA)
);

create table SECCION
(
   ID_SECCION           int not null AUTO_INCREMENT,
   SECCION              char(1),
   primary key (ID_SECCION)
);

create table TRIMESTRE
(
   ID_TRIMESTRE         int not null AUTO_INCREMENT,
   TRIMESTRE            char(50),
   ANIO                 char(50),
   primary key (ID_TRIMESTRE)
);

alter table ALUMNO add constraint FK_RELATIONSHIP_7 foreign key (ID_GRADOSECCION)
      references GRADOSECCION (ID_GRADOSECCION) on delete restrict on update restrict;

alter table EVALUACION add constraint FK_RELATIONSHIP_11 foreign key (ID_GRADOSECCIONMATERIA)
      references GRADOSECCIONMATERIA (ID_GRADOSECCIONMATERIA) on delete restrict on update restrict;

alter table EVALUACION add constraint FK_RELATIONSHIP_12 foreign key (ID_CATEGORIA)
      references CATEGORIA (ID_CATEGORIA) on delete restrict on update restrict;

alter table EVALUACION add constraint FK_RELATIONSHIP_15 foreign key (ID_TRIMESTRE)
      references TRIMESTRE (ID_TRIMESTRE) on delete restrict on update restrict;

alter table EVALUACIONALUMNO add constraint FK_RELATIONSHIP_13 foreign key (ID_EVALUACION)
      references EVALUACION (ID_EVALUACION) on delete restrict on update restrict;

alter table EVALUACIONALUMNO add constraint FK_RELATIONSHIP_14 foreign key (ID_ALUMNO)
      references ALUMNO (ID_ALUMNO) on delete restrict on update restrict;

alter table GRADOSECCION add constraint FK_RELATIONSHIP_6 foreign key (ID_GRADO)
      references GRADO (ID_GRADO) on delete restrict on update restrict;

alter table GRADOSECCION add constraint FK_RELATIONSHIP_9 foreign key (ID_SECCION)
      references SECCION (ID_SECCION) on delete restrict on update restrict;

alter table GRADOSECCIONMATERIA add constraint FK_RELATIONSHIP_10 foreign key (ID_MATERIA)
      references MATERIA (ID_MATERIA) on delete restrict on update restrict;

alter table GRADOSECCIONMATERIA add constraint FK_RELATIONSHIP_8 foreign key (ID_GRADOSECCION)
      references GRADOSECCION (ID_GRADOSECCION) on delete restrict on update restrict;

alter table MATERIA add constraint FK_RELATIONSHIP_4 foreign key (ID_DOCENTE)
      references DOCENTE (ID_DOCENTE) on delete restrict on update restrict;

