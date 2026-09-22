"""
Expense Tracker — Complete Login Test Suite
URL: https://expense-tracker-frontend-v1-0.vercel.app/login
Flow: Email + Password → Continue → /overview
"""

from playwright.sync_api import Page, expect
import re
import time

# ---------- Config ----------
BASE_URL      = "https://expense-tracker-frontend-v1-0.vercel.app"
LOGIN_URL     = f"{BASE_URL}/login"

VALID_EMAIL    = "sairaramzan63@gmail.com"
VALID_PASSWORD = "Saira@123"

INVALID_EMAIL    = "wronguser@example.com"
INVALID_PASSWORD = "WrongPassword!123"

MALFORMED_EMAIL = "not-an-email"


# ============================================================
# 1. SMOKE — Login page loads correctly
# ============================================================
def test_login_page_loads(page: Page):
    print("\n[1] Opening login page...")
    page.goto(LOGIN_URL)
    page.wait_for_timeout(1500)

    expect(page).to_have_url(re.compile(r".*/login/?$"))
    expect(page.get_by_role("heading", name=re.compile("sign in", re.I))).to_be_visible()
    expect(page.get_by_label("Email Address")).to_be_visible()
    expect(page.get_by_label("Password")).to_be_visible()
    expect(page.get_by_role("button", name="Continue")).to_be_visible()
    print("✅ Login page loaded with all fields")


# ============================================================
# 2. UI — Continue button disabled when form is empty
# ============================================================
def test_continue_disabled_when_empty(page: Page):
    print("\n[2] Checking disabled state of Continue button...")
    page.goto(LOGIN_URL)
    page.wait_for_timeout(1500)

    continue_btn = page.get_by_role("button", name="Continue")
    expect(continue_btn).to_be_disabled()
    print("✅ Continue button is disabled on empty form")


# ============================================================
# 3. UI — Continue stays disabled when only email is filled
# ============================================================
def test_continue_disabled_with_only_email(page: Page):
    print("\n[3] Filling email only...")
    page.goto(LOGIN_URL)
    page.wait_for_timeout(1500)

    page.get_by_label("Email Address").fill(VALID_EMAIL)
    page.wait_for_timeout(500)

    expect(page.get_by_role("button", name="Continue")).to_be_disabled()
    print("✅ Continue still disabled with email only")


# ============================================================
# 4. UI — Continue stays disabled when only password is filled
# ============================================================
def test_continue_disabled_with_only_password(page: Page):
    print("\n[4] Filling password only...")
    page.goto(LOGIN_URL)
    page.wait_for_timeout(1500)

    page.get_by_label("Password").fill(VALID_PASSWORD)
    page.wait_for_timeout(500)

    expect(page.get_by_role("button", name="Continue")).to_be_disabled()
    print("✅ Continue still disabled with password only")


# ============================================================
# 5. UI — Continue enables when both fields are filled
# ============================================================
def test_continue_enables_with_both_fields(page: Page):
    print("\n[5] Filling both fields...")
    page.goto(LOGIN_URL)
    page.wait_for_timeout(1500)

    page.get_by_label("Email Address").fill(VALID_EMAIL)
    page.get_by_label("Password").fill(VALID_PASSWORD)
    page.wait_for_timeout(500)

    expect(page.get_by_role("button", name="Continue")).to_be_enabled()
    print("✅ Continue enabled with both fields")


# ============================================================
# 6. HAPPY PATH — Valid login → lands on /overview
# ============================================================
def test_login_with_valid_credentials(page: Page):
    print("\n[6] Logging in with valid credentials...")
    page.goto(LOGIN_URL)
    page.wait_for_timeout(1500)

    page.get_by_label("Email Address").fill(VALID_EMAIL)
    page.get_by_label("Password").fill(VALID_PASSWORD)
    page.get_by_role("button", name="Continue").click()

    expect(page).to_have_url(re.compile(r".*/overview/?$"), timeout=15000)
    print(f"✅ Redirected to: {page.url}")

    expect(page.get_by_text("Welcome back", exact=False)).to_be_visible(timeout=10000)
    print("✅ Welcome message visible")


# ============================================================
# 7. HAPPY PATH — Logged-in email appears in header
# ============================================================
def test_logged_in_email_visible_in_header(page: Page):
    print("\n[7] Verifying logged-in email in header...")
    page.goto(LOGIN_URL)
    page.wait_for_timeout(1500)

    page.get_by_label("Email Address").fill(VALID_EMAIL)
    page.get_by_label("Password").fill(VALID_PASSWORD)
    page.get_by_role("button", name="Continue").click()

    expect(page).to_have_url(re.compile(r".*/overview/?$"), timeout=15000)
    expect(page.get_by_text(VALID_EMAIL, exact=False)).to_be_visible(timeout=10000)
    print("✅ User email visible in header")


# ============================================================
# 8. HAPPY PATH — Logout works from /overview
# ============================================================
def test_logout_redirects_to_login(page: Page):
    print("\n[8] Logging in, then logging out...")
    page.goto(LOGIN_URL)
    page.wait_for_timeout(1500)

    page.get_by_label("Email Address").fill(VALID_EMAIL)
    page.get_by_label("Password").fill(VALID_PASSWORD)
    page.get_by_role("button", name="Continue").click()
    expect(page).to_have_url(re.compile(r".*/overview/?$"), timeout=15000)

    print("Clicking Log out...")
    page.get_by_role("button", name=re.compile("log out", re.I)).click()
    page.wait_for_timeout(2500)

    assert "/overview" not in page.url, f"Still on {page.url} after logout"
    print(f"✅ Logged out — now on {page.url}")


# ============================================================
# 9. NEGATIVE — Wrong password keeps user on /login
# ============================================================
def test_login_with_wrong_password(page: Page):
    print("\n[9] Trying wrong password...")
    page.goto(LOGIN_URL)
    page.wait_for_timeout(1500)

    page.get_by_label("Email Address").fill(VALID_EMAIL)
    page.get_by_label("Password").fill(INVALID_PASSWORD)
    page.get_by_role("button", name="Continue").click()
    page.wait_for_timeout(3000)

    expect(page).to_have_url(re.compile(r".*/login/?$"))
    print("✅ Wrong password rejected — still on /login")


# ============================================================
# 10. NEGATIVE — Unknown email keeps user on /login
# ============================================================
def test_login_with_unknown_email(page: Page):
    print("\n[10] Trying unknown email...")
    page.goto(LOGIN_URL)
    page.wait_for_timeout(1500)

    page.get_by_label("Email Address").fill(INVALID_EMAIL)
    page.get_by_label("Password").fill(VALID_PASSWORD)
    page.get_by_role("button", name="Continue").click()
    page.wait_for_timeout(3000)

    expect(page).to_have_url(re.compile(r".*/login/?$"))
    print("✅ Unknown email rejected — still on /login")


# ============================================================
# 11. NEGATIVE — Malformed email disables Continue
# ============================================================
def test_malformed_email_keeps_continue_disabled(page: Page):
    print("\n[11] Entering malformed email...")
    page.goto(LOGIN_URL)
    page.wait_for_timeout(1500)

    page.get_by_label("Email Address").fill(MALFORMED_EMAIL)
    page.get_by_label("Password").fill(VALID_PASSWORD)
    page.wait_for_timeout(500)

    continue_btn = page.get_by_role("button", name="Continue")
    if continue_btn.is_disabled():
        print("✅ Continue disabled for malformed email")
    else:
        continue_btn.click()
        page.wait_for_timeout(2000)
        expect(page).to_have_url(re.compile(r".*/login/?$"))
        print("✅ Malformed email rejected — still on /login")


# ============================================================
# 12. NEGATIVE — Email field HTML validation (type=email)
# ============================================================
def test_email_field_type_validation(page: Page):
    print("\n[12] Checking email input type...")
    page.goto(LOGIN_URL)
    page.wait_for_timeout(1500)

    email_input = page.get_by_label("Email Address")
    input_type = email_input.get_attribute("type")
    assert input_type == "email", f"Expected type='email', got {input_type!r}"
    print("✅ Email field has type='email' (HTML5 validation active)")


# ============================================================
# 13. NEGATIVE — Password field is masked
# ============================================================
def test_password_field_is_masked(page: Page):
    print("\n[13] Checking password masking...")
    page.goto(LOGIN_URL)
    page.wait_for_timeout(1500)

    password_input = page.get_by_label("Password")
    input_type = password_input.get_attribute("type")
    assert input_type == "password", f"Expected type='password', got {input_type!r}"
    print("✅ Password field is masked")


# ============================================================
# 14. UI — 'Show' toggle reveals password
# ============================================================
def test_show_password_toggle(page: Page):
    print("\n[14] Testing Show/Hide password toggle...")
    page.goto(LOGIN_URL)
    page.wait_for_timeout(1500)

    page.get_by_label("Password").fill(VALID_PASSWORD)
    page.wait_for_timeout(300)

    page.get_by_role("button", name=re.compile("show", re.I)).click()
    page.wait_for_timeout(300)

    input_type = page.get_by_label("Password").get_attribute("type")
    print(f"   Type after Show: {input_type}")
    assert input_type == "text", "Password should be visible after Show"
    print("✅ Show toggle works")


# ============================================================
# 15. UI — 'Create an account' link navigation
# ============================================================
def test_create_account_link_navigates(page: Page):
    print("\n[15] Clicking 'Create an account'...")
    page.goto(LOGIN_URL)
    page.wait_for_timeout(1500)

    page.get_by_role("link", name=re.compile("create an account", re.I)).click()
    page.wait_for_timeout(2000)

    assert "/login" not in page.url, f"Still on /login: {page.url}"
    print(f"✅ Navigated to: {page.url}")


# ============================================================
# 16. UI — 'Forgot password?' link navigation
# ============================================================
def test_forgot_password_link_navigates(page: Page):
    print("\n[16] Clicking 'Forgot password?'...")
    page.goto(LOGIN_URL)
    page.wait_for_timeout(1500)

    page.get_by_role("link", name=re.compile("forgot password", re.I)).click()
    page.wait_for_timeout(2000)

    assert "/login" not in page.url, f"Still on /login: {page.url}"
    print(f"✅ Navigated to: {page.url}")


# ============================================================
# 17. UI — 'Sign In' nav button from home → /login
# ============================================================
def test_signin_button_from_home_navigates_to_login(page: Page):
    print("\n[17] Home → click Sign In...")
    page.goto(BASE_URL)
    page.wait_for_timeout(1500)

    # .first required — home has 3 "Sign in" links (header/main/footer)
    page.get_by_role("link", name=re.compile("^sign in$", re.I)).first.click()
    page.wait_for_timeout(2000)

    expect(page).to_have_url(re.compile(r".*/login/?$"))
    print("✅ Navigated to /login from home")


# ============================================================
# 18. UI — 'Get Started' button from home → /register
# ============================================================
def test_get_started_from_home(page: Page):
    print("\n[18] Home → click Get Started...")
    page.goto(BASE_URL)
    page.wait_for_timeout(1500)

    page.get_by_role("link", name=re.compile("get started", re.I)).first.click()
    page.wait_for_timeout(2000)

    print(f"   Landed on: {page.url}")
    assert any(x in page.url for x in ["/login", "/register", "/signup", "/auth"]), \
        f"Unexpected URL: {page.url}"
    print("✅ Get Started navigates to auth page")


# ============================================================
# 19. UI — Protected route redirects to /login when not auth'd
# ============================================================
def test_protected_route_redirects_to_login(page: Page):
    print("\n[19] Trying to access /overview while logged out...")
    page.goto(f"{BASE_URL}/overview")
    page.wait_for_timeout(2500)

    assert "/login" in page.url or "/overview" not in page.url, \
        f"Protected route not guarded: {page.url}"
    print(f"✅ Protected route guarded — landed on {page.url}")


# ============================================================
# 20. FULL E2E — Login, navigate, logout, verify
# ============================================================
def test_full_login_flow_e2e(page: Page):
    print("\n[20] Full end-to-end login → navigate → logout...")

    # 1. Home page
    page.goto(BASE_URL)
    page.wait_for_timeout(1500)
    print("   ✔ Home loaded")

    # 2. Click Sign In (first match — home has 3 of these links)
    page.get_by_role("link", name=re.compile("^sign in$", re.I)).first.click()
    page.wait_for_timeout(1500)
    expect(page).to_have_url(re.compile(r".*/login/?$"))
    print("   ✔ On /login")

    # 3. Fill and submit
    page.get_by_label("Email Address").fill(VALID_EMAIL)
    page.get_by_label("Password").fill(VALID_PASSWORD)
    page.get_by_role("button", name="Continue").click()

    # 4. Verify /overview
    expect(page).to_have_url(re.compile(r".*/overview/?$"), timeout=15000)
    expect(page.get_by_text("Welcome back", exact=False)).to_be_visible(timeout=10000)
    print("   ✔ Logged in → /overview")

    # 5. Click a sidebar item (Cost Analytics)
    page.get_by_role("link", name=re.compile("cost analytics", re.I)).first.click()
    page.wait_for_timeout(2000)
    print(f"   ✔ Navigated to: {page.url}")

    # 6. Logout
    page.get_by_role("button", name=re.compile("log out", re.I)).click()
    page.wait_for_timeout(2500)
    assert "/overview" not in page.url
    print(f"   ✔ Logged out → {page.url}")

    print("✅ E2E flow complete")
    time.sleep(2)