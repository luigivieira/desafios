# Desafio 2: Crawlers

Parte do trabalho na IDwall inclui desenvolver *crawlers/scrapers* para coletar dados de websites.
Como nós nos divertimos trabalhando, às vezes trabalhamos para nos divertir!

O Reddit é quase como um fórum com milhares de categorias diferentes. Com a sua conta, você pode navegar por assuntos técnicos, ver fotos de gatinhos, discutir questões de filosofia, aprender alguns life hacks e ficar por dentro das notícias do mundo todo!

Subreddits são como fóruns dentro do Reddit e as postagens são chamadas *threads*.

Para quem gosta de gatos, há o subreddit ["/r/cats"](https://www.reddit.com/r/cats) com threads contendo fotos de gatos fofinhos.
Para *threads* sobre o Brasil, vale a pena visitar ["/r/brazil"](https://www.reddit.com/r/brazil) ou ainda ["/r/worldnews"](https://www.reddit.com/r/worldnews/).
Um dos maiores subreddits é o "/r/AskReddit".

Cada *thread* possui uma pontuação que, simplificando, aumenta com "up votes" (tipo um like) e é reduzida com "down votes".

Sua missão é encontrar e listar as *threads* que estão bombando no Reddit naquele momento!
Consideramos como bombando *threads* com 5000 pontos ou mais.

# Solução

## Dependências

A minha solução para esse desafio também foi construída em Python 3. Porém, diferentemente do desafio anterior que utiliza apenas recursos nativos do Python, esta solução requer alguns pacotes que precisam ser instalados manualmente (via o comando `pip install <nome do pacote>`). São eles:

- [aiohttp](https://aiohttp.readthedocs.io/en/stable/)
- [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI)

O primeiro é utilizado para a comunicação HTTP com o servidor do Reddit, e o segundo para a comunicação do bot com o serviço do Telegram.

## Parte 1

A solução foi implementada em Python 3. O código da solução se encontra no arquivo `reddit.py` via a função assíncrona `get_subreddits`.

Ao invés de fazer webscrap no HTML, eu optei por acessar diretamente os dados disponíveis do servidor em formato JSON, já que o Reddit fornece uma API REST para tal. Exemplo de chamada nessa api:

GET https://old.reddit.com/r/cats/top.json?sort=top&t=day&limit=2

Retorna um JSON com as duas threads de maior score no subreddit "cats" na data de hoje (isto é, nas últimas 24 horas)

A função `get_subreddits` retorna um dicionário Python, de forma que a parte 1 foi implementada no arquivo de script `list_top_r.py`, um CLI que simplesmente processa esse dicionário e imprime na saída padrão os dados formatados. Ele é parametrizável via argumentos da linha de comando, de forma que se pode definir o número máximo de threads obtidas (utilizado para limitar a carga no servidor e na comunicação, com default em 50) e o score mínimo para uma thread ser considerada como "bombando" (utilizando o default de 5000, como indicado no enunciado). A sintaxe de chamada do programa pode ser obtida executando-se `python list_top_r.py -h`, produzindo a seguinte saída:

	usage: list_top_r.py [-h] -s "name[;name;...]" [-l value] [-m value]

	Lists the top reddit threads for the given subreddits. Created by Luiz C.
	Vieira for the IDWall Challenge (2018).

	optional arguments:
	  -h, --help            show this help message and exit
	  -s "name[;name;...]", --subreddits "name[;name;...]"
							Semicolon-separated list of subreddit names to query.
							IMPORTANT: The quotes are mandatory if you are
							providing more than one name, since the semicolons
							will be understood by the command line processor as
							separators for different commands.
	  -l value, --limit value
							Limit of threads to get for each subreddit. The
							default value is 50, and the minimum acceptable value
							is 1.
	  -m value, --min_score value
							Minimum score for threads to be considered as top,
							besides the indication of reddit itself. The default
							value is 5000, and the minimum acceptable value is 0
							(case in which this argument is disconsidered).
							
Exemplo de execução:

	> python list_top_r.py -s "cats;brazil" -l 10 -m 4000	
	================================================================================
	TOP THREADS ON REDDIT TODAY (limiting in 10 threads with minimum score of 4000)
	================================================================================
	SUBREDDIT: cats

			URL: https://v.redd.it/vohzzhby5mt11
			TITLE: Throwback to when my cat decided to race the laundry basket around the house. I still to this day don’t know how she managed this.
			SCORE: 10541
			UP VOTES: 10541
			DOWN VOTES: 0
			AUTHOR: Sw1fty3
			NUMBER OF COMMENTS: 159
			COMMENTS URL: https://old.reddit.com/r/cats/comments/9q7r5a/throwback_to_when_my_cat_decided_to_race_the/

			URL: https://imgur.com/gtJGlem
			TITLE: This is Zuli. She's 20 years old and I just adopted her Friday
			SCORE: 5528
			UP VOTES: 5528
			DOWN VOTES: 0
			AUTHOR: Meatloaf_In_Africa
			NUMBER OF COMMENTS: 134
			COMMENTS URL: https://old.reddit.com/r/cats/comments/9q9mr6/this_is_zuli_shes_20_years_old_and_i_just_adopted/

			URL: https://i.redd.it/rs41h3a77qt11.jpg
			TITLE: 18 years later and he is still killing it
			SCORE: 6441
			UP VOTES: 6441
			DOWN VOTES: 0
			AUTHOR: TheColorPeanut
			NUMBER OF COMMENTS: 83
			COMMENTS URL: https://old.reddit.com/r/cats/comments/9qd3x0/18_years_later_and_he_is_still_killing_it/

	SUBREDDIT: brazil

			There are no threads in the query conditions (i.e. limit and minimum score)

Outro exemplo:

	python list_top_r.py -s "cats;brazil" -l 1 -m 0
	================================================================================
	TOP THREADS ON REDDIT TODAY (limiting in 1 threads with minimum score of 0)
	================================================================================
	SUBREDDIT: cats

			URL: https://v.redd.it/vohzzhby5mt11
			TITLE: Throwback to when my cat decided to race the laundry basket around the house. I still to this day don’t know how she managed this.
			SCORE: 10542
			UP VOTES: 10542
			DOWN VOTES: 0
			AUTHOR: Sw1fty3
			NUMBER OF COMMENTS: 159
			COMMENTS URL: https://old.reddit.com/r/cats/comments/9q7r5a/throwback_to_when_my_cat_decided_to_race_the/

	SUBREDDIT: brazil

			URL: https://www.reddit.com/r/brasil
			TITLE: Looking to ask or post somethinga about Brazil? Check r/brasil!
			SCORE: 14
			UP VOTES: 14
			DOWN VOTES: 0
			AUTHOR: Tetizeraz
			NUMBER OF COMMENTS: 2
			COMMENTS URL: https://old.reddit.com/r/Brazil/comments/92vupe/looking_to_ask_or_post_somethinga_about_brazil/

	================================================================================

## Parte 2

A solução, também implementada em Python 3, está no arquivo `telegram_bot.py`. Ele é um servidor CLI que responde às requisições do bot para o token fornecido na linha de comando da execução do script. O script, quando executado como `python telegram_bot.py -h` exibe a seguinte ajuda:

	usage: telegram_bot.py [-h] -t digits

	Implementation of the Telegram Bot named @OciosDoOficioBot. Created by Luiz C.
	Vieira for the IDWall Challenge (2018).

	optional arguments:
	  -h, --help            show this help message and exit
	  -t digits, --token digits
							The token created by the @BotFather and used to
							command the OciosDoOficioBot bot.

Ou seja, para utilizá-la, simplesmente crie um novo bot no Telegram (utilizando @BotFather e seguindo a documentação online), e utilize o token obtido na execução do script. O nome do bot utilizado nos testes foi @OciosDoOficio, mas você pode utilizar qualquer nome de bot.