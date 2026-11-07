"""Isolate external NLP/models; execute the actual API and PubMed parser."""
import json
import sys
import types
from pathlib import Path

import pytest
import requests

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))
EVIDENCE_DIR = ROOT / "qa" / "evidencias"

# These replacements are intentionally test-only. No production code is changed.
nlp_stub = types.ModuleType("app.services.nlp")
nlp_stub.nlp = object()  # Long-text truncation is outside this small suite.
nlp_stub.palavras_chave = lambda claim: ["vaccination"]


class ControlledTranslator:
    def traduzir(self, text):
        return (
            "What is the best treatment?"
            if text.startswith("Qual")
            else "Does vaccination reduce transmission?"
        )


nlp_stub.Tradutor = ControlledTranslator
nlp_stub.pergunta_para_claim = lambda question: (
    None if question.startswith("What") else "Vaccination reduces transmission."
)
sys.modules["app.services.nlp"] = nlp_stub

classifier_stub = types.ModuleType("app.services.classificador")


class ControlledClassifier:
    def classificar(self, claim, evidences):
        # Labels are prescribed fixture data, not predictions of the real MLP.
        labels = {"PMC1001": "NEUTRAL", "PMC1002": "SUPPORTED", "PMC1003": "REFUTED"}
        for evidence in evidences:
            evidence.label = labels[evidence.pmcid]
        return evidences


classifier_stub.Classificador = ControlledClassifier
sys.modules["app.services.classificador"] = classifier_stub

from fastapi.testclient import TestClient
from app.main import app
from app.services import pubmed


@pytest.fixture
def scenario(monkeypatch):
    state = {"mode": "success", "calls": []}

    def controlled_get(url, params=None):
        state["calls"].append({"endpoint": url.rsplit("/", 1)[-1], "params": params})
        if state["mode"] == "unavailable":
            raise requests.Timeout("Controlled timeout; no network request was made")
        response = requests.Response()
        response.status_code = 200
        if url == pubmed.ESEARCH:
            ids = [] if state["mode"] == "empty" else ["1001", "1002", "1003"]
            response._content = json.dumps({"esearchresult": {"idlist": ids}}).encode()
        elif url == pubmed.ESUMMARY:
            response._content = json.dumps({"result": {
                str(i): {"articleids": [{"idtype": "pmc", "value": f"PMC{i}"}],
                         "title": f"Synthetic fixture article {i}",
                         "authors": [{"name": "Test Author"}], "pubdate": "2026 Oct 13"}
                for i in [1001, 1002, 1003]
            }}).encode()
        elif url == pubmed.EFETCH:
            identifier = params["id"]
            response._content = (
                '<pmc-articleset><article><body><sec sec-type="conclusions">'
                '<title>Conclusions</title><p>Synthetic evidence about vaccination '
                f'for {identifier}; this is test data, not a medical conclusion.</p>'
                '</sec></body></article></pmc-articleset>'
            ).encode()
        else:
            raise AssertionError(f"Unexpected endpoint in controlled test: {url}")
        return response

    monkeypatch.setattr(pubmed, "_get", controlled_get)
    return state


@pytest.fixture
def client(scenario):
    with TestClient(app, raise_server_exceptions=False) as test_client:
        yield test_client


@pytest.fixture
def record_evidence(request, scenario):
    def record(case_id, payload, response):
        EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
        evidence = {
            "case_id": case_id,
            "test": request.node.name,
            "request": {"method": "POST", "path": "/api/v1/verificacoes", "json": payload},
            "response": {"status_code": response.status_code, "json": response.json()},
            "external_calls": scenario["calls"],
            "scope": "Actual API, validation, orchestration and XML parsing with simulated external NLP, classifier and HTTP responses",
        }
        (EVIDENCE_DIR / f"{case_id}.json").write_text(
            json.dumps(evidence, ensure_ascii=False, indent=2), encoding="utf-8"
        )
    return record
