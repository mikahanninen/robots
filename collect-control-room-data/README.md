# Example of collecting data from Robocorp Control Room

Example is using Robocorp Process API and especially library `RPA.Robocorp.Process`
to collect the data from certain workspace and certain process.

## expected Secret variables in the `vault.yaml`

Secrets can be also set in the `vault.json` file or directly read from Control Room with VSCode Robocorp Code extension.

```yaml
control_room_process_<NAME_OF_THE_PROCESS>:
  workspace_id: <WORKSPACE_ID>
  process_id: <PROCESS_ID>
  api_key: <PROCESS_API_KEY>
```

The `<NAME_OF_THE_PROCESS>` should match `BOT['NAME']` in the `task.py`
