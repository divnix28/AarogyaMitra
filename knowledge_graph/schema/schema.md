# Knowledge Graph Schema

## Node Labels
- `Disease`: {name: String, code: String}
- `Symptom`: {name: String}
- `Prevention`: {action: String}
- `Vaccine`: {name: String, target_age: String}
- `Source`: {source_id: String, organization: String}

## Relationships
- `(:Disease)-[:HAS_SYMPTOM]->(:Symptom)`
- `(:Disease)-[:PREVENTED_BY]->(:Prevention)`
- `(:Disease)-[:PREVENTED_BY]->(:Vaccine)`
- `(:Disease)-[:SUPPORTED_BY]->(:Source)`