"""WidgetBridge IPC — Python example.

Drives the WidgetBridge plugin from VSCode (or anywhere) using the file-based IPC.
Requires UE5 editor running with the WidgetBridge plugin loaded.
"""
import json
import time
from pathlib import Path

SAVED = Path(r"C:/MyProject/Saved/WidgetBridge")   # your project


def cmd(command, **args):
    req = SAVED / "widget_request.json"
    resp = SAVED / "widget_response.json"
    if resp.exists():
        resp.unlink()
    req.parent.mkdir(parents=True, exist_ok=True)
    req.write_text(json.dumps({"command": command, "args": args}))
    start = time.time()
    while time.time() - start < 15:
        if resp.exists():
            data = json.loads(resp.read_text())
            resp.unlink()
            return data
        time.sleep(0.5)
    raise TimeoutError(f"No response for command: {command}")


if __name__ == "__main__":
    # Build a HUD widget from scratch
    cmd("create_widget", path="/Game/UI/WBP_TestHUD", parentClass="UserWidget")
    cmd("set_root", path="/Game/UI/WBP_TestHUD", widgetClass="CanvasPanel", name="Root")
    cmd("add_child",
        path="/Game/UI/WBP_TestHUD",
        parentName="Root",
        widgetClass="TextBlock",
        name="TextBlock_Score",
        properties={"Text": "Score: 0", "ColorAndOpacity": "(R=1,G=1,B=0,A=1)"})
    cmd("compile", path="/Game/UI/WBP_TestHUD")
    cmd("save", path="/Game/UI/WBP_TestHUD")
    print(cmd("get_widget", path="/Game/UI/WBP_TestHUD"))
