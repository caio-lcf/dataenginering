# Documentação de Arquitetura e Decisões de Engenharia de Dados

Este documento traz um resumo das principais decisões arquiteturais, estrutura do projeto e lógicas de transformação implementadas no fluxo de dados atual.

## 1. Arquitetura do Data Lake (Medallion Architecture)
O projeto adota a **Arquitetura Medallion** em um sistema de arquivos local (`c:/dataenginering/data/`), dividindo o armazenamento e processamento de dados nas seguintes camadas lógicas:
- **Raw**: Armazenamento dos dados brutos consumidos da API no formato original (`JSON`).
- **Bronze**: Conversão direta dos arquivos `JSON` da camada Raw para o formato colunar `Parquet` mantendo os dados como estão (schema copy).
- **Silver**: Dados da camada Bronze tratados, filtrados e mesclados, garantindo a qualidade e o schema ajustado às necessidades analíticas no formato `Parquet`.
- **Gold** (ainda sem uso): Camada destinada aos modelos de dados agregados, tabelas prontas para relatórios ou consumo final.

### Particionamento
Os dados ingeridos são salvos em estruturas de pastas orientadas a datas (`{date_of_collect}`) com o formato `DD-MM-YYYY` em todas as camadas, facilitando a recuperação e governança diária.

## 2. Decisões de Extração (Camada Raw)
A extração é feita via REST API para o **TMDB (The Movie Database)**.
- **Processo**: São coletados filmes populares (`movie/now_playing`) e os gêneros associados (`genre/movie/list`).
- **Data Quality Ingestion_Time**: Foi adicionada uma coluna sintética de `ingestion_time` via Python nativo (formato ISO) direto na resposta JSON antes de salvar, permitindo versionamento temporal das extrações.
- **Armazenamento**: O payload original é salvo usando a biblioteca padrão de `json` do Python. 

## 3. Decisões de Transformação e Tratamento (Python & Pandas)
O processamento usa **Pandas** pelo seu suporte nativo ao formato Parquet (eficiente, fortemente tipado e com compressão) e facilidades analíticas de transformação:

### Conversão Raw → Bronze
- Leitura direta via `pd.read_json` e exportação instantânea via `to_parquet()`. O objetivo é tirar o dado rápido de JSON (custoso de processar em bulk) e colocar como Parquet, garantindo melhor performance nos passos de tratamento.

### Conversão Bronze → Silver
O tratamento principal do dado e normalização ocorre nesta etapa:
1. **Explosion Array**: O campo `genre_ids` no arquivo de filmes vem como um Array no JSON original. Uma decisão crucial de design foi usar o comando `.explode("genre_ids")` do Pandas, que transforma cada ID dentro da lista de gêneros em uma nova linha no DataFrame.
2. **Merge/Join Híbrido**: Foi realizado um `LEFT JOIN` (`.merge(how="left")`) da tabela base de filmes com os metadados extraídos de gêneros, possibilitando que a base príncipal tenha o nome do gênero em vez dos IDs.
3. **Seleção de Colunas (Drop)**: Alguns campos de payload visual, que muitas vezes enchem relatórios como `backdrop_path`, `poster_path` e `video` foram dispensados com `.drop()`. O `id_y` (referente ao ID do gênero cruzado) também é removido após a obtenção do nome.
4. **Renomeação**: Padronização dos schemas com nomes mais significativos, renomeando a chave interna `id_x` para `movie_id`, e `name` (genérico) para `genre_name`.

## 4. Gerenciamento de Dependências e Configuração (`config.py`)
- **Centralização:** Paths (Raw, Bronze, etc.), Endpoints e Variáveis de data ficam isolados em um script de configuração dedicado, facilitando a escalabilidade.

## Próximos Passos (To-Dos mapeados no código)
- Tratar cenários com múltiplas páginas e paginação na chamada da API (`Pegar mais páginas`).
