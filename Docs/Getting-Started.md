# Getting Started

## Requirements

- Unreal Engine 5.7, Windows 64-bit
- Editor Scripting Utilities (ships with the engine; WidgetBridge enables it)

## Install

1. Copy the `WidgetBridge` folder into your project's `Plugins` folder, or install it from Fab into the engine.
2. Open the project. If the editor asks to rebuild modules, accept.
3. Check that **Edit > Plugins > UI > WidgetBridge** is enabled.

The folder `<YourProject>/Saved/WidgetBridge/` is created when the editor starts.

## Two ways to use it

**From the editor console** (`~`): create a widget blueprint from a C++ class.

```cpp
// MyGame/Public/UI_HealthBar.h
UCLASS()
class UUI_HealthBar : public UUserWidget
{
    GENERATED_BODY()
protected:
    UPROPERTY(meta = (BindWidget)) class UProgressBar* Progress_Health;
    UPROPERTY(meta = (BindWidget)) class UTextBlock* Text_Value;
    UPROPERTY(meta = (BindWidgetOptional)) class UImage* Image_Icon;
};
```

```
WidgetBridge.Create UI_HealthBar /Game/UI WBP_HealthBar
```

`/Game/UI/WBP_HealthBar` is created with `Progress_Health`, `Text_Value` and `Image_Icon` already in place, ready to lay out in
the UMG designer. After you add a property in C++, `WidgetBridge.Sync UI_HealthBar /Game/UI/WBP_HealthBar` adds the missing
widget without touching your layout.

**From an external program**: write a JSON request in `Saved/WidgetBridge/widget_request.json` and read the answer in
`widget_response.json`.

```json
{ "id": "1", "command": "get_widget", "args": { "path": "/Game/UI/WBP_HealthBar" } }
```

## A small client in Python

```python
import json, os, time, uuid

BRIDGE = r"C:/MyProject/Saved/WidgetBridge"

def call(command, args=None, timeout=60):
    for name in ("widget_response.json", "widget_ack.json"):
        try:
            os.remove(os.path.join(BRIDGE, name))
        except OSError:
            pass
    with open(os.path.join(BRIDGE, "widget_request.json"), "w", encoding="utf-8") as f:
        json.dump({"id": str(uuid.uuid4()), "command": command, "args": args or {}}, f)
    end = time.time() + timeout
    while time.time() < end:
        time.sleep(0.2)
        try:
            with open(os.path.join(BRIDGE, "widget_response.json"), encoding="utf-8-sig") as f:
                return json.load(f)
        except (OSError, ValueError):
            pass
    raise TimeoutError(command)

call("create_widget", {"path": "/Game/UI/WBP_Menu"})
call("set_root", {"path": "/Game/UI/WBP_Menu", "widgetClass": "VerticalBox", "name": "Root"})
call("batch_create_widgets", {"path": "/Game/UI/WBP_Menu", "widgets": [
    {"class": "Button", "name": "Button_Play", "parent": "Root"},
    {"class": "Button", "name": "Button_Quit", "parent": "Root"}]})
call("compile", {"path": "/Game/UI/WBP_Menu"})
call("save", {"path": "/Game/UI/WBP_Menu"})
```

Next: [Protocol](Protocol.md), [Commands](Commands.md).
