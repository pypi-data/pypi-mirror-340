# talk2dom

**talk2dom** is a focused utility that solves one of the hardest problems in browser automation and UI testing:

> ✅ **Finding the correct UI element on a page.**

---

## 🧠 Why `talk2dom`

In most automated testing or LLM-driven web navigation tasks, the real challenge is not how to click or type — it's how to **locate the right element**.

Think about it:

- Clicking a button is easy — *if* you know its selector.
- Typing into a field is trivial — *if* you've already located the right input.
- But finding the correct element among hundreds of `<div>`, `<span>`, or deeply nested Shadow DOM trees? That's the hard part.

**`talk2dom` is built to solve exactly that.**

---

## 🎯 What it does

`talk2dom` helps you locate elements by:

- Extracting clean HTML from Selenium `WebDriver` or any `WebElement`
- Formatting it for LLM consumption (e.g. GPT-4, Claude, etc.)
- Returning minimal, clear selectors (like `xpath: ...` or `css: ...`)
- Supporting retry logic for unstable DOM conditions
- Playing nicely with Shadow DOM traversal (you handle it your way)

---

## 🤔 Why Selenium?

While there are many modern tools for controlling browsers (like Playwright or Puppeteer), **Selenium remains the most robust and cross-platform solution**, especially when dealing with:

- ✅ Safari (WebKit)
- ✅ Firefox
- ✅ Mobile browsers
- ✅ Cross-browser testing grids

These tools often have limited support for anything beyond Chrome-based browsers. Selenium, by contrast, has battle-tested support across all major platforms and continues to be the industry standard in enterprise and CI/CD environments.

That’s why `talk2dom` is designed to integrate directly with Selenium — it works where the real-world complexity lives.

---

## 📦 Installation

```bash
pip install talk2dom
```

---

## 🔍 Usage Example

### Make sure you have OPENAI_API_KEY

```bash
export OPENAI_API_KEY="..."
```

### Sample Code

```python
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from talk2dom import get_locator

driver = webdriver.Chrome()
driver.get("http://www.python.org")
assert "Python" in driver.title
by, value = get_locator(driver, "Find the Search box")
elem = driver.find_element(by, value)
elem.clear()
elem.send_keys("pycon")
elem.send_keys(Keys.RETURN)
assert "No results found." not in driver.page_source
driver.close()
```

---

## ✨ Philosophy

> Our goal is not to control the browser — Selenium already does that well.  
> Our goal is to **find the right DOM element**, so you can tell the browser what to do.

---

## ✅ Key Features

- 📍 Locator-first mindset: focus on *where*, not *how*
- 🔁 Retry wrapper for flaky pages
- 🧠 Built for LLM-agent workflows
- 🧩 Shadow DOM friendly (you handle traversal, we return selectors)

---

## 📄 License

Apache 2.0

---

## Contributing

Please read [CONTRIBUTING.md](https://github.com/itbanque/talk2dom/blob/main/CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

---

## 💬 Questions or ideas?

We’d love to hear how you're using `talk2dom` in your AI agents or testing flows.  
Feel free to open issues or discussions!
