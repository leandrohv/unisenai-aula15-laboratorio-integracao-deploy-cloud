# Aula 15 — roteiro de evidências e desafio

**Equipe:** ______________________  **Turma:** ______________  **Data:** __________

## Missão: evoluir o ambiente da Aula 13
1. Validar `docker compose config --quiet` com arquivo principal + override.
2. Demonstrar frontend, backend e banco em execução; criar uma tarefa na interface.
3. Ler `/api/info`, alterar `APP_VERSION=1.1.0` e recriar apenas o backend (sem apagar banco).
4. Explicar diferença de `/api/live` vs `/api/ready` interrompendo e restaurando o banco.
5. Mostrar `stats --no-stream`, uma evidência dos logs e quais recursos são limitados no override.
6. Fazer backup + restauração de teste em `restauracao_aula15` (se houver Python no host) e verificar a contagem.
7. Propor arquitetura cloud para produção, indicando ao menos: entrada HTTPS, computação, rede privada, banco, segredos e monitoramento.

## Quadro de evidências
| Critério | Evidência observada | Resultado |
|--|--|--|
| Deploy | `compose ps`: 3 serviços | |
| Configuração | `api/info` antes/depois | |
| Disponibilidade | `/api/live` vs `/api/ready` após `stop db` | |
| Recursos | `stats` + trecho de `compose.lab.yaml` | |
| Dados | tarefa após `down/up` | |
| Backup | backup criado + restore/verify (ou justificativa) | |
| Arquitetura | desenho com trust boundaries/serviços | |

## Perguntas que precisam de explicação
- Por que `depends_on` não garante saúde contínua?
- Por que `.env` não deve ser tratado como cofre de segredos?
- Por que um volume local não equivale a alta disponibilidade nem a backup off-host?
- Como migraríamos o PostgreSQL para um serviço gerenciado?
- Quais controles impediriam o acesso direto à API e ao banco?

## Critérios — 10 pontos
- Integração e implantação demonstradas: 2,0
- Versionamento/configuração e reversão: 2,0
- Segurança, recursos e healthchecks: 2,0
- Persistência e restauração controlada: 2,0
- Arquitetura cloud e justificativa de trade-offs: 2,0

**Importante:** ambiente apenas de estudo. Não usar `docker compose down -v` sem autorização do docente.
