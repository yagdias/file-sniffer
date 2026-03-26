# Relatório de Inspeção de Arquivos (fsniff)

## Arquivo: data.csv
- **Tipo:** CSV (Columns: ID, Nome, Valor)
- **Tamanho:** 38 bytes
- **MD5:** `4a060b8f6d0970030ccef7c63ef95afe`

**Head (Conteúdo):**
```
ID, Nome, Valor
1, Teste, 100
```

---

## Arquivo: app.log
- **Tipo:** Log File
- **Tamanho:** 43 bytes
- **MD5:** `5dbcfd5f9340a430e1e35b605a6969eb`

**Head (Conteúdo):**
```
Este é um arquivo de log.
Erro na linha 2
```

---

## Arquivo: empty.txt
- **Tipo:** Plain Text
- **Tamanho:** 0 bytes
- **MD5:** `d41d8cd98f00b204e9800998ecf8427e`

**Head (Conteúdo):**
```
[Arquivo Vazio ou Erro de Leitura]
```

---

## Arquivo: archive.zip
- **Tipo:** ZIP Archive (2 items)
- **Tamanho:** 431 bytes
- **MD5:** `9b62b0bc3b94d61d9b0bf27c7f5c8e35`

**Head (Conteúdo):**
```
Zip contains 2 files:
samples/data.csv
samples/logs/app.log
```

---

### Arquivo: archive.zip > samples/data.csv
- **Tipo:** Inside Zip: CSV (Columns: ID, Nome, Valor)
- **Tamanho:** 38 bytes
- **MD5:** `4a060b8f6d0970030ccef7c63ef95afe`

**Head (Conteúdo):**
```
ID, Nome, Valor
1, Teste, 100
2, Outro, 200
```

---

### Arquivo: archive.zip > samples/logs/app.log
- **Tipo:** Inside Zip: Log File
- **Tamanho:** 43 bytes
- **MD5:** `5dbcfd5f9340a430e1e35b605a6969eb`

**Head (Conteúdo):**
```
Este é um arquivo de log.
Erro na linha 2
```

---
