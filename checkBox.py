from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def adjust_slider(slider_selector, target_value, driver):
    try:
        slider = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, slider_selector))
        )
        
        slider_thumb = slider.find_element(By.CSS_SELECTOR, '.MuiSlider-thumb')
        slider_thumb.click()

        
        driver.execute_script(f"arguments[0].value = {target_value};", slider_thumb)
        
        
        driver.execute_script("arguments[0].dispatchEvent(new Event('change', { bubbles: true }));", slider_thumb)
        
        
        slider_value = slider_thumb.get_attribute('aria-valuenow')
        assert slider_value == target_value, f"Expected slider value to be {target_value}, but got {slider_value}"
        print(f"Slider value set to {slider_value}")

    except Exception as e:
        print(f"Error adjusting slider: {e}")

def select_checkboxes(cpt_codes, driver):
    for code in cpt_codes:
        try:
            
            element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, f'//p[text()="{code}"]/ancestor::div[@class="MuiBox-root css-4o8pys"]'))
            )
            
            
            checkbox = element.find_element(By.XPATH, './/input[@type="checkbox"]')
            
            
            if not checkbox.is_selected():
                checkbox.click()
                print(f"Clicked checkbox for {code}")
            else:
                print(f"Checkbox for {code} is already selected")
            
            time.sleep(1)  

        except Exception as e:
            print(f"Error selecting checkbox for {code}: {e}")

def main():
    
    driver = webdriver.Chrome()

    try:
        
        driver.get('https://www.fitpeo.com/revenue-calculator')  

        
        cpt_codes = ['CPT-99091', 'CPT-99453', 'CPT-99454', 'CPT-99474']

        
        adjust_slider('.MuiSlider-root', '820', driver) 

        
        select_checkboxes(cpt_codes, driver)

        

    finally:
        
        driver.quit()

if __name__ == "__main__":
    main()
