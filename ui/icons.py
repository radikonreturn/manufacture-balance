"""
ui/icons.py — SVG icon definitions for Manufacture Balance 4.0
Replaces emoji with clean, scalable SVG icons.
"""

# Each icon returns an inline SVG string suitable for use in st.markdown(unsafe_allow_html=True)
# Usage: from ui.icons import svg
# Then:  svg("factory", size=20, color="#fff")


_ICONS = {
    # App / Header
    "factory": '<path stroke-linecap="round" stroke-linejoin="round" d="M3 21V9l5-3v3l5-3v3l5-3v15H3z"/><path stroke-linecap="round" stroke-linejoin="round" d="M9 21v-6h6v6"/>',
    # Sidebar
    "clock": '<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>',
    "lightning": '<polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>',
    # Tabs
    "download": '<path stroke-linecap="round" stroke-linejoin="round" d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/>',
    "bar_chart": '<line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/>',
    "hard_hat": '<path stroke-linecap="round" stroke-linejoin="round" d="M2 18h20v2a1 1 0 01-1 1H3a1 1 0 01-1-1v-2z"/><path stroke-linecap="round" stroke-linejoin="round" d="M12 3C8.134 3 5 6.134 5 10v8h14v-8c0-3.866-3.134-7-7-7z"/>',
    "leaf": '<path stroke-linecap="round" stroke-linejoin="round" d="M17 8C8 10 5.9 16.17 3.82 19.34A1 1 0 005 21c5-1 11-4 13-10 1.06-3.17.5-6.7-1-3zm0 0c0 0-4 2-6 8"/>',
    "scale": '<path stroke-linecap="round" stroke-linejoin="round" d="M12 3v18M3 9l9-6 9 6M5 20h14"/><path stroke-linecap="round" stroke-linejoin="round" d="M3 9l3 7a3 3 0 006 0l3-7M9 16v1M15 16v1"/>',
    # Actions
    "save": '<path d="M19 21H5a2 2 0 01-2-2V5a2 2 0 012-2h11l5 5v11a2 2 0 01-2 2z"/><polyline points="17 21 17 13 7 13 7 21"/><polyline points="7 3 7 8 15 8"/>',
    "upload": '<path stroke-linecap="round" stroke-linejoin="round" d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/>',
    "folder": '<path d="M22 19a2 2 0 01-2 2H4a2 2 0 01-2-2V5a2 2 0 012-2h5l2 3h9a2 2 0 012 2z"/>',
    "pencil": '<path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z"/>',
    "trend_up": '<polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline points="17 6 23 6 23 12"/>',
    "clipboard": '<path d="M16 4h2a2 2 0 012 2v14a2 2 0 01-2 2H6a2 2 0 01-2-2V6a2 2 0 012-2h2"/><rect x="8" y="2" width="8" height="4" rx="1" ry="1"/>',
    "pin": '<path stroke-linecap="round" stroke-linejoin="round" d="M12 2a3 3 0 013 3c0 1.5-.8 2.8-2 3.4V17l1 3H10l1-3V8.4A3.5 3.5 0 019 5a3 3 0 013-3z"/>',
    "document": '<path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/>',
    # Sustainability cards
    "dollar": '<circle cx="12" cy="12" r="10"/><path d="M12 6v12M9 9.5c0-1.1.9-2 2-2h2a2 2 0 010 4h-2a2 2 0 000 4h2a2 2 0 002-2"/>',
    "globe": '<circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 014 10 15.3 15.3 0 01-4 10 15.3 15.3 0 01-4-10 15.3 15.3 0 014-10z"/>',
    "zap": '<polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>',
    # Warning
    "warning": '<path stroke-linecap="round" stroke-linejoin="round" d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/>',
}


def svg(name: str, size: int = 16, color: str = "currentColor", style: str = "") -> str:
    """Return an inline SVG <img>-like element for the given icon name."""
    paths = _ICONS.get(name, "")
    extra = f' style="{style}"' if style else ""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" '
        f'viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" '
        f'stroke-linecap="round" stroke-linejoin="round" '
        f'style="vertical-align:middle; display:inline-block;"{extra}>'
        f'{paths}</svg>'
    )


def icon_label(icon_name: str, label: str, size: int = 16, color: str = "currentColor") -> str:
    """Return SVG icon + text label, useful for tab labels or section headers."""
    return f'{svg(icon_name, size=size, color=color)}&nbsp;{label}'
