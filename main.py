import time

from playwright.sync_api import sync_playwright


def main(uemail, upassword):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://app.subject.com")
        page.wait_for_selector("#email")
        page.wait_for_selector("#password")
        page.wait_for_selector(".css-nbamov")
        email = page.query_selector("#email")
        if email:
            email.fill(uemail)
        password = page.query_selector("#password")
        if password:
            password.fill(upassword)
        login = page.query_selector(".css-nbamov")
        if login:
            login.click()
        page.wait_for_selector(".pb-3")
        courses = page.query_selector_all(".pb-3")
        if courses:
            i = 0
            for course in courses:
                courseTitle = course.get_attribute("aria-label")
                if courseTitle:
                    print(f"{i}: {courseTitle.split('.')[0]}")
                    i += 1
        selectedCourse = courses[int(input("Which course will you be resuming? "))]
        selectedCourse.click()
        page.wait_for_selector(".react-player > video")
        player = page.locator(".react-player > video")
        if player:
            player.focus()
            page.keyboard.press("Space")
            page.wait_for_function(
                "document.querySelector('.react-player > video').duration > 0"
            )
            page.wait_for_function(
                "document.querySelector('.react-player > video').currentTime > 0"
            )
            duration = int(player.evaluate("e => e.duration"))
            current = int(player.evaluate("e => e.currentTime"))
            print(f"a video will be playing for {duration - current} seconds")
            time.sleep(duration - current)
            page.wait_for_selector(".chakra-button .css-z47iya")
            print("finished watching")
            next = page.query_selector(".chakra-button .css-z47iya")
            if next:
                next.click()
        browser.close()


if __name__ == "__main__":
    uemail = input("email: ")
    upassword = input("password: ")
    main(uemail, upassword)
