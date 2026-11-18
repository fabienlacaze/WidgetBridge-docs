# Commands

30 JSON commands (see [Protocol](Protocol.md)) and 13 console commands.

Paths are content paths without the object suffix (`/Game/UI/WBP_HUD`). Save with `save` (or `set_widget_property`, which saves by default) before closing the editor.

- [Widget blueprint assets](#widget-blueprint-assets)
- [Reading a widget tree](#reading-a-widget-tree)
- [Editing a widget tree](#editing-a-widget-tree)
- [Properties and layout](#properties-and-layout)
- [Named slots (master and child blueprints)](#named-slots-master-and-child-blueprints)
- [Console commands](#console-commands)

## Widget blueprint assets

### `create_widget`

Creates an empty widget blueprint.

| Argument | Type | Required | Description |
|---|---|---|---|
| `path` | string | yes | Asset path, e.g. `/Game/UI/WBP_HUD`. |
| `parentClass` | string | no | Parent class: `UserWidget` (default), a short C++ class name, or `/Script/MyGame.UI_HealthBar`. |

```json
{"id": "1", "command": "create_widget", "args": {"path": "/Game/UI/WBP_HUD", "parentClass": "UserWidget"}}
```

Answer:

```json
{
  "id": "1",
  "status": "ok",
  "message": "...",
  "data": {
    "path": "/Game/UI/WBP_HUD"
  }
}
```

### `delete_widget`

Deletes the widget blueprint **asset**. To remove one widget inside a blueprint, use `remove_child`.

| Argument | Type | Required | Description |
|---|---|---|---|
| `path` | string | yes | Asset path. |

```json
{"id": "1", "command": "delete_widget", "args": {"path": "/Game/UI/WBP_Old"}}
```

### `duplicate_asset`

Duplicates an asset. Does nothing if the target exists, unless `overwrite` is true.

| Argument | Type | Required | Description |
|---|---|---|---|
| `source` | string | yes | Source asset path. |
| `target` | string | yes | New asset path. |
| `overwrite` | bool | no | Replace an existing target. |

```json
{"id": "1", "command": "duplicate_asset", "args": {"source": "/Game/UI/WBP_HUD", "target": "/Game/UI/WBP_HUD_Night"}}
```

Answer:

```json
{
  "id": "1",
  "status": "ok",
  "message": "...",
  "data": {
    "source": "/Game/UI/WBP_HUD",
    "target": "/Game/UI/WBP_HUD_Night",
    "saved": true,
    "already_exists": false
  }
}
```

### `create_child_widget_blueprint`

Creates a widget blueprint whose parent class is another widget blueprint (to fill its named slots).

| Argument | Type | Required | Description |
|---|---|---|---|
| `parent_path` | string | yes | Parent widget blueprint. |
| `package_path` | string | yes | Folder of the new asset. |
| `asset_name` | string | yes | Name of the new asset. |

```json
{"id": "1", "command": "create_child_widget_blueprint", "args": {"parent_path": "/Game/UI/WBP_PanelBase", "package_path": "/Game/UI", "asset_name": "WBP_PanelShop"}}
```

Answer:

```json
{
  "id": "1",
  "status": "ok",
  "message": "...",
  "data": {
    "path": "/Game/UI/WBP_PanelShop",
    "parentClass": "WBP_PanelBase_C",
    "saved": true
  }
}
```

### `reparent_blueprint`

Changes the parent class of a widget blueprint.

| Argument | Type | Required | Description |
|---|---|---|---|
| `path` | string | yes | Widget blueprint. |
| `parentClass` | string | yes | New parent: short C++ class name or `/Script/Module.Class`. |

```json
{"id": "1", "command": "reparent_blueprint", "args": {"path": "/Game/UI/WBP_HUD", "parentClass": "UI_HealthBar"}}
```

Answer:

```json
{
  "id": "1",
  "status": "ok",
  "message": "...",
  "data": {
    "path": "/Game/UI/WBP_HUD",
    "newParentClass": "UI_HealthBar",
    "newParentClassPath": "/Script/MyGame.UI_HealthBar"
  }
}
```

### `compile`

Compiles a widget blueprint.

| Argument | Type | Required | Description |
|---|---|---|---|
| `path` | string | yes | Widget blueprint. |

```json
{"id": "1", "command": "compile", "args": {"path": "/Game/UI/WBP_HUD"}}
```

### `save`

Saves a widget blueprint.

| Argument | Type | Required | Description |
|---|---|---|---|
| `path` | string | yes | Widget blueprint. |

```json
{"id": "1", "command": "save", "args": {"path": "/Game/UI/WBP_HUD"}}
```

### `list_widgets`

Lists widget blueprints.

| Argument | Type | Required | Description |
|---|---|---|---|
| `filter` | string | no | Keep only paths containing this text, e.g. `/Game/UI`. |

```json
{"id": "1", "command": "list_widgets", "args": {"filter": "/Game/UI"}}
```

Answer:

```json
{
  "id": "1",
  "status": "ok",
  "message": "...",
  "data": {
    "count": 2,
    "widgets": [
      "/Game/UI/WBP_HUD",
      "/Game/UI/WBP_Menu"
    ]
  }
}
```

### `list_widget_classes`

Lists the C++ `UUserWidget` classes that can be used as parents.

| Argument | Type | Required | Description |
|---|---|---|---|
| `filter` | string | no | Keep only class names containing this text. |

```json
{"id": "1", "command": "list_widget_classes", "args": {"filter": "UI_"}}
```

Answer:

```json
{
  "id": "1",
  "status": "ok",
  "message": "...",
  "data": {
    "count": 1,
    "classes": [
      "UI_HealthBar"
    ]
  }
}
```

## Reading a widget tree

### `get_widget`

Returns the whole widget tree of a blueprint, with the parent class and the named slots.

| Argument | Type | Required | Description |
|---|---|---|---|
| `path` | string | yes | Widget blueprint. |

```json
{"id": "1", "command": "get_widget", "args": {"path": "/Game/UI/WBP_HUD"}}
```

Answer:

```json
{
  "id": "1",
  "status": "ok",
  "message": "...",
  "data": {
    "path": "/Game/UI/WBP_HUD",
    "parentClass": "UserWidget",
    "root": {
      "name": "Root",
      "class": "CanvasPanel",
      "children": [
        "..."
      ]
    }
  }
}
```

### `get_widget_properties`

Properties of one widget and of its slot.

| Argument | Type | Required | Description |
|---|---|---|---|
| `path` | string | yes | Widget blueprint. |
| `name` | string | yes | Widget name (`widget` is accepted too). |

```json
{"id": "1", "command": "get_widget_properties", "args": {"path": "/Game/UI/WBP_HUD", "name": "Text_Title"}}
```

Answer:

```json
{
  "id": "1",
  "status": "ok",
  "message": "...",
  "data": {
    "name": "Text_Title",
    "class": "TextBlock",
    "properties": {
      "Text": "Hello"
    },
    "slotClass": "CanvasPanelSlot",
    "slotProperties": {
      "...": "..."
    }
  }
}
```

### `list_named_widgets`

Every named widget of a blueprint with its class and visibility, in one call.

| Argument | Type | Required | Description |
|---|---|---|---|
| `path` | string | yes | Widget blueprint. |
| `filter` | string | no | Keep only names containing this text. |

```json
{"id": "1", "command": "list_named_widgets", "args": {"path": "/Game/UI/WBP_HUD", "filter": "Button_"}}
```

Answer:

```json
{
  "id": "1",
  "status": "ok",
  "message": "...",
  "data": {
    "wbp": "/Game/UI/WBP_HUD",
    "count": 1,
    "widgets": [
      {
        "name": "Button_Play",
        "class": "Button",
        "visibility": "Visible"
      }
    ]
  }
}
```

### `get_widget_class_info`

Parent C++ class of a blueprint and every `BindWidget` / `BindWidgetOptional` property it declares, with whether a widget of that name exists. Use it when C++ expects `Image_Icon` and the blueprint has `Image_74`.

| Argument | Type | Required | Description |
|---|---|---|---|
| `path` | string | yes | Widget blueprint. |

```json
{"id": "1", "command": "get_widget_class_info", "args": {"path": "/Game/UI/WBP_HUD"}}
```

Answer:

```json
{
  "id": "1",
  "status": "ok",
  "message": "...",
  "data": {
    "parentClass": "UI_HealthBar",
    "count": 3,
    "missingCount": 1,
    "bindings": [
      {
        "name": "Image_Icon",
        "expectedClass": "Image",
        "isBound": false
      }
    ]
  }
}
```

## Editing a widget tree

### `set_root`

Creates the root widget of an empty blueprint.

| Argument | Type | Required | Description |
|---|---|---|---|
| `path` | string | yes | Widget blueprint. |
| `widgetClass` | string | yes | Panel class, e.g. `CanvasPanel`. |
| `name` | string | no | Root name. |

```json
{"id": "1", "command": "set_root", "args": {"path": "/Game/UI/WBP_HUD", "widgetClass": "CanvasPanel", "name": "Root"}}
```

### `add_child`

Adds a widget under a panel.

| Argument | Type | Required | Description |
|---|---|---|---|
| `path` | string | yes | Widget blueprint. |
| `parentName` | string | yes | Panel that receives the widget. |
| `widgetClass` | string | yes | Class, e.g. `TextBlock`, `Button`, `VerticalBox`. |
| `name` | string | yes | Name of the new widget. |
| `index` | number | no | Position among the children. |
| `properties` | object | no | Property values as text, e.g. `{"Text": "Hello"}`. |

```json
{"id": "1", "command": "add_child", "args": {"path": "/Game/UI/WBP_HUD", "parentName": "Root", "widgetClass": "TextBlock", "name": "Text_Title", "properties": {"Text": "Hello"}}}
```

### `batch_create_widgets`

Adds several widgets in one call.

| Argument | Type | Required | Description |
|---|---|---|---|
| `path` | string | yes | Widget blueprint. |
| `widgets` | array | yes | Items `{ "class", "name", "parent", "properties" }`. |

```json
{"id": "1", "command": "batch_create_widgets", "args": {"path": "/Game/UI/WBP_HUD", "widgets": [{"class": "Button", "name": "Button_Play", "parent": "Root"}, {"class": "Button", "name": "Button_Quit", "parent": "Root"}]}}
```

Answer:

```json
{
  "id": "1",
  "status": "ok",
  "message": "...",
  "data": {
    "requested": 2,
    "created": 2
  }
}
```

### `remove_child`

Removes one widget (and its children) from the tree.

| Argument | Type | Required | Description |
|---|---|---|---|
| `path` | string | yes | Widget blueprint. |
| `name` | string | yes | Widget name. |

```json
{"id": "1", "command": "remove_child", "args": {"path": "/Game/UI/WBP_HUD", "name": "Text_Old"}}
```

### `delete_widgets_by_name`

Removes every widget whose name matches a pattern (`*` allowed). `bSave: false` is a dry run.

| Argument | Type | Required | Description |
|---|---|---|---|
| `path` | string | yes | Widget blueprint. |
| `names` | array of strings | yes | Names or patterns, e.g. `["Debug_*"]`. |
| `bSave` | bool | no | Default true. False = report only. |

```json
{"id": "1", "command": "delete_widgets_by_name", "args": {"path": "/Game/UI/WBP_HUD", "names": ["Debug_*"], "bSave": false}}
```

Answer:

```json
{
  "id": "1",
  "status": "ok",
  "message": "...",
  "data": {
    "simulated": true,
    "deleted": [
      "Debug_Fps"
    ],
    "not_found": []
  }
}
```

### `rename_widget`

Renames a widget.

| Argument | Type | Required | Description |
|---|---|---|---|
| `path` | string | yes | Widget blueprint. |
| `name` | string | yes | Current name. |
| `newName` | string | yes | New name. |

```json
{"id": "1", "command": "rename_widget", "args": {"path": "/Game/UI/WBP_HUD", "name": "Image_74", "newName": "Image_Icon"}}
```

Answer:

```json
{
  "id": "1",
  "status": "ok",
  "message": "...",
  "data": {
    "oldName": "Image_74",
    "newName": "Image_Icon"
  }
}
```

### `reparent`

Moves a widget under another panel.

| Argument | Type | Required | Description |
|---|---|---|---|
| `path` | string | yes | Widget blueprint. |
| `name` | string | yes | Widget to move. |
| `newParent` | string | yes | Destination panel. |

```json
{"id": "1", "command": "reparent", "args": {"path": "/Game/UI/WBP_HUD", "name": "Text_Title", "newParent": "VerticalBox_Header"}}
```

### `wrap_widget`

Wraps a widget in a new panel without losing its children or its place. The wrapper takes the widget's name, so C++ bindings keep working; the original becomes `<name>_Inner`.

| Argument | Type | Required | Description |
|---|---|---|---|
| `path` | string | yes | Widget blueprint. |
| `widget` | string | yes | Widget to wrap. |
| `wrapper` | string | yes | Wrapper class, e.g. `ScrollBox`. |
| `name` | string | no | Wrapper name. Default `<widget>_Wrapper`. |

```json
{"id": "1", "command": "wrap_widget", "args": {"path": "/Game/UI/WBP_HUD", "widget": "VerticalBox_List", "wrapper": "ScrollBox"}}
```

Answer:

```json
{
  "id": "1",
  "status": "ok",
  "message": "...",
  "data": {
    "wrapper": "VerticalBox_List",
    "wrapper_class": "ScrollBox",
    "inner": "VerticalBox_List_Inner"
  }
}
```

## Properties and layout

### `set_property`

Sets a property of a widget from its text form.

| Argument | Type | Required | Description |
|---|---|---|---|
| `path` | string | yes | Widget blueprint. |
| `name` | string | yes | Widget name. |
| `property` | string | yes | Property, e.g. `Text`, `ColorAndOpacity`. |
| `value` | string | yes | Value as Unreal text. |

```json
{"id": "1", "command": "set_property", "args": {"path": "/Game/UI/WBP_HUD", "name": "Text_Title", "property": "ColorAndOpacity", "value": "(SpecifiedColor=(R=1,G=0.8,B=0.2,A=1))"}}
```

### `set_widget_property`

Same as `set_property`, then compiles and saves (unless `save` is false). Also reaches widgets placed in inherited named slots.

| Argument | Type | Required | Description |
|---|---|---|---|
| `path` | string | yes | Widget blueprint. |
| `name` | string | yes | Widget name. |
| `property` | string | yes | Property. |
| `value` | string | yes | Value as Unreal text. |
| `save` | bool | no | Default true. |

```json
{"id": "1", "command": "set_widget_property", "args": {"path": "/Game/UI/WBP_HUD", "name": "Border_Panel", "property": "Visibility", "value": "Collapsed"}}
```

Answer:

```json
{
  "id": "1",
  "status": "ok",
  "message": "...",
  "data": {
    "widget": "Border_Panel",
    "property": "Visibility",
    "value": "Collapsed",
    "saved": true
  }
}
```

### `set_slot_property`

Sets layout properties on a widget's slot (padding, alignment, size, anchors).

| Argument | Type | Required | Description |
|---|---|---|---|
| `path` | string | yes | Widget blueprint. |
| `name` | string | yes | Widget name (`widget` is accepted too). |
| `properties` | object | yes | Slot properties as text, e.g. `{"Padding": "(Left=8,Top=4,Right=8,Bottom=4)", "HorizontalAlignment": "HAlign_Fill"}`. |

```json
{"id": "1", "command": "set_slot_property", "args": {"path": "/Game/UI/WBP_HUD", "name": "Button_Play", "properties": {"HorizontalAlignment": "HAlign_Right", "Padding": "(Left=0,Top=6,Right=6,Bottom=0)"}}}
```

Answer:

```json
{
  "id": "1",
  "status": "ok",
  "message": "...",
  "data": {
    "widget": "Button_Play",
    "slot_class": "OverlaySlot",
    "properties_set": 2,
    "failed": []
  }
}
```

### `copy_widget_style`

Copies every style property of one widget to one or several widgets of the same class (layout and identity are not copied).

| Argument | Type | Required | Description |
|---|---|---|---|
| `path` | string | yes | Widget blueprint. |
| `from` | string | yes | Source widget. |
| `to` | string or array | yes | Target widget(s). |
| `exclude` | array of strings | no | Properties to keep on the targets, e.g. `["Text"]`. |

```json
{"id": "1", "command": "copy_widget_style", "args": {"path": "/Game/UI/WBP_HUD", "from": "Button_Play", "to": ["Button_Options", "Button_Quit"]}}
```

Answer:

```json
{
  "id": "1",
  "status": "ok",
  "message": "...",
  "data": {
    "targets_ok": 2,
    "targets_failed": 0,
    "properties_copied": 14
  }
}
```

### `copy_slot_properties`

Copies the slot layout of one widget to others.

| Argument | Type | Required | Description |
|---|---|---|---|
| `path` | string | yes | Widget blueprint. |
| `from` | string | yes | Source widget. |
| `to` | string or array | yes | Target widget(s). |

```json
{"id": "1", "command": "copy_slot_properties", "args": {"path": "/Game/UI/WBP_HUD", "from": "Button_Play", "to": "Button_Quit"}}
```

Answer:

```json
{
  "id": "1",
  "status": "ok",
  "message": "...",
  "data": {
    "targets_ok": 1,
    "slot_class": "VerticalBoxSlot"
  }
}
```

### `set_default_value`

Sets an editable property on the blueprint's class defaults (for example a default texture). Object references are given by path.

| Argument | Type | Required | Description |
|---|---|---|---|
| `path` | string | yes | Widget blueprint. |
| `property` | string | yes | Property name. |
| `value` | string | yes | Value as Unreal text, or an asset path. |

```json
{"id": "1", "command": "set_default_value", "args": {"path": "/Game/UI/WBP_HUD", "property": "DefaultIcon", "value": "/Game/UI/Icons/T_Heart.T_Heart"}}
```

### `set_enum_property`

Sets an enum property on the blueprint's class defaults, by entry name.

| Argument | Type | Required | Description |
|---|---|---|---|
| `path` | string | yes | Widget blueprint. |
| `property` | string | yes | Enum property. |
| `value` | string | yes | Entry name, e.g. `Large` or `EPanelSize::Large`. |

```json
{"id": "1", "command": "set_enum_property", "args": {"path": "/Game/UI/WBP_HUD", "property": "PanelSize", "value": "Large"}}
```

Answer:

```json
{
  "id": "1",
  "status": "ok",
  "message": "...",
  "data": {
    "property": "PanelSize",
    "value": "Large",
    "saved": true
  }
}
```

## Named slots (master and child blueprints)

### `replace_children_with_named_slot`

In a master blueprint, replaces a range of children of a panel by a `NamedSlot` that child blueprints can fill.

| Argument | Type | Required | Description |
|---|---|---|---|
| `path` | string | yes | Master widget blueprint. |
| `parent_widget` | string | yes | Panel whose children are replaced. |
| `first_child` | string | yes | First child of the range. |
| `last_child` | string | yes | Last child of the range. |
| `slot_name` | string | yes | Name of the new NamedSlot. |

```json
{"id": "1", "command": "replace_children_with_named_slot", "args": {"path": "/Game/UI/WBP_PanelBase", "parent_widget": "VerticalBox_Body", "first_child": "Text_Info", "last_child": "Button_Buy", "slot_name": "Slot_Body"}}
```

Answer:

```json
{
  "id": "1",
  "status": "ok",
  "message": "...",
  "data": {
    "slot_name": "Slot_Body",
    "removed_count": 3,
    "saved": true
  }
}
```

### `copy_widgets_into_named_slot`

Copies a range of widgets from one blueprint into a named slot of a child blueprint.

| Argument | Type | Required | Description |
|---|---|---|---|
| `source_path` | string | yes | Blueprint to copy from. |
| `source_parent` | string | yes | Panel holding the widgets. |
| `first_child` | string | yes | First widget of the range. |
| `last_child` | string | yes | Last widget of the range. |
| `target_path` | string | yes | Child blueprint. |
| `slot_name` | string | yes | Named slot to fill. |
| `container_name` | string | no | Name of the panel created in the slot. |

```json
{"id": "1", "command": "copy_widgets_into_named_slot", "args": {"source_path": "/Game/UI/WBP_ShopOld", "source_parent": "VerticalBox_Body", "first_child": "Text_Info", "last_child": "Button_Buy", "target_path": "/Game/UI/WBP_PanelShop", "slot_name": "Slot_Body"}}
```

Answer:

```json
{
  "id": "1",
  "status": "ok",
  "message": "...",
  "data": {
    "slot_name": "Slot_Body",
    "copied_count": 3,
    "saved": true
  }
}
```

## Console commands

Type them in the editor's console (`~`), or send them through EditorBridge `exec_console_command`.

| Command | What it does |
|---|---|
| `WidgetBridge.Create <ClassName> <PackagePath> <AssetName>` | Creates a widget blueprint from a C++ `UUserWidget` class, with one widget per `BindWidget` property. |
| `WidgetBridge.Sync <ClassName> <WBPPath>` | Adds the `BindWidget` widgets missing from an existing blueprint, without touching the rest. |
| `WidgetBridge.Recreate <ClassName> <PackagePath> <AssetName>` | Deletes the blueprint and creates it again from the class. |
| `WidgetBridge.Validate <WBPPath>` | Compares a blueprint with its C++ class: missing widgets, orphans, wrong types. |
| `WidgetBridge.Reverse <WBPPath> <OutputHeader>` | Writes a C++ header with one `BindWidget` property per named widget of a blueprint. |
| `WidgetBridge.ListClasses [ModuleName]` | Lists the C++ widget classes that declare `BindWidget` properties. |
| `WidgetBridge.Dump <WBPPath>` | Writes the widget tree to `Saved/WidgetDumps/`. |
| `WidgetBridge.DumpTree <WBPPath>` | Same, following the parent blueprints (inherited widgets included). |
| `WidgetBridge.Compare <WBPPathA> <WBPPathB>` | Widgets present in both blueprints. |
| `WidgetBridge.SetVis <WBPPath> <Visibility> <Pattern[,Pattern...]>` | Sets the stored visibility of the widgets whose name matches. |
| `WidgetBridge.Delete <WBPPath> <Pattern[,Pattern...]> [simulate]` | Deletes the widgets whose name matches. |
| `WidgetBridge.Move <SrcWBP> <DstWBP> <Pattern[,Pattern...]> [simulate]` | Copies widgets from one blueprint to another. |
| `WidgetBridge.FreezeVisibility <WBPPath>` | Lists the widgets whose visibility is changed by C++ and those never touched. |
