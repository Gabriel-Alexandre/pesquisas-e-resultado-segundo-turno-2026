"""Copia, com hash, os derivados leves de projetos anteriores do canal que este projeto reaproveita (só leitura lá).

Cada cópia guarda no manifesto o projeto, o commit de lá e o caminho de origem. Nada é recalculado aqui sem ser conferido
(ver ferramentas/validacao-independente.py).
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from analise.comum import COPIAS, RAIZ, registrar_lote  # noqa: E402

REPOS = RAIZ.parent
COPIAR = {
    "investigacao-segundo-turno-2026": [
        "dados/derivados/historico_turnos.csv", "dados/derivados/polymarket_favoritos.csv", "dados/derivados/polymarket_eventos.csv",
        "dados/manuais/presidente_1989.csv", "dados/copias/pindograma-late-polls-2012-2018.csv",
        "dados/copias/pindograma-late-polls-2022.csv", "resultados/p_segundos_turnos.csv", "resultados/p3_disputas.csv",
        "resultados/p_historico.json", "resultados/d5_curva_noite.csv"],
    "previsao-segundo-turno-2026": [
        "resultados/abstencao_historica.csv", "resultados/transferencia_historica.csv", "resultados/h_regras_por_uf.csv",
        "resultados/institutos_erros.csv", "resultados/institutos_ranking.csv", "resultados/RESUMO.json",
        "resultados/teste_do_passado.csv", "resultados/p_pesquisas_usadas.csv",
        "dados/derivados/mun_votos.parquet", "dados/derivados/mun_detalhe.parquet"],
    "presidente-primeiro-turno-2026": ["resultados/b6_erro_por_instituto_e_rodada.csv"],
    "apuracao-eleicoes-2026": ["resultados/p7_margem_2022_por_pct_de_secoes.csv"],
}


def commit(repo: Path) -> str:
    try:
        return subprocess.run(["git", "-C", str(repo), "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip()
    except Exception:
        return "?"


def main() -> None:
    itens = []
    for proj, arquivos in COPIAR.items():
        c = commit(REPOS / proj)
        for rel in arquivos:
            src = REPOS / proj / rel
            dst = COPIAS / proj / Path(rel).name
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            itens.append((dst, f"{proj}@{c}:{rel}", "cópia de projeto anterior do canal"))
            print(proj, rel)
    registrar_lote(itens)


if __name__ == "__main__":
    main()
