# Protocol

## Files

All files live in `<YourProject>/Saved/WidgetBridge/`.

| File | Written by | Purpose |
|---|---|---|
| `widget_request.json` | your program | the command to run |
| `widget_ack.json` | editor | the request was read |
| `widget_response.json` | editor | the result |

## Exchange

1. Delete `widget_response.json` and `widget_ack.json` if they exist.
2. Write `widget_request.json`.
3. The editor checks for a request every 1.5 seconds, writes `widget_ack.json`, runs the command and writes
   `widget_response.json`. The request file is then deleted.

Send one request at a time. The editor accepts UTF-8 with or without BOM.

## Request

```json
{ "id": "7", "command": "rename_widget", "args": { "path": "/Game/UI/WBP_HUD", "name": "Image_74", "newName": "Image_Icon" } }
```

| Field | Meaning |
|---|---|
| `id` | any string; copied into the answer |
| `command` | command name (see [Commands](Commands.md)) |
| `args` | object with the arguments |

## Answer

```json
{ "id": "7", "status": "ok", "message": "Renamed Image_74 -> Image_Icon", "data": { "oldName": "Image_74", "newName": "Image_Icon" } }
```

`status` is `ok` or `error`; on `error`, `message` says why. An unknown command answers `Unknown command: <name>`.

## Paths and values

- Asset paths are content paths without the object suffix: `/Game/UI/WBP_HUD`.
- Widgets are referred to by their name in the tree (the name shown in the Hierarchy panel).
- Property values use Unreal's text format, the same you get with Copy on a property in the Details panel:
  `true`, `12.5`, `(R=1,G=0,B=0,A=1)`, `(Left=8,Top=4,Right=8,Bottom=4)`, `HAlign_Fill`, `Collapsed`.
- Changes are not saved automatically, except by `set_widget_property` and the commands that say so. Call `save`.
