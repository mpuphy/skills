---
name: browser-search
description: Force browser-based web search instead of using search API. Use when user asks to search the web, find information online, look up something on the internet, or any request involving web search. This skill overrides the default behavior of using web_search API and instead uses browser automation for search tasks.
---

# Browser Search Skill

## Purpose

This skill ensures that all web search requests are handled using browser automation (browser tool) rather than the search API (web_search tool).

## When to Use

Use this skill whenever the user asks for:
- Searching the web
- Looking up information online
- Finding something on the internet
- Researching a topic
- Any request that involves web search

## How to Execute

When a search request is received:

1. **DO NOT use `web_search` tool**

2. **Use `browser` tool instead:**
   - Start the browser if not running: `browser action=start`
   - Open a search engine: `browser action=open targetUrl="https://www.google.com/search?q=<query>"`
   - Or use DuckDuckGo: `browser action=open targetUrl="https://duckduckgo.com/?q=<query>"`

3. **Capture results:**
   - Take a snapshot: `browser action=snapshot`
   - Extract relevant information from the rendered page

4. **Navigate to specific results if needed:**
   - Click on result links: `browser action=act request={"kind":"click","ref":"<link-ref>"}`
   - Take screenshots or snapshots to capture content

## Example Flow

User: "Search for Python asyncio best practices"

Action:
1. `browser action=open targetUrl="https://www.google.com/search?q=Python+asyncio+best+practices"`
2. `browser action=snapshot` - capture search results
3. Summarize findings from the rendered page

## Notes

- Browser search provides more accurate, up-to-date results than API-based search
- JavaScript-rendered content is accessible via browser
- May take slightly longer due to page rendering
