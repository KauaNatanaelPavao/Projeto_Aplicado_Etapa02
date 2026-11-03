# Documentação Técnica do MVP - Parte 1: Metrologia e Calibração (Schulz S.A.)

## 1. Contextualização e Objetivo
Este documento apresenta a documentação técnica da primeira parte do MVP desenvolvido para a **Schulz S.A.**. O sistema tem como objetivo automatizar o registo de técnicos, instrumentos de medição e ensaios de calibração, aplicando regras metrológicas e persistência de dados em banco relacional.

---

## 2. Arquitetura e Padrões de Programação Orientada a Objetos (POO)
O código foi estruturado em **Python** utilizando os pilares da POO para garantir o encapsulamento, a modularidade e a clareza das regras de negócio:

* **Encapsulamento:** Os dados de cada entidade são agrupados em classes próprias, isolando as suas responsabilidades.
* **Separabilidade de Responsabilidades:** A lógica de persistência e conexão com o banco de dados é tratada de forma centralizada, separada das regras de domínio físico/metrológico.

---

## 3. Diagramação Textual das Classes de Domínio
A estrutura de classes implementada no sistema é composta por:

1. **`DatabaseManager`**
   * *Responsabilidade:* Gerencia a conexão com o ficheiro SQLite (`metrologia_schulz.db`) e a criação inicial das tabelas relacionais.
   * *Métodos principais:* `get_connection()`, `inicializar_banco()`.

2. **`Tecnico`**
   * *Atributos:* `matricula`, `nome`, `setor`.
   * *Responsabilidade:* Representa o operador/profissional responsável pelos ensaios.

3. **`Equipamento`**
   * *Atributos:* `codigo_tag`, `descricao`, `fabricante`.
   * *Responsabilidade:* Representa os instrumentos de medição da planta (ex: paquímetros, micrômetros).

4. **`Medicao`**
   * *Atributos:* `id_tecnico`, `id_equipamento`, `valor_nominal`, `valor_medido`, `tolerancia`, `data_ensaio`, `status`.
   * *Responsabilidade:* Encapsula o ensaio e executa a **validação metrológica automática**.

---

## 4. Regra de Negócio e Validação de Tolerância
O método `validar_tolerancia()` dentro da classe `Medicao` aplica a seguinte lógica matemática baseada no erro absoluto:

$$\text{Erro Absoluto} = |\text{Valor Medido} - \text{Valor Nominal}|$$

* Se $\text{Erro Absoluto} \le \text{Tolerância}$, o status é definido como **`APROVADO`**.
* Caso contrário, o status é definido como **`REPROVADO`**.

---

## 5. Tratamento de Erros e Persistência SQL
* **Tratamento de conexões:** Utilização de blocos `try...finally` combinados com `conn.close()` para garantir que as conexões com o SQLite sejam sempre encerradas de forma segura após cada operação de inserção ou consulta (`INSERT`, `SELECT`), prevenindo fugas de recursos do sistema.
* **Integridade Referencial:** O banco utiliza chaves estrangeiras (`FOREIGN KEY`) ligando a tabela de medições às tabelas de técnicos e equipamentos.

---

## 6. Validação do Fluxo Funcional
O fluxo do MVP foi testado e validado com sucesso no terminal através do script unificado (`sistema_completo.py`):
1. Inicialização do banco de dados SQLite.
2. Registo automático de técnicos e equipamentos de teste.
3. Execução de ensaios com emissão automática de status (`APROVADO` e `REPROVADO`).
4. Exibição do relatório consolidado no terminal utilizando consultas relacionais com operadores `JOIN`.