import json
from pathlib import Path

import numpy as np

from analise import modelo as M

RAIZ = Path(__file__).resolve().parent.parent
R = json.loads((RAIZ / "resultados" / "RESUMO.json").read_text(encoding="utf-8"))


def test_conta_fecha():
    v = R["resultado"]["variacao"]
    assert v["ganho_dos_dois"] == -(v["outros_candidatos"] + v["abstencao"] + v["branco_nulo"])


def test_transicao_recupera_matriz_conhecida():
    rng = np.random.default_rng(1)
    x = rng.dirichlet(np.ones(8), 300)
    t = rng.dirichlet(np.ones(4), 8)
    est = M._ajustar(x, x @ t, np.ones(300))
    assert np.allclose(est.sum(axis=1), 1, atol=1e-6)
    assert np.abs(est - t).max() < 0.05


def test_pesquisas_sem_numero_da_urna():
    assert R["pesquisas"]["nenhuma_chegou_na_urna"] is True
    assert R["pesquisas"]["todas"]["n"] == 53


def test_probabilidades_entre_zero_e_um():
    for v in R["probabilidade"]["leituras"].values():
        assert 0 < v < 1
