from __future__ import annotations

from backend.tools import app_launcher, communication_tools, file_system, office_tools, os_control_tools, scraper_tools, terminal_runner, vision_tools


TOOL_REGISTRY = {
	"office.create_excel": office_tools.create_excel_sheet,
	"office.create_word": office_tools.create_word_document,
	"vision.capture_screen": vision_tools.capture_screen,
	"web.search": scraper_tools.search_web,
	"media.youtube": os_control_tools.play_youtube_video,
	"filesystem.write": file_system.write_file,
	"filesystem.read": file_system.read_file,
	"filesystem.create_folder": file_system.create_folder,
	"filesystem.move": file_system.move_path,
	"filesystem.delete": file_system.delete_path,
	"app.launch": app_launcher.launch_application,
	"terminal.run": terminal_runner.run_command,
	"os.volume": os_control_tools.set_volume,
	"os.brightness": os_control_tools.set_brightness,
	"communication.send_email": communication_tools.send_email,
	"communication.send_whatsapp": communication_tools.send_whatsapp,
}


def get_tool(name: str):
	return TOOL_REGISTRY.get(name)
