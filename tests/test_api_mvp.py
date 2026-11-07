"""Six API contract/integration tests for the MVP's main response paths."""

QUESTION = "A vacinação reduz a transmissão?"


def test_ct01_query_returns_grouped_evidence_and_sources(client, scenario, record_evidence):
    payload = {"pergunta": f"  {QUESTION}  "}
    response = client.post("/api/v1/verificacoes", json=payload)
    record_evidence("CT01", payload, response)
    assert response.status_code == 200
    body = response.json()
    assert body["pergunta"] == QUESTION
    assert body["total"] == 3
    assert body["claim"] == "Vaccination reduces transmission."
    expected_ids = {"neutras": "1001", "suportam": "1002", "refutam": "1003"}
    for group, identifier in expected_ids.items():
        evidences = body["evidencias"][group]
        assert len(evidences) == 1
        evidence = evidences[0]
        assert evidence["pmid"] == identifier
        assert evidence["pmcid"] == f"PMC{identifier}"
        assert evidence["link"] == f"https://pmc.ncbi.nlm.nih.gov/articles/PMC{identifier}/"
        assert evidence["fonte"] == "PubMed"
        assert evidence["autores"] == "Test Author"
        assert evidence["ano"] == "2026"
        assert "Synthetic evidence" in evidence["trecho"]
    assert [call["endpoint"] for call in scenario["calls"]] == [
        "esearch.fcgi", "esummary.fcgi", "efetch.fcgi", "efetch.fcgi", "efetch.fcgi"
    ]


def test_ct02_empty_question_is_rejected_before_search(client, scenario, record_evidence):
    payload = {"pergunta": "   "}
    response = client.post("/api/v1/verificacoes", json=payload)
    record_evidence("CT02", payload, response)
    assert response.status_code == 422
    assert response.json()["erro"]["tipo"] == "vazia"
    assert response.json()["erro"]["mensagem"] == "Digite uma pergunta para começar."
    assert scenario["calls"] == []


def test_ct03_numeric_input_is_rejected_before_search(client, scenario, record_evidence):
    payload = {"pergunta": "123456"}
    response = client.post("/api/v1/verificacoes", json=payload)
    record_evidence("CT03", payload, response)
    assert response.status_code == 422
    assert response.json()["erro"]["tipo"] == "sem_letras"
    assert "números ou símbolos" in response.json()["erro"]["mensagem"]
    assert scenario["calls"] == []


def test_ct04_open_question_returns_guidance(client, scenario, record_evidence):
    payload = {"pergunta": "Qual o melhor tratamento?"}
    response = client.post("/api/v1/verificacoes", json=payload)
    record_evidence("CT04", payload, response)
    assert response.status_code == 422
    assert response.json()["erro"]["tipo"] == "pergunta_invalida"
    assert "sim ou não" in response.json()["erro"]["mensagem"]
    assert scenario["calls"] == []


def test_ct05_no_evidence_returns_reformulation_guidance(client, scenario, record_evidence):
    scenario["mode"] = "empty"
    payload = {"pergunta": QUESTION}
    response = client.post("/api/v1/verificacoes", json=payload)
    record_evidence("CT05", payload, response)
    assert response.status_code == 404
    assert response.json()["erro"]["tipo"] == "sem_evidencias"
    assert "reformulá-la" in response.json()["erro"]["mensagem"]
    assert [call["endpoint"] for call in scenario["calls"]] == ["esearch.fcgi"]


def test_ct06_pubmed_timeout_returns_controlled_error(client, scenario, record_evidence):
    scenario["mode"] = "unavailable"
    payload = {"pergunta": QUESTION}
    response = client.post("/api/v1/verificacoes", json=payload)
    record_evidence("CT06", payload, response)
    assert response.status_code == 502
    assert response.json()["erro"]["tipo"] == "pubmed_indisponivel"
    assert "Tente novamente" in response.json()["erro"]["mensagem"]
    assert [call["endpoint"] for call in scenario["calls"]] == ["esearch.fcgi"]
