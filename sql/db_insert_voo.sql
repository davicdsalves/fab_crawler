# adiciona informações na tabela de voo, dados repetidos sao ignorados, tabela tem index unico.
INSERT IGNORE INTO VOO (ORIGEM, DESTINO, DT_DECOLAGEM, DT_POUSO)
  (select origem, destino, data_decolagem, data_pouso from raw_data);



