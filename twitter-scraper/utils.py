def close_ntfn_popup(driver, By):
    try:
        ntfn_close_btn = driver.find_element(By.XPATH, './/div[@data-testid="app-bar-close"]')
        #perform click
        ntfn_close_btn.click()
    except:
        pass