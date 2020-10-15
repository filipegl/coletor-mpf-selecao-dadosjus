# Coletor do MPF para o dadosjus

Este é um coletor do site http://www.transparencia.mpf.mp.br/conteudo/contracheque feito para o [DadosJusBR](https://github.com/dadosjusbr)
## Instruções de execução
É recomendável criar um novo ambiente para execução. Você pode criar um com o [virtualenv](https://pypi.org/project/virtualenv/) utilizando os comandos: 
- `virtualenv env` - Cria um ambiente chamado *env*
- `source env/bin/activate` - Ativa o ambiente

Após a configuração do seu ambiente, instale as bibliotecas necessárias para rodar o coletor:

`pip install -r requirements.txt`

Para iniciar uma coleta dos contracheques de janeiro de 2020, por exemplo, execute o main.py da seguinte forma:

`python main.py --month=1 --year=2020`

Um arquivo .csv contendo as informações dos empregados de acordo com o [datapackage descriptor](https://github.com/dadosjusbr/coletores/blob/master/datapackage_descriptor.json) será baixado na pasta em que foi executado o script .
Caso deseja baixar em outra pasta utilize o parametro `--dir`

Consulte `python main.py --help`

## Como foi feito?

Uma breve descrição de como a implementação foi pensada.

### Como os dados foram baixados?
As próprias URLs das tabelas são estruturadas:
http://www.transparencia.mpf.mp.br/conteudo/contracheque/{tipo}/{ano}/{tipo}\_{ano}_{mes}.pdf<n/>

Onde **tipo** pode ser:
- remuneracao-servidores-ativos
- provento-servidores-inativos
- remuneracao-membros-ativos
- provento-membros-inativos
- valores-percebidos-pensionistas
- valores-percebidos-colaboradores

O **ano** escrito na forma YYYY, \
O **mes** escrito por extenso com a primeira letra maiuscula (e.g Janeiro)



Para as tabelas de verbas idenizatórias e outras remunerações temporárias:
http://www.transparencia.mpf.mp.br/conteudo/contracheque/verbas-indenizatorias-e-outras-remuneracoes-temporarias/{tipo_short}/{ano}/verbas-indenizatorias-e-outras-remuneracoes-temporarias_{ano}_{mes}.pdf<n/>

Onde **tipo_short** pode ser:
- servidores-ativos
- servidores-inativos
- membros-ativos
- membros-inativos
- pensionistas
- colaboradores

Para **ano** e **mes** se aplica a mesma regra do primeiro exemplo.

### Qual o formato dos dados baixados?
Para os contracheques de antes de 06/2019, as tabelas estão disponíveis nos formatos **xls** e **pdf**. Após esta data, estão disponíveis nos formatos **ods** e **pdf**.

Eu escolhi trabalhar com **pdf** pelo fato de estar disponível em todos os casos.
Utilizei a biblioteca [tabula-py](https://pypi.org/project/tabula-py/) que facilitou bastante o trabalho de download e conversão para [*DataFrame*](https://pt.wikipedia.org/wiki/Pandas_(software)).

Caso não exista nenhum arquivo com a data passada, o *tabula* retorna um erro com mensagem `HTTP Error 404: Not Found`.

O ponto negativo é o tempo de download e conversão do *pdf* para *dataframe*.\
Para minimizar este tempo, é necessário trabalhar com os arquivos **xls** e **ods**. (Está na lista de TODO ✅)
## Dificuldades
Percebi que os contracheques tem dois tipos de formatação.
São separadas pela data 07/2019. \
Para um melhor entendimento, vamos chamar a formatação antes desta data de **formatação velha**, e formatação a partir desta data de **formatação nova**. \
Na formatação nova existe uma coluna para "matrícula" e uma para "nome". Na formatação velha estas duas colunas são agrupadas em uma chamada "Nome ou Matrícula". \
Outro problema são nomes de colunas diferentes: na formatação nova, a 12ª coluna se chama "verbas idenizatórias", já na formatação velha esta mesma coluna move-se para a penultima posição passa a se chamar "Idenizações".

A partir de 07/2019 pode-se acessar detalhes sobre [verbas idenizatórias e outras remunerações temporárias](http://www.transparencia.mpf.mp.br/conteudo/contracheque/verbas-indenizatorias-e-outras-remuneracoes-temporarias). É possível visualizar campos como **auxílio-alimentação**, **ajuda de custo** e etc. \
Nestes casos, é feito um *merge* da tabela principal com esta tabela. \
Já os contracheques anteriores a esta data são desprovidos destas informações.

O grande desafio foi perceber e fazer a separação e formatação individual destes dois tipos de casos.
