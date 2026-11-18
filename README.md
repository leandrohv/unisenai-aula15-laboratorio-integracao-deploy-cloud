# UniSENAI • Aula 15 — Integração, implantação e configuração

## Origem e objetivo
Evolução autocontida do **laboratório da Aula 13 (frontend Nginx + API Flask + PostgreSQL)**. O projeto foi incluído integralmente neste pacote: não é necessário baixar o ZIP da Aula 13. A aula 15 aborda versão de aplicação, configuração por ambiente, limites de recursos, sinais de saúde, diagnóstico e backup/restauração de teste.

**Atenção:** laboratório didático LOCAL, não pronto para produção. Não usar dados reais nem credenciais verdadeiras. Sem autenticação, HTTPS, cofre de segredos, CI/CD real, balanceamento, backups automáticos ou alta disponibilidade.

## Requisitos
- Docker Engine/Docker Desktop com Linux containers + Docker Compose v2.
- Terminal Bash / PowerShell; porta 8081 disponível (ou alterar `APP_PORT`).
- Internet para obtenção das imagens no primeiro build.
- Python 3 no HOST é **opcional para os testes básicos** e necessário ao script portátil de backup/restauração de teste.

## Estrutura
```
aula15-conteineres/
├─ compose.yaml                  # definição principal
├─ compose.lab.yaml              # limites e logs da aula (override)
├─ .env.example                  # configurações não sensíveis + senha de demonstração
├─ frontend/                     # Nginx + HTML/CSS/JS
├─ backend/                      # API Flask + metadados de implantação
├─ db/init.sql                   # criação da tabela em banco vazio
├─ scripts/validar.sh|ps1        # verificações
├─ scripts/backup_restore.py     # backup/restore isolado, portátil
└─ ATIVIDADE_ALUNO.md            # roteiro e evidências
```

## 1) Preparar e subir a stack
**Linux/macOS:** `cp .env.example .env`  
**PowerShell:** `Copy-Item .env.example .env`

Na pasta raiz:
```
docker compose -f compose.yaml -f compose.lab.yaml config --quiet
docker compose -f compose.yaml -f compose.lab.yaml up -d --build
docker compose -f compose.yaml -f compose.lab.yaml ps
```
Acesse `http://127.0.0.1:8081` e crie uma tarefa. Use a porta em `.env` se alterada.

> O override precisa ser informado com `-f` em todas as operações que devam preservá-lo. `docker compose config --quiet` valida a definição, mas não o comportamento da aplicação.

## 2) Integração + configuração de versão
```
curl -i http://127.0.0.1:8081/api/live
curl -i http://127.0.0.1:8081/api/ready
curl -i http://127.0.0.1:8081/api/info
curl -i http://127.0.0.1:8081/api/tasks
```
`/api/live` testa apenas o processo; `/api/ready` testa a conexão SQL; `/api/info` expõe apenas metadados didáticos, sem segredos. Edite `.env` de `APP_VERSION=1.0.0` para `APP_VERSION=1.1.0` e recrie o backend:
```
docker compose -f compose.yaml -f compose.lab.yaml up -d --no-deps --force-recreate backend
curl -s http://127.0.0.1:8081/api/info
```
Para simular rollback, volte APP_VERSION=1.0.0 e repita o `up`. **Isso demonstra a reversão de configuração; não equivale a um rollback de imagem ou banco em produção.**

## 3) Limites, logs e persistência
Abra `compose.lab.yaml`: observe `mem_limit`, `cpus`, `pids_limit`, `security_opt`, `cap_drop` e configuração de logs. No laboratório, `backend` não roda como root (Dockerfile), não publica porta 8000, e PostgreSQL não publica 5432. Esses controles são apenas uma parte de um hardening real.
```
docker compose -f compose.yaml -f compose.lab.yaml logs --tail=50 backend
docker compose -f compose.yaml -f compose.lab.yaml stats --no-stream
docker compose -f compose.yaml -f compose.lab.yaml down
docker compose -f compose.yaml -f compose.lab.yaml up -d
```
A tarefa deve continuar presente porque `pgdata` é um volume nomeado. **Não executar `down -v`** durante a aula.

## 4) Backup e restauração controlada (requer Python 3 no HOST)
Para que o resultado seja confiável em Linux, macOS, Windows PowerShell e sem conversões de encoding no shell:
```
python scripts/backup_restore.py backup
python scripts/backup_restore.py restore
python scripts/backup_restore.py verify
```
O comando `restore` recria apenas a base **restauracao_aula15** no mesmo servidor PostgreSQL; não apaga a base principal. O arquivo `evidencias/backup_aula15.dump` é local; para um sistema real, o backup deveria ser armazenado fora do host e protegido. Este procedimento **não prova recuperação em caso de perda do host ou do volume Docker**.

## 5) Falha e diferenciação liveness/readiness
```
docker compose -f compose.yaml -f compose.lab.yaml stop db
curl -i http://127.0.0.1:8081/api/live       # esperado 200
curl -i http://127.0.0.1:8081/api/ready      # esperado 503 se db estiver parado
```
```
docker compose -f compose.yaml -f compose.lab.yaml start db
docker compose -f compose.yaml -f compose.lab.yaml ps
```
Aguarde a recuperação do banco e volte a consultar `/api/ready`. Exceções/tempo de resposta dependem do ambiente; fotografe a evidência observada em vez de inventar métricas.

## 6) Verificação final e saída
**Linux/macOS** `bash scripts/validar.sh` (se APP_PORT mudou, defina APP_PORT no shell).  
**Windows** `powershell -File scripts/validar.ps1`.

Interrompa com `docker compose -f compose.yaml -f compose.lab.yaml down` para manter o volume. Não use este projeto em redes públicas.

## Referências oficiais
- Compose files/merge: https://docs.docker.com/compose/how-tos/multiple-compose-files/merge/
- Environment variables: https://docs.docker.com/compose/how-tos/environment-variables/best-practices/
- Startup order: https://docs.docker.com/compose/how-tos/startup-order/
- ECS architecture: https://docs.aws.amazon.com/AmazonECS/latest/developerguide/application_architecture.html
