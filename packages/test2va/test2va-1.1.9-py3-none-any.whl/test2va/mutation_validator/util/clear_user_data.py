def clear_user_data(driver, app_id):
    """Clears user data for a specified app on an Android device using Appium.

    Args:
        driver (appium.webdriver.webdriver.WebDriver): The Appium WebDriver instance.
        app_id (str): The package name (app ID) of the application whose data should be cleared.

    Returns:
        None
    """
    driver.execute_script("mobile: shell", {
        "command": "pm clear",
        "args": [app_id]
    })
