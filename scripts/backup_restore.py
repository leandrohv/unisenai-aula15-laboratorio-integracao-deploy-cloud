#!/usr/bin/env python3
"""Backup e restauração de teste do PostgreSQL da Aula 15; nunca apaga o banco principal.
Requer Python 3 no host e Docker Compose (além da stack em funcionamento).
Uso: python scripts/backup_restore.py backup|restore|verify
"""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "evidencias" / "backup_aula15.dump"
RESTORE_DB = "restauracao_aula15"
BASE = ["docker", "compose", "-f", "compose.yaml", "-f", "compose.lab.yaml", "exec", "-T", "db"]


def run(args, *, input_file=None, output_file=None):
    with (input_file.open("rb") if input_file else _null()) as stdin, (output_file.open("wb") if output_file else _null()) as stdout:
        proc = subprocess.run(args, cwd=ROOT, stdin=stdin if input_file else None,
                              stdout=stdout if output_file else None, check=False)
    if proc.returncode != 0:
        raise RuntimeError(f"Falha no comando: status={proc.returncode}")


class _null:
    def __enter__(self): return None
    def __exit__(self, *args): return False


def main():
    if len(sys.argv) != 2 or sys.argv[1] not in {"backup", "restore", "verify"}:
        print("Uso: python scripts/backup_restore.py backup|restore|verify")
        return 2
    action = sys.argv[1]
    try:
        if action == "backup":
            DEST.parent.mkdir(exist_ok=True)
            run(BASE + ["sh", "-c", 'pg_dump -U "$POSTGRES_USER" -d "$POSTGRES_DB" --format=custom --no-owner --no-privileges'], output_file=DEST)
            if DEST.stat().st_size == 0: raise RuntimeError("Backup vazio")
            print(f"Backup criado em {DEST.name} ({DEST.stat().st_size} bytes)")
        if action == "restore":
            if not DEST.exists(): raise RuntimeError("Execute backup antes de restore")
            # Recria apenas o banco isolado de restauração. Nunca altera unisenai/pgdata.
            run(BASE + ["sh", "-c", f'psql -U "$POSTGRES_USER" -d postgres -v ON_ERROR_STOP=1 -c "DROP DATABASE IF EXISTS {RESTORE_DB} WITH (FORCE)"'])
            run(BASE + ["sh", "-c", f'createdb -U "$POSTGRES_USER" {RESTORE_DB}'])
            run(BASE + ["sh", "-c", f'pg_restore -U "$POSTGRES_USER" -d {RESTORE_DB} --no-owner --no-privileges'], input_file=DEST)
            print(f"Restauração concluída no banco isolado: {RESTORE_DB}")
        if action == "verify":
            run(BASE + ["sh", "-c", f'psql -U "$POSTGRES_USER" -d {RESTORE_DB} -tAc "SELECT COUNT(*) FROM tarefas"'])
            print("Compare o total com o banco principal e com o registro de evidências")
        return 0
    except (RuntimeError, OSError, subprocess.SubprocessError) as exc:
        print(f"ERRO: {exc}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
