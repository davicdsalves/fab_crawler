CREATE TABLE raw_data (
  ID int NOT NULL AUTO_INCREMENT,
  autoridade           VARCHAR(255) NOT NULL,
  origem               VARCHAR(255) NOT NULL,
  data_decolagem       DATETIME NOT NULL,
  destino              VARCHAR(255) NOT NULL,
  data_pouso           DATETIME NOT NULL,
  motivo               VARCHAR(255) NOT NULL,
  previsao_passageiros INT NOT NULL,
  PRIMARY KEY (ID)
);