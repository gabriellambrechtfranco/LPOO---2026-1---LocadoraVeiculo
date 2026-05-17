# LPOO - 2026-1 - Locadora de Veículos

Este é o projeto base utilizado na disciplina de **Linguagem de Programação Orientada a Objetos (LPOO)** do curso de Ciência da Computação, semestre **2026-1**, ministrada pela **Professora Vanessa**.

O objetivo deste projeto é servir como base prática para a aplicação de conceitos de Orientação a Objetos e Padrões de Projeto (Design Patterns) estudados em sala de aula.

## Tutoriais

Os guias práticos para a implementação dos padrões de projeto no sistema da locadora estão disponíveis na pasta `tutoriais/`:

*   [Aula 2 - Factory Method](<tutoriais/aula-2-tutorial--factory--locadora-veiculos.md>)
*   [Aula 3.1 - Strategy](<tutoriais/aula-3-1-tutorial-strategy--locadora-veiculos.md>)
*   [Aula 3.2 - State](<tutoriais/aula-3-2-tutorial-state--locadora-veiculos.md>)
*   [Aula 3.3 - Decorator](<tutoriais/aula-3-3-tutorial-decorator--locadora-veiculos.md>)

## Funcionalidades implementadas

Foram adicionadas as telas de locacoes solicitadas na atividade:

* Menu principal com as opcoes Cadastro > Veiculo, Cadastro > Locacoes (Admin) e Acao > Locar Veiculo.
* Tela administrativa de locacoes com cadastro, edicao, visualizacao e remocao.
* Tela operacional da locadora com nova reserva, locar, devolver, cancelar e ver detalhes.
* Controle de status da locacao: reservado, locado, devolvido e cancelado.
* Validacao de disponibilidade de veiculos por periodo e categoria para novas reservas.

## Detalhamento de Aprendizado

Durante o desenvolvimento foi necessario revisar a estrutura MVC do projeto e separar a responsabilidade das telas, controllers e modelos. A maior dificuldade foi organizar o fluxo entre janelas `tk.Toplevel`, principalmente para recarregar a listagem apos fechar uma tela de cadastro usando `wait_window`.

O principal aprendizado foi entender melhor como o estado de uma locacao muda conforme as acoes do usuario: uma reserva pode virar locacao ativa, depois devolucao, ou pode ser cancelada antes da retirada. Tambem ficou mais claro como validar periodos de datas para evitar que o mesmo veiculo seja reservado em intervalos conflitantes.

## Declaracao de Uso de IA

- [ ] Nenhuma IA foi utilizada na elaboracao deste codigo.
- [x] Utilizei IA como ferramenta de apoio.
- Ferramenta: ChatGPT.
- Finalidade: apoio na organizacao das telas Tkinter, implementacao do controller de locacoes e validacao dos fluxos de criar, editar, locar, devolver e cancelar.
- Validacao: o codigo foi revisado e testado localmente antes da entrega.

---

### ⚠️ Aviso - 09 de Março

Hoje, dia **09 de março**, foi trabalhado o conteúdo da aula 3. Durante a aula, foi repassado o material do tutorial referente ao padrão **Strategy** (Tutorial 3.1).

**Tarefa para a próxima aula (16 de março):**
Os alunos devem realizar os tutoriais a seguir e enviá-los através do Google Classroom antes do nosso próximo encontro no dia 16:
*   [Aula 3.2 - State](<tutoriais/aula-3-2-tutorial-state--locadora-veiculos.md>)
*   [Aula 3.3 - Decorator](<tutoriais/aula-3-3-tutorial-decorator--locadora-veiculos.md>)
