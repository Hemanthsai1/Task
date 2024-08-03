from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def adjust_slider(slider_selector, target_value, driver):
    try:
        # Wait for the slider to be present
        slider = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, slider_selector))
        )
        
        # Click the slider thumb to set the value
        slider_thumb = slider.find_element(By.CSS_SELECTOR, '.MuiSlider-thumb')
        slider_thumb.click()

        # Adjust slider value (depends on how the slider is set, this is an example)
        driver.execute_script(f"arguments[0].value = {target_value};", slider_thumb)
        
        # Trigger the change event
        driver.execute_script("arguments[0].dispatchEvent(new Event('change', { bubbles: true }));", slider_thumb)
        
        # Verify the slider value
        slider_value = slider_thumb.get_attribute('aria-valuenow')
        assert slider_value == target_value, f"Expected slider value to be {target_value}, but got {slider_value}"
        print(f"Slider value set to {slider_value}")

    except Exception as e:
        print(f"Error adjusting slider: {e}")

def select_checkboxes(cpt_codes, driver):
    for code in cpt_codes:
        try:
            # Wait for the element containing the code
            element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, f'//p[text()="{code}"]/ancestor::div[@class="MuiBox-root css-4o8pys"]'))
            )
            
            # Locate the checkbox based on its position relative to the label
            checkbox = element.find_element(By.XPATH, './/input[@type="checkbox"]')
            
            # Click the checkbox if it is not selected
            if not checkbox.is_selected():
                checkbox.click()
                print(f"Clicked checkbox for {code}")
            else:
                print(f"Checkbox for {code} is already selected")
            
            time.sleep(1)  # Optional: Wait for the action to complete

        except Exception as e:
            print(f"Error selecting checkbox for {code}: {e}")

def main():
    # Initialize WebDriver
    driver = webdriver.Chrome()

    try:
        # Open the page
        driver.get('https://www.fitpeo.com/revenue-calculator')  # Replace with your actual page URL

        # List of CPT codes to select
        cpt_codes = ['CPT-99091', 'CPT-99453', 'CPT-99454', 'CPT-99474']

        # Adjust slider value
        adjust_slider('.MuiSlider-root', '820', driver)  # Replace '.MuiSlider-root' with the actual CSS selector for the slider

        # Select checkboxes
        select_checkboxes(cpt_codes, driver)

        # Other operations...

    finally:
        # Close the WebDriver
        driver.quit()

if __name__ == "__main__":
    main()
