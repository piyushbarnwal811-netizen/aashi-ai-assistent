#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

mod tray;

use tauri::{Manager, WindowEvent};
use tauri_plugin_autostart::ManagerExt;

#[tauri::command]
fn show_window(app: tauri::AppHandle) -> Result<(), String> {
	tray::show_main_window(&app).map_err(|error| error.to_string())
}

#[tauri::command]
fn hide_window(app: tauri::AppHandle) -> Result<(), String> {
	tray::hide_main_window(&app).map_err(|error| error.to_string())
}

#[tauri::command]
fn toggle_window(app: tauri::AppHandle) -> Result<(), String> {
	tray::toggle_main_window(&app).map_err(|error| error.to_string())
}

#[tauri::command]
fn set_autostart(app: tauri::AppHandle, enabled: bool) -> Result<bool, String> {
	let manager = app.autolaunch();
	if enabled {
		manager.enable().map_err(|error| error.to_string())?;
	} else {
		manager.disable().map_err(|error| error.to_string())?;
	}
	Ok(enabled)
}

#[tauri::command]
fn is_autostart_enabled(app: tauri::AppHandle) -> Result<bool, String> {
	app.autolaunch().is_enabled().map_err(|error| error.to_string())
}

fn main() {
	tauri::Builder::default()
		.plugin(tauri_plugin_autostart::Builder::new().build())
		.setup(|app| {
			tray::create_tray(app.handle())?;
			Ok(())
		})
		.on_window_event(|window, event| {
			if let WindowEvent::CloseRequested { api, .. } = event {
				api.prevent_close();
				let _ = window.hide();
			}
		})
		.invoke_handler(tauri::generate_handler![
			show_window,
			hide_window,
			toggle_window,
			set_autostart,
			is_autostart_enabled
		])
		.run(tauri::generate_context!())
		.expect("error while running AASHI desktop shell");
}
