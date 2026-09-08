use tauri::{
	menu::{Menu, MenuItem, PredefinedMenuItem},
	tray::{MouseButton, MouseButtonState, TrayIconBuilder, TrayIconEvent},
	AppHandle, Manager, Wry,
};

const TRAY_ID: &str = "aashi-tray";
const WINDOW_LABEL: &str = "main";

pub fn create_tray(app: &AppHandle<Wry>) -> tauri::Result<()> {
	let show = MenuItem::with_id(app, "show", "Show AASHI", true, None::<&str>)?;
	let hide = MenuItem::with_id(app, "hide", "Hide AASHI", true, None::<&str>)?;
	let separator = PredefinedMenuItem::separator(app)?;
	let quit = MenuItem::with_id(app, "quit", "Quit", true, None::<&str>)?;
	let menu = Menu::with_items(app, &[&show, &hide, &separator, &quit])?;

	TrayIconBuilder::with_id(TRAY_ID)
		.menu(&menu)
		.show_menu_on_left_click(false)
		.tooltip("AASHI AI Companion")
		.on_menu_event(|app, event| match event.id().as_ref() {
			"show" => {
				let _ = show_main_window(app);
			}
			"hide" => {
				let _ = hide_main_window(app);
			}
			"quit" => app.exit(0),
			_ => {}
		})
		.on_tray_icon_event(|tray, event| {
			if let TrayIconEvent::Click {
				button: MouseButton::Left,
				button_state: MouseButtonState::Up,
				..
			} = event
			{
				let _ = toggle_main_window(tray.app_handle());
			}
		})
		.build(app)?;

	Ok(())
}

pub fn show_main_window(app: &AppHandle<Wry>) -> tauri::Result<()> {
	let window = app.get_webview_window(WINDOW_LABEL).ok_or_else(|| tauri::Error::WindowNotFound)?;
	window.show()?;
	window.unminimize()?;
	window.set_focus()?;
	Ok(())
}

pub fn hide_main_window(app: &AppHandle<Wry>) -> tauri::Result<()> {
	let window = app.get_webview_window(WINDOW_LABEL).ok_or_else(|| tauri::Error::WindowNotFound)?;
	window.hide()
}

pub fn toggle_main_window(app: &AppHandle<Wry>) -> tauri::Result<()> {
	let window = app.get_webview_window(WINDOW_LABEL).ok_or_else(|| tauri::Error::WindowNotFound)?;
	if window.is_visible()? {
		window.hide()
	} else {
		show_main_window(app)
	}
}
