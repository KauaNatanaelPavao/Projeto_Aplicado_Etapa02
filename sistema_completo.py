import sqlite3
from datetime import datetime

class DatabaseManager:
    """Responsável por gerenciar a conexão com o banco de dados e a criação das tabelas."""
    def __init__(self, db_name="metrologia_schulz.db"):
        self.db_name = db_name

    def get_connection(self):
        return sqlite3.connect(self.db_name)

    def inicializar_banco(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Tabela de Técnicos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tecnicos (
                matricula TEXT PRIMARY KEY,
                nome TEXT NOT NULL,
                setor TEXT NOT NULL
            )
        """)
        
        # Tabela de Equipamentos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS equipamentos (
                codigo_tag TEXT PRIMARY KEY,
                descricao TEXT NOT NULL,
                fabricante TEXT NOT NULL
            )
        """)
        
        # Tabela de Medições / Ensaios
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS medicoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                matricula_tecnico TEXT,
                codigo_equipamento TEXT,
                valor_nominal REAL,
                valor_medido REAL,
                tolerancia REAL,
                data_ensaio TEXT,
                status TEXT,
                FOREIGN KEY (matricula_tecnico) REFERENCES tecnicos(matricula),
                FOREIGN KEY (codigo_equipamento) REFERENCES equipamentos(codigo_tag)
            )
        """)
        
        conn.commit()
        conn.close()

class Tecnico:
    def __init__(self, matricula, nome, setor):
        self.matricula = matricula
        self.nome = nome
        self.setor = setor

    def salvar(self, db_manager):
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR IGNORE INTO tecnicos (matricula, nome, setor) 
            VALUES (?, ?, ?)
        """, (self.matricula, self.nome, self.setor))
        conn.commit()
        conn.close()

class Equipamento:
    def __init__(self, codigo_tag, descricao, fabricante):
        self.codigo_tag = codigo_tag
        self.descricao = descricao
        self.fabricante = fabricante

    def salvar(self, db_manager):
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR IGNORE INTO equipamentos (codigo_tag, descricao, fabricante) 
            VALUES (?, ?, ?)
        """, (self.codigo_tag, self.descricao, self.fabricante))
        conn.commit()
        conn.close()

class Medicao:
    def __init__(self, tecnico, equipamento, valor_nominal, valor_medido, tolerancia):
        self.tecnico = tecnico
        self.equipamento = equipamento
        self.valor_nominal = valor_nominal
        self.valor_medido = valor_medido
        self.tolerancia = tolerancia
        self.data_ensaio = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.status = self.validar_tolerancia()

    def validar_tolerancia(self):
        erro_absoluto = abs(self.valor_medido - self.valor_nominal)
        if erro_absoluto <= self.tolerancia:
            return "APROVADO"
        else:
            return "REPROVADO"

    def salvar(self, db_manager):
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO medicoes (matricula_tecnico, codigo_equipamento, valor_nominal, valor_medido, tolerancia, data_ensaio, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            self.tecnico.matricula, 
            self.equipamento.codigo_tag, 
            self.valor_nominal, 
            self.valor_medido, 
            self.tolerancia, 
            self.data_ensaio, 
            self.status
        ))
        conn.commit()
        conn.close()

# --- Fluxo Principal de Execução ---
if __name__ == "__main__":
    db = DatabaseManager()
    db.inicializar_banco()

    # 1. Instanciar e salvar Técnico e Equipamento
    tec1 = Tecnico("T001", "Carlos Silva", "Metrologia Industrial")
    tec1.salvar(db)

    eq1 = Equipamento("PAQ-01", "Paquímetro Universal 150mm", "Mitutoyo")
    eq1.salvar(db)

    # 2. Realizar medições de teste (uma aprovada e uma reprovada)
    med1 = Medicao(tec1, eq1, valor_nominal=50.0, valor_medido=50.02, tolerancia=0.05)
    med1.salvar(db)

    med2 = Medicao(tec1, eq1, valor_nominal=25.0, valor_medido=25.12, tolerancia=0.05)
    med2.salvar(db)

    # 3. Consultar relatório consolidado com JOIN
    print("\n--- RELATÓRIO DE ENSAIOS METROLÓGICOS (SCHULZ S.A.) ---")
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT m.id, t.nome, e.codigo_tag, m.valor_nominal, m.valor_medido, m.status 
        FROM medicoes m
        JOIN tecnicos t ON m.matricula_tecnico = t.matricula
        JOIN equipamentos e ON m.codigo_equipamento = e.codigo_tag
    """)
    for linha in cursor.fetchall():
        print(f"ID: {linha[0]} | Técnico: {linha[1]} | Equipamento: {linha[2]} | Nom: {linha[3]} | Medido: {linha[4]} | Status: {linha[5]}")
    conn.close()