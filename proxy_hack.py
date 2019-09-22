import socket
import json

import instapy

# import InstaPy modules
from instapy.time_util import sleep
from instapy.util import update_activity
from instapy.login_util import login_user
from instapy.xpath import read_xpath


def check_browser(browser, logfolder, logger, proxy_address):
    # set initial state to offline
    update_activity(
        browser,
        action=None,
        state="trying to connect",
        logfolder=logfolder,
        logger=logger,
    )

    # check connection status
    try:
        logger.info("-- Connection Checklist [1/3] (Internet Connection Status)")
        browser.get("view-source:https://api.myip.com/")
        pre = browser.find_element_by_tag_name("pre").text
        current_ip_info = json.loads(pre)
        if (
            proxy_address is not None
            and socket.gethostbyname(proxy_address) != current_ip_info["ip"]
        ):
            logger.warn("- Proxy is set, but it's not working properly")
            logger.warn(
                '- Expected Proxy IP is "{}", and the current IP is "{}"'.format(
                    proxy_address, current_ip_info["ip"]
                )
            )
            # logger.warn("- Try again or disable the Proxy Address on your setup")
            # logger.warn("- Aborting connection...")
            # return False
        else:
            logger.info("- Internet Connection Status: ok")
            logger.info(
                '- Current IP is "{}" and it\'s from "{}/{}"'.format(
                    current_ip_info["ip"],
                    current_ip_info["country"],
                    current_ip_info["cc"],
                )
            )
            update_activity(
                browser,
                action=None,
                state="Internet connection is ok",
                logfolder=logfolder,
                logger=logger,
            )
    except Exception:
        logger.warn("- Internet Connection Status: error")
        update_activity(
            browser,
            action=None,
            state="There is an issue with the internet connection",
            logfolder=logfolder,
            logger=logger,
        )
        return False

    # check Instagram.com status
    try:
        logger.info("-- Connection Checklist [2/3] (Instagram Server Status)")
        browser.get("https://isitdownorjust.me/instagram-com/")
        sleep(2)
        # collect isitdownorjust.me website information
        website_status = browser.find_element_by_xpath(
            read_xpath(login_user.__name__, "website_status")
        )
        response_time = browser.find_element_by_xpath(
            read_xpath(login_user.__name__, "response_time")
        )
        response_code = browser.find_element_by_xpath(
            read_xpath(login_user.__name__, "response_code")
        )

        logger.info("- Instagram WebSite Status: {} ".format(website_status.text))
        logger.info("- Instagram Response Time: {} ".format(response_time.text))
        logger.info("- Instagram Reponse Code: {}".format(response_code.text))
        logger.info("- Instagram Server Status: ok")
        update_activity(
            browser,
            action=None,
            state="Instagram servers are running correctly",
            logfolder=logfolder,
            logger=logger,
        )
    except Exception:
        logger.warn("- Instagram Server Status: error")
        update_activity(
            browser,
            action=None,
            state="Instagram server is down",
            logfolder=logfolder,
            logger=logger,
        )
        return False

    # check if hide-selenium extension is running
    logger.info("-- Connection Checklist [3/3] (Hide Selenium Extension)")
    webdriver = browser.execute_script("return window.navigator.webdriver")
    logger.info("- window.navigator.webdriver response: {}".format(webdriver))
    if webdriver:
        logger.warn("- Hide Selenium Extension: error")
    else:
        logger.info("- Hide Selenium Extension: ok")

    # everything is ok, then continue(True)
    return True


setattr(instapy.login_util, 'check_browser', check_browser)
