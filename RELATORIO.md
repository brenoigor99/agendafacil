
# RELATÓRIO DO PROJETO DA UNIDADE 1 — AGENDAFÁCIL

* **Integrantes (nome e matrícula):** Breno Igor da Silva (20250065477)
* **Linguagem:** Python (3.10+)
* **Repositório:** https://github.com/brenoigor99/agendafacil

---

## 1. Diagnóstico do código-base

| # | Categoria | Anomalia e onde está | Por que é um problema |
|---|---|---|---|
| 1 | Adequação e lógica | Ausência de validação de término do expediente na função `add` (linhas 13-14). | Permite agendamento às 17h30 com 60 minutos de duração, ultrapassando o horário de fechamento da clínica. |
| 2 | Adequação e lógica | Lógica de verificação de conflitos duplicada e inline nas funções `add` e `rem` (linhas 18-20 e 34-36). | Viola o princípio DRY; qualquer alteração futura na regra de conflito exigirá manutenção em múltiplos locais. |
| 3 | Manutenibilidade | Uso de listas indexadas genéricas (`a[0]`, `a[1]`, `a[2]`, etc.) em todo o código. | Torna o código extremamente frágil e ilegível; mudar a ordem dos elementos quebra a aplicação sem aviso prévio. |
| 4 | Manutenibilidade | Função `add` acumula validação, regra de negócio, manipulação de lista e impressão em um único bloco. | Viola o princípio de responsabilidade única (SRP), dificultando testes automatizados e reutilização. |
| 5 | Organização e estética | Números mágicos espalhados pelo código (`8`, `18`, `0`). | Dificulta a compreensão do domínio do negócio por novos desenvolvedores, pois os limites de horário não são explicitados. |
| 6 | Organização e estética | Comentário desatualizado em `lst` dizendo "lista os atendimentos do mes" quando na verdade filtra por dia exato. | Confunde quem lê a documentação e o código, gerando falsas expectativas sobre o comportamento da função. |
| 7 | Programação defensiva e segurança | Bloco `try...except: pass` genérico e vazio na função `add` (linhas 30-31). | Engole exceções e falhas críticas silenciosamente, impossibilitando o rastreamento de bugs de runtime. |
| 8 | Programação defensiva e segurança | Falta de validação de formato de data (`d` recebida como string crua sem checar se é `AAAA-MM-DD`). | Permite entradas corrompidas ou malformadas que corrompem a integridade dos dados em memória. |
| 9 | Desempenho e recursos | Busca linear ineficiente aninhada (`for` dentro de `for`) para verificar conflitos em listas grandes. | Embora o volume atual seja baixo, degrada o desempenho desnecessariamente em listas extensas de atendimentos. |
| 10 | Desempenho e recursos | Uso de variáveis globais mutáveis (`ag`) sem encapsulamento ou controle de acesso. | Qualquer parte do código pode corromper o estado global da agenda sem validações prévias. |

---

## 2. O que foi resolvido e o que ficou como dívida

| # | Situação | Como foi resolvida, ou por que ficou |
|---|---|---|
| 1 | Resolvida | Implementada validação explícita do horário de término (`hora + duracao <= 18h`) nas regras de horário. |
| 2 | Resolvida | A lógica de verificação de conflito foi isolada em uma única função pura (`existe_conflito`). |
| 3 | Resolvida | Substituição das listas por uma `dataclass` (`Atendimento`), permitindo acesso por campos nomeados claros. |
| 4 | Resolvida | O código foi modularizado separando validações, lógica de negócio e exibição em funções distintas. |
| 5 | Resolvida | Extração de todos os valores mágicos para constantes nomeadas em caixa alta (`HORARIO_MIN_INICIO`, etc.). |
| 6 | Resolvida | Remoção de comentários ruídos e correção das docstrings explicativas no padrão Google. |
| 7 | Resolvida | Eliminação do `except: pass` genérico, substituído por tratamento específico de exceções. |
| 8 | Resolvida | Adição de função robusta de validação de formato de data (`validar_formato_data`) usando `datetime`. |
| 9 | Dívida assumida | Mantida a busca linear (`for`), pois para o escopo reduzido em memória a complexidade é irrelevante. |
| 10 | Dívida assumida | Mantida a lista global `ag` encapsulada no módulo, pois a introdução de um banco de dados relacional ou ORM viola as restrições técnicas do projeto. |

---

## 3. Decisões de projeto

| Decisão tomada | Alternativa descartada | Por que decidimos assim |
|---|---|---|
| Utilização de `dataclass` para representar os atendimentos. | Dicionários ou tuplas indexadas (`a[0]`). | `dataclasses` fornecem tipagem estática clara, legibilidade superior e acesso a atributos por nome, eliminando os riscos de erros por índices numéricos incorretos. |
| Lançamento de exceções específicas (`ValueError`, `DataInvalidaError`) para entradas inválidas. | Retornar códigos de erro booleanos (`True`/`False`) ou strings de erro. | Segue os princípios modernos de programação defensiva e separação de fluxos de exceção, garantindo que erros críticos não passem despercebidos. |
| Isolar validações em funções de guarda dedicadas (`validar_regras_horario`, `validar_formato_data`). | Validar diretamente dentro da função de cadastro. | Melhora a legibilidade, permite reutilização das regras de validação na remarcação e mantém cada função com uma única responsabilidade. |

---

## 4. Mudanças de comportamento

| Entrada ou situação | O que acontecia antes | O que acontece agora |
|---|---|---|
| Entrada de data com formato inválido (ex: `10-05-2026`) | O sistema aceitava silenciosamente e gerava inconsistências na listagem. | O sistema lança uma exceção `DataInvalidaError` detalhando o erro esperado. |
| Tentativa de agendamento fora do expediente (ex: 20h) | O sistema falhava silenciosamente (ignorava o comando) sem avisar ninguém. | O sistema intercepta e levanta uma exceção `HorarioInvalidoError` explicativa. |

---

## 5. Como executar e gerar a documentação

| Item | Resposta |
|---|---|
| **Comando para compilar e executar** | `python3 agenda.py` |
| **Comando para gerar a documentação de API** | `pdoc agenda.py -o docs/` |
| **Onde a documentação gerada ficou no repositório** | Pasta `docs/` |
| **Saída do programa de demonstração** | `Atendimento marcado para Ana`<br>`Horario ocupado`<br>`Atendimento marcado para Carla`<br>`Remarcado`<br>`14 Carla Dra. Souza MARCADO` |

---

## 6. Uso de ferramentas de IA

* **Foram usadas ferramentas de IA neste trabalho?** (X) Sim &nbsp;&nbsp;&nbsp;&nbsp; ( ) Não
* **Em quais etapas, e para quê?** A IA foi Utilizada para auxiliar na estruturação do diagnóstico, sugestão de refatoração com dataclasses e na revisão da documentação (docstrings e README).