import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementClickInterceptedException,
    StaleElementReferenceException,
)
import requests
import json


DOWNLOAD_DIR = "./downloads"
TEXT_PARSING_URL = "http://localhost:8000/parse"

COOKIES = [
    {
        "domain": ".naukri.com",
        "expirationDate": 1800612055.914942,
        "hostOnly": False,
        "httpOnly": False,
        "name": "__utma",
        "path": "/",
        "secure": False,
        "session": False,
        "value": "266160400.1216351894.1765887463.1766052056.1766052056.1",
    },
    {
        "domain": ".naukri.com",
        "expirationDate": 1781820055,
        "hostOnly": False,
        "httpOnly": False,
        "name": "__utmz",
        "path": "/",
        "secure": False,
        "session": False,
        "value": "266160400.1766052056.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)",
    },
    {
        "domain": ".naukri.com",
        "expirationDate": 1797423480,
        "hostOnly": False,
        "httpOnly": False,
        "name": "_clck",
        "path": "/",
        "secure": False,
        "session": False,
        "value": "ce7z8c%5E2%5Eg1w%5E0%5E2176",
    },
    {
        "domain": ".naukri.com",
        "expirationDate": 1778051079.1863,
        "hostOnly": False,
        "httpOnly": True,
        "name": "_did",
        "path": "/",
        "secure": True,
        "session": False,
        "value": "68842fd13b",
    },
    {
        "domain": ".naukri.com",
        "expirationDate": 1782369853,
        "hostOnly": False,
        "httpOnly": False,
        "name": "_fbp",
        "path": "/",
        "secure": False,
        "session": False,
        "value": "fb.1.1765887563284.386325289940204468",
    },
    {
        "domain": ".naukri.com",
        "expirationDate": 1809155079.939064,
        "hostOnly": False,
        "httpOnly": False,
        "name": "_ga",
        "path": "/",
        "secure": False,
        "session": False,
        "value": "GA1.2.1216351894.1765887463",
    },
    {
        "domain": ".naukri.com",
        "expirationDate": 1800450865.621418,
        "hostOnly": False,
        "httpOnly": False,
        "name": "_ga_7TYVEWTVRG",
        "path": "/",
        "secure": False,
        "session": False,
        "value": "GS2.1.s1765890853$o2$g1$t1765890865$j48$l0$h0",
    },
    {
        "domain": ".naukri.com",
        "expirationDate": 1800447467.413724,
        "hostOnly": False,
        "httpOnly": False,
        "name": "_ga_F01VRRM5X6",
        "path": "/",
        "secure": False,
        "session": False,
        "value": "GS2.1.s1765887462$o1$g0$t1765887467$j55$l0$h0",
    },
    {
        "domain": ".naukri.com",
        "expirationDate": 1800450865.644942,
        "hostOnly": False,
        "httpOnly": False,
        "name": "_ga_JCSR1LRE3X",
        "path": "/",
        "secure": False,
        "session": False,
        "value": "GS2.1.s1765890853$o2$g1$t1765890865$j48$l0$h0",
    },
    {
        "domain": ".naukri.com",
        "expirationDate": 1809155217.581233,
        "hostOnly": False,
        "httpOnly": False,
        "name": "_ga_K2YBNZVRLL",
        "path": "/",
        "secure": False,
        "session": False,
        "value": "GS2.1.s1774593798$o11$g1$t1774595217$j60$l0$h0",
    },
    {
        "domain": ".naukri.com",
        "expirationDate": 1800508173.32848,
        "hostOnly": False,
        "httpOnly": False,
        "name": "_ga_T749QGK6MQ",
        "path": "/",
        "secure": False,
        "session": False,
        "value": "GS2.1.s1765948014$o2$g1$t1765948173$j56$l0$h0",
    },
    {
        "domain": ".naukri.com",
        "expirationDate": 1782369798,
        "hostOnly": False,
        "httpOnly": False,
        "name": "_gcl_au",
        "path": "/",
        "secure": False,
        "session": False,
        "value": "1.1.137424548.1774593798",
    },
    {
        "domain": ".naukri.com",
        "expirationDate": 1774681479,
        "hostOnly": False,
        "httpOnly": False,
        "name": "_gid",
        "path": "/",
        "secure": False,
        "session": False,
        "value": "GA1.2.1009517711.1774594140",
    },
    {
        "domain": ".naukri.com",
        "expirationDate": 1777187078.457195,
        "hostOnly": False,
        "httpOnly": True,
        "name": "_odur",
        "path": "/",
        "secure": True,
        "session": False,
        "value": "9b4320e4c7",
    },
    {
        "domain": ".naukri.com",
        "expirationDate": 1777187078.457562,
        "hostOnly": False,
        "httpOnly": True,
        "name": "_t_ds",
        "path": "/",
        "secure": True,
        "session": False,
        "value": "414a20c81774593796-43414a20c8-0414a20c8",
    },
    {
        "domain": ".naukri.com",
        "hostOnly": False,
        "httpOnly": True,
        "name": "1de287eda6a540b1723eafc33609d7421s7",
        "path": "/",
        "secure": True,
        "session": True,
        "value": "a",
    },
    {
        "domain": ".naukri.com",
        "expirationDate": 1774680538.313108,
        "hostOnly": False,
        "httpOnly": True,
        "name": "65b8ed21bb7d08986a57df3faebbdc5f1s7",
        "path": "/",
        "secure": True,
        "session": False,
        "value": "v0%7CGJbgzt1RrlhyyQwF7HCRGljMl9ZEiyPgADE%2BTnNLsggh4%2Bj3k57E7j6TnnSkz9ZkAyG%2F9EDFDC34%2FRRzM99%2Bg6SMzzJ4T2X%2BO%2FGjNBY%2F8IWAmNnI9OdUXBIC3KqyzEn1550KksgWu7FQBhochMDf7PgNgcvLboNma3VJWiHjl1Y%3D",
    },
    {
        "domain": ".naukri.com",
        "expirationDate": 1777186138.313634,
        "hostOnly": False,
        "httpOnly": True,
        "name": "ACCESS",
        "path": "/",
        "secure": True,
        "session": False,
        "value": "1774594138454",
    },
    {
        "domain": ".naukri.com",
        "expirationDate": 1774600995.953809,
        "hostOnly": False,
        "httpOnly": True,
        "name": "ak_bmsc",
        "path": "/",
        "secure": False,
        "session": False,
        "value": "673D4F3032134A4BC1D081A6544474D7~000000000000000000000000000000~YAAQjonTF5JQw+WcAQAA5G8ILh9x0/axXWnNpnVWRrruihWwR9Qf2IMyHYWwdEQpNNPe33fsbyI4ZdzKzgrWS4HN6KhddZJUlhtdHeFnGMQa0NTT9cW+1R9hGwRHb9hyScdgmq69UfGlDsUopNQLW9MhHu7q3U7OcN3dKo/FZ26ZusYLhd5ZpjKv5LzgRPdwy6N2vpjCnRDwHxp66JcSEf9YHanApm/m6bQLwh3zPHW7OVqpcpp8vFlqh32QbYEOeVl2zyqz8gOSaZQTclvT98sixMz81kkszk+3z7FBzQTNQezRjXEIFFc5Iq1SWssDP1gzXxex1PJmTGLzLHGMeYc+cMxs/9umVLORsTCMP9PPZ34G5bK6LuFyXfinePSomsa9f809qMepASXqYe4WHxDoczkwkvzskCMt7yvJsno5XssLR0uM7yo/l4ha1wx8rvqc1BRcRW/2hxNFLkOan2s=",
    },
    {
        "domain": ".naukri.com",
        "expirationDate": 1774600997.613691,
        "hostOnly": False,
        "httpOnly": False,
        "name": "bm_sv",
        "path": "/",
        "secure": True,
        "session": False,
        "value": "48CC4660E109BC10FB2A5038F447BFED~YAAQP/TfF1mv7BmdAQAA4xFHLh9LtRvhpSqf0L7rj0McNHK5ZsLx+KSG2rnbfESwA8M5pmSQ+3Gio/nfPfQS3wDrTdKnglWKk8pIDJ2wwDVEvvYG6Fgv2iWpxf3xUrjtnul8/L18rD6oD23eKvUlVKRipUetL9EVcUUdmotGlCsfuHKfNiWgKXEEq2uUzgiIUlk1pTj2rL/1IFxXZy+RyyIF0ttwaN+pgcAOUfbSrBuF5UlF8s/5IsK8VY9Vcmw8KQ==~1",
    },
    {
        "domain": ".naukri.com",
        "expirationDate": 1774680538.312908,
        "hostOnly": False,
        "httpOnly": False,
        "name": "bs_rnd",
        "path": "/",
        "secure": True,
        "session": False,
        "value": "L09d396L",
    },
    {
        "domain": ".naukri.com",
        "expirationDate": 1774680538.315803,
        "hostOnly": False,
        "httpOnly": True,
        "name": "dashboard",
        "path": "/",
        "secure": True,
        "session": False,
        "value": "1",
    },
    {
        "domain": ".naukri.com",
        "expirationDate": 1774680538.31614,
        "hostOnly": False,
        "httpOnly": False,
        "name": "encId",
        "path": "/",
        "secure": True,
        "session": False,
        "value": "8504862bcaa748e966e84a41eed88fc25c580b514d110d6",
    },
    {
        "domain": ".naukri.com",
        "expirationDate": 1777186138.314853,
        "hostOnly": False,
        "httpOnly": True,
        "name": "ER",
        "path": "/",
        "secure": True,
        "session": False,
        "value": "52947",
    },
    {
        "domain": ".naukri.com",
        "expirationDate": 1806135373.42079,
        "hostOnly": False,
        "httpOnly": True,
        "name": "J",
        "path": "/",
        "secure": True,
        "session": False,
        "value": "0",
    },
    {
        "domain": ".naukri.com",
        "expirationDate": 1777186138.313265,
        "hostOnly": False,
        "httpOnly": True,
        "name": "kycEligibleCookie52947",
        "path": "/",
        "secure": True,
        "session": False,
        "value": "False",
    },
    {
        "domain": ".naukri.com",
        "expirationDate": 1806130138.315934,
        "hostOnly": False,
        "httpOnly": False,
        "name": "lastLoggedInUser",
        "path": "/",
        "secure": True,
        "session": False,
        "value": "preeti.singh@neerinfo.com",
    },
    {
        "domain": ".naukri.com",
        "expirationDate": 1806130138.315131,
        "hostOnly": False,
        "httpOnly": True,
        "name": "loginMethod",
        "path": "/",
        "secure": True,
        "session": False,
        "value": "naukriLauncher",
    },
    {
        "domain": ".naukri.com",
        "expirationDate": 1806130138.315318,
        "hostOnly": False,
        "httpOnly": True,
        "name": "loginPreference",
        "path": "/",
        "secure": True,
        "session": False,
        "value": "secureLoginMandatory",
    },
    {
        "domain": ".naukri.com",
        "expirationDate": 1797484081.329783,
        "hostOnly": False,
        "httpOnly": False,
        "name": "MYNAUKRI[UNID]",
        "path": "/",
        "secure": True,
        "session": False,
        "value": "170b800de3c044d7820e37aa49c2bf5b",
    },
    {
        "domain": ".naukri.com",
        "expirationDate": 1797426869.215917,
        "hostOnly": False,
        "httpOnly": False,
        "name": "ninjas_new_marketing_token",
        "path": "/",
        "secure": True,
        "session": False,
        "value": "87c900b9677e642e9d1689c081ff56e2",
    },
    {
        "domain": ".naukri.com",
        "expirationDate": 1797426865,
        "hostOnly": False,
        "httpOnly": False,
        "name": "ph_phc_s4aJa5RpiiZlHbbxy4Y1Btjhosozg9ECrSuJNVrvZuP_posthog",
        "path": "/",
        "secure": True,
        "session": False,
        "value": "%7B%22distinct_id%22%3A%2219b271892bb6db-03fd6a9e0eac9f8-15462c69-1fa400-19b271892bc556%22%7D",
    },
    {
        "domain": ".naukri.com",
        "expirationDate": 1779778138.315528,
        "hostOnly": False,
        "httpOnly": False,
        "name": "secureloginenabled",
        "path": "/",
        "secure": True,
        "session": False,
        "value": "True",
    },
    {
        "domain": ".naukri.com",
        "expirationDate": 1777186138.315019,
        "hostOnly": False,
        "httpOnly": True,
        "name": "slag",
        "path": "/",
        "secure": True,
        "session": False,
        "value": "",
    },
    {
        "domain": ".naukri.com",
        "expirationDate": 1774600996.868108,
        "hostOnly": False,
        "httpOnly": False,
        "name": "SnippedURL",
        "path": "/",
        "secure": True,
        "session": False,
        "value": "https%3A%2F%2Frecruit.naukri.com%2F",
    },
    {
        "domain": ".naukri.com",
        "expirationDate": 1775199880.346129,
        "hostOnly": False,
        "httpOnly": True,
        "name": "test",
        "path": "/",
        "secure": True,
        "session": False,
        "value": "naukri.com",
    },
    {
        "domain": ".naukri.com",
        "expirationDate": 1777186138.31409,
        "hostOnly": False,
        "httpOnly": True,
        "name": "UNCC",
        "path": "/",
        "secure": True,
        "session": False,
        "value": "4520724",
    },
    {
        "domain": ".naukri.com",
        "expirationDate": 1775199879.186542,
        "hostOnly": False,
        "httpOnly": True,
        "name": "UNID",
        "path": "/",
        "secure": True,
        "session": False,
        "value": "aHV9clW0bMQT9M7nEahxB7mqsLvWdR9RU343nEXc",
    },
    {
        "domain": ".naukri.com",
        "expirationDate": 1777186138.313945,
        "hostOnly": False,
        "httpOnly": True,
        "name": "UNPC",
        "path": "/",
        "secure": True,
        "session": False,
        "value": "52947",
    },
]

USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36"


# ============================================================================
# DRIVER
# ============================================================================
def _create_driver() -> webdriver.Chrome:
    options = Options()
    options.add_argument(f"--user-agent={USER_AGENT}")
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )
    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {
            "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined});"
        },
    )
    return driver


# ============================================================================
# COOKIE INJECTION
# ============================================================================
def _inject_cookies(driver: webdriver.Chrome) -> bool:
    print("🍪 Injecting cookies...")

    # Navigate to naukri.com first so domain context is set
    driver.get("https://www.naukri.com/404")
    time.sleep(3)

    injected_count = 0
    skipped_count = 0

    for cookie in COOKIES:
        try:
            c = dict(cookie)
            # Remove keys Selenium rejects
            for key in ["sameSite", "storeId", "id", "hostOnly", "session"]:
                c.pop(key, None)

            # Skip expired
            exp = c.get("expirationDate") or c.get("expiry")
            if exp and float(exp) < time.time():
                skipped_count += 1
                continue

            # Rename expirationDate → expiry (Selenium standard)
            if "expirationDate" in c:
                c["expiry"] = int(c.pop("expirationDate"))

            if "naukri.com" not in c.get("domain", ""):
                skipped_count += 1
                continue

            c["domain"] = ".naukri.com"
            driver.add_cookie(c)
            injected_count += 1
        except Exception:
            skipped_count += 1
            continue

    print(f"✅ Injected: {injected_count} | Skipped: {skipped_count}")

    # Verify — use the exact URL your cookies came from
    print("🔄 Verifying session...")
    driver.get("https://recruit.naukri.com")
    time.sleep(6)

    current = driver.current_url.lower()
    print(f"   Current URL: {driver.current_url}")

    if any(x in current for x in ["login", "nlogin", "signin"]):
        # Try enterprise subdomain as fallback
        print("⚠️ recruit.naukri.com rejected, trying enterprise.naukri.com...")
        driver.get("https://enterprise.naukri.com/recruit/")
        time.sleep(6)
        current = driver.current_url.lower()
        print(f"   Current URL: {driver.current_url}")

        if any(x in current for x in ["login", "nlogin", "signin"]):
            print("❌ Session rejected on both domains.")
            print("   → Your cookies may be expired. Please export fresh ones.")
            os.makedirs(DOWNLOAD_DIR, exist_ok=True)
            driver.save_screenshot(os.path.join(DOWNLOAD_DIR, "auth_failed.png"))
            return False

    print("✅ Session authorized!")
    return True


# ============================================================================
# POPUP DISMISSAL
# ============================================================================
def _dismiss_popups(driver: webdriver.Chrome):
    try:
        driver.execute_script("""
            const selectors = [
                '[role="dialog"]','[role="alertdialog"]',
                '[class*="modal"]','[class*="Modal"]',
                '[class*="popup"]','[class*="Popup"]',
                '[class*="overlay"]','[class*="Overlay"]',
                '[class*="backdrop"]','[class*="Backdrop"]'
            ];
            selectors.forEach(sel => {
                document.querySelectorAll(sel).forEach(el => {
                    el.style.display = 'none'; el.remove();
                });
            });
            document.body.style.overflow = 'auto';
            document.documentElement.style.overflow = 'auto';
        """)
    except Exception:
        pass

    for btn_text in ["Okay", "OK", "Ok", "Close", "Got it", "Accept", "×"]:
        try:
            xpath = f"//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{btn_text.lower()}')]"
            for btn in driver.find_elements(By.XPATH, xpath):
                if btn.is_displayed():
                    try:
                        btn.click()
                    except Exception:
                        driver.execute_script("arguments[0].click();", btn)
                    time.sleep(0.5)
                    break
        except Exception:
            continue


# ============================================================================
# SEARCH CANDIDATES BY JOB TITLE  ← NEW
# ============================================================================
def _search_candidates(
    driver: webdriver.Chrome, job_title: str, max_results: int = 10
) -> list[str]:
    encoded = requests.utils.quote(job_title)

    # Use v3 search — matches your resdex URL pattern
    search_url = (
        f"https://resdex.naukri.com/v3/search"
        f"?EZ_KEYWORD_ANY={encoded}&activeIn=90&resPerPage=40&pageNo=1&oneDaySearch=false"
    )

    print(f"\n🔍 Searching: '{job_title}'")
    print(f"   URL: {search_url}")

    driver.get(search_url)
    time.sleep(8)
    _dismiss_popups(driver)

    # Always save debug snapshot so you can inspect DOM if XPath fails
    debug_dir = os.path.join(DOWNLOAD_DIR, "debug")
    os.makedirs(debug_dir, exist_ok=True)
    driver.save_screenshot(os.path.join(debug_dir, "search_result.png"))
    with open(os.path.join(debug_dir, "search_page.html"), "w", encoding="utf-8") as f:
        f.write(driver.page_source)
    print(f"   📸 Debug saved → {debug_dir}/")
    print(f"   🌐 Landed on: {driver.current_url}")

    # XPaths ordered by likelihood for resdex v3
    candidate_xpaths = [
        "//a[contains(@class, 'candidateName')]",
        "//a[contains(@class, 'candidate-name')]",
        "//a[contains(@class, 'cand-name')]",
        "//div[contains(@class,'tuple')]//a[contains(@href,'preview')]",
        "//div[contains(@class,'resultCard')]//a[contains(@href,'preview')]",
        "//div[contains(@class,'srp-tuple')]//a[contains(@href,'preview')]",
        "//a[contains(@href,'resdex.naukri.com/v3/preview')]",
        "//a[contains(@href,'/v3/preview')]",
        "//a[contains(@href,'tabKey=profile')]",
    ]

    elements = []
    for xpath in candidate_xpaths:
        try:
            found = driver.find_elements(By.XPATH, xpath)
            if found:
                elements = found
                print(f"✅ XPath matched: {xpath} → {len(found)} results")
                break
        except Exception:
            continue

    if not elements:
        print("⚠️ No candidate links found.")
        print(f"   → Open {debug_dir}/search_page.html to inspect the DOM")
        print(
            "   → Look for candidate name anchor tags and share the class/href pattern"
        )
        return []

    profile_urls = []
    for elem in elements[:max_results]:
        try:
            href = elem.get_attribute("href")
            if href and href not in profile_urls:
                profile_urls.append(href)
                print(f"   [{len(profile_urls):02d}] {href}")
        except StaleElementReferenceException:
            continue

    print(f"\n✅ Collected {len(profile_urls)} profile URLs.")
    return profile_urls


# ============================================================================
# CV DOWNLOAD  (your original working logic — unchanged)
# ============================================================================
def _click_download(driver, download_path):
    try:
        driver.switch_to.default_content()
        driver.execute_cdp_cmd(
            "Page.setDownloadBehavior",
            {"behavior": "allow", "downloadPath": download_path},
        )
        print("✅ Download path configured")
    except Exception as e:
        print(f"⚠️ Could not set download behavior: {e}")

    print("⏳ Waiting for page to fully load...")
    try:
        WebDriverWait(driver, 20).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        print("✅ Page fully loaded")
    except TimeoutException:
        print("⚠️ Page load timeout, continuing...")

    time.sleep(2)

    # Dismiss popups
    print("\n🔍 DISMISSING POPUPS/MODALS...")
    popup_dismissed = False
    for attempt in range(3):
        for btn_text in [
            "Okay",
            "OK",
            "Ok",
            "okay",
            "Close",
            "Dismiss",
            "Got it",
            "Continue",
            "Accept",
            "×",
        ]:
            try:
                xpath = f"//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{btn_text.lower()}')]"
                for element in driver.find_elements(By.XPATH, xpath):
                    if element.is_displayed():
                        try:
                            element.click()
                        except ElementClickInterceptedException:
                            driver.execute_script("arguments[0].click();", element)
                        print(f"   ✅ Clicked '{btn_text}'")
                        time.sleep(1)
                        popup_dismissed = True
                        break
                if popup_dismissed:
                    break
            except Exception:
                continue
        if popup_dismissed:
            break

        try:
            hidden_count = driver.execute_script("""
                const selectors = ['[role="dialog"]','[role="alertdialog"]',
                    '[class*="modal"]','[class*="Modal"]','[class*="dialog"]',
                    '[class*="popup"]','[class*="overlay"]','[class*="backdrop"]'];
                let hidden = 0;
                selectors.forEach(s => {
                    document.querySelectorAll(s).forEach(el => {
                        if (el && getComputedStyle(el).display !== 'none') {
                            el.style.display='none'; el.remove(); hidden++;
                        }
                    });
                });
                document.body.style.overflow = 'auto';
                return hidden;
            """)
            if hidden_count > 0:
                print(f"   ✅ Removed {hidden_count} modals via JS")
                popup_dismissed = True
                time.sleep(1)
        except Exception:
            pass
        time.sleep(0.5)

    def check_folder():
        if not os.path.exists(download_path):
            return False
        return [
            f
            for f in os.listdir(download_path)
            if not f.endswith((".crdownload", ".tmp", ".part"))
        ]

    xpaths = [
        "//i[contains(@class, 'icon-download')]/..",
        "//i[contains(@class, 'download')]/..",
        "//*[contains(., 'Download') and contains(., 'contact info')]",
        "//button[contains(., 'Download')]",
        "//a[contains(., 'Download')]",
        "//span[contains(., 'Download')]/..",
        "//*[@title='Download']",
        "//*[@aria-label='Download']",
        "//button[contains(@class, 'download')]",
        "//a[contains(@class, 'download')]",
        "//button[contains(translate(., 'DOWNLOAD', 'download'), 'download')]",
        "//a[contains(translate(., 'DOWNLOAD', 'download'), 'download')]",
    ]

    print("\n🔍 Scanning page for download buttons...")
    for xpath in xpaths:
        try:
            elements = driver.find_elements(By.XPATH, xpath)
            if not elements:
                continue
            print(f"   ✅ Found {len(elements)} elements: {xpath}")

            for elem_idx, element in enumerate(elements):
                try:
                    if not element.is_displayed():
                        continue
                    print(f"   🎯 Clicking element {elem_idx + 1}...")
                    try:
                        driver.execute_script(
                            "arguments[0].scrollIntoView({block:'center'});", element
                        )
                        time.sleep(0.5)
                    except Exception:
                        pass

                    click_successful = False
                    try:
                        element.click()
                        click_successful = True
                        print("      ✅ Standard click")
                    except ElementClickInterceptedException:
                        try:
                            ActionChains(driver).move_to_element(
                                element
                            ).click().perform()
                            click_successful = True
                            print("      ✅ ActionChains click")
                        except Exception:
                            try:
                                driver.execute_script("arguments[0].click();", element)
                                click_successful = True
                                print("      ✅ JS click")
                            except Exception as e:
                                print(f"      ❌ All clicks failed: {e}")
                    except Exception as e:
                        print(f"      ❌ Click error: {e}")

                    if click_successful:
                        print("      👀 Watching folder...")
                        for _ in range(50):
                            if check_folder():
                                print(f"\n🎉 DOWNLOAD SUCCESS! Files: {check_folder()}")
                                return True
                            time.sleep(0.1)

                        # Handle post-click popup
                        try:
                            popup_button = WebDriverWait(driver, 1).until(
                                EC.element_to_be_clickable(
                                    (
                                        By.XPATH,
                                        "//button[contains(translate(.,'OKAY','okay'),'okay') or "
                                        "contains(translate(.,'OK','ok'),'ok') or contains(.,'Got it')]",
                                    )
                                )
                            )
                            print("      🔔 Popup after click — dismissing...")
                            popup_button.click()
                            time.sleep(1)
                            driver.execute_script("arguments[0].click();", element)
                            for _ in range(50):
                                if check_folder():
                                    print("\n🎉 DOWNLOAD SUCCESS (after popup)!")
                                    return True
                                time.sleep(0.1)
                        except TimeoutException:
                            pass

                except StaleElementReferenceException:
                    continue
                except Exception as e:
                    print(f"   ❌ Element error: {e}")
        except Exception as e:
            print(f"   ❌ XPath failed: {e}")

    print("\n❌ DOWNLOAD FAILED")
    try:
        driver.save_screenshot(os.path.join(download_path, "download_failed.png"))
        with open(
            os.path.join(download_path, "page_source.html"), "w", encoding="utf-8"
        ) as f:
            f.write(driver.page_source)
    except Exception:
        pass
    return False


# ============================================================================
# PROFILE TEXT EXTRACTION  (your original working logic — unchanged)
# ============================================================================
def _click_and_extract_all_texts(
    driver: WebDriver, target_url: str, file_dir: str
) -> dict | None:
    if "tabKey=cv" in target_url:
        target_url = target_url.replace("tabKey=cv", "tabKey=profile")

    driver.get(target_url)
    time.sleep(8)

    wait = WebDriverWait(driver, 30)

    try:
        button = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[.//div[contains(@class,'NnYPh')]]")
            )
        )
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", button)
        try:
            button.click()
        except Exception:
            driver.execute_script("arguments[0].click();", button)
        time.sleep(2)
    except TimeoutException:
        print("⚠️ Contact button not found, continuing...")

    linkedin_link = ""
    try:
        for element in driver.find_elements(By.TAG_NAME, "a"):
            link = element.get_attribute("href") or ""
            if "https://www.linkedin.com" in link.lower():
                linkedin_link = "LinkedIn URL:" + link
                break
        print(f"💼 linkedin_link: {linkedin_link}")
    except Exception:
        pass

    profile_lookup = ""
    try:
        profile_lookup = driver.find_element(By.CLASS_NAME, "fyK6F").text
        print(f"👤 profile_lookup: {profile_lookup[:50]}.........")
    except Exception:
        pass

    profile_summary = ""
    try:
        profile_summary = driver.find_element(
            By.CLASS_NAME, "profile-width-content"
        ).text
        print(f"📝 profile_summary: {profile_summary[:50]}.........")
    except Exception:
        pass

    full_text = (
        str(profile_lookup + linkedin_link + profile_summary)
        .replace("Call candidate", "")
        .replace("WhatsApp", "")
        .replace("Linkedin", "")
    )

    if full_text.strip():
        parsed_data = _request_text_parsing(text=full_text)
        print(f"👤 First Name: {parsed_data.get('data', {}).get('First Name')}")
        print(f"☎️ Mobile: {parsed_data.get('data', {}).get('Contact/Mobile Number')}")
        with open(os.path.join(file_dir, "Portal_Parsed_data.json"), "w") as f:
            json.dump(parsed_data, f, indent=4)
        return parsed_data
    return None


# ============================================================================
# TEXT PARSING API  (your original — unchanged)
# ============================================================================
def _request_text_parsing(text: str) -> dict | None:
    print("⏳ Requesting Parsing API...")
    payload = json.dumps({"resume_text": text})
    headers = {"Content-Type": "application/json"}
    response = requests.request("POST", TEXT_PARSING_URL, headers=headers, data=payload)
    return json.loads(response.text)


# ============================================================================
# ORIGINAL SINGLE-PROFILE DOWNLOAD  (your original — unchanged)
# ============================================================================
def run_download(target_url: str, task_id: str, user_agent: str, cookies: list[dict]):
    """Original function — downloads a single known profile URL."""
    print("🚀 Initializing Browser...")

    options = Options()
    options.add_argument(f"--user-agent={user_agent}")
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )
    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {
            "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined});"
        },
    )

    file_dir = os.path.join(DOWNLOAD_DIR, task_id)
    os.makedirs(file_dir, exist_ok=True)

    driver.execute_cdp_cmd(
        "Page.setDownloadBehavior",
        {"behavior": "allow", "downloadPath": os.path.abspath(file_dir)},
    )
    driver.execute_cdp_cmd(
        "Browser.setDownloadBehavior",
        {
            "behavior": "allow",
            "downloadPath": os.path.abspath(file_dir),
            "eventsEnabled": True,
        },
    )

    try:
        print("🍪 Preparing to inject cookies...")
        driver.get("https://www.naukri.com/404")

        injected_count = 0
        for cookie in cookies:
            try:
                c = dict(cookie)
                for key in ["sameSite", "storeId", "id", "hostOnly", "session"]:
                    c.pop(key, None)
                exp = c.get("expirationDate") or c.get("expiry")
                if exp and float(exp) < time.time():
                    continue
                if "expirationDate" in c:
                    c["expiry"] = int(c.pop("expirationDate"))
                if "naukri.com" in c.get("domain", ""):
                    c["domain"] = ".naukri.com"
                    driver.add_cookie(c)
                    injected_count += 1
            except Exception:
                pass

        print(f"✅ Injected {injected_count} valid cookies.")
        driver.get("https://recruit.naukri.com")
        time.sleep(5)

        if "login" in driver.current_url.lower():
            print("❌ Cookie rejected")
            return

        print(f"✅ Session OK: {driver.current_url}")

        if "tabKey=profile" in target_url:
            target_url = target_url.replace("tabKey=profile", "tabKey=cv")

        driver.get(target_url)
        time.sleep(8)

        frames = driver.find_elements(By.TAG_NAME, "iframe")
        if frames:
            for frame in frames:
                try:
                    driver.switch_to.frame(frame)
                    if _click_download(driver, file_dir):
                        _click_and_extract_all_texts(
                            driver=driver, target_url=target_url, file_dir=file_dir
                        )
                        return
                    driver.switch_to.default_content()
                except Exception:
                    driver.switch_to.default_content()

        _click_download(driver, file_dir)
        _click_and_extract_all_texts(
            driver=driver, target_url=target_url, file_dir=file_dir
        )

    finally:
        driver.quit()


# ============================================================================
# NEW — SEARCH BY JOB TITLE + PROCESS TOP N CANDIDATES
# ============================================================================
def run_search_and_download(search_query: str, task_id: str, max_candidates: int = 10):
    """
    Search Naukri Resdex for top candidates by job title,
    then download CV + parse profile for each.
    """
    print(f"\n{'=' * 60}")
    print("🚀 Naukri Candidate Search")
    print(f"   Job Title : {search_query}")
    print(f"   Task ID   : {task_id}")
    print(f"   Max       : {max_candidates}")
    print(f"{'=' * 60}\n")

    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    base_dir = os.path.join(DOWNLOAD_DIR, task_id)
    os.makedirs(base_dir, exist_ok=True)

    driver = _create_driver()
    driver.execute_cdp_cmd(
        "Page.setDownloadBehavior",
        {"behavior": "allow", "downloadPath": os.path.abspath(base_dir)},
    )
    driver.execute_cdp_cmd(
        "Browser.setDownloadBehavior",
        {
            "behavior": "allow",
            "downloadPath": os.path.abspath(base_dir),
            "eventsEnabled": True,
        },
    )

    results = []

    try:
        # Step 1: Authenticate
        if not _inject_cookies(driver):
            print("❌ Aborting — authentication failed.")
            return None

        # Step 2: Search
        profile_urls = _search_candidates(driver, search_query, max_candidates)
        if not profile_urls:
            print("❌ No candidates found.")
            return None

        # Step 3: Process each candidate
        for idx, profile_url in enumerate(profile_urls, start=1):
            print(f"\n{'─' * 60}")
            print(f"👤 Candidate {idx}/{len(profile_urls)}")
            print(f"   URL: {profile_url}")

            candidate_dir = os.path.join(DOWNLOAD_DIR, f"{task_id}_c{idx:02d}")
            os.makedirs(candidate_dir, exist_ok=True)

            driver.execute_cdp_cmd(
                "Page.setDownloadBehavior",
                {"behavior": "allow", "downloadPath": os.path.abspath(candidate_dir)},
            )
            driver.execute_cdp_cmd(
                "Browser.setDownloadBehavior",
                {
                    "behavior": "allow",
                    "downloadPath": os.path.abspath(candidate_dir),
                    "eventsEnabled": True,
                },
            )

            result = {
                "index": idx,
                "profile_url": profile_url,
                "candidate_dir": candidate_dir,
                "cv_downloaded": False,
                "parsed_data": None,
                "error": None,
            }

            try:
                # Build CV tab URL
                cv_url = profile_url
                if "tabKey=profile" in cv_url:
                    cv_url = cv_url.replace("tabKey=profile", "tabKey=cv")
                elif "tabKey=" not in cv_url:
                    sep = "&" if "?" in cv_url else "?"
                    cv_url = cv_url + f"{sep}tabKey=cv"

                driver.get(cv_url)
                time.sleep(8)
                _dismiss_popups(driver)

                # Try iframes first, then main page
                downloaded = False
                frames = driver.find_elements(By.TAG_NAME, "iframe")
                if frames:
                    for frame in frames:
                        try:
                            driver.switch_to.frame(frame)
                            if _click_download(driver, candidate_dir):
                                downloaded = True
                                break
                            driver.switch_to.default_content()
                        except Exception:
                            driver.switch_to.default_content()

                if not downloaded:
                    downloaded = _click_download(driver, candidate_dir)

                result["cv_downloaded"] = downloaded

                parsed = _click_and_extract_all_texts(
                    driver=driver, target_url=profile_url, file_dir=candidate_dir
                )
                result["parsed_data"] = parsed

            except Exception as e:
                print(f"❌ Error: {e}")
                result["error"] = str(e)

            results.append(result)
            time.sleep(3)  # Polite delay between candidates

        # Step 4: Save summary
        summary = {
            "job_title": search_query,
            "task_id": task_id,
            "total_found": len(profile_urls),
            "total_processed": len(results),
            "candidates": results,
        }
        summary_path = os.path.join(base_dir, "search_summary.json")
        with open(summary_path, "w") as f:
            json.dump(summary, f, indent=4)

        print(f"\n{'=' * 60}")
        print(f"✅ Done! {len(results)} candidates processed.")
        print(f"   Summary: {summary_path}")
        print(f"{'=' * 60}\n")
        return summary

    finally:
        driver.quit()


# ============================================================================
# ENTRY POINT
# ============================================================================
if __name__ == "__main__":
    run_search_and_download(
        search_query="Java Developer 10 year experience",
        task_id="search_python_001",
        max_candidates=3,
    )
