from ExtendedSelenium import ExtendedSelenium

element_download_link = (
    "//a[contains(@href, 'https://downloads.robocorp.com/workforce-agent/')]"
)
element_accept_cookies = "//button//span[text()='I understand']"


def main():
    library = ExtendedSelenium(download_dir="./output")
    try:
        url = "https://robocorp.com/download"
        library.open_site(url)
        library.click_element_when_visible(element_accept_cookies)
        library.wait_until_element_is_visible(element_download_link)
        expected_filename = library.get_element_attribute(element_download_link, "href")
        library.firefox_download_and_wait_until_file_has_been_downloaded(
            element_download_link, expected_filename
        )
    finally:
        library.close_all_browsers()


if __name__ == "__main__":
    main()
