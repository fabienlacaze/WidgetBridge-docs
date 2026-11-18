# Changelog

## 1.2.0 (2026-11-18)

- 30 JSON commands: widget and slot properties, style and slot copy, wrapping, named slots (master and child blueprints),
  class defaults and enum properties, batch creation, deletion by name pattern, asset duplication.
- Console commands Compare, SetVis, Delete, Move, FreezeVisibility, DumpTree.
- All messages in English. Documentation split into pages (Docs/README.md).
- MCP server (`Mcp/bridge_mcp.py`): use WidgetBridge from Claude Code, Claude Desktop, Cursor or OpenAI Codex.

## 1.1.0 — 2026-04-08

### Added
- **File-based IPC subsystem** — `FWidgetBridgeIPC` polls `Saved/WidgetBridge/widget_request.json` every 1.5s via `FTSTicker`, with ack file, reentrancy guard, and `widget_response.json` output. Lets external tools (Python/Node/VSCode) drive WidgetBridge with no console interaction.
- **11 granular IPC commands** for node-by-node widget editing:
  `get_widget`, `create_widget`, `delete_widget`, `add_child`, `remove_child`, `set_property`, `reparent`, `set_root`, `compile`, `save`, `list_widgets`.
- **Transaction support** — every mutating operation is wrapped in `FScopedTransaction` for full Editor Undo/Redo.
- **Property reflection** — `set_property` and `add_child.properties` use `FindFProperty` + `ImportText_Direct` to set any UPROPERTY by name.
- `Docs/IPC_PROTOCOL.md` — full JSON schema and examples for every command.
- `Docs/PYTHON_EXAMPLE.py` — minimal Python client showing the create→set_root→add_child→compile→save flow.

### Build
- Added `Json`, `JsonUtilities` to public deps.

## 1.0.0 — 2026-04-08

Initial marketplace release.

### Features
- `WidgetBridge.Create` — scaffold a new Widget Blueprint from a C++ `UUserWidget` subclass, auto-populating every `BindWidget` / `BindWidgetOptional` member as a named child widget.
- `WidgetBridge.CreateAll` — batch-create a preset list of project widgets.
- `WidgetBridge.Sync` — add new `BindWidget`s to an existing WBP without touching user-edited layout.
- `WidgetBridge.Recreate` — force-delete an existing WBP and regenerate from scratch.
- `WidgetBridge.Validate` — compare a WBP against its parent C++ class and report missing widgets, orphans and type mismatches. Output also saved to `Saved/WidgetDumps/<name>_validation.txt`.
- `WidgetBridge.Reverse` — reverse-engineer a C++ `UUserWidget` header from an existing WBP.
- `WidgetBridge.ListClasses` — list every `UUserWidget`-derived C++ class with `BindWidget` members (optionally filtered by module).
- `WidgetBridge.Dump` — dump the full widget tree of a WBP to log and to `Saved/WidgetDumps/`.
- Minimal Slate window (`Window > Widget Kit`) exposing Create / Sync / Recreate / Dump.

### Supported
- Unreal Engine 5.3, 5.4, 5.5, 5.6, 5.7
- Editor-only module, loads at `PostEngineInit`.
