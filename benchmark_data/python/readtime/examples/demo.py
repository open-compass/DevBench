from readtime.api import of_text, of_markdown, of_html

print("\nText: The shortest blog post in the world!")
reading_time_text = of_text("The shortest blog post in the world!")
print("Text Reading Time (in seconds):", reading_time_text.seconds)
print("Text Reading Time (in text):", reading_time_text.text)

print("\nHTML: This is <strong>HTML</strong>")
reading_time_html = of_html("This is <strong>HTML</strong>")
print("HTML Reading Time (in seconds):", reading_time_html.seconds)
print("HTML Reading Time (in text):", reading_time_html.text)

print("\nMarkdown: This is **Markdown**")
reading_time_markdown = of_markdown("This is **Markdown**")
print("Markdown Reading Time (in seconds):", reading_time_markdown.seconds)
print("Markdown Reading Time (in text):", reading_time_markdown.text)

print("\nCustom WPM: The shortest blog post in the world! (WPM = 5)")
reading_time_wpm = of_text("The shortest blog post in the world!", wpm=5)
print("Custom WPM:", reading_time_wpm.wpm)
