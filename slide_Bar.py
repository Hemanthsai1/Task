from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

def get_slider_values(slider_thumb, driver):
    
    min_value = int(driver.execute_script("return arguments[0].getAttribute('aria-valuemin');", slider_thumb))
    max_value = int(driver.execute_script("return arguments[0].getAttribute('aria-valuemax');", slider_thumb))
    return min_value, max_value

def main():
    
    driver = webdriver.Chrome()

    try:
        
        driver.get('https://www.fitpeo.com/revenue-calculator')  

        
        target_value = 560

        
        slider = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'span.MuiSlider-root'))
        )

        
        slider_thumb = driver.find_element(By.CSS_SELECTOR, 'input[type=range]')

        
        min_value, max_value = get_slider_values(slider_thumb, driver)

        
        slider_width = slider.size['width']
        offset = (target_value - min_value) / (max_value - min_value) * slider_width

        
        print(f"Min Value: {min_value}")
        print(f"Max Value: {max_value}")
        print(f"Target Value: {target_value}")
        print(f"Calculated Offset: {offset}")

        
        actions = ActionChains(driver)
        for i in range(int(offset // 10)):  # Adjust the increment step as needed
            actions.click_and_hold(slider_thumb).move_by_offset(10, 0).release().perform()
            time.sleep(0.1) 

        
        remaining_offset = offset % 10
        if remaining_offset > 0:
            actions.click_and_hold(slider_thumb).move_by_offset(remaining_offset, 0).release().perform()

        
        time.sleep(2)  

        
        driver.execute_script("""
            var slider = arguments[0];
            var targetValue = arguments[1];
            slider.value = targetValue;
            slider.dispatchEvent(new Event('input', { bubbles: true }));
            slider.dispatchEvent(new Event('change', { bubbles: true }));
        """, slider_thumb, target_value)

        
        time.sleep(2) 

        
        displayed_value_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, 'body > div.MuiBox-root.css-3f59le > div.MuiBox-root.css-rfiegf > div.MuiGrid-root.MuiGrid-spacing-xs-6.css-l0ykmo > div:nth-child(1) > div > div:nth-child(5) > p.MuiTypography-root.MuiTypography-body1.inter.css-12bch19')
            )
        )

        
        displayed_value = displayed_value_element.text.strip().replace('$', '').replace(',', '')
        displayed_value = int(displayed_value)

        
        print("Displayed Value:", displayed_value)

        
        assert displayed_value == target_value, f"Expected displayed value to be {target_value}, but got {displayed_value}"

        print("Slider and displayed value updated successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        
        driver.quit()

if __name__ == "__main__":
    main()
