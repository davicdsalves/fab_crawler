DROP FUNCTION IF EXISTS translate_autoridade_gabinete;
CREATE FUNCTION translate_autoridade_gabinete(autoridade varchar(255))
  RETURNS VARCHAR(255)
READS SQL DATA
  BEGIN
    DECLARE parsed_autoridade varchar(255);
    SELECT
      REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(
      REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(
      REPLACE( REPLACE( REPLACE( REPLACE( REPLACE( REPLACE( REPLACE( REPLACE( REPLACE( REPLACE( REPLACE( REPLACE( REPLACE( REPLACE( REPLACE( REPLACE(
      REPLACE (REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(
      lower( REPLACE( IF (LOCATE('(', REPLACE(autoridade, 'do(a)', '')) >0, LEFT(autoridade, LOCATE('(', autoridade)-1), autoridade), 'da PR', '') ),
      'interino', ''),'interina', ''), 'da presidência da república', ''), 'deput.', 'deputados' ), 'das fa', 'das forças armadas'),
      'advogado geral', 'advocacia-geral'), 'advogado-geral', 'advocacia-geral'), 'comandante', 'comando'), 'ministro-chefe da ', ''),
      'ministra-chefe da ', ''), 'ministra chefe da ', ''), 'ministro chefe da ', ''), 'controladoria geral', 'controladoria-geral'),
      'secretário', 'secretaria'), 'disp.', 'disposição'), 'missão à disposição da ' , ''), 'missão à disposição do ' , ''),
      'presidente', 'presidência') , 'ministro-chefe do ', ''), 'de política para', 'de políticas para'),
      'ministro chefe do ', ''), 'à disposição do ', ''), 'à disposição da ', ''), 'à disposição do(a) ', ''),
      'ministro-chefe ', ''), 'chefe do ', ''), ' afastado', ''), ' em exercício', ''), ' em excercício', ''),
      # casos especificos
      'gabinete institucional', 'gabinete de segurança institucional'), 'gab pessoal ', 'gabinete pessoal '),
      'câmara dos deputados comissão especial - transposição de níveis)', 'presidência da câmara dos deputados'),
      'presidência da câmada dos deputados', 'presidência da câmara dos deputados'),
      'ministro dos esportes', 'ministro do esporte'),
      'ministro do desenvolvimento da indústria', 'ministro do desenvolvimento, indústria'),
      'mulheres, igualdade racial e direitos humanos', 'mulheres, da igualdade racial e dos direitos humanos'),
      'transparência, fiscalização e controle', 'transparência, fiscalização e controladoria-geral da união'),
      'ministro da controladoria-geral da união', 'controladoria-geral da união'),
      'secretaria-geral', 'secretaria de governo'),
      'ministro das minas e energia', 'ministério de minas e energia'),
      'ministro desenvolvimento social e agrário', 'ministério do desenvolvimento social e agrário'),
      'secretaria especial de políticas para as mulheres', 'secretaria de políticas para as mulheres'),
      'casa civil  ) ', 'casa civil'),
      'indústria, comércio e serviços', 'indústria, comércio exterior e serviços'),
      'gabinete pessoal da presidenta da república', 'gabinete pessoal da presidência da república'),

      'ministro', 'ministério'), 'ministra', 'ministério') into parsed_autoridade;
    RETURN parsed_autoridade;
  END;