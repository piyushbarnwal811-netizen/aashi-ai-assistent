from __future__ import annotations

from urllib.parse import quote_plus


def search_web(query: str, limit: int = 5) -> list[dict[str, str]]:
	import requests
	from bs4 import BeautifulSoup

	response = requests.get(
		f"https://html.duckduckgo.com/html/?q={quote_plus(query)}",
		headers={"User-Agent": "AASHI Desktop Agent/1.0"},
		timeout=10,
	)
	response.raise_for_status()
	soup = BeautifulSoup(response.text, "html.parser")
	results = []
	for item in soup.select(".result")[: max(1, min(limit, 10))]:
		link = item.select_one(".result__a")
		snippet = item.select_one(".result__snippet")
		if link:
			results.append({"title": link.get_text(" ", strip=True), "url": link.get("href", ""), "snippet": snippet.get_text(" ", strip=True) if snippet else ""})
	return results
