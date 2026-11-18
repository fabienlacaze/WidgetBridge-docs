# Using several Bridges together

The Bridge plugins (EditorBridge, WidgetBridge, MaterialBridge, DataTableBridge and the others) are sold separately and work
alone. Installed together, they share three things and nothing else:

- **The same request format**: `{ "id", "command", "args" }` in, `{ "id", "status", "message", "data" }` out.
- **One folder each** under `Saved/`: `Saved/EditorBridge/`, `Saved/WidgetBridge/`, `Saved/MaterialBridge/`... A client talks
  to each plugin through its own folder, so requests to different Bridges never collide.
- **One menu**: each Bridge adds its panel under **Window > Dev Tools**. The submenu is created by whichever Bridge loads first.

No Bridge includes code from another one, so removing one never breaks the others.

## Example: build a menu and check it

```python
widget = Bridge("C:/MyProject/Saved/WidgetBridge", "widget")   # WidgetBridge
editor = Bridge("C:/MyProject/Saved/EditorBridge", "editor")   # EditorBridge

widget.call("create_widget", {"path": "/Game/UI/WBP_Menu"})
widget.call("set_root", {"path": "/Game/UI/WBP_Menu", "widgetClass": "VerticalBox", "name": "Root"})
widget.call("save", {"path": "/Game/UI/WBP_Menu"})
editor.call("start_pie")
editor.call("capture_pie", {"output_path": "C:/Temp/menu.png"})
editor.call("stop_pie")
```

`Bridge` is the small client of the Getting Started page with the folder and the file prefix as parameters
(`<prefix>_request.json`, `<prefix>_response.json`).
