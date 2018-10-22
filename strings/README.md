# Desafio 1: Strings

Após ler o coding style do kernel Linux, você descobre a mágica que é
ter linhas de código com no máximo 80 caracteres cada uma.

Assim, você decide que de hoje em diante seus e-mails enviados também
seguirão um padrão parecido e resolve desenvolver um plugin para te ajudar
com isso. Contudo, seu plugin aceitará no máximo 40 caracteres por linha.

Implemente uma função que receba:
1. um texto qualquer
2. um limite de comprimento

e seja capaz de gerar os outputs dos desafios abaixo.

# Solução

A solução foi implementada em Python 3. O código da solução se encontra no arquivo `stringutils.py`, e é acessada por meio da função `word_wrap_text`.

A parte 1 é realizada simplesmente quebrando as palavras em grupos que formem linhas de tamanho máximo igual ao parâmetro dado. Ou seja, se uma próxima palavra sendo processada não couber na linha atual, ela será usada como palavra inicial da próxima linha. Isso é realizado pela função auxiliar chamada `_break_by_max_len`.

A parte 2 é realizada a partir da parte 1. Ou seja, primeiramente as palavras são agrupadas em linhas considerando o limite dado. Então, um algoritmo é utilizado para distribuir os espaçamentos no final de uma linha entre as palavras que formam essa linha. Esse algoritmo, implementado pela função auxiliar `_add_justification_spaces`, funciona assim:

- Primeiramente ele trata os casos especiais, em que uma linha não tem nenhuma ou somente 1 palavra (casos que podem ocorrer se o limite de colunas é muito baixo).
- Então processa de acordo com as seguintes regras (veja que não é exatamente um pseudocódigo - mas você pode obter detalhes nos comentários dentro do código):
	1. São calculados os números de espaços únicos já existentes na linha (separando cada palavra) e o número de espaços necessários para que a linha seja justificada (i.e. o número de espaços finais até que a linha tenha exatamente o tamanho mínimo utilizado para a quebra)
	2. Um "salto" (variável `step` no código) é calculado como a diferença absoluta entre essas duas quantidades de espaços. Esse salto é utilizado para distribuir os espaços adicionais necessários de forma igualmente balanceada, para que a linha permaneça suficientemente equilibrada e bonita.
	3. O algoritmo sempre inicia na primeira palavra (de forma que se existir apenas 1 espaço adicional necessário, ele seja colocado ali), e adiciona um espaço ao final de uma palavra se e somente se ela não for a última da linha.
	4. Após adicionar um espaço na palavra, o algoritmo pula para a próxima palavra na lista (linha) segundo o pulo calculado.
	5. O algoritmo circula o array, de forma que ao pular da última palavra ele retorna para o início da lista proporcionalmente ao salto utilizado.
	
Exemplo de código utilizando a função:

	from stringutils import word_wrap_text

	with open('input.txt', mode='r', encoding='utf-8') as file:
		_input = file.read()

	max_len = 80
	print(f'Quebra em {max_len} colunas sem justificar:')
	print('-' * max_len)
	_output = word_wrap_text(_input, max_line_len=max_len, justify=False)
	print(_output)
	print('-' * max_len)

	print('')

	print(f'Quebra em {max_len} colunas justificando:')
	print('-' * max_len)
	_output = word_wrap_text(_input, max_line_len=max_len, justify=True)
	print(_output)
	print('-' * max_len)

Esse código, se salvo em um arquivo chamado `run.py`, pode ser executado da seguinte forma na linha de comando:

	python run.py
	
E ele produz a seguinte saída:

	Quebra em 80 colunas sem justificar:
	--------------------------------------------------------------------------------
	In the beginning God created the heavens and the earth. Now the earth was
	formless and empty, darkness was over the surface of the deep, and the Spirit of
	God was hovering over the waters.

	And God said, "Let there be light," and there was light. God saw that the light
	was good, and he separated the light from the darkness. God called the light
	"day," and the darkness he called "night." And there was evening, and there was
	morning - the first day.

	--------------------------------------------------------------------------------

	Quebra em 80 colunas justificando:
	--------------------------------------------------------------------------------
	In  the beginning  God created  the heavens  and the  earth. Now  the earth  was
	formless and empty, darkness was over the surface of the deep, and the Spirit of
	God           was           hovering          over          the          waters.

	And  God said, "Let there be light," and there was light. God saw that the light
	was  good, and he separated  the light from the darkness.  God called the  light
	"day,"  and the darkness he called "night." And there was evening, and there was
	morning               -               the               first               day.

	--------------------------------------------------------------------------------

Os testes unitários foram criados no arquivo `tests.py` e são executados utilizando o módulo nativo do Python chamado [unittest](https://docs.python.org/3/library/unittest.html) da seguinte forma na linha de comando:

	python -m unittest tests.py

Nele há testes para avaliar o resultado da entrada de exemplo e alguns outros testes adicionais (utilizando, por exemplo, o famoso texto [Lorem ipsum](https://pt.wikipedia.org/wiki/Lorem_ipsum)). A documentação dos testes está dentro do próprio código dessa classe.