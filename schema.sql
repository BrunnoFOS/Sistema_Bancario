CREATE TABLE contas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    agencia VARCHAR(20),
    numero_conta INT,
    cliente_id INT,
    saldo DECIMAL(15, 2),
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id)
);