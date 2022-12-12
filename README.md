# exa-foo-fighting-service

A service for demonstrating `octue` inter-service communication using `octue/exa`.

## Usage

The service's SRUID (service revision unique identifier) is `octue/exa-foo-fighting-service:foamy-gopher`. Questions
can be sent to it in the following format:

```python
input_values = {
    "test_id": 1234,
    "max_duration": 30,
    "randomise_duration": True,
}
```
