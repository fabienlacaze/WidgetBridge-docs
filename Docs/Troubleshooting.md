# Troubleshooting

| Symptom | What to check |
|---|---|
| No answer at all | The editor is not running, the plugin is disabled, or the request went to another project's `Saved` folder. Search the Output Log for `LogWidgetBridge`. |
| `delete_widget` removed my whole blueprint | `delete_widget` deletes the asset. To remove one widget inside a blueprint, use `remove_child` or `delete_widgets_by_name`. |
| A property does not change | Check the property name in `get_widget_properties`, and write the value in Unreal's text format (copy it from the Details panel). |
| Slot properties are ignored | They belong to the slot, not the widget: use `set_slot_property`. The slot type depends on the parent panel (`CanvasPanelSlot`, `VerticalBoxSlot`...). |
| C++ `BindWidget` errors when compiling | `get_widget_class_info` lists the expected widgets and which ones are missing; `WidgetBridge.Sync` adds them. |
| Changes lost after closing the editor | Call `save` (or `set_widget_property`, which saves by default). |
| `create_child_widget_blueprint` opens a dialog | Project Settings > UMG Editor > "Use Widget Template Selector" is on; turn it off for automation. |

## Questions

**Is it included in my packaged game?** No. WidgetBridge is an Editor module.

**Does it open a network port?** No. It only reads and writes files in `Saved/WidgetBridge/`.

**Can I use it with the other Bridge plugins?** Yes. Each Bridge has its own folder in `Saved/` and they do not depend on each
other; see [Using several Bridges](Several-Bridges.md).

**Support**: open an issue on the documentation repository (link on the Fab page).
