# exa-foo-fighting-service

A service for demonstrating `octue` inter-service communication using `octue/exa`.

## Usage

The service's SRUID (service revision unique identifier) is `octue/exa-foo-fighting-service:foamy-gopher`. Questions
can be sent to it in the following format (see the schema in [twine.json](./twine.json)):

```python
input_values = {
    "test_id": "a96387f2-7336-49bf-bf25-5a11ba6a6f41",
    "max_duration": 30,
    "randomise_duration": True,
}
```
