html_theme_options = {
    "icon": {
        "repo": "fontawesome/brands/github",
    },
    "font": {
        "code": "JetBrains Mono",
        "text": "Urbanist"
    },
    "globaltoc_collapse": True,
    "features": [
        "navigation.top",
        "search.share",
        "navigation.tracking",
        "toc.follow",
        "content.tabs.link"
    ],
    "palette": [
        {
            "media": "(prefers-color-scheme: light)",
            "scheme": "default",
            "primary": "yellow",
            "accent": "yellow",
            "toggle": {
                "icon": "material/weather-night",
                "name": "Switch to dark mode",
            },
        },
        {
            "media": "(prefers-color-scheme: dark)",
            "scheme": "slate",
            "primary": "yellow",
            "accent": "yellow",
            "toggle": {
                "icon": "material/weather-sunny",
                "name": "Switch to light mode",
            },
        },
    ],
    "toc_title_is_page_title": True,
    "toc_title": "Contents",
}
