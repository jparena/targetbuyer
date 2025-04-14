from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = p.chromium.launch_persistent_context(
        user_data_dir="./target_session",
        headless=False
    )
    page = context.new_page()
    page.goto("https://www.target.com/p/2025-pok-233-mon-scarlet-violet-s9-elite-trainer-box/-/A-93803439?type=scroll_to_review_section#lnk=sametab")
    print(page.content())
    input("Log in manually, then press Enter here to save your session...")
   
    context.close()
    browser.close()
