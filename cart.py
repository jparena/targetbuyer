from playwright.sync_api import sync_playwright
import time
import os
from datetime import datetime
import re
import random

URL = input("Enter the URL of the target product: ")  # e.g., "https://www.target.com/p/2025-pok-233-mon-scarlet-violet-s9-elite-trainer-box/-/A-93803439?type=scroll_to_review_section#lnk=sametab"
HARD_REFRESH_EVERY = 20  # number of loops before hard refresh, resests page in case u get blacked or flagged
MAX_PRICE = float(input("Enter the maximum price you're willing to pay: "))  # e.g., 50.00

loop_counter = 0

def check_target(p, context, page):
    global loop_counter

    if page.url != URL:
        page.goto(URL, timeout=15000)
    else:
        page.reload(timeout=15000)

    time.sleep(random.uniform(2, 4))

    try:
        button = page.locator('[data-test="orderPickupButton"], [data-test="shippingButton"], [data-test="addToCartButton"]')
        button = button.filter(has_text="Add to cart").first


        print(f"Found {button.count()} matching buttons.")

        if button.count() > 0 and button.is_enabled():
            print("✅ IN STOCK at Target!")
            button.click(force=True)
            print("✅ Added to cart!")

            time.sleep(0.5)
            page.goto("https://www.target.com/co-cart")
            time.sleep(2)

            # grab cart price this took me forever
            price_element = page.locator('div.sc-82d6cef6-1.eoKzsN')
            price_text = price_element.first.inner_text().strip()
            match = re.search(r"([\d.,]+)", price_text)  # this grabs just the number
            if match:
                price = float(match.group(1).replace(',', ''))
                print(f"🧾 Cart price: ${price}")
                if price > MAX_PRICE:
                    print(f"❌ Price ${price} exceeds limit of ${MAX_PRICE}. Skipping.")
                    return False
                else:
                    print("✅ Price acceptable. Proceeding to checkout...")

                    # check cart content
                    cart_items = page.locator('[data-test="cartItem"]')
                    if cart_items.count() > 0:
                        print(f"🛒 {cart_items.count()} item(s) in cart.")

                        # checkout button (step 1)
                        checkout_btn = page.locator('[data-test="checkout-button"]')
                        if checkout_btn.count() > 0 and checkout_btn.first.is_enabled():
                            checkout_btn.first.click(force=True)
                            print("🚀 Navigated to checkout page.")

                            time.sleep(2)  # Give time for the new page to load

                            #delete notes for auto checkout
                            # Place order button (step 2)
                            #place_order_btn = page.locator('[data-test="placeOrderButton"]')
                            #if place_order_btn.count() > 0 and place_order_btn.first.is_enabled():
                               # place_order_btn.first.click(force=True)
                               # print("🎉 Order placed!")

                              #  os.system('say "Order placed."')
                             #   with open("order_log.txt", "a") as f:
                             #       f.write(f"✅ Order placed at {datetime.now()} for ${price}\n")
                            #    return True
                          #  else:
                         #       print("❌ Place Order button not found or disabled.")
                        else:
                            print("❌ Checkout button not available.")
                    else:
                        print("⚠️ Cart appears empty.")
            else:
                print("⚠️ Couldn't locate cart price.")
        else:
            print("❌ Add to Cart button not found or disabled.")
    except Exception as e:
        print(f"💥 Error during check: {e}")

    return False


def run_bot():
    global loop_counter
    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir="./target_session",
            headless=False
        )
        page = context.new_page()

        while True:
            loop_counter += 1
            print(f"\n🔁 Loop #{loop_counter} — {datetime.now().strftime('%H:%M:%S')}")
            found = check_target(p, context, page)

            if found:
                print("✅ Auto-checkout complete. Exiting.")
                break

            if loop_counter % HARD_REFRESH_EVERY == 0:
                print("🔄 Hard refresh triggered...")
                context.close()
                context = p.chromium.launch_persistent_context(
                    user_data_dir="./target_session",
                    headless=False
                )
                page = context.new_page()

            time.sleep(3)


run_bot()
