DROP PROCEDURE IF EXISTS ADD_VOO_PASSAGEIRO;
DELIMITER //
CREATE PROCEDURE ADD_VOO_PASSAGEIRO()
MODIFIES SQL DATA
  BEGIN
    DECLARE no_more_rows BOOLEAN;
    DECLARE number_of_rows INT DEFAULT 0;
    DECLARE loop_control INT DEFAULT 0;
    DECLARE autoridade_normalizado VARCHAR(255);
    DECLARE tmp_gabinete_id VARCHAR(255);
    DECLARE gabinete_normalizado VARCHAR(255);
    DECLARE tmp_voo_id INT(11);
    DECLARE tmp_passageiro_id INT(11);

    DECLARE cursor_autoridade VARCHAR(255);
    DECLARE cursor_origem VARCHAR(255);
    DECLARE cursor_data_decolagem DATETIME;
    DECLARE cursor_destino VARCHAR(255);
    DECLARE cursor_data_pouso DATETIME;
    DECLARE cursor_motivo VARCHAR(255);
    DECLARE cursor_previsao_passageiros INT(11);

    DECLARE raw_data_cursor CURSOR FOR SELECT
                                         autoridade,
                                         origem,
                                         data_decolagem,
                                         destino,
                                         data_pouso,
                                         motivo,
                                         previsao_passageiros
                                       FROM raw_data;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET no_more_rows = TRUE;

    OPEN raw_data_cursor;
    SELECT FOUND_ROWS()
    INTO number_of_rows;

    data_loop: LOOP

      FETCH raw_data_cursor
      INTO cursor_autoridade, cursor_origem, cursor_data_decolagem, cursor_destino, cursor_data_pouso, cursor_motivo, cursor_previsao_passageiros;

      IF no_more_rows
      THEN
        CLOSE raw_data_cursor;
        LEAVE data_loop;
      END IF;

      # obtem o voo pois foi salvo em outro momento.
      SET tmp_voo_id = (SELECT V.VOO_ID
                        FROM VOO V
                        WHERE V.ORIGEM = cursor_origem AND V.DESTINO = cursor_destino AND V.DT_DECOLAGEM = cursor_data_decolagem AND V.DT_POUSO = cursor_data_pouso);

      # normaliza autoridade para obter um passageiro unico, mas mantendo o texto do pdf
      SET autoridade_normalizado = REPLACE(
          REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(cursor_autoridade, '(1)', ''), '(2)', ''), '(3)', ''), '(4)', ''),
                  '(Interino)', 'Interino'), '(interino )', 'Interino'); #passageiro

      # obtendo id do passageiro
      SET tmp_passageiro_id = (SELECT P.PASSAGEIRO_ID FROM PASSAGEIRO P WHERE P.NOME = autoridade_normalizado);
      IF (tmp_passageiro_id IS NULL)  # testei e assim foi mais rapido do que usando insert ignore
      THEN
        INSERT INTO PASSAGEIRO (NOME) VALUES (autoridade_normalizado);
        SET tmp_passageiro_id = (SELECT LAST_INSERT_ID());
      END IF;

      # precisamos alterar as variações do nome de autoridade para encontrar o gabinete
      SET gabinete_normalizado = translate_autoridade_gabinete(autoridade_normalizado);
      SET tmp_gabinete_id = (SELECT GABINETE_ID FROM GABINETE WHERE NOME = gabinete_normalizado);
      IF (tmp_gabinete_id IS NULL) THEN
        SELECT gabinete_normalizado, autoridade_normalizado;
      END IF;

      INSERT INTO VOO_PASSAGEIRO (FK_PASSAGEIRO_ID, FK_GABINETE_ID, FK_VOO_ID, MOTIVO, PREVISAO_PASSAGEIROS) VALUES
        (tmp_passageiro_id, tmp_gabinete_id, tmp_voo_id, cursor_motivo, cursor_previsao_passageiros);

      SET loop_control = loop_control + 1;

    END LOOP data_loop;
    SELECT
      number_of_rows,
      loop_control;

  END //
DELIMITER ;